# SPDX-FileCopyrightText: 2022 - 2024
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Mixin classes that may be used for multiple authentification mechanisms."""

import json
import pathlib

from flask import current_app

from ....api.models import Contact, User
from ....api.models.base_model import db


class CreateNewUserByUserinfoMixin:
    """
    Mixin to create new users if we need to do so.

    As we rely on the data that we get from the idp, we
    create new users in case there is the very first request.
    If we find existing ones, we can go on with those.
    """

    @staticmethod
    def get_user_or_create_new(identity, attributes):
        """Return an existing user or create a new one."""
        # We check if we find a user for this identity entry.
        found_user = db.session.query(User).filter_by(subject=identity).one_or_none()
        if found_user:
            vo_list_for_export_control_check = current_app.config[
                "EXPORT_CONTROL_VO_LIST"
            ]
            # Check the current setting and overwrite the permission.
            if vo_list_for_export_control_check and attributes.get(
                "eduperson_entitlement"
            ):
                should_be_allowed_to_handle_export_control = any(
                    [
                        vo in attributes["eduperson_entitlement"]
                        for vo in vo_list_for_export_control_check
                    ]
                )
                if (
                    found_user.is_export_control
                    != should_be_allowed_to_handle_export_control
                ):
                    found_user.is_export_control = (
                        should_be_allowed_to_handle_export_control
                    )
                    db.session.add(found_user)
                    db.session.commit()
            return found_user

        # We haven't found any user with the subject.
        # But as we rely on the IDP, we will insert it in the database.
        # However, every user gets a contact.
        # Do we have one already?
        email = attributes["email"]
        contact = db.session.query(Contact).filter_by(email=email).one_or_none()
        if contact:
            if not contact.active:
                contact.given_name = attributes["given_name"]
                contact.family_name = attributes["family_name"]
                contact.active = True
                db.session.add(contact)
        if not contact:
            organization_names_file = (
                pathlib.Path(__file__).parent.parent.parent.parent
                / "static"
                / "organization_names.json"
            )
            with organization_names_file.open() as infile:
                organization_names = json.load(infile)

            domain = attributes["email"].split("@")[-1]
            organization = organization_names.get(domain)

            contact = Contact(
                given_name=attributes["given_name"],
                family_name=attributes["family_name"],
                email=attributes["email"],
                organization=organization,
                active=True,
            )
            db.session.add(contact)
        apikey = User.generate_new_apikey()
        is_export_control = False

        vo_list_for_export_control_check = current_app.config["EXPORT_CONTROL_VO_LIST"]
        # Check the current setting and overwrite the permission.
        if vo_list_for_export_control_check and attributes.get("eduperson_entitlement"):
            is_export_control = any(
                [
                    vo in attributes["eduperson_entitlement"]
                    for vo in vo_list_for_export_control_check
                ]
            )

        user = User(
            subject=identity,
            contact=contact,
            active=True,
            apikey=apikey,
            is_export_control=is_export_control,
        )
        db.session.add(user)
        db.session.commit()
        return user
