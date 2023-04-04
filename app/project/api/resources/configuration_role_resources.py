"""Resources for configuration contact roles."""

from flask_rest_jsonapi import ResourceDetail
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.exc import NoResultFound

from ...frj_csv_export.resource import ResourceList
from ..models import Configuration
from ..models.base_model import db
from ..models.contact_role import ConfigurationContactRole
from ..permissions.common import DelegateToCanFunctions
from ..permissions.rules import filter_visible
from ..schemas.role import ConfigurationRoleSchema
from ..token_checker import token_required
from .base_resource import (
    check_if_object_not_found,
    query_configuration_and_set_update_description_text,
    set_update_description_text_and_update_by_user,
)


class ConfigurationRoleList(ResourceList):
    """
    List resource for configuration contact roles.

    Provides get and post methods to retrieve
    a collection of Configuration Role or create one.
    """

    def query(self, view_kwargs):
        """Query the entries from the database."""
        query_ = filter_visible(self.session.query(self.model))
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

    def after_post(self, result):
        """
        Add update description to related platform.

        :param result:
        :return:
        """
        result_id = result[0]["data"]["relationships"]["configuration"]["data"]["id"]
        msg = "create;contact"
        query_configuration_and_set_update_description_text(msg, result_id)

        return result

    schema = ConfigurationRoleSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": ConfigurationContactRole,
        "methods": {"query": query},
    }
    permission_classes = [DelegateToCanFunctions]


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

    def after_patch(self, result):
        """
        Add update description to related configuration.

        :param result:
        :return:
        """
        result_id = result["data"]["relationships"]["configuration"]["data"]["id"]
        msg = "update;contact"
        query_configuration_and_set_update_description_text(msg, result_id)
        return result

    def before_delete(self, args, kwargs):
        """Check that we are allowed to delete."""
        contact_role = (
            db.session.query(ConfigurationContactRole)
            .filter_by(id=kwargs["id"])
            .one_or_none()
        )
        if contact_role is None:
            raise ObjectNotFound("Object not found!")
        configuration = contact_role.get_parent()
        msg = "delete;contact"
        set_update_description_text_and_update_by_user(configuration, msg)

    schema = ConfigurationRoleSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": ConfigurationContactRole,
    }
    permission_classes = [DelegateToCanFunctions]
