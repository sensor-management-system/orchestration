"""Resource classes for the generic platform actions."""

from flask_rest_jsonapi import ResourceDetail, ResourceRelationship
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.orm.exc import NoResultFound

from ..auth.permission_utils import get_collection_with_permissions_for_related_objects
from ...frj_csv_export.resource import ResourceList
from .base_resource import check_if_object_not_found
from ..models.base_model import db
from ..models.generic_actions import GenericPlatformAction
from ..models.platform import Platform
from ..schemas.generic_actions_schema import GenericPlatformActionSchema
from ..token_checker import token_required
from ...frj_csv_export.resource import ResourceList


class GenericPlatformActionList(ResourceList):
    """List resource for generic platform actions (get & post)."""

    def after_get_collection(self, collection, qs, view_kwargs):
        """Take the intersection between requested collection and
        what the user allowed querying.

        :param collection:
        :param qs:
        :param view_kwargs:
        :return:
        """

        return get_collection_with_permissions_for_related_objects(
            self.model, collection
        )

    def query(self, view_kwargs):
        """
        Query the actions from the database.

        Also handle optional pre-filters (for specific platforms, for example).
        """
        query_ = self.session.query(GenericPlatformAction)
        platform_id = view_kwargs.get("platform_id")

        if platform_id is not None:
            try:
                self.session.query(Platform).filter_by(id=platform_id).one()
            except NoResultFound:
                raise ObjectNotFound(
                    {"parameter": "id",}, "Platform: {} not found".format(platform_id),
                )
            else:
                query_ = query_.filter(GenericPlatformAction.platform_id == platform_id)
        return query_

    schema = GenericPlatformActionSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": GenericPlatformAction,
        "methods": {"query": query, "after_get_collection": after_get_collection},
    }


class GenericPlatformActionDetail(ResourceDetail):
    """Detail resource for generic platform actions (get, delete, patch)."""

    def before_get(self, args, kwargs):
        """Return 404 Responses if GenericPlatformAction not found"""
        check_if_object_not_found(self._data_layer.model, kwargs)

    schema = GenericPlatformActionSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": GenericPlatformAction,
    }


class GenericPlatformActionRelationship(ResourceRelationship):
    """Relationship resource for the generic platform actions."""

    schema = GenericPlatformActionSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": GenericPlatformAction,
    }
