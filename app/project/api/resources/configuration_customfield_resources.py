"""Module for the configuration customfield resources."""
from flask_rest_jsonapi import ResourceDetail, ResourceList
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.orm.exc import NoResultFound

from ..auth.permission_utils import (
    check_deletion_permission_for_configuration_related_objects,
    check_patch_permission_for_configuration_related_objects,
    check_permissions_for_configuration_related_objects,
    check_post_permission_for_configuration_related_objects,
    get_query_with_permissions_for_configuration_related_objects,
)
from ..models.base_model import db
from ..models.configuration import Configuration
from ..models.configuration_customfield import ConfigurationCustomField
from ..schemas.configuration_customfield_schema import ConfigurationCustomFieldSchema
from ..token_checker import token_required
from .base_resource import (
    check_if_object_not_found,
    query_configuration_and_set_update_description_text,
    set_update_description_text_and_update_by_user,
)


class ConfigurationCustomFieldList(ResourceList):
    """
    List resource for configuration custom fields.

    Provides get and post methods to retrieve
    a list of custom fields or to create a new one.
    """

    def query(self, view_kwargs):
        """
        Query the data from the database & filter for what the user is allowed to query.

        Normally it should query all the customfields.
        However, if we give a configuration_id with a url like
        /configurations/<configuration_id>/configuration-customfields
        we want to filter according to them.
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
                    ConfigurationCustomField.configuration_id == configuration_id
                )
        return query_

    def before_post(self, args, kwargs, data=None):
        """Run checks before posting."""
        check_post_permission_for_configuration_related_objects()

    def after_post(self, result):
        """
        Add update description to related configuration.

        :param result:
        :return:
        """
        result_id = result[0]["data"]["relationships"]["configuration"]["data"]["id"]
        msg = "create;custom field"
        query_configuration_and_set_update_description_text(msg, result_id)

        return result

    schema = ConfigurationCustomFieldSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": ConfigurationCustomField,
        "methods": {"query": query},
    }


class ConfigurationCustomFieldDetail(ResourceDetail):
    """
    Detail resource for configuration custom fields.

    Provides get, patch & delete methods to retrieve
    a custom field, update it or to delete it.
    """

    def before_get(self, args, kwargs):
        """Return 404 Responses if ConfigurationCustomField can't be found."""
        check_if_object_not_found(self._data_layer.model, kwargs)
        check_permissions_for_configuration_related_objects(
            self._data_layer.model, kwargs["id"]
        )

    def before_patch(self, args, kwargs, data=None):
        """Run checks before patching."""
        check_patch_permission_for_configuration_related_objects(
            kwargs, self._data_layer.model
        )

    def after_patch(self, result):
        """
        Add update description to related configuration.

        :param result:
        :return:
        """
        result_id = result["data"]["relationships"]["configuration"]["data"]["id"]
        msg = "update;custom field"
        query_configuration_and_set_update_description_text(msg, result_id)
        return result

    def before_delete(self, args, kwargs):
        """Run checks before deleting."""
        check_deletion_permission_for_configuration_related_objects(
            kwargs, self._data_layer.model
        )
        custom_field = (
            db.session.query(ConfigurationCustomField)
            .filter_by(id=kwargs["id"])
            .one_or_none()
        )
        if custom_field is None:
            raise ObjectNotFound("Object not found!")
        configuration = custom_field.get_parent()
        msg = "delete;custom field"
        set_update_description_text_and_update_by_user(configuration, msg)

    schema = ConfigurationCustomFieldSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": ConfigurationCustomField,
    }
