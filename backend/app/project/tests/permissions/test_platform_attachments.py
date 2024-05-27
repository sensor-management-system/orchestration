# SPDX-FileCopyrightText: 2022 - 2023
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Tests for the permissions of platform attachments."""

import json
from unittest.mock import patch

from project import base_url
from project.api.models import Contact, Platform, PlatformAttachment, User
from project.api.models.base_model import db
from project.extensions.idl.models.user_account import UserAccount
from project.extensions.instances import idl
from project.tests.base import BaseTestCase, create_token, fake, query_result_to_list
from project.tests.permissions import create_a_test_platform
from project.tests.permissions.test_platforms import IDL_USER_ACCOUNT


def prepare_platform_attachment_payload(platform):
    """Prepare a payload to send to the backend."""
    payload = {
        "data": {
            "type": "platform_attachment",
            "attributes": {"label": fake.pystr(), "url": fake.url()},
            "relationships": {
                "platform": {"data": {"type": "platform", "id": str(platform.id)}}
            },
        }
    }
    return payload


class TesPlatformAttachment(BaseTestCase):
    """Test PlatformAttachment."""

    url = base_url + "/platform-attachments"

    def test_get_public_platform_attachments(self):
        """Ensure that we can get a list of public platform_attachments."""
        platform1 = create_a_test_platform(
            public=True,
            private=False,
            internal=False,
        )
        platform2 = create_a_test_platform(
            public=True,
            private=False,
            internal=False,
        )

        attachment1 = PlatformAttachment(
            label=fake.pystr(),
            url=fake.url(),
            platform=platform1,
        )
        attachment2 = PlatformAttachment(
            label=fake.pystr(),
            url=fake.url(),
            platform=platform1,
        )
        attachment3 = PlatformAttachment(
            label=fake.pystr(),
            url=fake.url(),
            platform=platform2,
        )

        db.session.add_all([attachment1, attachment2, attachment3])
        db.session.commit()

        with self.client:
            response = self.client.get(
                self.url,
                content_type="application/vnd.api+json",
            )
            self.assertEqual(response.status_code, 200)
            payload = response.get_json()

            self.assertEqual(len(payload["data"]), 3)

    def test_get_internal_platform_attachments(self):
        """Ensure that we can get a list of internal platform_attachments only with a valid jwt."""
        platform1 = create_a_test_platform(
            public=False,
            private=False,
            internal=True,
        )
        platform2 = create_a_test_platform(
            public=False,
            private=False,
            internal=True,
        )

        attachment1 = PlatformAttachment(
            label=fake.pystr(),
            url=fake.url(),
            platform=platform1,
        )
        attachment2 = PlatformAttachment(
            label=fake.pystr(),
            url=fake.url(),
            platform=platform2,
        )

        db.session.add_all([attachment1, attachment2])
        db.session.commit()

        with self.client:
            response = self.client.get(
                self.url,
                content_type="application/vnd.api+json",
            )
            self.assertEqual(response.status_code, 200)
            payload = response.get_json()

            self.assertEqual(len(payload["data"]), 0)

        # With a valid JWT
        access_headers = create_token()
        response = self.client.get(self.url, headers=access_headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 2)

    def test_post_to_a_platform_with_a_permission_group(self):
        """Post to platform,with permission Group."""
        platform = create_a_test_platform(IDL_USER_ACCOUNT.membered_permission_groups)
        self.assertTrue(platform.id is not None)
        count_platform_attachments = (
            db.session.query(PlatformAttachment)
            .filter_by(
                platform_id=platform.id,
            )
            .count()
        )

        self.assertEqual(count_platform_attachments, 0)
        payload = prepare_platform_attachment_payload(platform)
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:

                response = self.client.post(
                    self.url,
                    data=json.dumps(payload),
                    content_type="application/vnd.api+json",
                    headers=create_token(),
                )
        self.assertEqual(response.status_code, 201)
        platform_attachments = query_result_to_list(
            db.session.query(PlatformAttachment).filter_by(
                platform_id=platform.id,
            )
        )
        self.assertEqual(len(platform_attachments), 1)

        attachment = platform_attachments[0]
        self.assertEqual(attachment.label, payload["data"]["attributes"]["label"])
        self.assertEqual(attachment.url, payload["data"]["attributes"]["url"])
        self.assertEqual(attachment.platform_id, platform.id)
        self.assertEqual(str(attachment.platform_id), response.get_json()["data"]["id"])

    def test_post_to_archived_platform_with_a_permission_group(self):
        """Ensure that we can't add an attachment to an archived platform."""
        platform = create_a_test_platform(IDL_USER_ACCOUNT.membered_permission_groups)
        platform.archived = True
        db.session.add(platform)
        db.session.commit()

        payload = prepare_platform_attachment_payload(platform)
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:

                response = self.client.post(
                    self.url,
                    data=json.dumps(payload),
                    content_type="application/vnd.api+json",
                    headers=create_token(),
                )
        self.assertEqual(response.status_code, 403)

    def test_post_to_a_platform_with_an_other_permission_group(self):
        """Post to a platform with a different permission Group from the user."""
        platform = create_a_test_platform([403])
        self.assertTrue(platform.id is not None)
        count_platform_attachments = (
            db.session.query(PlatformAttachment)
            .filter_by(
                platform_id=platform.id,
            )
            .count()
        )

        self.assertEqual(count_platform_attachments, 0)
        payload = prepare_platform_attachment_payload(platform)
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                response = self.client.post(
                    self.url,
                    data=json.dumps(payload),
                    content_type="application/vnd.api+json",
                    headers=create_token(),
                )
        self.assertEqual(response.status_code, 403)

    def test_patch_to_a_platform_with_a_permission_group(self):
        """Patch Custom field attached to platform with same group as user."""
        platform = create_a_test_platform(IDL_USER_ACCOUNT.membered_permission_groups)
        self.assertTrue(platform.id is not None)
        count_platform_attachments = (
            db.session.query(PlatformAttachment)
            .filter_by(
                platform_id=platform.id,
            )
            .count()
        )

        self.assertEqual(count_platform_attachments, 0)
        attachment = PlatformAttachment(
            label=fake.pystr(),
            url=fake.url(),
            platform=platform,
        )
        db.session.add(attachment)
        db.session.commit()
        payload = {
            "data": {
                "id": attachment.id,
                "type": "platform_attachment",
                "attributes": {"label": "changed", "url": attachment.url},
                "relationships": {
                    "platform": {"data": {"type": "platform", "id": str(platform.id)}}
                },
            }
        }
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                url = self.url + "/" + str(attachment.id)

                response = self.client.patch(
                    url,
                    data=json.dumps(payload),
                    content_type="application/vnd.api+json",
                    headers=create_token(),
                )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(attachment.label, data["data"]["attributes"]["label"])
        self.assertEqual(attachment.url, data["data"]["attributes"]["url"])
        self.assertEqual(attachment.platform_id, platform.id)

    def test_patch_to_archived_platform(self):
        """Ensure that we can't patch an attachment for an archived platform."""
        platform = create_a_test_platform(IDL_USER_ACCOUNT.membered_permission_groups)

        attachment = PlatformAttachment(
            label=fake.pystr(),
            url=fake.url(),
            platform=platform,
        )
        platform.archived = True
        db.session.add_all([attachment, platform])
        db.session.commit()

        payload = {
            "data": {
                "id": attachment.id,
                "type": "platform_attachment",
                "attributes": {"label": "changed", "url": attachment.url},
                "relationships": {
                    "platform": {"data": {"type": "platform", "id": str(platform.id)}}
                },
            }
        }
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                url = self.url + "/" + str(attachment.id)

                response = self.client.patch(
                    url,
                    data=json.dumps(payload),
                    content_type="application/vnd.api+json",
                    headers=create_token(),
                )
        self.assertEqual(response.status_code, 403)

    def test_delete_for_a_platform_with_a_permission_group(self):
        """Delete attached to platform with same group as group admin."""
        platform = create_a_test_platform(
            IDL_USER_ACCOUNT.administrated_permission_groups
        )
        self.assertTrue(platform.id is not None)
        count_platform_attachments = (
            db.session.query(PlatformAttachment)
            .filter_by(
                platform_id=platform.id,
            )
            .count()
        )

        self.assertEqual(count_platform_attachments, 0)
        attachment = PlatformAttachment(
            label=fake.pystr(),
            url=fake.url(),
            platform=platform,
        )
        db.session.add(attachment)
        db.session.commit()
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                url = self.url + "/" + str(attachment.id)

                response = self.client.delete(
                    url,
                    content_type="application/vnd.api+json",
                    headers=create_token(),
                )
        self.assertEqual(response.status_code, 200)

    def test_delete_for_archived_platform(self):
        """Ensure that we can't delete when the platform is archived."""
        platform = create_a_test_platform(
            IDL_USER_ACCOUNT.administrated_permission_groups
        )
        attachment = PlatformAttachment(
            label=fake.pystr(),
            url=fake.url(),
            platform=platform,
        )
        platform.archived = True
        db.session.add_all([attachment, platform])
        db.session.commit()
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                url = self.url + "/" + str(attachment.id)

                response = self.client.delete(
                    url,
                    content_type="application/vnd.api+json",
                    headers=create_token(),
                )
        self.assertEqual(response.status_code, 403)

    def test_delete_to_a_platform_with_a_permission_group_as_a_member(self):
        """Delete attachment of platform with same group as user (member)."""
        platform = create_a_test_platform(IDL_USER_ACCOUNT.membered_permission_groups)
        self.assertTrue(platform.id is not None)
        count_platform_attachments = (
            db.session.query(PlatformAttachment)
            .filter_by(
                platform_id=platform.id,
            )
            .count()
        )

        self.assertEqual(count_platform_attachments, 0)
        attachment = PlatformAttachment(
            label=fake.pystr(),
            url=fake.url(),
            platform=platform,
        )
        db.session.add(attachment)
        db.session.commit()
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                url = self.url + "/" + str(attachment.id)

                response = self.client.delete(
                    url,
                    content_type="application/vnd.api+json",
                    headers=create_token(),
                )
        self.assertEqual(response.status_code, 200)

        # and we want to make sure that we have an updated update
        # description for the platform
        reloaded_platform = db.session.query(Platform).filter_by(id=platform.id).first()
        self.assertEqual(reloaded_platform.update_description, "delete;attachment")

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
        attachment = PlatformAttachment(
            label="k",
            url="v",
            platform=platform1,
        )
        user = User(
            subject=contact.email,
            contact=contact,
        )
        db.session.add_all([platform1, platform2, contact, user, attachment])
        db.session.commit()

        payload = {
            "data": {
                "type": "platform_attachment",
                "id": attachment.id,
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
                        f"{self.url}/{attachment.id}",
                        data=json.dumps(payload),
                        content_type="application/vnd.api+json",
                    )
        self.assertEqual(response.status_code, 403)
