"""Resource classes for Configuration static location begin actions."""

from flask_rest_jsonapi import ResourceDetail, ResourceRelationship
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.orm.exc import NoResultFound

from ...frj_csv_export.resource import ResourceList
from ..auth.permission_utils import (
    check_deletion_permission_for_configuration_related_objects,
    check_patch_permission_for_configuration_related_objects,
    check_permissions_for_configuration_related_objects,
    check_post_permission_for_configuration_related_objects,
    get_query_with_permissions_for_configuration_related_objects,
)
from ..helpers.resource_mixin import add_created_by_id, add_updated_by_id
from ..models import Configuration, ConfigurationStaticLocationBeginAction
from ..models.base_model import db
from ..schemas.configuration_static_location_actions_schema import (
    ConfigurationStaticLocationBeginActionSchema,
)
from ..token_checker import token_required
from .base_resource import check_if_object_not_found


class ConfigurationStaticLocationBeginActionList(ResourceList):
    """List resource for Configuration static location begin actions (get, post)."""

    def before_create_object(self, data, *args, **kwargs):
        """Use jwt to add user id to dataset."""
        add_created_by_id(data)

    def query(self, view_kwargs):
        """
        Query the Configuration static location begin actions from the database.

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
                    ConfigurationStaticLocationBeginAction.configuration_id
                    == configuration_id
                )
        return query_

    def before_post(self, args, kwargs, data=None):
        check_post_permission_for_configuration_related_objects()

    schema = ConfigurationStaticLocationBeginActionSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": ConfigurationStaticLocationBeginAction,
        "methods": {
            "query": query,
            "before_create_object": before_create_object,
        },
    }


class ConfigurationStaticLocationBeginActionDetail(ResourceDetail):
    """Detail resource for Configuration static location begin actions (get, delete, patch)."""

    def before_get(self, args, kwargs):
        """Return 404 Responses if ConfigurationStaticLocationBeginAction not found"""
        check_if_object_not_found(self._data_layer.model, kwargs)
        check_permissions_for_configuration_related_objects(
            self._data_layer.model, kwargs["id"]
        )

    def before_patch(self, args, kwargs, data=None):
        check_patch_permission_for_configuration_related_objects(
            kwargs, self._data_layer.model
        )
        add_updated_by_id(data)

    def before_delete(self, args, kwargs):
        check_deletion_permission_for_configuration_related_objects(
            kwargs, self._data_layer.model
        )

    schema = ConfigurationStaticLocationBeginActionSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": ConfigurationStaticLocationBeginAction,
    }


class ConfigurationStaticLocationBeginActionRelationship(ResourceRelationship):
    """Relationship resource for Configuration static location begin actions."""

    schema = ConfigurationStaticLocationBeginActionSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": ConfigurationStaticLocationBeginAction,
    }
