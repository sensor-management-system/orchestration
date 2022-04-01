from flask_rest_jsonapi import ResourceDetail, ResourceRelationship
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.exc import NoResultFound

from .base_resource import check_if_object_not_found
from ..auth.permission_utils import (
    check_permissions_for_configuration_related_objects,
    get_query_with_permissions_for_configuration_related_objects,
    check_patch_permission_for_configuration_related_objects,
    check_deletion_permission_for_configuration_related_objects,
    check_post_permission_for_configuration_related_objects,
)
from ..models import Configuration
from ..models.base_model import db
from ..models.generic_action_attachments import GenericConfigurationActionAttachment
from ..schemas.generic_action_attachment_schema import (
    GenericConfigurationActionAttachmentSchema,
)
from ..token_checker import token_required
from ...frj_csv_export.resource import ResourceList


class GenericConfigurationActionAttachmentList(ResourceList):
    def query(self, view_kwargs):
        """
        Query the entries from the database.
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
                    {"parameter": "id", },
                    "Configuration: {} not found".format(configuration_id),
                )
            else:
                query_ = query_.filter(
                    GenericConfigurationActionAttachment.configuration_id
                    == configuration_id
                )
        return query_

    def before_post(self, args, kwargs, data=None):
        check_post_permission_for_configuration_related_objects()

    schema = GenericConfigurationActionAttachmentSchema
    decorators = (token_required,)
    data_layer = {"session": db.session, "model": GenericConfigurationActionAttachment,
                  "methods": {"query": query}}


class GenericConfigurationActionAttachmentDetail(ResourceDetail):
    def before_get(self, args, kwargs):
        """Return 404 Responses if GenericConfigurationActionAttachment not found"""
        check_if_object_not_found(self._data_layer.model, kwargs)
        check_permissions_for_configuration_related_objects(
            self._data_layer.model, kwargs["id"]
        )

    def before_patch(self, args, kwargs, data=None):
        check_patch_permission_for_configuration_related_objects(
            kwargs, self._data_layer.model
        )

    def before_delete(self, args, kwargs):
        check_deletion_permission_for_configuration_related_objects(
            kwargs, self._data_layer.model
        )

    schema = GenericConfigurationActionAttachmentSchema
    decorators = (token_required,)
    data_layer = {"session": db.session, "model": GenericConfigurationActionAttachment}


class GenericConfigurationActionAttachmentRelationship(ResourceRelationship):
    schema = GenericConfigurationActionAttachmentSchema
    decorators = (token_required,)
    data_layer = {"session": db.session, "model": GenericConfigurationActionAttachment}
