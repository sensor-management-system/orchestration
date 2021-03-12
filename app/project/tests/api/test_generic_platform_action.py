from datetime import datetime

from project import base_url
from project.tests.base import BaseTestCase, fake, generate_token_data
from project.tests.read_from_json import extract_data_from_json_file


class TestGenericPlatformAction(BaseTestCase):
    """Tests for the GenericPlatformAction endpoints."""

    url = base_url + "/generic-platform-actions"
    platform_url = base_url + "/platforms"
    device_url = base_url + "/devices"
    contact_url = base_url + "/contacts"
    object_type = "generic_platform_action"
    json_data_url = "/usr/src/app/project/tests/drafts/configurations_test_data.json"
    device_json_data_url = "/usr/src/app/project/tests/drafts/devices_test_data.json"
    platform_json_data_url = (
        "/usr/src/app/project/tests/drafts/platforms_test_data.json"
    )

    def test_get_generic_platform_action(self):
        """Ensure the GET /generic_platform_action route behaves correctly."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        # no data yet
        self.assertEqual(response.json["data"], [])

    def make_generic_platform_action_data(self):
        platform_json = extract_data_from_json_file(
            self.platform_json_data_url, "platforms"
        )
        platform_data = {"data": {"type": "platform", "attributes": platform_json[0]}}
        platform = super().add_object(
            url=self.platform_url, data_object=platform_data, object_type="platform"
        )
        mock_jwt = generate_token_data()
        contact_data = {
            "data": {
                "type": "contact",
                "attributes": {
                    "given_name": mock_jwt["given_name"],
                    "family_name": mock_jwt["family_name"],
                    "email": mock_jwt["email"],
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
                    "platform": {
                        "data": {"type": "platform", "id": platform["data"]["id"]}
                    },
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
        generic_platform_action = super().add_object(
            url=f"{self.url}?include=platform,contact",
            data_object=generic_platform_action_data,
            object_type=self.object_type,
        )
        mock_jwt = generate_token_data()
        contact_data1 = {
            "data": {
                "type": "contact",
                "attributes": {
                    "given_name": mock_jwt["given_name"],
                    "family_name": mock_jwt["family_name"],
                    "email": mock_jwt["email"],
                    "website": fake.url(),
                },
            }
        }
        contact = super().add_object(
            url=self.contact_url, data_object=contact_data1, object_type="contact"
        )
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
                    "contact": {
                        "data": {"type": "contact", "id": contact["data"]["id"]}
                    },
                },
            }
        }
        _ = super().update_object(
            url=f"{self.url}/{generic_platform_action['data']['id']}?include=platform,contact",
            data_object=new_data,
            object_type=self.object_type,
        )

    def test_delete_generic_platform_action(self):
        """Ensure a generic_platform_action can be deleted"""

        generic_platform_action_data = self.make_generic_platform_action_data()

        obj = super().add_object(
            url=f"{self.url}?include=platform,contact",
            data_object=generic_platform_action_data,
            object_type=self.object_type,
        )
        _ = super().delete_object(
            url=f"{self.url}/{obj['data']['id']}",
        )
