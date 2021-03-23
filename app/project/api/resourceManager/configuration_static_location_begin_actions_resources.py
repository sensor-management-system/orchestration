"""Resource classes for Configuration static location begin actions."""

from flask_rest_jsonapi import ResourceDetail, ResourceRelationship
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.orm.exc import NoResultFound

from ..models import ConfigurationStaticLocationBeginAction, Configuration
from ..models.base_model import db
from ..schemas.configuration_static_location_actions_schema import \
    ConfigurationStaticLocationBeginActionSchema
from ..token_checker import token_required
from ...frj_csv_export.resource import ResourceList


class ConfigurationStaticLocationBeginActionList(ResourceList):
    """List resource for Configuration static location begin actions (get, post)."""

    def query(self, view_kwargs):
        """
        Query the Configuration static location begin actions from the database.

        Also handle optional pre-filters (for specific configuration, for example).
        """
        query_ = self.session.query(ConfigurationStaticLocationBeginAction)
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
                    ConfigurationStaticLocationBeginAction.configuration_id == configuration_id)
        return query_

    schema = ConfigurationStaticLocationBeginActionSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": ConfigurationStaticLocationBeginAction,
        "methods": {
            "query": query,
        },
    }


class ConfigurationStaticLocationBeginActionDetail(ResourceDetail):
    """Detail resource for Configuration static location begin actions (get, delete, patch)."""

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
