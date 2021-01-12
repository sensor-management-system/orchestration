from flask_rest_jsonapi import ResourceDetail
from flask_rest_jsonapi.exceptions import ObjectNotFound
from project.api.models.base_model import db
from project.api.models.platform import Platform
from project.api.resourceManager.base_resource import add_updated_by_id
from project.api.schemas.platform_schema import PlatformSchema
from project.api.token_checker import token_required
from sqlalchemy.orm.exc import NoResultFound


class PlatformDetail(ResourceDetail):
    """
    provides get, patch and delete methods to retrieve details
    of an object, update an object and delete an Event
    """

    def before_get_object(self, view_kwargs):
        if view_kwargs.get("id") is not None:
            try:
                _ = self.session.query(Platform).filter_by(id=view_kwargs["id"]).one()
            except NoResultFound:
                raise ObjectNotFound(
                    {"parameter": "id"},
                    "Platform: {} not found".format(view_kwargs["id"]),
                )

    def before_patch(self, args, kwargs, data):
        """Add Created by user id to the data"""
        add_updated_by_id(data)

    schema = PlatformSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": Platform,
        "methods": {"before_get_object": before_get_object},
    }
