# SPDX-FileCopyrightText: 2022 - 2023
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Tests for the platform software update actions api."""
import datetime
import json

from project import base_url
from project.api.models import (
    Contact,
    PermissionGroup,
    PermissionGroupMembership,
    Platform,
    PlatformSoftwareUpdateAction,
    User,
)
from project.api.models.base_model import db
from project.tests.base import BaseTestCase, create_token, fake
from project.tests.models.test_software_update_actions_model import (
    add_platform_software_update_action_model,
)
from project.tests.permissions import create_a_test_contact, create_a_test_platform


def prepare_software_update_action_payload(object_type, platform, contact):
    """Create some example payload to post to the backend."""
    data = {
        "data": {
            "type": object_type,
            "attributes": {
                "description": "Test platform_software_update_action",
                "version": f"v_{fake.pyint()}",
                "software_type_name": fake.pystr(),
                "software_type_uri": fake.uri(),
                "repository_url": fake.url(),
                "update_date": fake.future_datetime().__str__(),
            },
            "relationships": {
                "platform": {"data": {"type": "platform", "id": platform.id}},
                "contact": {"data": {"type": "contact", "id": contact.id}},
            },
        }
    }
    return data


class TestPlatformSoftwareUpdateAction(BaseTestCase):
    """Tests for the PlatformSoftwareUpdateAction endpoints."""

    url = base_url + "/platform-software-update-actions"
    object_type = "platform_software_update_action"

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

    def test_get_platform_software_update_action_collection(self):
        """Test retrieve a collection of public PlatformSoftwareUpdateAction objects."""
        sau = add_platform_software_update_action_model()
        with self.client:
            response = self.client.get(self.url)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 1)
        self.assertEqual(sau.description, data["data"][0]["attributes"]["description"])

    def test_get_internal_platform_software_update_action_collection(self):
        """Test retrieve a collection of internal PlatformSoftwareUpdateAction objects."""
        _ = add_platform_software_update_action_model(
            public=False, private=False, internal=True
        )
        with self.client:
            response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 0)

        # With a valid JWT
        access_headers = create_token()
        response = self.client.get(self.url, headers=access_headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 1)

    def test_post_action_with_a_permission_group(self):
        """Post to platform,with permission Group."""
        platform = create_a_test_platform([str(self.permission_group.id)])
        self.assertTrue(platform.id is not None)
        contact = create_a_test_contact()
        payload = prepare_software_update_action_payload(
            self.object_type, platform, contact
        )
        with self.run_requests_as(self.normal_user):
            response = self.client.post(
                self.url,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )

        self.assertEqual(response.status_code, 201)

    def test_post_action_archived_platform(self):
        """Ensure we can't add a action if the platform is archived."""
        platform = create_a_test_platform([str(self.permission_group.id)])
        platform.archived = True
        db.session.add(platform)
        db.session.commit()
        contact = create_a_test_contact()
        payload = prepare_software_update_action_payload(
            self.object_type, platform, contact
        )
        with self.run_requests_as(self.normal_user):
            response = self.client.post(
                self.url,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )

        self.assertEqual(response.status_code, 403)

    def test_post_action_user_not_in_the_permission_group(self):
        """Post to platform,with permission Group different from the user group."""
        platform = create_a_test_platform([str(self.other_group.id)])
        self.assertTrue(platform.id is not None)
        contact = create_a_test_contact()
        payload = prepare_software_update_action_payload(
            self.object_type, platform, contact
        )
        with self.run_requests_as(self.normal_user):
            response = self.client.post(
                f"{self.url}?include=platform,contact",
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 403)

    def test_patch_action_with_a_permission_group(self):
        """Post to platform,with permission Group."""
        platform_software_update_action = add_platform_software_update_action_model(
            group_ids=[str(self.permission_group.id)]
        )
        self.assertTrue(platform_software_update_action.id is not None)
        platform_software_update_action_updated = {
            "data": {
                "type": self.object_type,
                "id": platform_software_update_action.id,
                "attributes": {
                    "description": "updated",
                },
            }
        }
        url = f"{self.url}/{platform_software_update_action.id}"
        with self.run_requests_as(self.normal_user):
            response = self.client.patch(
                url,
                data=json.dumps(platform_software_update_action_updated),
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 200)

    def test_patch_action_for_archived_platform(self):
        """Ensure that we can't change if the platform is archived."""
        platform_software_update_action = add_platform_software_update_action_model(
            group_ids=[str(self.permission_group.id)]
        )
        platform_software_update_action.platform.archived = True
        db.session.add(platform_software_update_action.platform)
        db.session.commit()
        self.assertTrue(platform_software_update_action.id is not None)
        platform_software_update_action_updated = {
            "data": {
                "type": self.object_type,
                "id": platform_software_update_action.id,
                "attributes": {
                    "description": "updated",
                },
            }
        }
        url = f"{self.url}/{platform_software_update_action.id}"
        with self.run_requests_as(self.normal_user):
            response = self.client.patch(
                url,
                data=json.dumps(platform_software_update_action_updated),
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 403)

    def test_patch_action__user_is_not_part_from_permission_group(self):
        """Post to platform,with permission Group."""
        platform_software_update_action = add_platform_software_update_action_model(
            group_ids=[str(self.other_group.id)]
        )
        self.assertTrue(platform_software_update_action.id is not None)
        platform_software_update_action_updated = {
            "data": {
                "type": self.object_type,
                "id": platform_software_update_action.id,
                "attributes": {
                    "description": "updated",
                },
            }
        }
        url = f"{self.url}/{platform_software_update_action.id}"
        with self.run_requests_as(self.normal_user):
            response = self.client.patch(
                url,
                data=json.dumps(platform_software_update_action_updated),
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 403)

    def test_delete_software_update_action(self):
        """Delete PlatformSoftwareUpdateAction."""
        platform_software_update_action = add_platform_software_update_action_model(
            group_ids=[str(self.permission_group.id)]
        )
        url = f"{self.url}/{platform_software_update_action.id}"
        with self.run_requests_as(self.normal_user):
            response = self.client.delete(
                url,
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 200)

    def test_delete_software_update_action_for_archived_platform(self):
        """Ensure that we can't delete if the platform is archived."""
        platform_software_update_action = add_platform_software_update_action_model(
            group_ids=[str(self.permission_group.id)]
        )
        platform_software_update_action.platform.archived = True
        db.session.add(platform_software_update_action.platform)
        db.session.commit()
        url = f"{self.url}/{platform_software_update_action.id}"
        with self.run_requests_as(self.normal_user):
            response = self.client.delete(
                url,
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 403)

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
        action = PlatformSoftwareUpdateAction(
            platform=platform1,
            contact=contact,
            update_date=datetime.datetime(
                2022, 12, 24, 0, 0, 0, tzinfo=datetime.timezone.utc
            ),
            software_type_name="OS",
            software_type_uri="something",
        )
        db.session.add_all([platform1, platform2, contact, action])
        db.session.commit()

        payload = {
            "data": {
                "type": "platform_software_update_action",
                "id": action.id,
                "attributes": {},
                "relationships": {
                    # We try to switch here to another platform for
                    # which we have no edit permissions.
                    "platform": {
                        "data": {
                            "type": "platform",
                            "id": platform2.id,
                        }
                    },
                },
            }
        }

        with self.run_requests_as(self.normal_user):
            response = self.client.patch(
                f"{self.url}/{action.id}",
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 403)
