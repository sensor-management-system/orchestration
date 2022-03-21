from flask_rest_jsonapi import ResourceDetail
from flask_rest_jsonapi import ResourceRelationship
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.exc import NoResultFound

from .base_resource import check_if_object_not_found
from ..models import Platform
from ..models.base_model import db
from ..models.contact_role import PlatformContactRole
from ..schemas.role import PlatformRoleSchema
from ..token_checker import token_required
from ...frj_csv_export.resource import ResourceList


class PlatformRoleList(ResourceList):
    """
    provides get and post methods to retrieve
     a collection of Platform Role or create one.
    """

    def query(self, view_kwargs):
        """
        Query the entries from the database.

        Handle also cases to get all the platform attachments
        for a specific platform.
        """
        query_ = self.session.query(PlatformContactRole)
        platform_id = view_kwargs.get("platform_id")

        if platform_id is not None:
            try:
                self.session.query(Platform).filter_by(id=platform_id).one()
            except NoResultFound:
                raise ObjectNotFound(
                    {"parameter": "id"}, "Platform: {} not found".format(platform_id)
                )
            else:
                query_ = query_.filter(PlatformContactRole.platform_id == platform_id)
        return query_

    schema = PlatformRoleSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": PlatformContactRole,
        "methods": {"query": query},
    }


class PlatformRoleDetail(ResourceDetail):
    """
    provides get, patch and delete methods to retrieve details
    of an object, update an object and delete a Platform Role
    """

    def before_get(self, args, kwargs):
        """Return 404 Responses if role not found"""
        check_if_object_not_found(self._data_layer.model, kwargs)

    schema = PlatformRoleSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": PlatformContactRole,
    }


class PlatformRoleRelationship(ResourceRelationship):
    """
    provides get, post, patch and delete methods to get relationships,
    create relationships, update relationships and delete
    relationships between Platform Role and other objects.
    """

    schema = PlatformRoleSchema
    decorators = (token_required,)
    data_layer = {"session": db.session, "model": PlatformContactRole}
