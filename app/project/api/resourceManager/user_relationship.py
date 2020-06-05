from flask_rest_jsonapi import ResourceRelationship

from project.api.models.base_model import db
from project.api.models.user import User
from project.api.schemas.user_schema import UserSchema


class UserRelationship(ResourceRelationship):
    """
    provides get, post, patch and delete methods to get relationships,
    create relationships, update relationships and delete
    relationships between Event and other objects.
    """
    schema = UserSchema
    data_layer = {'session': db.session,
                  'model': User}
