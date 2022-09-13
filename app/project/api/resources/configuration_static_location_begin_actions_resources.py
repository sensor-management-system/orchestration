"""Resource classes for Configuration static location begin actions."""

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
from ..helpers.location_checks import StaticLocationActionValidator
from ..helpers.resource_mixin import (
    add_created_by_id,
    add_updated_by_id,
    decode_json_request_data,
)
from ..models import Configuration, ConfigurationStaticLocationBeginAction
from ..models.base_model import db
from ..schemas.configuration_static_location_actions_schema import (
    ConfigurationStaticLocationBeginActionSchema,
)
from ..token_checker import token_required
from .base_resource import (
    check_if_object_not_found,
    query_configuration_and_set_update_description_text,
    set_update_description_text_and_update_by_user,
)


class ConfigurationStaticLocationBeginActionList(ResourceList):
    """List resource for Configuration static location begin actions (get, post)."""

    def before_create_object(self, data, *args, **kwargs):
        """Run some validations before we create the object."""
        data_with_relationships = decode_json_request_data()
        StaticLocationActionValidator().validate_create(data_with_relationships)
        add_created_by_id(data)

    def query(self, view_kwargs):
        """
        Query the Configuration static location begin actions from the database.

        Also handle optional pre-filters (for specific configuration, for example).
        """
        query_ = get_query_with_permissions_for_configuration_related_objects(
            self.model
        )
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
                    ConfigurationStaticLocationBeginAction.configuration_id
                    == configuration_id
                )
        return query_

    def before_post(self, args, kwargs, data=None):
        """Run some checks before we create the object."""
        check_post_permission_for_configuration_related_objects()

    def after_post(self, result):
        """
        Add update description to related platform.

        :param result:
        :return:
        """
        result_id = result[0]["data"]["relationships"]["configuration"]["data"]["id"]
        msg = "create;static location action"
        query_configuration_and_set_update_description_text(msg, result_id)

        return result

    schema = ConfigurationStaticLocationBeginActionSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": ConfigurationStaticLocationBeginAction,
        "methods": {
            "query": query,
            "before_create_object": before_create_object,
        },
    }


class ConfigurationStaticLocationBeginActionDetail(ResourceDetail):
    """Detail resource for Configuration static location begin actions (get, delete, patch)."""

    validator = StaticLocationActionValidator()

    def before_get(self, args, kwargs):
        """
        Return some checks before we return ob object.

        Currently we have the following checks:
        - Check if the object exists (return 404 otherwise)
        - Check that the user is allowed to see the object (401 or 405 otherwise)
        """
        check_if_object_not_found(self._data_layer.model, kwargs)
        check_permissions_for_configuration_related_objects(
            self._data_layer.model, kwargs["id"]
        )

    def before_patch(self, args, kwargs, data=None):
        """Run some checks before we update an object."""
        check_patch_permission_for_configuration_related_objects(
            kwargs, self._data_layer.model
        )
        data_with_relationships = decode_json_request_data()
        self.validator.validate_update(data_with_relationships, kwargs["id"])
        add_updated_by_id(data)

    def after_patch(self, result):
        """
        Add update description to related configuration.

        :param result:
        :return:
        """
        result_id = result["data"]["relationships"]["configuration"]["data"]["id"]
        msg = "update;static location action"
        query_configuration_and_set_update_description_text(msg, result_id)
        return result

    def before_delete(self, args, kwargs):
        """Run some checks before we delete."""
        check_deletion_permission_for_configuration_related_objects(
            kwargs, self._data_layer.model
        )
        location_action = (
            db.session.query(ConfigurationStaticLocationBeginAction)
            .filter_by(id=kwargs["id"])
            .one_or_none()
        )
        if location_action is None:
            raise ObjectNotFound("Object not found!")
        configuration = location_action.get_parent()
        msg = "delete;static location action"
        set_update_description_text_and_update_by_user(configuration, msg)

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
