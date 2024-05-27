# SPDX-FileCopyrightText: 2022 - 2024
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Luca Johannes Nendel <Luca-Johannes.Nendel@ufz.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Device list resource."""

import os

from flask import g, request
from flask_rest_jsonapi import JsonApiException, ResourceDetail, ResourceList

from ...extensions.instances import pidinst
from ..datalayers.esalchemy import (
    AndFilter,
    EsSqlalchemyDataLayer,
    TermEqualsExactStringFilter,
)
from ..helpers.db import save_to_db
from ..helpers.errors import ConflictError
from ..helpers.resource_mixin import (
    add_updated_by_id,
    set_default_permission_view_to_internal_if_not_exists_or_all_false,
)
from ..models import (
    Configuration,
    Device,
    DeviceContactRole,
    DeviceMountAction,
    ManufacturerModel,
    Platform,
)
from ..models.base_model import db
from ..permissions.common import DelegateToCanFunctions
from ..permissions.rules import filter_visible, filter_visible_es
from ..schemas.device_schema import DeviceSchema
from ..token_checker import token_required
from .base_resource import check_if_object_not_found, delete_attachments_in_minio_by_url
from .mixins.csv_export import CsvListMixin


class DeviceList(CsvListMixin, ResourceList):
    """
    Resource for the device list endpoint.

    Supports GET (list) & POST (create) methods.
    """

    def query(self, view_kwargs):
        """
        Filter for what the user is allowed to query.

        :param view_kwargs:
        :return: queryset
        """
        false_values = ["false"]
        # hide archived must be disabled explicitly
        hide_archived = request.args.get("hide_archived") not in false_values
        query_ = filter_visible(self.session.query(self.model))
        if hide_archived:
            query_ = query_.filter_by(archived=False)
        return query_

    def es_query(self, view_kwargs):
        """
        Return the elasticsearch filter for the query.

        Should return the same set as query, but using
        the elasticsearch fields.
        """
        and_filters = [filter_visible_es(self.model)]

        false_values = ["false"]
        # hide archived must be disabled explicitly
        hide_archived = request.args.get("hide_archived") not in false_values
        if hide_archived:
            and_filters.append(TermEqualsExactStringFilter("archived", False))
        return AndFilter.combine_optionals(and_filters)

    def before_create_object(self, data, *args, **kwargs):
        """
        Set the visibility of the object (internal of nothing else is given).

        :param data: data of the request (as dict)
        :param args:
        :param kwargs:
        :return: None
        """
        # Will modify the data inplace.
        set_default_permission_view_to_internal_if_not_exists_or_all_false(data)

    def after_post(self, result):
        """
        Automatically add the created user to object contacts.

        Also add the owner to contact role.

        :param result:
        :return:
        """
        result_id = result[0]["data"]["id"]
        device = db.session.query(Device).filter_by(id=result_id).first()
        contact = g.user.contact
        cv_url = os.environ.get("CV_URL")
        role_name = "Owner"
        role_uri = f"{cv_url}/contactroles/4/"
        contact_role = DeviceContactRole(
            contact_id=contact.id,
            device_id=device.id,
            role_name=role_name,
            role_uri=role_uri,
        )
        save_to_db(contact_role)

        msg = "create;basic data"
        device.update_description = msg
        device.updated_by_id = g.user.id

        save_to_db(device)

        if device.manufacturer_name and device.model:
            existing_manufacturer_model = (
                db.session.query(ManufacturerModel)
                .filter_by(
                    manufacturer_name=device.manufacturer_name, model=device.model
                )
                .first()
            )
            if not existing_manufacturer_model:
                manufacturer_model = ManufacturerModel(
                    manufacturer_name=device.manufacturer_name, model=device.model
                )
                save_to_db(manufacturer_model)

        return result

    schema = DeviceSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": Device,
        "class": EsSqlalchemyDataLayer,
        "methods": {
            "before_create_object": before_create_object,
            "query": query,
            "es_query": es_query,
        },
    }
    permission_classes = [DelegateToCanFunctions]


class DeviceDetail(ResourceDetail):
    """
    Detail resource class for devices.

    Provides get, patch and delete methods to retrieve details
    of an object, update an object and delete a Device.
    """

    def before_get(self, args, kwargs):
        """Run some tests before the get method."""
        check_if_object_not_found(self._data_layer.model, kwargs)

    def delete(self, *args, **kwargs):
        """
        Try to delete an object through sqlalchemy. If could not be done give a ConflictError.

        :param args: args from the resource view
        :param kwargs: kwargs from the resource view
        :return:
        """
        device = check_if_object_not_found(Device, kwargs)

        urls = [a.internal_url for a in device.device_attachments if a.internal_url]
        try:
            super().delete(*args, **kwargs)
        except JsonApiException as e:
            raise ConflictError("Deletion failed for the device.", str(e))

        for url in urls:
            delete_attachments_in_minio_by_url(url)

        if device.manufacturer_name and device.model:
            existing_manufacturer_model = (
                db.session.query(ManufacturerModel)
                .filter_by(
                    manufacturer_name=device.manufacturer_name, model=device.model
                )
                .first()
            )
            if not any(
                [
                    existing_manufacturer_model.external_system_name,
                    existing_manufacturer_model.external_system_url,
                    existing_manufacturer_model.export_control,
                    existing_manufacturer_model.export_control_attachments,
                ]
            ):
                other_device = (
                    db.session.query(Device)
                    .filter_by(
                        manufacturer_name=device.manufacturer_name, model=device.model
                    )
                    .first()
                )
                if not other_device:
                    other_platform = (
                        db.session.query(Platform)
                        .filter_by(
                            manufacturer_name=device.manufacturer_name,
                            model=device.model,
                        )
                        .first()
                    )
                    if not other_platform:
                        db.session.delete(existing_manufacturer_model)
                        db.session.commit()

        final_result = {"meta": {"message": "Object successfully deleted"}}
        return final_result

    def before_patch(self, args, kwargs, data):
        """
        Run logic before the patch.

        In this case we want to make sure that we update the updated_by_id
        with the id of the user that run the request.
        In Flask those data should be stored in the `g` object.
        """
        add_updated_by_id(data)
        device = db.session.query(Device).filter_by(id=kwargs["id"]).first()
        if device:
            self.device_manufacturer_name_before_patch = device.manufacturer_name
            self.device_model_before_patch = device.model

    def after_patch(self, result):
        """Run some update logic after the change by the patch request."""
        result_id = result["data"]["id"]
        device = db.session.query(Device).filter_by(id=result_id).first()
        msg = "update;basic data"
        device.update_description = msg

        save_to_db(device)

        if pidinst.has_external_metadata(device):
            pidinst.update_external_metadata(device)

        for configuration in (
            db.session.query(Configuration)
            .join(DeviceMountAction)
            .filter(DeviceMountAction.device_id == result_id)
        ):
            if pidinst.has_external_metadata(configuration):
                pidinst.update_external_metadata(configuration)

        if (
            self.device_manufacturer_name_before_patch is not None
            and self.device_model_before_patch is not None
        ):
            if (
                self.device_manufacturer_name_before_patch
                != self.device_manufacturer_name_before_patch
                or self.device_model_before_patch != device.model
            ):
                existing_manufacturer_model = (
                    db.session.query(ManufacturerModel)
                    .filter_by(
                        manufacturer_name=self.device_manufacturer_name_before_patch,
                        model=self.device_model_before_patch,
                    )
                    .first()
                )
                if not any(
                    [
                        existing_manufacturer_model.external_system_name,
                        existing_manufacturer_model.external_system_url,
                        existing_manufacturer_model.export_control,
                        existing_manufacturer_model.export_control_attachments,
                    ]
                ):
                    other_device = (
                        db.session.query(Device)
                        .filter_by(
                            manufacturer_name=existing_manufacturer_model.manufacturer_name,
                            model=existing_manufacturer_model.model,
                        )
                        .first()
                    )
                    if not other_device:
                        other_platform = (
                            db.session.query(Platform)
                            .filter_by(
                                manufacturer_name=existing_manufacturer_model.manufacturer_name,
                                model=existing_manufacturer_model.model,
                            )
                            .first()
                        )
                        if not other_platform:
                            db.session.delete(existing_manufacturer_model)
                            db.session.commit()

        if device.manufacturer_name and device.model:
            existing_manufacturer_model = (
                db.session.query(ManufacturerModel)
                .filter_by(
                    manufacturer_name=device.manufacturer_name, model=device.model
                )
                .first()
            )
            if not existing_manufacturer_model:
                manufacturer_model = ManufacturerModel(
                    manufacturer_name=device.manufacturer_name, model=device.model
                )
                save_to_db(manufacturer_model)

        self.device_manufacturer_name_before_patch = None
        self.device_model_before_patch = None
        return result

    schema = DeviceSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": Device,
    }
    permission_classes = [DelegateToCanFunctions]
