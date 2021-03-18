"""Resource classes for generic configuration actions."""

from flask_rest_jsonapi import ResourceDetail, ResourceRelationship
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.orm.exc import NoResultFound

from project.api.models.base_model import db
from project.api.models.configuration import Configuration
from project.api.models.generic_actions import GenericConfigurationAction
from project.api.resourceManager.base_resource import (
    add_created_by_id,
    add_updated_by_id,
)
from project.api.schemas.generic_actions_schema import GenericConfigurationActionSchema
from project.api.token_checker import token_required
from project.frj_csv_export.resource import ResourceList


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
        query_ = self.session.query(GenericConfigurationAction)
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

    schema = GenericConfigurationActionSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": GenericConfigurationAction,
        "methods": {"before_create_object": before_create_object, "query": query},
    }


class GenericConfigurationActionDetail(ResourceDetail):
    """Detail resources for generic configuration actions (get, delete, patch)."""

    def before_patch(self, args, kwargs, data):
        """Add Created by user id to the data."""
        add_updated_by_id(data)

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
