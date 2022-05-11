"""Resources for configuration contact roles."""

from flask_rest_jsonapi import ResourceDetail, ResourceRelationship
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.exc import NoResultFound

from ..auth.permission_utils import (
    check_deletion_permission_for_configuration_related_objects,
    check_patch_permission_for_configuration_related_objects,
    check_permissions_for_configuration_related_objects,
    check_post_permission_for_configuration_related_objects,
    get_query_with_permissions_for_configuration_related_objects,
)
from ..models import Configuration
from ..models.base_model import db
from ..models.contact_role import ConfigurationContactRole
from ..schemas.role import ConfigurationRoleSchema
from ..token_checker import token_required
from .base_resource import check_if_object_not_found
from ...frj_csv_export.resource import ResourceList


class ConfigurationRoleList(ResourceList):
    """
    List resource for configuration contact roles.

    Provides get and post methods to retrieve
    a collection of Configuration Role or create one.
    """

    def query(self, view_kwargs):
        """Query the entries from the database."""
        query_ = get_query_with_permissions_for_configuration_related_objects(
            self.model
        )
        configuration_id = view_kwargs.get("configuration_id")

        if configuration_id is not None:
            try:
                self.session.query(Configuration).filter_by(id=configuration_id).one()
            except NoResultFound:
                raise ObjectNotFound(
                    {"parameter": "id"},
                    "Configuration: {} not found".format(configuration_id),
                )
            query_ = query_.filter(
                ConfigurationContactRole.configuration_id == configuration_id
            )
        return query_

    def before_post(self, args, kwargs, data=None):
        """Run some checks to ensure we are allows to post."""
        check_post_permission_for_configuration_related_objects()

    schema = ConfigurationRoleSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": ConfigurationContactRole,
        "methods": {"query": query},
    }


class ConfigurationRoleDetail(ResourceDetail):
    """
    Detail resource for configuration contact roles.

    Provides get, patch and delete methods to retrieve details
    of an object, update an object and delete a Configuration Role.
    """
    def before_get(self, args, kwargs):
        """
        Return 404 Responses if role not found.

        Also check if we are allowed to see the entry.
        """
        check_if_object_not_found(self._data_layer.model, kwargs)
        check_permissions_for_configuration_related_objects(
            self._data_layer.model, kwargs["id"]
        )

    def before_patch(self, args, kwargs, data=None):
        """Check that we are allowed to patch."""
        check_patch_permission_for_configuration_related_objects(
            kwargs, self._data_layer.model
        )

    def before_delete(self, args, kwargs):
        """Check that we are allowed to delete."""
        check_deletion_permission_for_configuration_related_objects(
            kwargs, self._data_layer.model
        )

    schema = ConfigurationRoleSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": ConfigurationContactRole,
    }


class ConfigurationRoleRelationship(ResourceRelationship):
    """
    Relationship resource for configuration contact roles.

    Provides get, post, patch and delete methods to get relationships,
    create relationships, update relationships and delete
    relationships between Configuration Role and other objects.
    """

    schema = ConfigurationRoleSchema
    decorators = (token_required,)
    data_layer = {"session": db.session, "model": ConfigurationContactRole}
