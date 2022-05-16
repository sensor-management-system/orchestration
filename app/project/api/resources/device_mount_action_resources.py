"""Resource classes for device mount actions."""

from flask_rest_jsonapi import ResourceDetail, ResourceRelationship, ResourceList
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.orm.exc import NoResultFound

from ..auth.permission_utils import get_query_with_permissions_for_related_objects
from ..helpers.mounting_checks import assert_object_is_free_to_be_mounted
from ..helpers.resource_mixin import decode_json_request_data
from ..models.base_model import db
from ..models.configuration import Configuration
from ..models.device import Device
from ..models.mount_actions import DeviceMountAction
from ..models.platform import Platform
from ..resources.base_resource import check_if_object_not_found
from ..schemas.mount_actions_schema import DeviceMountActionSchema
from ..token_checker import token_required


class DeviceMountActionList(ResourceList):
    """List resource for device mount actions (get, post)."""

    def before_post(self, args, kwargs, data=None):
        data_with_relationships = decode_json_request_data()
        assert_object_is_free_to_be_mounted(data_with_relationships)

    def query(self, view_kwargs):
        """
        Query the actions from the database.

        Also handle optional pre-filters (for specific configurations, for example).
        """
        query_ = get_query_with_permissions_for_related_objects(self.model)
        configuration_id = view_kwargs.get("configuration_id")
        device_id = view_kwargs.get("device_id")
        parent_platform_id = view_kwargs.get("parent_platform_id")

        if configuration_id is not None:
            try:
                self.session.query(Configuration).filter_by(id=configuration_id).one()
            except NoResultFound:
                raise ObjectNotFound(
                    {
                        "parameter": "id",
                    },
                    "Configuration: {} not found".format(configuration_id),
                )
            else:
                query_ = query_.filter(
                    DeviceMountAction.configuration_id == configuration_id
                )
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
                query_ = query_.filter(DeviceMountAction.device_id == device_id)
        if parent_platform_id is not None:
            try:
                self.session.query(Platform).filter_by(id=parent_platform_id).one()
            except NoResultFound:
                raise ObjectNotFound(
                    {
                        "parameter": "id",
                    },
                    "Platform: {} not found".format(parent_platform_id),
                )
            else:
                query_ = query_.filter(
                    DeviceMountAction.parent_platform_id == parent_platform_id
                )

        return query_

    schema = DeviceMountActionSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": DeviceMountAction,
        "methods": {"query": query, },
    }


class DeviceMountActionDetail(ResourceDetail):
    """Detail resource for device mount actions (get, delete, patch)."""

    def before_get(self, args, kwargs):
        """Return 404 Responses if DeviceMountAction not found"""
        check_if_object_not_found(self._data_layer.model, kwargs)

    schema = DeviceMountActionSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": DeviceMountAction,
    }


class DeviceMountActionRelationship(ResourceRelationship):
    """Relationship resource for device mount actions."""

    schema = DeviceMountActionSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": DeviceMountAction,
    }
