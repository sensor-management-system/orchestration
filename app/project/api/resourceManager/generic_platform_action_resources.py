"""Resource classes for the generic platform actions."""

from flask_rest_jsonapi import ResourceDetail, ResourceRelationship
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.orm.exc import NoResultFound

from ...frj_csv_export.resource import ResourceList
from ..helpers.errors import MethodNotAllowed
from ..models.base_model import db
from ..models.generic_actions import GenericPlatformAction
from ..models.platform import Platform
from ..resourceManager.base_resource import (
    add_created_by_id,
    add_updated_by_id,
    check_if_object_not_found,
)
from ..schemas.generic_actions_schema import GenericPlatformActionSchema
from ..token_checker import token_required


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
        query_ = self.session.query(GenericPlatformAction)
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
        """Add Created by user id to the data."""
        add_updated_by_id(data)

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


class GenericPlatformActionRelationshipReadOnly(GenericPlatformActionRelationship):
    """A readonly relationship endpoint for generic platform actions."""

    def before_post(self, args, kwargs, json_data=None):
        raise MethodNotAllowed("This endpoint is readonly!")

    def before_patch(self, args, kwargs, data=None):
        raise MethodNotAllowed("This endpoint is readonly!")

    def before_delete(self, args, kwargs):
        raise MethodNotAllowed("This endpoint is readonly!")
