"""Resource classes for contacts."""

from flask import g
from flask_rest_jsonapi import ResourceDetail
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.orm.exc import NoResultFound

from ...frj_csv_export.resource import ResourceList
from ..auth.permission_utils import is_superuser
from ..datalayers.esalchemy import EsSqlalchemyDataLayer
from ..helpers.errors import ForbiddenError
from ..helpers.resource_mixin import add_created_by_id, add_updated_by_id
from ..models.base_model import db
from ..models.configuration import Configuration
from ..models.contact import Contact
from ..models.device import Device
from ..models.platform import Platform
from ..schemas.contact_schema import ContactSchema
from ..token_checker import token_required
from .base_resource import check_if_object_not_found


class ContactList(ResourceList):
    """
    Contact list resource.

    Provides get and post methods to retrieve a collection of contacts
    or create one.
    """

    def query(self, view_kwargs):
        """Return the base query to search for contacts."""
        query_ = self.session.query(Contact)
        configuration_id = view_kwargs.get("configuration_id")
        platform_id = view_kwargs.get("platform_id")
        device_id = view_kwargs.get("device_id")

        if configuration_id is not None:
            try:
                self.session.query(Configuration).filter_by(id=configuration_id).one()
            except NoResultFound:
                raise ObjectNotFound(
                    {"parameter": "id"},
                    "Configuration: {} not found".format(configuration_id),
                )
            else:
                query_ = query_.join(Contact.configurations).filter(
                    Configuration.id == configuration_id
                )

        if platform_id is not None:
            try:
                self.session.query(Platform).filter_by(id=platform_id).one()
            except NoResultFound:
                raise ObjectNotFound(
                    {"parameter": "id"}, "Platform: {} not found".format(platform_id)
                )
            else:
                query_ = query_.join(Contact.platforms).filter(
                    Platform.id == platform_id
                )

        if device_id is not None:
            try:
                self.session.query(Device).filter_by(id=device_id).one()
            except NoResultFound:
                raise ObjectNotFound(
                    {"parameter": "id"}, "Device: {} not found".format(platform_id)
                )
            else:
                query_ = query_.join(Contact.devices).filter(Device.id == device_id)

        return query_

    def before_create_object(self, data, *args, **kwargs):
        """Run hooks for data we want to add before creating the contact."""
        add_created_by_id(data)

    schema = ContactSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": Contact,
        "class": EsSqlalchemyDataLayer,
        "methods": {"query": query, "before_create_object": before_create_object},
    }


class ContactDetail(ResourceDetail):
    """
    Detail resource for contacts.

    Provides get, patch and delete methods to retrieve details
    of an object, update an object and delete a contact.
    """

    def before_get(self, args, kwargs):
        """Return 404 Responses if contact not found."""
        check_if_object_not_found(self._data_layer.model, kwargs)

    def before_patch(self, args, kwargs, data):
        """Check if the user has the permission to change this contact."""
        contact = db.session.query(Contact).filter_by(id=data["id"]).one_or_none()
        if contact and not is_superuser():
            is_self = contact.id == g.user.contact.id
            is_creator = contact.created_by_id == g.user.id
            if not (is_self or is_creator):
                raise ForbiddenError("User is not allowed to edit this contact")
        add_updated_by_id(data)

    def before_delete(self, args, kwargs):
        """Check if the user is allowed to delete the contact."""
        contact = db.session.query(Contact).filter_by(id=kwargs["id"]).one_or_none()
        if contact and not is_superuser():
            # It doesn't make sense to delete the own contact as
            # it is still needed for the user entry in the db.
            # So we only check if the user created that contact.
            if not contact.created_by_id == g.user.id:
                raise ForbiddenError("User is not allowed to delete this contact")
        # in any case the foreign key settings will not allow to delete
        # contacts that are used in actions or still have a user for it.
        pass

    schema = ContactSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": Contact,
    }
