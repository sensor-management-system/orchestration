# SPDX-FileCopyrightText: 2021 - 2022
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

import os

from project import base_url
from project.api.models.mixin import utc_now
from project.tests.base import (
    BaseTestCase,
    fake,
    generate_userinfo_data,
    test_file_path,
)
from project.tests.models.test_configurations_model import generate_configuration_model


class TestGenericConfigurationActionServices(BaseTestCase):
    """Tests for the GenericConfigurationAction endpoints."""

    url = base_url + "/generic-configuration-actions"
    platform_url = base_url + "/platforms"
    device_url = base_url + "/devices"
    contact_url = base_url + "/contacts"
    configurations_url = base_url + "/configurations"
    object_type = "generic_configuration_action"

    json_data_url = os.path.join(
        test_file_path, "drafts", "configurations_test_data.json"
    )
    device_json_data_url = os.path.join(
        test_file_path, "drafts", "devices_test_data.json"
    )
    platform_json_data_url = os.path.join(
        test_file_path, "drafts", "platforms_test_data.json"
    )

    def test_get_generic_configuration_action(self):
        """Ensure the List /generic_configuration_action route behaves correctly."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        # no data yet
        self.assertEqual(response.json["data"], [])

    def test_add_generic_configuration_action(self):
        """
        Ensure POST a new generic config
        action can be added to the database.
        """
        data = self.make_generic_configuration_action_data()

        _ = super().add_object(
            url=f"{self.url}?include=configuration,contact",
            data_object=data,
            object_type=self.object_type,
        )

    def make_generic_configuration_action_data(self):
        config = generate_configuration_model(
            is_public=True, is_private=False, is_internal=False
        )
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
                    "begin_date": utc_now().__str__(),
                },
                "relationships": {
                    "configuration": {
                        "data": {"type": "configuration", "id": config.id}
                    },
                    "contact": {
                        "data": {"type": "contact", "id": contact["data"]["id"]}
                    },
                },
            }
        }
        return data

    def test_update_generic_configuration_action(self):
        """Ensure a generic_configuration_action can be updated."""
        old_generic_configuration_action_data = (
            self.make_generic_configuration_action_data()
        )
        old_generic_configuration_action = super().add_object(
            url=f"{self.url}?include=configuration,contact",
            data_object=old_generic_configuration_action_data,
            object_type=self.object_type,
        )
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
        new_data = {
            "data": {
                "type": self.object_type,
                "id": old_generic_configuration_action["data"]["id"],
                "attributes": {
                    "description": fake.paragraph(nb_sentences=2),
                    "action_type_name": fake.lexify(
                        text="Random type: ??????????", letters="ABCDE"
                    ),
                    "action_type_uri": fake.uri(),
                    "begin_date": utc_now().__str__(),
                },
                "relationships": {
                    "configuration": {"data": {"type": "configuration", "id": "1"}},
                    "contact": {
                        "data": {"type": "contact", "id": contact["data"]["id"]}
                    },
                },
            }
        }
        old_id = old_generic_configuration_action["data"]["id"]

        _ = super().update_object(
            url=f"{self.url}/{old_id}?include=configuration,contact",
            data_object=new_data,
            object_type=self.object_type,
        )

    def test_delete_generic_configuration_action(self):
        """Ensure a generic_configuration_action can be deleted"""

        generic_configuration_action_data = (
            self.make_generic_configuration_action_data()
        )

        generic_configuration_action = super().add_object(
            url=f"{self.url}?include=configuration,contact",
            data_object=generic_configuration_action_data,
            object_type=self.object_type,
        )
        _ = super().delete_object(
            url=f"{self.url}/{generic_configuration_action['data']['id']}",
        )

    def test_http_response_not_found(self):
        """Make sure that the backend responds with 404 HTTP-Code if a resource was not found."""
        url = f"{self.url}/{fake.random_int()}"
        _ = super().http_code_404_when_resource_not_found(url)
