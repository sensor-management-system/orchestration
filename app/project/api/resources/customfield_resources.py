"""Module for hte customfield list resource."""
from flask_rest_jsonapi import ResourceDetail, ResourceList
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.orm.exc import NoResultFound

from ..auth.permission_utils import get_query_with_permissions_for_related_objects
from ..models.base_model import db
from ..models.customfield import CustomField
from ..models.device import Device
from ..schemas.customfield_schema import CustomFieldSchema
from ..token_checker import token_required
from .base_resource import (
    check_if_object_not_found,
    query_device_and_set_update_description_text,
    set_update_description_text_and_update_by_user,
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
        query_ = get_query_with_permissions_for_related_objects(self.model)
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
        query_device_and_set_update_description_text(msg, result_id)

        return result

    schema = CustomFieldSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": CustomField,
        "methods": {"query": query},
    }


"""Module for the custom field detail resource."""


class CustomFieldDetail(ResourceDetail):
    """
    Detail resource for custom fields.

    Provides get, patch & delete methods to retrieve
    a custom field, update it or to delete it.
    """

    def before_get(self, args, kwargs):
        """Return 404 Responses if CustomField not found"""
        check_if_object_not_found(self._data_layer.model, kwargs)

    def after_patch(self, result):
        """
        Add update description to related device.

        :param result:
        :return:
        """
        result_id = result["data"]["relationships"]["device"]["data"]["id"]
        msg = "update;custom field"
        query_device_and_set_update_description_text(msg, result_id)
        return result

    def before_delete(self, args, kwargs):
        custom_field = (
            db.session.query(CustomField).filter_by(id=kwargs["id"]).one_or_none()
        )
        if custom_field is None:
            raise ObjectNotFound("Object not found!")
        device = custom_field.get_parent()
        msg = "delete;custom field"
        set_update_description_text_and_update_by_user(device, msg)

    schema = CustomFieldSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": CustomField,
    }
