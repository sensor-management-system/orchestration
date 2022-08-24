"""Resource classes for the generic platform actions."""

from flask_rest_jsonapi import ResourceDetail, ResourceRelationship
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.orm.exc import NoResultFound

from ...frj_csv_export.resource import ResourceList
from ..auth.permission_utils import get_query_with_permissions_for_related_objects
from ..helpers.resource_mixin import add_created_by_id, add_updated_by_id
from ..models.base_model import db
from ..models.generic_actions import GenericPlatformAction
from ..models.platform import Platform
from ..schemas.generic_actions_schema import GenericPlatformActionSchema
from ..token_checker import token_required
from .base_resource import (
    check_if_object_not_found,
    query_platform_and_set_update_description_text,
    set_update_description_text_and_update_by_user,
)


class GenericPlatformActionList(ResourceList):
    """List resource for generic platform actions (get & post)."""

    def before_create_object(self, data, *args, **kwargs):
        """Use jwt to add user id to dataset."""
        add_created_by_id(data)

    def query(self, view_kwargs):
        """
        Query the actions from the database.

        Also handle optional pre-filters (for specific platforms, for example).
        """
        query_ = get_query_with_permissions_for_related_objects(self.model)
        platform_id = view_kwargs.get("platform_id")

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
                query_ = query_.filter(GenericPlatformAction.platform_id == platform_id)
        return query_

    def after_post(self, result):
        """
        Add update description to related platform.

        :param result:
        :return:
        """
        result_id = result[0]["data"]["relationships"]["platform"]["data"]["id"]
        msg = "create;action"
        query_platform_and_set_update_description_text(msg, result_id)

        return result

    schema = GenericPlatformActionSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": GenericPlatformAction,
        "methods": {
            "before_create_object": before_create_object,
            "query": query,
        },
    }


class GenericPlatformActionDetail(ResourceDetail):
    """Detail resource for generic platform actions (get, delete, patch)."""

    def before_get(self, args, kwargs):
        """Return 404 Responses if GenericPlatformAction not found"""
        check_if_object_not_found(self._data_layer.model, kwargs)

    def before_patch(self, args, kwargs, data):
        """Add updated by user id to the data."""
        add_updated_by_id(data)

    def after_patch(self, result):
        """
        Add update description to related platform.

        :param result:
        :return:
        """
        result_id = result["data"]["relationships"]["platform"]["data"]["id"]
        msg = "update;action"
        query_platform_and_set_update_description_text(msg, result_id)
        return result

    def before_delete(self, args, kwargs):
        action = (
            db.session.query(GenericPlatformAction)
            .filter_by(id=kwargs["id"])
            .one_or_none()
        )
        if action is None:
            raise ObjectNotFound("Object not found!")
        platform = action.get_parent()
        msg = "delete;action"
        set_update_description_text_and_update_by_user(platform, msg)

    schema = GenericPlatformActionSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": GenericPlatformAction,
    }


class GenericPlatformActionRelationship(ResourceRelationship):
    """Relationship resource for the generic platform actions."""

    schema = GenericPlatformActionSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": GenericPlatformAction,
    }
