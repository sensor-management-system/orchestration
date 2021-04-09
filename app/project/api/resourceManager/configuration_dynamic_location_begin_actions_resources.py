"""Resource classes for Configuration dynamic location begin actions."""

from flask_rest_jsonapi import ResourceDetail, ResourceRelationship
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.orm.exc import NoResultFound

from ...frj_csv_export.resource import ResourceList
from ..models import (
    Configuration,
    ConfigurationDynamicLocationBeginAction,
    DeviceProperty,
)
from ..models.base_model import db
from ..schemas.configuration_dynamic_location_actions_schema import (
    ConfigurationDynamicLocationBeginActionSchema,
)
from ..token_checker import token_required


class ConfigurationDynamicLocationBeginActionList(ResourceList):
    """List resource for Configuration dynamic location begin actions (get, post)."""

    def query(self, view_kwargs):
        """
        Query the Configuration dynamic location begin actions from the database.

        Also handle optional pre-filters (for specific configuration, for example).
        """
        query_ = self.session.query(ConfigurationDynamicLocationBeginAction)
        configuration_id = view_kwargs.get("configuration_id")
        x_property_id = view_kwargs.get("x_property_id")
        y_property_id = view_kwargs.get("y_property_id")
        z_property_id = view_kwargs.get("z_property_id")

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
                    ConfigurationDynamicLocationBeginAction.configuration_id
                    == configuration_id
                )
        if x_property_id is not None:
            try:
                self.session.query(DeviceProperty).filter_by(id=x_property_id).one()
            except NoResultFound:
                raise ObjectNotFound(
                    {
                        "parameter": "id",
                    },
                    "Device property: {} not found".format(x_property_id),
                )
            else:
                query_ = query_.filter(
                    ConfigurationDynamicLocationBeginAction.x_property_id
                    == x_property_id
                )
        if y_property_id is not None:
            try:
                self.session.query(DeviceProperty).filter_by(id=y_property_id).one()
            except NoResultFound:
                raise ObjectNotFound(
                    {
                        "parameter": "id",
                    },
                    "Device property: {} not found".format(y_property_id),
                )
            else:
                query_ = query_.filter(
                    ConfigurationDynamicLocationBeginAction.y_property_id
                    == y_property_id
                )
        if z_property_id is not None:
            try:
                self.session.query(DeviceProperty).filter_by(id=z_property_id).one()
            except NoResultFound:
                raise ObjectNotFound(
                    {
                        "parameter": "id",
                    },
                    "Device property: {} not found".format(z_property_id),
                )
            else:
                query_ = query_.filter(
                    ConfigurationDynamicLocationBeginAction.z_property_id
                    == z_property_id
                )
        return query_

    schema = ConfigurationDynamicLocationBeginActionSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": ConfigurationDynamicLocationBeginAction,
        "methods": {
            "query": query,
        },
    }


class ConfigurationDynamicLocationBeginActionDetail(ResourceDetail):
    """Detail resource for Configuration dynamic location begin actions (get, delete, patch)."""

    schema = ConfigurationDynamicLocationBeginActionSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": ConfigurationDynamicLocationBeginAction,
    }


class ConfigurationDynamicLocationBeginActionRelationship(ResourceRelationship):
    """Relationship resource for Configuration dynamic location begin actions."""

    schema = ConfigurationDynamicLocationBeginActionSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": ConfigurationDynamicLocationBeginAction,
    }
