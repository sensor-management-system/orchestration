from flask_rest_jsonapi import JsonApiException, ResourceDetail
from flask_rest_jsonapi.exceptions import ObjectNotFound

from ..helpers.errors import ConflictError
from ..helpers.resource_mixin import add_updated_by_id
from ..models.base_model import db
from ..models.platform import Platform
from ..schemas.platform_schema import PlatformSchema
from ..token_checker import token_required
from .base_resource import check_if_object_not_found, delete_attachments_in_minio_by_url


class PlatformDetail(ResourceDetail):
    """
    provides get, patch and delete methods to retrieve details
    of an object, update an object and delete an Event
    """

    def before_get(self, args, kwargs):
        """Return 404 Responses if platform not found"""
        check_if_object_not_found(self._data_layer.model, kwargs)

    def delete(self, *args, **kwargs):
        """
        Try to delete an object through sqlalchemy. If could not be done give a ConflictError.
        :param args: args from the resource view
        :param kwargs: kwargs from the resource view
        :return:
        """
        platform = db.session.query(Platform).filter_by(id=kwargs["id"]).first()
        if platform is None:
            raise ObjectNotFound({"pointer": ""}, "Object Not Found")
        urls = [a.url for a in platform.platform_attachments]
        try:
            super().delete(*args, **kwargs)
        except JsonApiException as e:
            raise ConflictError("Deletion failed for the platform.", str(e))

        for url in urls:
            delete_attachments_in_minio_by_url(url)

        final_result = {"meta": {"message": "Object successfully deleted"}}
        return final_result

    def before_patch(self, args, kwargs, data):
        """
        Run logic before the patch.

        In this case we want to make sure that we update the updated_by_id
        with the id of the user that run the request.
        """
        add_updated_by_id(data)

    schema = PlatformSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": Platform,
    }
