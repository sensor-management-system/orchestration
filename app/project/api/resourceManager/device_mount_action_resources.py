"""Resource classes for device mount actions."""
import json

from flask import request
from flask_rest_jsonapi import ResourceDetail, ResourceRelationship
from flask_rest_jsonapi.exceptions import ObjectNotFound, JsonApiException
from sqlalchemy.orm.exc import NoResultFound

from ..auth.permission_utils import (
    check_permissions_for_related_objects,
    get_collection_with_permissions,
    get_collection_with_permissions_for_related_objects,
)
from ..helpers.errors import ConflictError
from ..models.base_model import db
from ..models.configuration import Configuration
from ..models.device import Device
from ..models.mount_actions import DeviceMountAction
from ..models.platform import Platform
from ..schemas.mount_actions_schema import DeviceMountActionSchema
from ..token_checker import token_required
from ...frj_csv_export.resource import ResourceList


class DeviceMountActionList(ResourceList):
    """List resource for device mount actions (get, post)."""

    def after_get_collection(self, collection, qs, view_kwargs):
        """Take the intersection between requested collection and
        what the user allowed querying.

        :param collection:
        :param qs:
        :param view_kwargs:
        :return:
        """

        return get_collection_with_permissions_for_related_objects(
            self.model, collection
        )

    # def post(self, *args, **kwargs):
    #     data = json.loads(request.data.decode())["data"]
    #     device_id = data["relationships"]["device"]["data"]["id"]
    #     device = db.session.query(Device).filter_by(id=device_id).one_or_none()
    #     action = (
    #         db.session.query(DeviceMountAction)
    #         .filter_by(device_id=device_id)
    #         .one_or_none()
    #     )
    #     if device.is_private:
    #         raise ConflictError("Private device can't be used.")
    #     raise ConflictError(
    #         f"Device mounted on  Configuration with the id :{str(device.device_unmount_actions[-1].end_date)}"
    #     )
    #     if device.device_unmount_actions.end_date:
    #         raise ConflictError(
    #             f"Device mounted on  Configuration with the id :{str(device.device_unmount_actions[0])}"
    #         )
    #     try:
    #         super().post(*args, **kwargs)
    #     except JsonApiException as e:
    #         raise ConflictError("Mount failed.", str(e))

    def query(self, view_kwargs):
        """
        Query the actions from the database.

        Also handle optional pre-filters (for specific configurations, for example).
        """
        query_ = self.session.query(DeviceMountAction)
        configuration_id = view_kwargs.get("configuration_id")
        device_id = view_kwargs.get("device_id")
        parent_platform_id = view_kwargs.get("parent_platform_id")

        if configuration_id is not None:
            try:
                self.session.query(Configuration).filter_by(id=configuration_id).one()
            except NoResultFound:
                raise ObjectNotFound(
                    {"parameter": "id",},
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
                    {"parameter": "id",}, "Device: {} not found".format(device_id),
                )
            else:
                query_ = query_.filter(DeviceMountAction.device_id == device_id)
        if parent_platform_id is not None:
            try:
                self.session.query(Platform).filter_by(id=parent_platform_id).one()
            except NoResultFound:
                raise ObjectNotFound(
                    {"parameter": "id",},
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
        "methods": {"query": query, "after_get_collection": after_get_collection,},
    }


class DeviceMountActionDetail(ResourceDetail):
    """Detail resource for device mount actions (get, delete, patch)."""

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
