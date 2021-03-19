"""Resource classes for platform unmount actions."""
from flask_rest_jsonapi import ResourceDetail, ResourceRelationship
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.orm.exc import NoResultFound

from project.api.models.base_model import db
from project.api.models.configuration import Configuration
from project.api.models.platform import Platform
from project.api.models.unmount_actions import PlatformUnmountAction
from project.api.resourceManager.base_resource import (
    add_created_by_id,
    add_updated_by_id,
)
from project.api.schemas.unmount_actions_schema import PlatformUnmountActionSchema
from project.api.token_checker import token_required
from project.frj_csv_export.resource import ResourceList


class PlatformUnmountActionList(ResourceList):
    """List resource for platform unmount actions (get, post)."""

    def before_create_object(self, data, *args, **kwargs):
        """Use jwt to add user id to dataset."""
        add_created_by_id(data)

    def query(self, view_kwargs):
        """
        Query the actions from the database.

        Also handle optional pre-filters (for specific configurations, for example).
        """
        query_ = self.session.query(PlatformUnmountAction)
        configuration_id = view_kwargs.get("configuration_id")
        platform_id = view_kwargs.get("platform_id")
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
                    PlatformUnmountAction.configuration_id == configuration_id
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
                query_ = query_.filter(PlatformUnmountAction.platform_id == platform_id)
        return query_

    schema = PlatformUnmountActionSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": PlatformUnmountAction,
        "methods": {
            "before_create_object": before_create_object,
            "query": query,
        },
    }


class PlatformUnmountActionDetail(ResourceDetail):
    """Detail resource for platform unmount actions (get, delete, patch)."""

    def before_patch(self, args, kwargs, data):
        """Add Created by user id to the data."""
        add_updated_by_id(data)

    schema = PlatformUnmountActionSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": PlatformUnmountAction,
    }


class PlatformUnmountActionRelationship(ResourceRelationship):
    """Relationship resource for platform unmount actions."""

    schema = PlatformUnmountActionSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": PlatformUnmountAction,
    }
