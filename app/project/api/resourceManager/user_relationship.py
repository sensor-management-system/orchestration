from flask_rest_jsonapi import ResourceRelationship

from ..models.base_model import db
from ..models.user import User
from ..schemas.user_schema import UserSchema
from ..token_checker import token_required


class UserRelationship(ResourceRelationship):
    """
    provides get, post, patch and delete methods to get relationships,
    create relationships, update relationships and delete
    relationships between User and other objects.
    """

    schema = UserSchema
    decorators = (token_required,)
    data_layer = {"session": db.session, "model": User}
