# SPDX-FileCopyrightText: 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Test classes for generic platform action attachments."""
import datetime
import json

from project import base_url
from project.api.models import (
    Contact,
    GenericPlatformAction,
    GenericPlatformActionAttachment,
    PermissionGroup,
    PermissionGroupMembership,
    Platform,
    PlatformAttachment,
    User,
)
from project.api.models.base_model import db
from project.tests.base import BaseTestCase


class TestGenericPlatformActionAttachments(BaseTestCase):
    """Test class for generic platform action attachments."""

    url = base_url + "/generic-platform-action-attachments"

    def setUp(self):
        """Set stuff up for the tests."""
        super().setUp()
        normal_contact = Contact(
            given_name="normal", family_name="user", email="normal.user@localhost"
        )
        self.normal_user = User(subject=normal_contact.email, contact=normal_contact)

        self.permission_group = PermissionGroup(name="test", entitlement="test")
        self.other_group = PermissionGroup(name="other", entitlement="other")
        self.membership = PermissionGroupMembership(
            permission_group=self.permission_group, user=self.normal_user
        )
        db.session.add_all(
            [
                normal_contact,
                self.normal_user,
                self.permission_group,
                self.other_group,
                self.membership,
            ]
        )
        db.session.commit()

    def test_patch_to_non_editable_platform(self):
        """Ensure we can't update to a platform we can't edit."""
        platform1 = Platform(
            short_name="platform1",
            is_public=False,
            is_internal=True,
            is_private=False,
            group_ids=[str(self.permission_group.id)],
        )
        platform2 = Platform(
            short_name="platform2",
            is_public=False,
            is_internal=True,
            is_private=False,
            group_ids=[str(self.other_group.id)],
        )
        contact = Contact(
            given_name="first",
            family_name="contact",
            email="first.contact@localhost",
        )
        action1 = GenericPlatformAction(
            platform=platform1,
            contact=contact,
            begin_date=datetime.datetime(
                2022, 12, 24, 0, 0, 0, tzinfo=datetime.timezone.utc
            ),
            action_type_name="Something",
            action_type_uri="something",
        )
        action2 = GenericPlatformAction(
            platform=platform2,
            contact=contact,
            begin_date=datetime.datetime(
                2022, 12, 24, 0, 0, 0, tzinfo=datetime.timezone.utc
            ),
            action_type_name="Something",
            action_type_uri="something",
        )
        attachment1 = PlatformAttachment(
            platform=platform1,
            url="https://gfz-potsdam.de",
            label="GFZ",
        )
        attachment2 = PlatformAttachment(
            platform=platform2,
            url="https://gfz-potsdam.de",
            label="GFZ",
        )
        action_attachment = GenericPlatformActionAttachment(
            action=action1,
            attachment=attachment1,
        )
        db.session.add_all(
            [
                platform1,
                platform2,
                contact,
                action1,
                action2,
                attachment1,
                attachment2,
                action_attachment,
            ]
        )
        db.session.commit()

        payload = {
            "data": {
                "type": "generic_platform_action_attachment",
                "id": action_attachment.id,
                "attributes": {},
                "relationships": {
                    # We try to switch here to another platform for
                    # which we have no edit permissions.
                    "action": {
                        "data": {
                            "type": "generic_platform_action",
                            "id": action2.id,
                        }
                    },
                    "attachment": {
                        "data": {
                            "type": "platform_attachment",
                            "id": attachment2.id,
                        }
                    },
                },
            }
        }

        with self.run_requests_as(self.normal_user):
            response = self.client.patch(
                f"{self.url}/{action_attachment.id}",
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 403)
