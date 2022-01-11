from flask_rest_jsonapi import ResourceDetail
from flask_rest_jsonapi import ResourceRelationship
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.orm.exc import NoResultFound

from .base_resource import check_if_object_not_found
from ..datalayers.esalchemy import EsSqlalchemyDataLayer
from ..models.base_model import db
from ..models.contact_role import Role
from ..models.device import Device
from ..schemas.role import RoleSchema
from ..token_checker import token_required
from ...frj_csv_export.resource import ResourceList


class RoleList(ResourceList):
    """
    provides get and post methods to retrieve
     a collection of Role or create one.
    """

    def query(self, view_kwargs):

        query_ = self.session.query(Role)
        contact_id = view_kwargs.get("contact_id")

        if contact_id is not None:
            try:
                self.session.query(Device).filter_by(id=contact_id).one()
            except NoResultFound:
                raise ObjectNotFound(
                    {"parameter": "id"}, "Contact: {} not found".format(contact_id)
                )
            else:
                query_ = query_.join(Role.devices).filter(Device.id == contact_id)

        return query_

    schema = RoleSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": Role,
        "class": EsSqlalchemyDataLayer,
        "methods": {"query": query,},
    }


class RoleDetail(ResourceDetail):
    """
    provides get, patch and delete methods to retrieve details
    of an object, update an object and delete a Role
    """

    def before_get(self, args, kwargs):
        """Return 404 Responses if role not found"""
        check_if_object_not_found(self._data_layer.model, kwargs)

    schema = RoleSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": Role,
    }


class RoleRelationship(ResourceRelationship):
    """
    provides get, post, patch and delete methods to get relationships,
    create relationships, update relationships and delete
    relationships between Roles and other objects.
    """

    schema = RoleSchema
    decorators = (token_required,)
    data_layer = {"session": db.session, "model": Role}
