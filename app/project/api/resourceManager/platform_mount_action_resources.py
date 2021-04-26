"""Resource classes for platform mount actions."""

from flask_rest_jsonapi import ResourceDetail, ResourceRelationship
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.orm.exc import NoResultFound

from ...frj_csv_export.resource import ResourceList
from ..models.base_model import db
from ..models.configuration import Configuration
from ..models.mount_actions import PlatformMountAction
from ..models.platform import Platform
from ..resourceManager.base_resource import add_created_by_id, add_updated_by_id
from ..schemas.mount_actions_schema import PlatformMountActionSchema
from ..token_checker import token_required


class PlatformMountActionList(ResourceList):
    """List resource for platform mount actions (get, post)."""

    def before_create_object(self, data, *args, **kwargs):
        """Use jwt to add user id to dataset."""
        add_created_by_id(data)

    def query(self, view_kwargs):
        """
        Query the actions from the database.

        Also handle optional pre-filters (for specific configurations, for example).
        """
        query_ = self.session.query(PlatformMountAction)
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

    schema = PlatformMountActionSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": PlatformMountAction,
        "methods": {
            "before_create_object": before_create_object,
            "query": query,
        },
    }


class PlatformMountActionDetail(ResourceDetail):
    """Detail resource for platform mount actions (get, delete, patch)."""

    def before_patch(self, args, kwargs, data):
        """Add Created by user id to the data."""
        add_updated_by_id(data)

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
