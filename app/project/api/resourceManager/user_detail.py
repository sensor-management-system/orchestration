from flask_rest_jsonapi import ResourceDetail
from project.api.models.base_model import db
from project.api.models.user import User
from project.api.schemas.user_schema import UserSchema


class UserDetail(ResourceDetail):
    """
     provides get, patch and delete methods to retrieve details
     of an object, update an Event and delete a Event
    """

    schema = UserSchema
    data_layer = {'session': db.session,
                  'model': User,
                  }
