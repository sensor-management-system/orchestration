from flask_rest_jsonapi import ResourceDetail

from .base_resource import check_if_object_not_found
from ..models.base_model import db
from ..models.user import User
from ..schemas.user_schema import UserSchema
from ..token_checker import token_required


class UserDetail(ResourceDetail):
    """
    provides get, patch and delete methods to retrieve details
    of an object, update an Event and delete a Event
    """

    def before_get(self, args, kwargs):
        """Return 404 Responses if user not found"""
        check_if_object_not_found(self._data_layer.model, kwargs)

    schema = UserSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": User,
    }
