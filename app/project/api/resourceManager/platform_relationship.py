from flask_rest_jsonapi import ResourceRelationship

from ..helpers.errors import MethodNotAllowed
from ..models.base_model import db
from ..models.platform import Platform
from ..schemas.platform_schema import PlatformSchema
from ..token_checker import token_required


class PlatformRelationship(ResourceRelationship):
    """
    Provides get, post, patch and delete methods to get relationships,
    create relationships, update relationships and delete
    relationships between Platforms.
    """

    schema = PlatformSchema
    decorators = (token_required,)
    data_layer = {"session": db.session, "model": Platform}


class PlatformRelationshipReadOnly(PlatformRelationship):
    """A readonly relationship endpoint for platforms."""

    def before_post(self, args, kwargs, json_data=None):
        raise MethodNotAllowed("This endpoint is readonly!")

    def before_patch(self, args, kwargs, data=None):
        raise MethodNotAllowed("This endpoint is readonly!")

    def before_delete(self, args, kwargs):
        raise MethodNotAllowed("This endpoint is readonly!")
