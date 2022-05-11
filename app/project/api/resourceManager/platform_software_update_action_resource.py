"""Resource classes for platform software update actions."""

from flask_rest_jsonapi import ResourceDetail, ResourceRelationship
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.orm.exc import NoResultFound

from ...frj_csv_export.resource import ResourceList
from ..auth.permission_utils import get_query_with_permissions_for_related_objects
from ..helpers.errors import MethodNotAllowed
from ..helpers.resource_mixin import add_created_by_id, add_updated_by_id
from ..models.base_model import db
from ..models.platform import Platform
from ..models.software_update_actions import PlatformSoftwareUpdateAction
from ..resourceManager.base_resource import check_if_object_not_found
from ..schemas.software_update_action_schema import PlatformSoftwareUpdateActionSchema
from ..token_checker import token_required


class PlatformSoftwareUpdateActionList(ResourceList):
    """List resource for platform software update actions (get, post)."""

    def before_create_object(self, data, *args, **kwargs):
        """Use jwt to add user id to dataset."""
        add_created_by_id(data)

    def query(self, view_kwargs):
        """
        Query the actions from the database.

        Also handle optional pre-filters (for specific platforms, for example).
        """
        query_ = get_query_with_permissions_for_related_objects(self.model)
        platform_id = view_kwargs.get("platform_id")
        if platform_id is not None:
            try:
                self.session.query(Platform).filter_by(id=platform_id).one()
            except NoResultFound:
                raise ObjectNotFound(
                    {
                        "parameter": "id",
                    },
                    "Platform: {} not found".format(platform_id),
                )
            else:
                query_ = query_.filter(
                    PlatformSoftwareUpdateAction.platform_id == platform_id
                )
        return query_

    schema = PlatformSoftwareUpdateActionSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": PlatformSoftwareUpdateAction,
        "methods": {
            "before_create_object": before_create_object,
            "query": query,
        },
    }


class PlatformSoftwareUpdateActionDetail(ResourceDetail):
    """Detail relationship for platform software update actions (get, delete, patch)."""

    def before_get(self, args, kwargs):
        """Return 404 Responses if PlatformSoftwareUpdateAction not found"""
        check_if_object_not_found(self._data_layer.model, kwargs)

    def before_patch(self, args, kwargs, data):
        """Add updated by user id to the data."""
        add_updated_by_id(data)

    schema = PlatformSoftwareUpdateActionSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": PlatformSoftwareUpdateAction,
    }


class PlatformSoftwareUpdateActionRelationship(ResourceRelationship):
    """Relationship resource for platform software update actions."""

    schema = PlatformSoftwareUpdateActionSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": PlatformSoftwareUpdateAction,
    }


class PlatformSoftwareUpdateActionRelationshipReadOnly(
    PlatformSoftwareUpdateActionRelationship
):
    """A readonly relationship endpoint for platform software update actions."""

    def before_post(self, args, kwargs, json_data=None):
        raise MethodNotAllowed("This endpoint is readonly!")

    def before_patch(self, args, kwargs, data=None):
        raise MethodNotAllowed("This endpoint is readonly!")

    def before_delete(self, args, kwargs):
        raise MethodNotAllowed("This endpoint is readonly!")
