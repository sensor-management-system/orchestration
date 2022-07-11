"""Tests for the generic platform action api."""

import os
from datetime import datetime
from unittest.mock import patch

from project import base_url, db
from project.api.models import Contact, GenericPlatformAction, Platform
from project.extensions.instances import idl
from project.tests.base import (
    BaseTestCase,
    create_token,
    fake,
    generate_userinfo_data,
    test_file_path,
)
from project.tests.permissions.test_platforms import IDL_USER_ACCOUNT


class TestGenericPlatformAction(BaseTestCase):
    """Tests for the GenericPlatformAction endpoints."""

    url = base_url + "/generic-platform-actions"
    platform_url = base_url + "/platforms"
    device_url = base_url + "/devices"
    contact_url = base_url + "/contacts"
    object_type = "generic_platform_action"
    json_data_url = os.path.join(
        test_file_path, "drafts", "configurations_test_data.json"
    )
    device_json_data_url = os.path.join(
        test_file_path, "drafts", "devices_test_data.json"
    )
    platform_json_data_url = os.path.join(
        test_file_path, "drafts", "platforms_test_data.json"
    )

    def test_get_generic_platform_action(self):
        """Ensure the GET /generic_platform_action route behaves correctly."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        # no data yet
        self.assertEqual(response.json["data"], [])

    def make_generic_platform_action_data(self):
        """
        Create the json payload for a generic platform action.

        This also creates some additional objects in the database.
        """
        group_id_test_user_is_member_in_2 = IDL_USER_ACCOUNT.membered_permission_groups
        platform = Platform(
            short_name=fake.pystr(),
            manufacturer_name=fake.company(),
            is_public=True,
            is_private=False,
            is_internal=False,
            group_ids=group_id_test_user_is_member_in_2,
        )
        db.session.add(platform)
        db.session.commit()
        userinfo = generate_userinfo_data()
        contact_data = {
            "data": {
                "type": "contact",
                "attributes": {
                    "given_name": userinfo["given_name"],
                    "family_name": userinfo["family_name"],
                    "email": userinfo["email"],
                    "website": fake.url(),
                },
            }
        }
        contact = super().add_object(
            url=self.contact_url, data_object=contact_data, object_type="contact"
        )
        data = {
            "data": {
                "type": self.object_type,
                "attributes": {
                    "description": fake.paragraph(nb_sentences=3),
                    "action_type_name": fake.lexify(
                        text="Random type: ??????????", letters="ABCDE"
                    ),
                    "action_type_uri": fake.uri(),
                    "begin_date": datetime.now().__str__(),
                },
                "relationships": {
                    "platform": {"data": {"type": "platform", "id": platform.id}},
                    "contact": {
                        "data": {"type": "contact", "id": contact["data"]["id"]}
                    },
                },
            }
        }
        return data

    def test_update_generic_platform_action(self):
        """Ensure a generic_platform_action can be updateded."""
        generic_platform_action_data = self.make_generic_platform_action_data()
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups:
            test_get_all_permission_groups.return_value = IDL_USER_ACCOUNT
            generic_platform_action = super().add_object(
                url=f"{self.url}?include=platform,contact",
                data_object=generic_platform_action_data,
                object_type=self.object_type,
            )
            userinfo = generate_userinfo_data()
            contact = Contact(
                given_name=userinfo["given_name"],
                family_name=userinfo["family_name"],
                email=userinfo["email"],
            )
            db.session.add(contact)
            db.session.commit()
            new_data = {
                "data": {
                    "type": self.object_type,
                    "id": generic_platform_action["data"]["id"],
                    "attributes": {
                        "description": fake.paragraph(nb_sentences=2),
                        "action_type_name": fake.lexify(
                            text="Random type: ??????????", letters="ABCDE"
                        ),
                        "action_type_uri": fake.uri(),
                        "begin_date": datetime.now().__str__(),
                    },
                    "relationships": {
                        "platform": {"data": {"type": "platform", "id": "1"}},
                        "contact": {"data": {"type": "contact", "id": contact.id}},
                    },
                }
            }
            _ = super().update_object(
                url=f"{self.url}/{generic_platform_action['data']['id']}?include=platform,contact",
                data_object=new_data,
                object_type=self.object_type,
            )

    def test_delete_generic_platform_action(self):
        """Ensure a generic_platform_action can be deleted."""
        generic_platform_action_data = self.make_generic_platform_action_data()
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups:
            test_get_all_permission_groups.return_value = IDL_USER_ACCOUNT
            obj = super().add_object(
                url=f"{self.url}?include=platform,contact",
                data_object=generic_platform_action_data,
                object_type=self.object_type,
            )
            access_headers = create_token()
            with self.client:
                response = self.client.delete(
                    f"{self.url}/{obj['data']['id']}",
                    content_type="application/vnd.api+json",
                    headers=access_headers,
                )
            self.assertEqual(response.status_code, 200)

    def test_filtered_by_platform(self):
        """Ensure that I can prefilter by a specific platform."""
        platform1 = Platform(
            short_name="sample platform",
            manufacturer_name=fake.company(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        db.session.add(platform1)
        platform2 = Platform(
            short_name="sample platform II",
            manufacturer_name=fake.company(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        db.session.add(platform2)

        contact = Contact(
            given_name="Nils", family_name="Brinckmann", email="nils@gfz-potsdam.de"
        )
        db.session.add(contact)

        action1 = GenericPlatformAction(
            platform=platform1,
            contact=contact,
            description="Some first action",
            begin_date=fake.date_time(),
            action_type_name="PlatformActivity",
        )
        db.session.add(action1)

        action2 = GenericPlatformAction(
            platform=platform2,
            contact=contact,
            description="Some other action",
            begin_date=fake.date_time(),
            action_type_name="PlatformActivity",
        )
        db.session.add(action2)
        db.session.commit()

        # first check to get them all
        with self.client:
            url_get_all = base_url + "/generic-platform-actions"
            response = self.client.get(
                url_get_all, content_type="application/vnd.api+json"
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 2)

        # then test only for the first platform
        with self.client:
            url_get_for_platform1 = (
                base_url + f"/platforms/{platform1.id}/generic-platform-actions"
            )
            response = self.client.get(
                url_get_for_platform1, content_type="application/vnd.api+json"
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 1)
        self.assertEqual(
            response.json["data"][0]["attributes"]["description"], "Some first action"
        )

        # and test the second platform
        with self.client:
            url_get_for_platform2 = (
                base_url + f"/platforms/{platform2.id}/generic-platform-actions"
            )
            response = self.client.get(
                url_get_for_platform2, content_type="application/vnd.api+json"
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 1)
        self.assertEqual(
            response.json["data"][0]["attributes"]["description"], "Some other action"
        )

        # and for a non existing
        with self.client:
            url_get_for_non_existing_platform = (
                base_url + f"/platforms/{platform2.id + 9999}/generic-platform-actions"
            )
            response = self.client.get(
                url_get_for_non_existing_platform,
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 404)

    # def test_delete_generic_platform_action_with_attachment_link(self):
    #     """Ensure a generic_platform_action with attachment link can be deleted."""
    #     generic_platform_action_attachment = (
    #         add_generic_platform_action_attachment_model()
    #     )
    #     access_headers = create_token()
    #     with self.client:
    #         response = self.client.delete(
    #             f"{self.url}/{generic_platform_action_attachment.id}",
    #             content_type="application/vnd.api+json",
    #             headers=access_headers,
    #         )
    #     self.assertNotEqual(response.status_code, 200)

    def test_http_response_not_found(self):
        """Make sure that the backend responds with 404 HTTP-Code if a resource was not found."""
        url = f"{self.url}/{fake.random_int()}"
        _ = super().http_code_404_when_resource_not_found(url)
