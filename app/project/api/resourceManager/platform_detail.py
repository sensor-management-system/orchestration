from flask_rest_jsonapi import ResourceDetail
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.orm.exc import NoResultFound

from project.api.models.base_model import db
from project.api.models.platform import Platform
from project.api.schemas.platform_schema import PlatformSchema

from project.api.models.platform_attachment import PlatformAttachment

from project.api.flask_minio import FlaskMinio


def delete_attachments_in_minio_by_device_id(platform_id_intended_for_deletion):
    """
    use the minio class to delete an attachment or a list of attachments
    :param platform_intended_for_deletion:
    :return:
    """
    attachments_related_to_platform = (
        db.session.query(PlatformAttachment)
            .filter_by(platform_id=platform_id_intended_for_deletion)
            .all()
    )
    minio = FlaskMinio()
    for attachment in attachments_related_to_platform:
        minio.remove_an_object(attachment.url)


class PlatformDetail(ResourceDetail):
    """
     provides get, patch and delete methods to retrieve details
     of an object, update an object and delete an Event
    """

    def before_get_object(self, view_kwargs):
        if view_kwargs.get('id') is not None:
            try:
                _ = self.session.query(Platform).filter_by(
                    id=view_kwargs['id']).one()
            except NoResultFound:
                raise ObjectNotFound({'parameter': 'Platform_id'},
                                     "Platform: {} not found".format(view_kwargs['id']))

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
    # decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": Platform,
        'methods': {'before_get_object': before_get_object}
    }
