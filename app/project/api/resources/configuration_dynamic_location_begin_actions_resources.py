"""Resource classes for Configuration dynamic location begin actions."""

from flask_rest_jsonapi import ResourceDetail, ResourceRelationship
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.orm.exc import NoResultFound

from ...frj_csv_export.resource import ResourceList
from ..auth.permission_utils import (
    check_deletion_permission_for_configuration_related_objects,
    check_patch_permission_for_configuration_related_objects,
    check_permissions_for_configuration_related_objects,
    check_post_permission_for_configuration_related_objects,
    get_query_with_permissions_for_configuration_related_objects,
)
from ..helpers.resource_mixin import add_created_by_id, add_updated_by_id
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
from .base_resource import check_if_object_not_found


class ConfigurationDynamicLocationBeginActionList(ResourceList):
    """List resource for Configuration dynamic location begin actions (get, post)."""

    def before_create_object(self, data, *args, **kwargs):
        """Use jwt to add user id to dataset."""
        add_created_by_id(data)

    def query(self, view_kwargs):
        """
        Query the Configuration dynamic location begin actions from the database.

        Also handle optional pre-filters (for specific configuration, for example).
        """
        query_ = get_query_with_permissions_for_configuration_related_objects(
            self.model
        )
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

    def before_post(self, args, kwargs, data=None):
        check_post_permission_for_configuration_related_objects()

    schema = ConfigurationDynamicLocationBeginActionSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": ConfigurationDynamicLocationBeginAction,
        "methods": {
            "query": query,
            "before_create_object": before_create_object,
        },
    }


class ConfigurationDynamicLocationBeginActionDetail(ResourceDetail):
    """Detail resource for Configuration dynamic location begin actions (get, delete, patch)."""

    def before_get(self, args, kwargs):
        """Return 404 Responses if ConfigurationDynamicLocationBeginAction not found"""
        check_if_object_not_found(self._data_layer.model, kwargs)
        check_permissions_for_configuration_related_objects(
            self._data_layer.model, kwargs["id"]
        )

    def before_patch(self, args, kwargs, data=None):
        check_patch_permission_for_configuration_related_objects(
            kwargs, self._data_layer.model
        )
        add_updated_by_id(data)

    def before_delete(self, args, kwargs):
        check_deletion_permission_for_configuration_related_objects(
            kwargs, self._data_layer.model
        )

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
