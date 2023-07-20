# SPDX-FileCopyrightText: 2022 - 2023
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Resource classes for contacts."""

import itertools

from flask_rest_jsonapi import ResourceDetail
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.orm.exc import NoResultFound

from ...extensions.instances import pidinst
from ...frj_csv_export.resource import ResourceList
from ..datalayers.esalchemy import EsSqlalchemyDataLayer
from ..helpers.errors import ConflictError
from ..helpers.resource_mixin import add_created_by_id, add_updated_by_id
from ..models import (
    Configuration,
    ConfigurationContactRole,
    Contact,
    Device,
    DeviceContactRole,
    Platform,
    PlatformContactRole,
)
from ..models.base_model import db
from ..permissions.common import DelegateToCanFunctions
from ..permissions.rules import filter_visible
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
        query_ = filter_visible(self.session.query(self.model))
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
        orcid = data.get("orcid")
        if orcid:
            has_orcid = db.session.query(Contact).filter(Contact.orcid == orcid).first()
            if has_orcid:
                raise ConflictError("Orcid already used.")
        email = data.get("email")
        if email:
            has_email = db.session.query(Contact).filter(Contact.email == email).first()
            if has_email:
                raise ConflictError("E-Mail already used.")

    schema = ContactSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": Contact,
        "class": EsSqlalchemyDataLayer,
        "methods": {"query": query, "before_create_object": before_create_object},
    }
    permission_classes = [DelegateToCanFunctions]


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
        add_updated_by_id(data)

        # And lets add some checks for the orcid & email
        orcid = data.get("orcid")
        if orcid:
            has_orcid = (
                db.session.query(Contact)
                .filter(Contact.id != data["id"])
                .filter(Contact.orcid == orcid)
                .first()
            )
            if has_orcid:
                raise ConflictError("Orcid already used.")
        email = data.get("email")
        if email:
            has_email = (
                db.session.query(Contact)
                .filter(Contact.id != data["id"])
                .filter(Contact.email == email)
                .first()
            )
            if has_email:
                raise ConflictError("Email already used.")

    def after_patch(self, result, *args, **kwargs):
        """Run some actions after patching the entry."""
        contact_id = result["data"]["id"]
        for instrument in itertools.chain(
            db.session.query(Device)
            .join(DeviceContactRole)
            .filter(DeviceContactRole.contact_id == contact_id),
            db.session.query(Platform)
            .join(PlatformContactRole)
            .filter(PlatformContactRole.contact_id == contact_id),
            db.session.query(Configuration)
            .join(ConfigurationContactRole)
            .filter(ConfigurationContactRole.contact_id == contact_id),
        ):
            if pidinst.has_external_metadata(instrument):
                pidinst.update_external_metadata(instrument)
        return result

    def before_delete(self, args, kwargs):
        """Collect some tasks to run for the point after the deletion."""
        contact_id = kwargs["id"]
        instruments_with_external_metadata = []
        for instrument in itertools.chain(
            db.session.query(Device)
            .join(DeviceContactRole)
            .filter(DeviceContactRole.contact_id == contact_id),
            db.session.query(Platform)
            .join(PlatformContactRole)
            .filter(PlatformContactRole.contact_id == contact_id),
            db.session.query(Configuration)
            .join(ConfigurationContactRole)
            .filter(ConfigurationContactRole.contact_id == contact_id),
        ):
            if pidinst.has_external_metadata(instrument):
                instruments_with_external_metadata.append(instrument)

        self.tasks_after_delete = []

        def run_updates():
            for instrument in instruments_with_external_metadata:
                pidinst.update_external_metadata(instrument)

        self.tasks_after_delete.append(run_updates)

    def after_delete(self, *args, **kwargs):
        """Run some tasks after the deletion."""
        for task in self.tasks_after_delete:
            task()
        return super().after_delete(*args, **kwargs)

    schema = ContactSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": Contact,
    }
    permission_classes = [DelegateToCanFunctions]
