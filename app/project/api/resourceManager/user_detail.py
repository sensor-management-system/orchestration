from flask_rest_jsonapi import ResourceDetail
from flask_rest_jsonapi.exceptions import ObjectNotFound
from project.api.models.base_model import db
from project.api.models.user import User
from project.api.schemas.user_schema import UserSchema
from project.api.token_checker import token_required
from sqlalchemy.orm.exc import NoResultFound


class UserDetail(ResourceDetail):
    """
    provides get, patch and delete methods to retrieve details
    of an object, update an Event and delete a Event
    """

    def before_get_object(self, view_kwargs):
        if view_kwargs.get("id") is not None:
            try:
                _ = self.session.query(User).filter_by(id=view_kwargs["id"]).one()
            except NoResultFound:
                raise ObjectNotFound(
                    {"parameter": "id"},
                    "User: {} not found".format(view_kwargs["id"]),
                )

    schema = UserSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": User,
        "methods": {"before_get_object": before_get_object},
    }
