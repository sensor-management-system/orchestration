"""Resource classes for platform mount actions."""

from flask_rest_jsonapi import ResourceDetail, ResourceRelationship
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.orm.exc import NoResultFound

from ...frj_csv_export.resource import ResourceList
from ..auth.permission_utils import get_query_with_permissions_for_related_objects
from ..helpers.mounting_checks import PlatformMountActionValidator
from ..helpers.resource_mixin import (
    add_created_by_id,
    add_updated_by_id,
    decode_json_request_data,
)
from ..models.base_model import db
from ..models.configuration import Configuration
from ..models.mount_actions import PlatformMountAction
from ..models.platform import Platform
from ..resources.base_resource import (
    check_if_object_not_found,
    query_configuration_and_set_update_description_text,
    set_update_description_text_and_update_by_user,
)
from ..schemas.mount_actions_schema import PlatformMountActionSchema
from ..token_checker import token_required


class PlatformMountActionList(ResourceList):
    """List resource for platform mount actions (get, post)."""

    validator = PlatformMountActionValidator()

    def before_post(self, args, kwargs, data=None):
        data_with_relationships = decode_json_request_data()
        self.validator.validate_create(data_with_relationships)

    def before_create_object(self, data, *args, **kwargs):
        """Use jwt to add user id to dataset."""
        add_created_by_id(data)

    def query(self, view_kwargs):
        """
        Query the actions from the database.

        Also handle optional pre-filters (for specific configurations, for example).
        """
        query_ = get_query_with_permissions_for_related_objects(self.model)
        configuration_id = view_kwargs.get("configuration_id")
        platform_id = view_kwargs.get("platform_id")
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
                    PlatformMountAction.configuration_id == configuration_id
                )
        if platform_id is not None:
            try:
                self.session.query(Platform).filter_by(id=platform_id).one()
            except NoResultFound:
                raise ObjectNotFound(
                    {
                        "parameter": "id",
                    },
                    "Platform: {} not found".format(platform_id),
                )
            else:
                query_ = query_.filter(PlatformMountAction.platform_id == platform_id)
        if parent_platform_id is not None:
            try:
                self.session.query(Platform).filter_by(id=parent_platform_id).one()
            except NoResultFound:
                raise ObjectNotFound(
                    {
                        "parameter": "id",
                    },
                    "Parent platform: {} not found".format(parent_platform_id),
                )
            else:
                query_ = query_.filter(
                    PlatformMountAction.parent_platform_id == parent_platform_id
                )
        return query_

    def after_post(self, result):
        """
        Add update description to related platform.

        :param result:
        :return:
        """
        result_id = result[0]["data"]["relationships"]["configuration"]["data"]["id"]
        msg = "create;platform mount action"
        query_configuration_and_set_update_description_text(msg, result_id)

        return result

    schema = PlatformMountActionSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": PlatformMountAction,
        "methods": {"before_create_object": before_create_object, "query": query,},
    }


class PlatformMountActionDetail(ResourceDetail):
    """Detail resource for platform mount actions (get, delete, patch)."""

    validator = PlatformMountActionValidator()

    def before_get(self, args, kwargs):
        """Return 404 Responses if PlatformMountAction not found"""
        check_if_object_not_found(self._data_layer.model, kwargs)

    def before_patch(self, args, kwargs, data):
        """
        Do some checks if the wanted time-interval is available or not & some additional checks.
        """
        data_with_relationships = decode_json_request_data()
        self.validator.validate_update(data_with_relationships, kwargs["id"])
        add_updated_by_id(data)

    def after_patch(self, result):
        """
        Add update description to related configuration.

        :param result:
        :return:
        """
        result_id = result["data"]["relationships"]["configuration"]["data"]["id"]
        msg = "update;platform mount action"
        query_configuration_and_set_update_description_text(msg, result_id)
        return result

    def before_delete(self, args, kwargs):
        """Do some checks for possible orphans."""
        self.validator.validate_delete(kwargs["id"])
        mount_action = (
            db.session.query(PlatformMountAction).filter_by(id=kwargs["id"]).one_or_none()
        )
        if mount_action is None:
            raise ObjectNotFound("Object not found!")
        configuration = mount_action.configuration
        msg = "delete;platform mount action"
        set_update_description_text_and_update_by_user(configuration, msg)

    schema = PlatformMountActionSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": PlatformMountAction,
    }


class PlatformMountActionRelationship(ResourceRelationship):
    """Relationship resource for platform mount actions."""

    schema = PlatformMountActionSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": PlatformMountAction,
    }
