from flask_rest_jsonapi import ResourceRelationship

from project.api.models.base_model import db
from project.api.models.platform import Platform
from project.api.schemas.platform_schema import PlatformSchema
from project.api.token_checker import token_required


class PlatformRelationship(ResourceRelationship):
    """
    Provides get, post, patch and delete methods to get relationships,
    create relationships, update relationships and delete
    relationships between Platforms.
    """
    schema = PlatformSchema
    # decorators = (token_required,)
    data_layer = {'session': db.session,
                  'model': Platform}
