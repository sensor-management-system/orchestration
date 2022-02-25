"""Resource classes for Configuration static location end actions."""

from flask_rest_jsonapi import ResourceDetail, ResourceRelationship
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.orm.exc import NoResultFound

from .base_resource import check_if_object_not_found
from ..models import Configuration, ConfigurationStaticLocationEndAction
from ..models.base_model import db
from ..schemas.configuration_static_location_actions_schema import (
    ConfigurationStaticLocationEndActionSchema,
)
from ..token_checker import token_required
from ...frj_csv_export.resource import ResourceList


class ConfigurationStaticLocationEndActionList(ResourceList):
    """List resource for Configuration static location end actions (get, post)."""

    def query(self, view_kwargs):
        """
        Query the Configuration static location end actions from the database.

        Also handle optional pre-filters (for specific configuration, for example).
        """
        query_ = self.session.query(ConfigurationStaticLocationEndAction)
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
                    ConfigurationStaticLocationEndAction.configuration_id
                    == configuration_id
                )
        return query_

    schema = ConfigurationStaticLocationEndActionSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": ConfigurationStaticLocationEndAction,
        "methods": {"query": query,},
    }


class ConfigurationStaticLocationEndActionDetail(ResourceDetail):
    """Detail resource for Configuration static location end actions (get, delete, patch)."""

    def before_get(self, args, kwargs):
        """Return 404 Responses if ConfigurationStaticLocationEndAction not found"""
        check_if_object_not_found(self._data_layer.model, kwargs)

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
