# SPDX-FileCopyrightText: 2022 - 2024
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Luca Johannes Nendel <Luca-Johannes.Nendel@ufz.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Platform list resource."""

import os

from flask import g, request
from flask_rest_jsonapi import JsonApiException, ResourceDetail, ResourceList
from flask_rest_jsonapi.exceptions import ObjectNotFound

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
    ManufacturerModel,
    Platform,
    PlatformContactRole,
    PlatformMountAction,
)
from ..models.base_model import db
from ..permissions.common import DelegateToCanFunctions
from ..permissions.rules import filter_visible, filter_visible_es
from ..schemas.platform_schema import PlatformSchema
from ..token_checker import token_required
from .base_resource import check_if_object_not_found, delete_attachments_in_minio_by_url
from .mixins.csv_export import CsvListMixin


class PlatformList(CsvListMixin, ResourceList):
    """
    Resource for the platform list endpoint.

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
        if not hide_archived:
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
        platform = db.session.query(Platform).filter_by(id=result_id).first()
        contact = g.user.contact
        cv_url = os.environ.get("CV_URL")
        role_name = "Owner"
        role_uri = f"{cv_url}/contactroles/4/"
        contact_role = PlatformContactRole(
            contact_id=contact.id,
            platform_id=platform.id,
            role_name=role_name,
            role_uri=role_uri,
        )
        save_to_db(contact_role)

        msg = "create;basic data"
        platform.update_description = msg
        platform.updated_by_id = g.user.id

        save_to_db(platform)

        if platform.manufacturer_name and platform.model:
            existing_manufacturer_model = (
                db.session.query(ManufacturerModel)
                .filter_by(
                    manufacturer_name=platform.manufacturer_name, model=platform.model
                )
                .first()
            )
            if not existing_manufacturer_model:
                manufacturer_model = ManufacturerModel(
                    manufacturer_name=platform.manufacturer_name, model=platform.model
                )
                save_to_db(manufacturer_model)
        return result

    schema = PlatformSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": Platform,
        "class": EsSqlalchemyDataLayer,
        "methods": {
            "before_create_object": before_create_object,
            "query": query,
            "es_query": es_query,
        },
    }
    permission_classes = [DelegateToCanFunctions]


class PlatformDetail(ResourceDetail):
    """
    Detail resource for the platforms.

    Provides get, patch and delete methods to retrieve details
    of an object, update an object and delete a platform.
    """

    def before_get(self, args, kwargs):
        """Return a 404 response if the platform was not found."""
        check_if_object_not_found(self._data_layer.model, kwargs)

    def after_patch(self, result):
        """
        Run some updates after the patch.

        For example here we can update the update description.
        """
        result_id = result["data"]["id"]
        platform = db.session.query(Platform).filter_by(id=result_id).first()
        msg = "update;basic data"
        platform.update_description = msg
        save_to_db(platform)

        if pidinst.has_external_metadata(platform):
            pidinst.update_external_metadata(platform)

        for configuration in (
            db.session.query(Configuration)
            .join(PlatformMountAction)
            .filter(PlatformMountAction.platform_id == result_id)
        ):
            if pidinst.has_external_metadata(configuration):
                pidinst.update_external_metadata(configuration)

        if (
            self.platform_manufacturer_name_before_patch is not None
            and self.platform_model_before_patch is not None
        ):
            if (
                self.platform_manufacturer_name_before_patch
                != self.platform_manufacturer_name_before_patch
                or self.platform_model_before_patch != platform.model
            ):
                existing_manufacturer_model = (
                    db.session.query(ManufacturerModel)
                    .filter_by(
                        manufacturer_name=self.platform_manufacturer_name_before_patch,
                        model=self.platform_model_before_patch,
                    )
                    .first()
                )
                # If we found one entry, but it has no information yet,
                # we check if we should delete the old one.
                if existing_manufacturer_model and not any(
                    [
                        existing_manufacturer_model.external_system_name,
                        existing_manufacturer_model.external_system_url,
                        existing_manufacturer_model.export_control,
                        existing_manufacturer_model.export_control_attachments,
                    ]
                ):
                    other_platform = (
                        db.session.query(Platform)
                        .filter_by(
                            manufacturer_name=existing_manufacturer_model.manufacturer_name,
                            model=existing_manufacturer_model.model,
                        )
                        .first()
                    )
                    if not other_platform:
                        other_device = (
                            db.session.query(Device)
                            .filter_by(
                                manufacturer_name=existing_manufacturer_model.manufacturer_name,
                                model=existing_manufacturer_model.model,
                            )
                            .first()
                        )
                        if not other_device:
                            db.session.delete(existing_manufacturer_model)
                            db.session.commit()

        if platform.manufacturer_name and platform.model:
            existing_manufacturer_model = (
                db.session.query(ManufacturerModel)
                .filter_by(
                    manufacturer_name=platform.manufacturer_name, model=platform.model
                )
                .first()
            )
            if not existing_manufacturer_model:
                manufacturer_model = ManufacturerModel(
                    manufacturer_name=platform.manufacturer_name, model=platform.model
                )
                save_to_db(manufacturer_model)

        self.platform_manufacturer_name_before_patch = None
        self.platform_model_before_patch = None
        return result

    def delete(self, *args, **kwargs):
        """
        Try to delete an object through sqlalchemy.

        If could not be done give a ConflictError.
        :param args: args from the resource view
        :param kwargs: kwargs from the resource view
        :return:
        """
        platform = db.session.query(Platform).filter_by(id=kwargs["id"]).first()

        if platform is None:
            raise ObjectNotFound({"pointer": ""}, "Object Not Found")
        urls = [a.internal_url for a in platform.platform_attachments if a.internal_url]
        try:
            super().delete(*args, **kwargs)
        except JsonApiException as e:
            raise ConflictError("Deletion failed for the platform.", str(e))

        for url in urls:
            delete_attachments_in_minio_by_url(url)

        if platform.manufacturer_name and platform.model:
            existing_manufacturer_model = (
                db.session.query(ManufacturerModel)
                .filter_by(
                    manufacturer_name=platform.manufacturer_name, model=platform.model
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
                other_platform = (
                    db.session.query(Platform)
                    .filter_by(
                        manufacturer_name=platform.manufacturer_name,
                        model=platform.model,
                    )
                    .first()
                )
                if not other_platform:
                    other_device = (
                        db.session.query(Device)
                        .filter_by(
                            manufacturer_name=platform.manufacturer_name,
                            model=platform.model,
                        )
                        .first()
                    )
                    if not other_device:
                        db.session.delete(existing_manufacturer_model)
                        db.session.commit()

        final_result = {"meta": {"message": "Object successfully deleted"}}
        return final_result

    def before_patch(self, args, kwargs, data):
        """
        Run logic before the patch.

        In this case we want to make sure that we update the updated_by_id
        with the id of the user that run the request.
        """
        add_updated_by_id(data)
        platform = db.session.query(Platform).filter_by(id=kwargs["id"]).first()
        if platform:
            self.platform_manufacturer_name_before_patch = platform.manufacturer_name
            self.platform_model_before_patch = platform.model

    schema = PlatformSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": Platform,
    }
    permission_classes = [DelegateToCanFunctions]
