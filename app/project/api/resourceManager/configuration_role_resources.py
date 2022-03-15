from flask_rest_jsonapi import ResourceDetail
from flask_rest_jsonapi import ResourceRelationship

from .base_resource import check_if_object_not_found
from ..models.base_model import db
from ..models.contact_role import ConfigurationContactRole
from ..schemas.role import ConfigurationRoleSchema
from ..token_checker import token_required
from ...frj_csv_export.resource import ResourceList


class ConfigurationRoleList(ResourceList):
    """
    provides get and post methods to retrieve
    a collection of Configuration Role or create one.
    """

    schema = ConfigurationRoleSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": ConfigurationContactRole,
    }


class ConfigurationRoleDetail(ResourceDetail):
    """
    provides get, patch and delete methods to retrieve details
    of an object, update an object and delete a Configuration Role
    """

    def before_get(self, args, kwargs):
        """Return 404 Responses if role not found"""
        check_if_object_not_found(self._data_layer.model, kwargs)

    schema = ConfigurationRoleSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": ConfigurationContactRole,
    }


class ConfigurationRoleRelationship(ResourceRelationship):
    """
    provides get, post, patch and delete methods to get relationships,
    create relationships, update relationships and delete
    relationships between Configuration Role and other objects.
    """

    schema = ConfigurationRoleSchema
    decorators = (token_required,)
    data_layer = {"session": db.session, "model": ConfigurationContactRole}
