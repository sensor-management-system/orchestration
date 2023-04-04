"""Resource classes for generic configuration actions."""

from flask_rest_jsonapi import ResourceDetail
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.orm.exc import NoResultFound

from ...frj_csv_export.resource import ResourceList
from ..helpers.resource_mixin import add_created_by_id, add_updated_by_id
from ..models.base_model import db
from ..models.configuration import Configuration
from ..models.generic_actions import GenericConfigurationAction
from ..permissions.common import DelegateToCanFunctions
from ..permissions.rules import filter_visible
from ..resources.base_resource import (
    check_if_object_not_found,
    query_configuration_and_set_update_description_text,
    set_update_description_text_and_update_by_user,
)
from ..schemas.generic_actions_schema import GenericConfigurationActionSchema
from ..token_checker import token_required


class GenericConfigurationActionList(ResourceList):
    """List resource for the generic configuration actions (get & post)."""

    def before_create_object(self, data, *args, **kwargs):
        """Use jwt to add user id to dataset."""
        add_created_by_id(data)

    def query(self, view_kwargs):
        """
        Query the actions from the database.

        Also handle optional pre-filters (for specific configurations, for example).
        """
        query_ = filter_visible(self.session.query(self.model))
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
                    GenericConfigurationAction.configuration_id == configuration_id
                )
        return query_

    def after_post(self, result):
        """
        Add update description to related configuration.

        :param result:
        :return:
        """
        result_id = result[0]["data"]["relationships"]["configuration"]["data"]["id"]
        msg = "create;action"
        query_configuration_and_set_update_description_text(msg, result_id)

        return result

    schema = GenericConfigurationActionSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": GenericConfigurationAction,
        "methods": {"before_create_object": before_create_object, "query": query},
    }
    permission_classes = [DelegateToCanFunctions]


class GenericConfigurationActionDetail(ResourceDetail):
    """Detail resources for generic configuration actions (get, delete, patch)."""

    def before_get(self, args, kwargs):
        """Return 404 Responses if GenericConfigurationAction not found."""
        check_if_object_not_found(self._data_layer.model, kwargs)

    def before_patch(self, args, kwargs, data=None):
        """Add the updated by info."""
        add_updated_by_id(data)

    def after_patch(self, result):
        """
        Add update description to related configuration.

        :param result:
        :return:
        """
        result_id = result["data"]["relationships"]["configuration"]["data"]["id"]
        msg = "update;action"
        query_configuration_and_set_update_description_text(msg, result_id)
        return result

    def before_delete(self, args, kwargs):
        """Update the configurations update description."""
        action = (
            db.session.query(GenericConfigurationAction)
            .filter_by(id=kwargs["id"])
            .one_or_none()
        )
        if action is None:
            raise ObjectNotFound("Object not found!")
        configuration = action.get_parent()
        msg = "delete;action"
        set_update_description_text_and_update_by_user(configuration, msg)

    schema = GenericConfigurationActionSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": GenericConfigurationAction,
    }
    permission_classes = [DelegateToCanFunctions]
