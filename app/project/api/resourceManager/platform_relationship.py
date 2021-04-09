from flask_rest_jsonapi import ResourceRelationship

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
