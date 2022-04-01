"""Resource classes for Configuration static location begin actions."""

from flask_rest_jsonapi import ResourceDetail, ResourceRelationship
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.orm.exc import NoResultFound

from .base_resource import check_if_object_not_found
from ..auth.permission_utils import (
    get_query_with_permissions_for_configuration_related_objects,
    check_permissions_for_configuration_related_objects,
    check_patch_permission_for_configuration_related_objects,
    check_deletion_permission_for_configuration_related_objects,
    check_post_permission_for_configuration_related_objects,
)
from ..models import Configuration, ConfigurationStaticLocationBeginAction
from ..models.base_model import db
from ..schemas.configuration_static_location_actions_schema import (
    ConfigurationStaticLocationBeginActionSchema,
)
from ..token_checker import token_required
from ...frj_csv_export.resource import ResourceList


class ConfigurationStaticLocationBeginActionList(ResourceList):
    """List resource for Configuration static location begin actions (get, post)."""

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
                    {"parameter": "id",},
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
        "methods": {"query": query},
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
