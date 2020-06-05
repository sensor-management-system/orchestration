from project.api.models.attachment import Attachment
from project.api.models.base_model import db
from flask_rest_jsonapi import ResourceDetail
from project.api.schemas.attachment_schema import AttachmentSchema


class AttachmentDetail(ResourceDetail):
    """
     provides get, patch and delete methods to retrieve details
     of an object, update an object and delete an Attachment
    """

    def before_get_object(self, view_kwargs):
        """

        :param view_kwargs:
        :return:
        """

    schema = AttachmentSchema
    data_layer = {'session': db.session,
                  'model': Attachment,
                  'methods': {'before_create_object': before_get_object}}
