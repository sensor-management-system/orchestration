from flask_rest_jsonapi import ResourceDetail
from flask_rest_jsonapi import ResourceRelationship
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.exc import NoResultFound

from .base_resource import check_if_object_not_found
from ..models import Configuration
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

    def query(self, view_kwargs):
        """
        Query the entries from the database.
        """
        query_ = self.session.query(ConfigurationContactRole)
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

    schema = ConfigurationRoleSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": ConfigurationContactRole,
        "methods": {"query": query},
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
