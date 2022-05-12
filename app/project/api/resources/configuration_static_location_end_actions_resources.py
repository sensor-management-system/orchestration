"""Resource classes for Configuration static location end actions."""

from flask_rest_jsonapi import ResourceDetail, ResourceRelationship
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.orm.exc import NoResultFound

from ...frj_csv_export.resource import ResourceList
from ..auth.permission_utils import (
    check_permissions_for_configuration_related_objects,
    check_post_permission_for_configuration_related_objects,
    get_query_with_permissions_for_configuration_related_objects,
)
from ..helpers.resource_mixin import add_created_by_id, add_updated_by_id
from ..models import Configuration, ConfigurationStaticLocationEndAction
from ..models.base_model import db
from ..schemas.configuration_static_location_actions_schema import (
    ConfigurationStaticLocationEndActionSchema,
)
from ..token_checker import token_required
from .base_resource import check_if_object_not_found


class ConfigurationStaticLocationEndActionList(ResourceList):
    """List resource for Configuration static location end actions (get, post)."""

    def before_create_object(self, data, *args, **kwargs):
        """Use jwt to add user id to dataset."""
        add_created_by_id(data)

    def query(self, view_kwargs):
        """
        Query the Configuration static location end actions from the database.

        Also handle optional pre-filters (for specific configuration, for example).
        """
        query_ = get_query_with_permissions_for_configuration_related_objects(
            self.model
        )
        configuration_id = view_kwargs.get("configuration_id")

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
                    ConfigurationStaticLocationEndAction.configuration_id
                    == configuration_id
                )
        return query_

    def before_post(self, args, kwargs, data=None):
        check_post_permission_for_configuration_related_objects()

    schema = ConfigurationStaticLocationEndActionSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": ConfigurationStaticLocationEndAction,
        "methods": {
            "query": query,
            "before_create_object": before_create_object,
        },
    }


class ConfigurationStaticLocationEndActionDetail(ResourceDetail):
    """Detail resource for Configuration static location end actions (get, delete, patch)."""

    def before_get(self, args, kwargs):
        """Return 404 Responses if ConfigurationStaticLocationEndAction not found"""
        check_if_object_not_found(self._data_layer.model, kwargs)
        check_permissions_for_configuration_related_objects(
            self._data_layer.model, kwargs["id"]
        )

    def before_patch(self, args, kwargs, data):
        """Add updated by user id to the data."""
        add_updated_by_id(data)

    schema = ConfigurationStaticLocationEndActionSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": ConfigurationStaticLocationEndAction,
    }


class ConfigurationStaticLocationEndActionRelationship(ResourceRelationship):
    """Relationship resource for Configuration static location end actions."""

    schema = ConfigurationStaticLocationEndActionSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": ConfigurationStaticLocationEndAction,
    }
