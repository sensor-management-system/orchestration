# SPDX-FileCopyrightText: 2021 - 2023
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Tests for the api usage for platform software update action attachments."""

from project import base_url
from project.api.models import (
    Contact,
    Platform,
    PlatformAttachment,
    PlatformSoftwareUpdateAction,
)
from project.api.models.base_model import db
from project.tests.base import BaseTestCase, fake, generate_userinfo_data
from project.tests.models.test_software_update_actions_attachment_model import (
    add_platform_software_update_action_attachment_model,
)


class TestPlatformSoftwareUpdateActionAttachment(BaseTestCase):
    """Tests for the PlatformSoftwareUpdateActionAttachment endpoints."""

    url = base_url + "/platform-software-update-action-attachments"
    object_type = "platform_software_update_action_attachment"

    def test_get_platform_software_update_action_attachment(self):
        """Ensure the GET /platform_software_update_action_attachments route reachable."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        # no data yet
        self.assertEqual(response.json["data"], [])

    def test_get_platform_software_update_action_attachment_collection(self):
        """Test retrieve attachment collection of PlatformSoftwareUpdateActionAttachments."""
        platform_software_update_action_attachment = (
            add_platform_software_update_action_attachment_model()
        )
        platform = platform_software_update_action_attachment.action.platform
        platform.is_public = True
        platform.is_internal = False
        db.session.add(platform)
        db.session.commit()

        with self.client:
            response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        # should be only one
        self.assertEqual(response.json["meta"]["count"], 1)
        self.assertEqual(
            response.json["data"][0]["id"],
            str(platform_software_update_action_attachment.id),
        )

    def test_get_platform_software_update_action_attachment_collection_internal(self):
        """Ensure we don't show infos for internal platforms without login."""
        platform_software_update_action_attachment = (
            add_platform_software_update_action_attachment_model()
        )
        platform = platform_software_update_action_attachment.action.platform
        self.assertTrue(platform.is_internal)

        with self.client:
            response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        # should be only one
        self.assertEqual(response.json["meta"]["count"], 0)

    def test_post_platform_software_update_action_attachment(self):
        """Create PlatformSoftwareUpdateActionAttachment."""
        userinfo = generate_userinfo_data()
        platform = Platform(
            short_name="Platform 144",
            manufacturer_name=fake.company(),
            is_public=False,
            is_private=False,
            is_internal=True,
        )

        contact = Contact(
            given_name=userinfo["given_name"],
            family_name=userinfo["family_name"],
            email=userinfo["email"],
        )
        db.session.add(platform)
        db.session.commit()
        attachment = PlatformAttachment(
            label=fake.pystr(), url=fake.url(), platform_id=platform.id
        )
        platform_software_update_action = PlatformSoftwareUpdateAction(
            platform=platform,
            software_type_name=fake.pystr(),
            software_type_uri=fake.uri(),
            update_date=fake.date(),
            version="0.54",
            repository_url=fake.url(),
            description=fake.paragraph(nb_sentences=3),
            contact=contact,
        )
        db.session.add_all(
            [platform, attachment, contact, platform_software_update_action]
        )
        db.session.commit()
        data = {
            "data": {
                "type": self.object_type,
                "attributes": {},
                "relationships": {
                    "action": {
                        "data": {
                            "type": "platform_software_update_action",
                            "id": platform_software_update_action.id,
                        }
                    },
                    "attachment": {
                        "data": {"type": "platform_attachment", "id": attachment.id}
                    },
                },
            }
        }
        _ = super().add_object(
            url=f"{self.url}?include=action,attachment",
            data_object=data,
            object_type=self.object_type,
        )

    def test_update_platform_software_update_action_attachment(self):
        """Update PlatformSoftwareUpdateActionAttachment."""
        platform_software_update_action_attachment = (
            add_platform_software_update_action_attachment_model()
        )
        platform = Platform(
            short_name="Platform new 144",
            manufacturer_name=fake.company(),
            is_public=False,
            is_private=False,
            is_internal=True,
        )
        db.session.add(platform)
        db.session.commit()
        attachment = PlatformAttachment(
            label=fake.pystr(), url=fake.url(), platform_id=platform.id
        )
        db.session.add(attachment)
        db.session.commit()
        data = {
            "data": {
                "type": self.object_type,
                "id": platform_software_update_action_attachment.id,
                "attributes": {},
                "relationships": {
                    "attachment": {
                        "data": {"type": "platform_attachment", "id": attachment.id}
                    },
                },
            }
        }
        _ = super().update_object(
            url=f"{self.url}/{platform_software_update_action_attachment.id}?include=attachment",
            data_object=data,
            object_type=self.object_type,
        )

    def test_delete_platform_software_update_action_attachment(self):
        """Delete PlatformSoftwareUpdateActionAttachment."""
        platform_software_update_action_attachment = (
            add_platform_software_update_action_attachment_model()
        )
        _ = super().delete_object(
            url=f"{self.url}/{platform_software_update_action_attachment.id}",
        )

    def test_http_response_not_found(self):
        """Make sure that the backend responds with 404 HTTP-Code if a resource was not found."""
        url = f"{self.url}/{fake.random_int()}"
        _ = super().http_code_404_when_resource_not_found(url)
