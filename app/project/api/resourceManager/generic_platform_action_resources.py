"""Resource classes for the generic platform actions."""

from flask_rest_jsonapi import ResourceDetail, ResourceRelationship
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.orm.exc import NoResultFound

from project.api.models.base_model import db
from project.api.models.generic_actions import GenericPlatformAction
from project.api.models.platform import Platform
from project.api.resourceManager.base_resource import (
    add_created_by_id,
    add_updated_by_id,
)
from project.api.schemas.generic_actions_schema import GenericPlatformActionSchema
from project.api.token_checker import token_required
from project.frj_csv_export.resource import ResourceList


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
