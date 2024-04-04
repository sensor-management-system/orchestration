# SPDX-FileCopyrightText:  2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Module for the export control resource classes."""

from flask import g
from flask_rest_jsonapi import ResourceDetail, ResourceList
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.orm.exc import NoResultFound

from ..helpers.errors import ConflictError
from ..helpers.resource_mixin import add_created_by_id, add_updated_by_id
from ..models import (
    Device,
    ExportControl,
    ExportControlAttachment,
    ManufacturerModel,
    Platform,
)
from ..models.base_model import db
from ..permissions.common import DelegateToCanFunctions
from ..permissions.rules import filter_visible
from ..schemas.export_control_schema import ExportControlSchema
from .base_resource import check_if_object_not_found


class ExportControlList(ResourceList):
    """Resource class for the list endpoint for export control data."""

    def query(self, view_kwargs):
        """Return the query to list the elements."""
        query_ = filter_visible(self.session.query(self.model))
        manufacturer_name = None
        model = None

        device_id = view_kwargs.get("device_id")
        if device_id:
            try:
                device = self.session.query(Device).filter_by(id=device_id).one()
                manufacturer_name = device.manufacturer_name
                model = device.model
            except NoResultFound:
                raise ObjectNotFound(
                    {
                        "parameter": "id",
                    },
                    "Device: {} not found".format(device_id),
                )
        platform_id = view_kwargs.get("platform_id")
        if platform_id:
            try:
                platform = self.session.query(Platform).filter_by(id=platform_id).one()
                manufacturer_name = platform.manufacturer_name
                model = platform.model
            except NoResultFound:
                raise ObjectNotFound(
                    {
                        "parameter": "id",
                    },
                    "Platform: {} not found".format(platform_id),
                )

        manufacturer_model_id = view_kwargs.get("manufacturer_model_id")

        if manufacturer_model_id is not None:
            try:
                self.session.query(ManufacturerModel).filter_by(
                    id=manufacturer_model_id
                ).one()
            except NoResultFound:
                raise ObjectNotFound(
                    {
                        "parameter": "id",
                    },
                    "ManufacturerModel: {} not found".format(manufacturer_model_id),
                )
            else:
                query_ = query_.filter(
                    ExportControl.manufacturer_model_id == manufacturer_model_id
                )

        if manufacturer_name is not None or model is not None:
            query_ = query_.join(ManufacturerModel)
        if manufacturer_name is not None:
            query_ = query_.filter(
                ManufacturerModel.manufacturer_name == manufacturer_name
            )
        if model is not None:
            query_ = query_.filter(ManufacturerModel.model == model)

        return query_

    def before_create_object(self, data, *args, **kwargs):
        """Add the created by information."""
        manufacturer_model_id = data.get("manufacturer_model")
        if manufacturer_model_id:
            if (
                db.session.query(ExportControl)
                .filter_by(manufacturer_model_id=manufacturer_model_id)
                .first()
            ):
                raise ConflictError(
                    "There is already an export control dataset for the manufacturer model"
                )
        add_created_by_id(data)

    def after_get(self, result):
        """Remove some fields if the user is not allowed to see it."""
        if not (g.user and (g.user.is_export_control or g.user.is_superuser)):
            for entry in result["data"]:
                del entry["attributes"]["internal_note"]
        return result

    schema = ExportControlSchema
    data_layer = {
        "session": db.session,
        "model": ExportControl,
        "methods": {
            "query": query,
            "before_create_object": before_create_object,
        },
    }
    permission_classes = [DelegateToCanFunctions]


class ExportControlDetail(ResourceDetail):
    """Resource class for the detail endpoint for export control data."""

    def before_get(self, args, kwargs):
        """Run some tests before the get method."""
        check_if_object_not_found(self._data_layer.model, kwargs)

    def after_get(self, result):
        """Remove some fields if the user is not allowed to see it."""
        if not (g.user and (g.user.is_export_control or g.user.is_superuser)):
            del result["data"]["attributes"]["internal_note"]
        return result

    def before_patch(self, args, kwargs, data):
        """Add the updated by field."""
        entry = check_if_object_not_found(self._data_layer.model, kwargs)
        if data.get("manufacturer_model"):
            if entry.manufacturer_model_id != data["manufacturer_model"]:
                raise ConflictError(
                    "Changing the manufacturer model relationship is not allowed"
                )
        add_updated_by_id(data)

    def delete(self, *args, **kwargs):
        """Extend the standard delete function by checking if we can delete the manfacturer model entry too."""
        export_control = check_if_object_not_found(self._data_layer.model, kwargs)
        manufacturer_model = export_control.manufacturer_model

        result = super().delete(*args, **kwargs)

        can_delete_manfuacturer_model_too = True

        if (
            manufacturer_model.external_system_name
            or manufacturer_model.external_system_url
        ):
            can_delete_manfuacturer_model_too = False
        elif (
            self._data_layer.session.query(Device)
            .filter_by(
                manufacturer_name=manufacturer_model.manufacturer_name,
                model=manufacturer_model.model,
            )
            .first()
        ):
            can_delete_manfuacturer_model_too = False
        elif (
            self._data_layer.session.query(Platform)
            .filter_by(
                manufacturer_name=manufacturer_model.manufacturer_name,
                model=manufacturer_model.model,
            )
            .first()
        ):
            can_delete_manfuacturer_model_too = False
        elif (
            self._data_layer.session.query(ExportControlAttachment)
            .filter_by(manufacturer_model=manufacturer_model)
            .first()
        ):
            can_delete_manfuacturer_model_too = False

        if can_delete_manfuacturer_model_too:
            self._data_layer.session.delete(manufacturer_model)
            self._data_layer.session.commit()

        return result

    schema = ExportControlSchema
    data_layer = {
        "session": db.session,
        "model": ExportControl,
    }
    permission_classes = [DelegateToCanFunctions]
