from flask_rest_jsonapi import ResourceList

from project.api.models.base_model import db
from project.api.models.user import User
from project.api.schemas.user_schema import UserSchema
from project.api.token_checker import token_required


class UserList(ResourceList):
    """
    provides get and post methods to retrieve a
    collection of Events or create one.
    """

    schema = UserSchema
    decorators = (token_required,)
    data_layer = {"session": db.session, "model": User}
