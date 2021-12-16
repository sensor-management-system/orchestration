"""Resource classes for platform mount actions."""
import json

from flask import request
from flask_rest_jsonapi import ResourceDetail, ResourceRelationship
from flask_rest_jsonapi.exceptions import ObjectNotFound, JsonApiException
from sqlalchemy.orm.exc import NoResultFound

from ..auth.permission_utils import get_collection_with_permissions_for_related_objects
from ..helpers.errors import ConflictError
from ...frj_csv_export.resource import ResourceList
from ..models.base_model import db
from ..models.configuration import Configuration
from ..models.mount_actions import PlatformMountAction
from ..models.platform import Platform
from ..schemas.mount_actions_schema import PlatformMountActionSchema
from ..token_checker import token_required


class PlatformMountActionList(ResourceList):
    """List resource for platform mount actions (get, post)."""

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

    # def post(self, *args, **kwargs):
    #     data = json.loads(request.data.decode())["data"]
    #     platform_id = data["relationships"]["platform"]["data"]["id"]
    #     platform = db.session.query(Platform).filter_by(id=platform_id).one_or_none()
    #     action = (
    #         db.session.query(PlatformMountAction)
    #         .filter_by(platform_id=platform_id)
    #         .one_or_none()
    #     )
    #     if platform.is_private:
    #         raise ConflictError("Private Platform can't be used.")
    #     if action:
    #         raise ConflictError(
    #             f"Platform mounted on Configuration with the id :{action.configuration_id}"
    #         )
    #     try:
    #         super().post(*args, **kwargs)
    #     except JsonApiException as e:
    #         raise ConflictError("Mount failed.", str(e))

    def query(self, view_kwargs):
        """
        Query the actions from the database.

        Also handle optional pre-filters (for specific configurations, for example).
        """
        query_ = self.session.query(PlatformMountAction)
        configuration_id = view_kwargs.get("configuration_id")
        platform_id = view_kwargs.get("platform_id")
        parent_platform_id = view_kwargs.get("parent_platform_id")
        if configuration_id is not None:
            try:
                self.session.query(Configuration).filter_by(id=configuration_id).one()
            except NoResultFound:
                raise ObjectNotFound(
                    {"parameter": "id",},
                    "Configuration: {} not found".format(configuration_id),
                )
            else:
                query_ = query_.filter(
                    PlatformMountAction.configuration_id == configuration_id
                )
        if platform_id is not None:
            try:
                self.session.query(Platform).filter_by(id=platform_id).one()
            except NoResultFound:
                raise ObjectNotFound(
                    {"parameter": "id",}, "Platform: {} not found".format(platform_id),
                )
            else:
                query_ = query_.filter(PlatformMountAction.platform_id == platform_id)
        if parent_platform_id is not None:
            try:
                self.session.query(Platform).filter_by(id=parent_platform_id).one()
            except NoResultFound:
                raise ObjectNotFound(
                    {"parameter": "id",},
                    "Parent platform: {} not found".format(parent_platform_id),
                )
            else:
                query_ = query_.filter(
                    PlatformMountAction.parent_platform_id == parent_platform_id
                )
        return query_

    schema = PlatformMountActionSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": PlatformMountAction,
        "methods": {"query": query, "after_get_collection": after_get_collection,},
    }


class PlatformMountActionDetail(ResourceDetail):
    """Detail resource for platform mount actions (get, delete, patch)."""

    schema = PlatformMountActionSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": PlatformMountAction,
    }


class PlatformMountActionRelationship(ResourceRelationship):
    """Relationship resource for platform mount actions."""

    schema = PlatformMountActionSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": PlatformMountAction,
    }
