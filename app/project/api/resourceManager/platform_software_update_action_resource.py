"""Resource classes for platform software update actions."""

from flask_rest_jsonapi import ResourceDetail, ResourceRelationship
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.orm.exc import NoResultFound

from ..auth.permission_utils import get_collection_with_permissions_for_related_objects
from ...frj_csv_export.resource import ResourceList
from ..models.base_model import db
from ..models.platform import Platform
from ..models.software_update_actions import PlatformSoftwareUpdateAction
from ..schemas.software_update_action_schema import PlatformSoftwareUpdateActionSchema
from ..token_checker import token_required


class PlatformSoftwareUpdateActionList(ResourceList):
    """List resource for platform software update actions (get, post)."""

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
        query_ = self.session.query(PlatformSoftwareUpdateAction)
        platform_id = view_kwargs.get("platform_id")
        if platform_id is not None:
            try:
                self.session.query(Platform).filter_by(id=platform_id).one()
            except NoResultFound:
                raise ObjectNotFound(
                    {"parameter": "id",}, "Platform: {} not found".format(platform_id),
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
        "methods": {"query": query, "after_get_collection": after_get_collection},
    }


class PlatformSoftwareUpdateActionDetail(ResourceDetail):
    """Detail relationship for platform software update actions (get, delete, patch)."""

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
