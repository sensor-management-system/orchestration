"""Resource classes for the generic device actions."""

from flask_rest_jsonapi import ResourceDetail, ResourceRelationship
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.orm.exc import NoResultFound

from ..auth.permission_utils import get_collection_with_permissions_for_related_objects
from ...frj_csv_export.resource import ResourceList
from ..models.base_model import db
from ..models.device import Device
from ..models.generic_actions import GenericDeviceAction
from ..schemas.generic_actions_schema import GenericDeviceActionSchema
from ..token_checker import token_required


class GenericDeviceActionList(ResourceList):
    """List resource for generic device actions (get & post)."""

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

        Also handle optional pre-filters (for specific devices, for example).
        """
        query_ = self.session.query(GenericDeviceAction)
        device_id = view_kwargs.get("device_id")

        if device_id is not None:
            try:
                self.session.query(Device).filter_by(id=device_id).one()
            except NoResultFound:
                raise ObjectNotFound(
                    {"parameter": "id",}, "Device: {} not found".format(device_id),
                )
            else:
                query_ = query_.filter(GenericDeviceAction.device_id == device_id)
        return query_

    schema = GenericDeviceActionSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": GenericDeviceAction,
        "methods": {"query": query, "after_get_collection": after_get_collection,},
    }


class GenericDeviceActionDetail(ResourceDetail):
    """Detail resource for generic device actions (get, delete, patch)."""

    schema = GenericDeviceActionSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": GenericDeviceAction,
    }


class GenericDeviceActionRelationship(ResourceRelationship):
    """Relationship resource for generic device actions."""

    schema = GenericDeviceActionSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": GenericDeviceAction,
    }
