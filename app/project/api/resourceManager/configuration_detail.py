from flask_rest_jsonapi import JsonApiException, ResourceDetail
from flask_rest_jsonapi.exceptions import ObjectNotFound

from .base_resource import delete_attachments_in_minio_by_url
from ..helpers.errors import ConflictError
from ..models.base_model import db
from ..models.configuration import Configuration
from ..resourceManager.base_resource import add_updated_by_id
from ..schemas.configuration_schema import ConfigurationSchema
from ..token_checker import token_required


class ConfigurationDetail(ResourceDetail):
    """
    provides get, patch and delete methods to retrieve details
    of an object, update an object and delete a Device
    """

    def before_patch(self, args, kwargs, data):
        """Add Created by user id to the data"""
        add_updated_by_id(data)

    def delete(self, *args, **kwargs):
        """
        Try to delete an object through sqlalchemy. If could not be done give a ConflictError.
        :param args: args from the resource view
        :param kwargs: kwargs from the resource view
        :return:
        """
        configuration = (
            db.session.query(Configuration).filter_by(id=kwargs["id"]).first()
        )
        if configuration is None:
            raise ObjectNotFound({"pointer": ""}, "Object Not Found")
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
