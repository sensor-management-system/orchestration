"""Resource classes for Configuration dynamic location end actions."""

from flask_rest_jsonapi import ResourceDetail, ResourceRelationship
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.orm.exc import NoResultFound

from ...frj_csv_export.resource import ResourceList
from ..models import Configuration, ConfigurationDynamicLocationEndAction
from ..models.base_model import db
from ..schemas.configuration_dynamic_location_actions_schema import (
    ConfigurationDynamicLocationEndActionSchema,
)
from ..token_checker import token_required


class ConfigurationDynamicLocationEndActionList(ResourceList):
    """List resource for Configuration dynamic location end actions (get, post)."""

    def query(self, view_kwargs):
        """
        Query the Configuration dynamic location end actions from the database.

        Also handle optional pre-filters (for specific configuration, for example).
        """
        query_ = self.session.query(ConfigurationDynamicLocationEndAction)
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
                    ConfigurationDynamicLocationEndAction.configuration_id
                    == configuration_id
                )
        return query_

    schema = ConfigurationDynamicLocationEndActionSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": ConfigurationDynamicLocationEndAction,
        "methods": {
            "query": query,
        },
    }


class ConfigurationDynamicLocationEndActionDetail(ResourceDetail):
    """Detail resource for Configuration dynamic location end actions (get, delete, patch)."""

    schema = ConfigurationDynamicLocationEndActionSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": ConfigurationDynamicLocationEndAction,
    }


class ConfigurationDynamicLocationEndActionRelationship(ResourceRelationship):
    """Relationship resource for Configuration dynamic location end actions."""

    schema = ConfigurationDynamicLocationEndActionSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": ConfigurationDynamicLocationEndAction,
    }
