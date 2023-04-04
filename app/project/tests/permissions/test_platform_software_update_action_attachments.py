"""Test classes for platform software update action attachments."""
import datetime
import json
from unittest.mock import patch

import pytz

from project import base_url
from project.api.models import (
    Contact,
    Platform,
    PlatformAttachment,
    PlatformSoftwareUpdateAction,
    PlatformSoftwareUpdateActionAttachment,
    User,
)
from project.api.models.base_model import db
from project.extensions.idl.models.user_account import UserAccount
from project.extensions.instances import idl
from project.tests.base import BaseTestCase


class TestPlatformSoftwarUpdateActionAttachments(BaseTestCase):
    """Test class for permission management on platform software update action attachments."""

    url = base_url + "/platform-software-update-action-attachments"

    def test_patch_to_non_editable_platform(self):
        """Ensure we can't update to a platform we can't edit."""
        platform1 = Platform(
            short_name="platform1",
            is_public=False,
            is_internal=True,
            is_private=False,
            group_ids=["1"],
        )
        platform2 = Platform(
            short_name="platform2",
            is_public=False,
            is_internal=True,
            is_private=False,
            group_ids=["2"],
        )
        contact = Contact(
            given_name="first",
            family_name="contact",
            email="first.contact@localhost",
        )
        action1 = PlatformSoftwareUpdateAction(
            platform=platform1,
            contact=contact,
            update_date=datetime.datetime(2022, 12, 24, 0, 0, 0, tzinfo=pytz.utc),
            software_type_name="OS",
            software_type_uri="something",
        )
        action2 = PlatformSoftwareUpdateAction(
            platform=platform2,
            contact=contact,
            update_date=datetime.datetime(2022, 12, 24, 0, 0, 0, tzinfo=pytz.utc),
            software_type_name="OS",
            software_type_uri="something",
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
        update_attachment = PlatformSoftwareUpdateActionAttachment(
            action=action1,
            attachment=attachment1,
        )
        user = User(
            subject=contact.email,
            contact=contact,
        )
        db.session.add_all(
            [
                platform1,
                platform2,
                contact,
                user,
                action1,
                action2,
                attachment1,
                attachment2,
                update_attachment,
            ]
        )
        db.session.commit()

        payload = {
            "data": {
                "type": "platform_software_update_action_attachment",
                "id": update_attachment.id,
                "attributes": {},
                "relationships": {
                    # We try to switch here to another platform for
                    # which we have no edit permissions.
                    "action": {
                        "data": {
                            "type": "platform_software_update_action",
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

        with self.run_requests_as(user):
            with patch.object(idl, "get_all_permission_groups_for_a_user") as mock:
                mock.return_value = UserAccount(
                    id="123",
                    username=user.subject,
                    administrated_permission_groups=[],
                    membered_permission_groups=[*platform1.group_ids],
                )
                with self.client:
                    response = self.client.patch(
                        f"{self.url}/{update_attachment.id}",
                        data=json.dumps(payload),
                        content_type="application/vnd.api+json",
                    )
        self.assertEqual(response.status_code, 403)
