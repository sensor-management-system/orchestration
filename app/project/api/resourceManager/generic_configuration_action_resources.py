"""Resource classes for generic configuration actions."""

from flask_rest_jsonapi import ResourceDetail, ResourceRelationship
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.orm.exc import NoResultFound

from ..auth.permission_utils import (
    get_query_with_permissions_for_configuration_related_objects,
    check_permissions_for_configuration_related_objects,
    check_patch_permission_for_configuration_related_objects,
    check_deletion_permission_for_configuration_related_objects,
    check_post_permission_for_configuration_related_objects,
)
from ..models.base_model import db
from ..models.configuration import Configuration
from ..models.generic_actions import GenericConfigurationAction
from ..resourceManager.base_resource import check_if_object_not_found
from ..schemas.generic_actions_schema import GenericConfigurationActionSchema
from ..token_checker import token_required
from ...frj_csv_export.resource import ResourceList


class GenericConfigurationActionList(ResourceList):
    """List resource for the generic configuration actions (get & post)."""

    def query(self, view_kwargs):
        """
        Query the actions from the database.

        Also handle optional pre-filters (for specific configurations, for example).
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
                    GenericConfigurationAction.configuration_id == configuration_id
                )
        return query_

    def before_post(self, args, kwargs, data=None):
        check_post_permission_for_configuration_related_objects()

    schema = GenericConfigurationActionSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": GenericConfigurationAction,
        "methods": {"query": query},
    }


class GenericConfigurationActionDetail(ResourceDetail):
    """Detail resources for generic configuration actions (get, delete, patch)."""

    def before_get(self, args, kwargs):
        """Return 404 Responses if GenericConfigurationAction not found"""
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

    schema = GenericConfigurationActionSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": GenericConfigurationAction,
    }


class GenericConfigurationActionRelationship(ResourceRelationship):
    """Relationship resources for generic configuration actions."""

    schema = GenericConfigurationActionSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": GenericConfigurationAction,
    }
