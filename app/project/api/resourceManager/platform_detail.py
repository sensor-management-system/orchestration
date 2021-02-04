from flask_rest_jsonapi import ResourceDetail
from project.api.models.base_model import db
from project.api.models.platform import Platform
from project.api.resourceManager.base_resource import add_updated_by_id
from project.api.schemas.platform_schema import PlatformSchema
from project.api.models.platform_attachment import PlatformAttachment
from project.api.token_checker import token_required

from project.api import minio


def delete_attachments_in_minio_by_device_id(platform_id_intended_for_deletion):
    """
    Use the minio class to delete an attachment or a list of attachments.
    :param platform_intended_for_deletion:
    :return:
    """
    attachments_related_to_platform = (
        db.session.query(PlatformAttachment)
            .filter_by(platform_id=platform_id_intended_for_deletion)
            .all()
    )
    for attachment in attachments_related_to_platform:
        minio.remove_an_object(attachment.url)


class PlatformDetail(ResourceDetail):
    """
    provides get, patch and delete methods to retrieve details
    of an object, update an object and delete an Event
    """

    def before_patch(self, args, kwargs, data):
        """Add Created by user id to the data"""
        add_updated_by_id(data)

    def before_delete(self, args, kwargs):
        """
        Delete the platform attachments at the minio server
        :param args:
        :param kwargs:
        :return:
        """
        platform_id_intended_for_deletion = kwargs.get("id")
        delete_attachments_in_minio_by_device_id(platform_id_intended_for_deletion)
        return kwargs

    schema = PlatformSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": Platform,
    }
