from flask_rest_jsonapi import JsonApiException, ResourceDetail

from .base_resource import delete_attachments_in_minio_by_url, check_if_object_not_found
from ..auth.permission_utils import (
    check_deletion_permission,
    is_superuser,
    is_user_in_a_group,
)
from ..helpers.errors import ConflictError, ForbiddenError
from ..helpers.resource_mixin import add_updated_by_id
from ..models.base_model import db
from ..models.configuration import Configuration
from ..schemas.configuration_schema import ConfigurationSchema
from ..token_checker import token_required, current_user_or_none


class ConfigurationDetail(ResourceDetail):
    """
    provides get, patch and delete methods to retrieve details
    of an object, update an object and delete a Device
    """

    def before_get(self, args, kwargs):
        """Prevent not registered users form viewing internal configs."""
        check_if_object_not_found(self._data_layer.model, kwargs)
        config = db.session.query(Configuration).filter_by(id=kwargs["id"]).first()
        if config:
            if config.is_internal:
                current_user_or_none()

    def before_patch(self, args, kwargs, data):
        """check if a user has the permission to change this configuration"""
        if not is_superuser():
            configuration = (
                db.session.query(Configuration).filter_by(id=data["id"]).one_or_none()
            )
            group_id = configuration.cfg_permission_group
            if not is_user_in_a_group([group_id]):
                raise ForbiddenError(
                    "User is not part of any group to edit this object."
                )
        add_updated_by_id(data)

    def before_delete(self, args, kwargs):
        """Checks for permission"""
        check_deletion_permission(kwargs, Configuration)

    def delete(self, *args, **kwargs):
        """
        Try to delete an object through sqlalchemy. If could not be done give a ConflictError.
        :param args: args from the resource view
        :param kwargs: kwargs from the resource view
        :return:
        """
        configuration = check_if_object_not_found(Configuration, kwargs)
        urls = [a.url for a in configuration.configuration_attachments]
        try:
            super().delete(*args, **kwargs)
        except JsonApiException as e:
            raise ConflictError("Deletion failed for the configuration.", str(e))

        for url in urls:
            delete_attachments_in_minio_by_url(url)

        final_result = {"meta": {"message": "Object successfully deleted"}}
        return final_result

    schema = ConfigurationSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": Configuration,
    }
