# SPDX-FileCopyrightText: 2022 - 2023
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Module for hte customfield list resource."""
from flask_rest_jsonapi import ResourceDetail, ResourceList
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.orm.exc import NoResultFound

from ..models.base_model import db
from ..models.customfield import CustomField
from ..models.device import Device
from ..permissions.common import DelegateToCanFunctions
from ..permissions.rules import filter_visible
from ..schemas.customfield_schema import CustomFieldSchema
from ..token_checker import token_required
from .base_resource import (
    check_if_object_not_found,
    query_device_set_update_description_and_update_pidinst,
    set_update_description_text_user_and_pidinst,
)


class CustomFieldList(ResourceList):
    """
    List resource for custom fields.

    Provides get and post methods to retrieve
    a list of custom fields or to create a new one.
    """

    def query(self, view_kwargs):
        """
        Query the data from the database & Filter for what the user is allowed to query.

        Normally it should query all the customfields.
        However, if we give a device_id with a url like
        /devices/<device_id>/customfields
        we want to filter according to them.
        """
        query_ = filter_visible(self.session.query(self.model))
        device_id = view_kwargs.get("device_id")

        if device_id is not None:
            try:
                self.session.query(Device).filter_by(id=device_id).one()
            except NoResultFound:
                raise ObjectNotFound(
                    {
                        "parameter": "id",
                    },
                    "Device: {} not found".format(device_id),
                )
            else:
                query_ = query_.filter(CustomField.device_id == device_id)
        return query_

    def after_post(self, result):
        """
        Add update description to related device.

        :param result:
        :return:
        """
        result_id = result[0]["data"]["relationships"]["device"]["data"]["id"]
        msg = "create;custom field"
        query_device_set_update_description_and_update_pidinst(msg, result_id)

        return result

    schema = CustomFieldSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": CustomField,
        "methods": {"query": query},
    }
    permission_classes = [DelegateToCanFunctions]


class CustomFieldDetail(ResourceDetail):
    """
    Detail resource for custom fields.

    Provides get, patch & delete methods to retrieve
    a custom field, update it or to delete it.
    """

    def before_get(self, args, kwargs):
        """Return 404 Responses if CustomField not found."""
        check_if_object_not_found(self._data_layer.model, kwargs)

    def after_patch(self, result):
        """
        Add update description to related device.

        :param result:
        :return:
        """
        result_id = result["data"]["relationships"]["device"]["data"]["id"]
        msg = "update;custom field"
        query_device_set_update_description_and_update_pidinst(msg, result_id)
        return result

    def before_delete(self, args, kwargs):
        """Update the devices update description."""
        custom_field = (
            db.session.query(CustomField).filter_by(id=kwargs["id"]).one_or_none()
        )
        if custom_field is None:
            raise ObjectNotFound("Object not found!")
        self.tasks_after_delete = []
        device = custom_field.get_parent()
        msg = "delete;custom field"

        def run_updates():
            """Set the update description & update external metadata for pidinst."""
            set_update_description_text_user_and_pidinst(device, msg)

        self.tasks_after_delete.append(run_updates)

    def after_delete(self, *args, **kwargs):
        """Run some hooks after deleting."""
        for task in self.tasks_after_delete:
            task()
        return super().after_delete(*args, **kwargs)

    schema = CustomFieldSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": CustomField,
    }
    permission_classes = [DelegateToCanFunctions]
