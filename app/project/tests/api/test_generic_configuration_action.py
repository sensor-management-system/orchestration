# SPDX-FileCopyrightText: 2021 - 2023
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Tests for generic configuration actions."""

import json
import os

from project import base_url
from project.api.models import Configuration, Contact, GenericConfigurationAction
from project.api.models.base_model import db
from project.tests.base import (
    BaseTestCase,
    fake,
    generate_userinfo_data,
    test_file_path,
)
from project.tests.models.test_configurations_model import generate_configuration_model
from project.tests.models.test_generic_action_attachment_model import (
    add_generic_configuration_action_model,
)
from project.tests.models.test_generic_actions_models import (
    generate_configuration_action_model,
)


class TestGenericConfigurationAction(BaseTestCase):
    """Tests for the GenericConfigurationAction endpoints."""

    url = base_url + "/generic-configuration-actions"
    platform_url = base_url + "/platforms"
    device_url = base_url + "/devices"
    contact_url = base_url + "/contacts"
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
        """Ensure the GET /generic_configuration_actions route reachable."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        # no data yet
        self.assertEqual(response.json["data"], [])

    def test_get_generic_configuration_action_collection(self):
        """Test retrieve a collection of GenericConfigurationAction objects."""
        configuration_action = generate_configuration_action_model(
            is_public=True, is_private=False, is_internal=False
        )
        with self.client:
            response = self.client.get(self.url)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            configuration_action.description,
            data["data"][0]["attributes"]["description"],
        )

    def test_post_generic_configuration_action(self):
        """Create GenericConfigurationAction."""
        configuration = generate_configuration_model()
        userinfo = generate_userinfo_data()
        contact = Contact(
            given_name=userinfo["given_name"],
            family_name=userinfo["family_name"],
            email=userinfo["email"],
        )
        db.session.add_all([configuration, contact])
        db.session.commit()
        data = {
            "data": {
                "type": self.object_type,
                "attributes": {
                    "description": "Test GenericConfigurationAction",
                    "action_type_name": fake.pystr(),
                    "action_type_uri": fake.uri(),
                    "begin_date": fake.future_datetime().__str__(),
                    "end_date": fake.future_datetime().__str__(),
                },
                "relationships": {
                    "configuration": {
                        "data": {"type": "configuration", "id": configuration.id}
                    },
                    "contact": {"data": {"type": "contact", "id": contact.id}},
                },
            }
        }
        _ = super().add_object(
            url=f"{self.url}?include=configuration,contact",
            data_object=data,
            object_type=self.object_type,
        )
        configuration = (
            db.session.query(Configuration).filter_by(id=configuration.id).first()
        )
        self.assertEqual(configuration.update_description, "create;action")

    def test_update_generic_configuration_action(self):
        """Update GenericConfigurationAction."""
        configuration_action = generate_configuration_action_model()
        gca_updated = {
            "data": {
                "type": self.object_type,
                "id": configuration_action.id,
                "attributes": {
                    "description": "updated",
                },
            }
        }
        _ = super().update_object(
            url=f"{self.url}/{configuration_action.id}",
            data_object=gca_updated,
            object_type=self.object_type,
        )
        configuration_id = configuration_action.configuration_id
        configuration = (
            db.session.query(Configuration).filter_by(id=configuration_id).first()
        )
        self.assertEqual(configuration.update_description, "update;action")

    def test_delete_generic_configuration_action(self):
        """Delete GenericConfigurationAction."""
        configuration_action = generate_configuration_action_model()
        configuration_id = configuration_action.configuration_id
        _ = super().delete_object(
            url=f"{self.url}/{configuration_action.id}",
        )
        configuration = (
            db.session.query(Configuration).filter_by(id=configuration_id).first()
        )
        self.assertEqual(configuration.update_description, "delete;action")

    def test_filtered_by_configuration(self):
        """Ensure that I can prefilter by a specific configuration."""
        configuration1 = Configuration(
            label="sample configuration",
            is_public=True,
            is_internal=False,
        )
        db.session.add(configuration1)
        configuration2 = Configuration(
            label="sample configuration II",
            is_public=True,
            is_internal=False,
        )
        db.session.add(configuration2)

        contact = Contact(
            given_name="Nils", family_name="Brinckmann", email="nils@gfz-potsdam.de"
        )
        db.session.add(contact)

        action1 = GenericConfigurationAction(
            configuration=configuration1,
            contact=contact,
            description="Some first action",
            begin_date=fake.date_time(),
            action_type_name="ConfigurationActivity",
        )
        db.session.add(action1)

        action2 = GenericConfigurationAction(
            configuration=configuration2,
            contact=contact,
            description="Some other action",
            begin_date=fake.date_time(),
            action_type_name="ConfigurationActivity",
        )
        db.session.add(action2)
        db.session.commit()

        # first check to get them all
        with self.client:
            url_get_all = base_url + "/generic-configuration-actions"
            response = self.client.get(
                url_get_all, content_type="application/vnd.api+json"
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 2)

        # then test only for the first configuration
        with self.client:
            url_get_for_configuration1 = (
                base_url
                + f"/configurations/{configuration1.id}/generic-configuration-actions"
            )
            response = self.client.get(
                url_get_for_configuration1, content_type="application/vnd.api+json"
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 1)
        self.assertEqual(
            response.json["data"][0]["attributes"]["description"], "Some first action"
        )

        # and test the second configuration
        with self.client:
            url_get_for_configuration2 = (
                base_url
                + f"/configurations/{configuration2.id}/generic-configuration-actions"
            )
            response = self.client.get(
                url_get_for_configuration2, content_type="application/vnd.api+json"
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 1)
        self.assertEqual(
            response.json["data"][0]["attributes"]["description"], "Some other action"
        )

        # and for a non existing
        with self.client:
            url_get_for_non_existing_configuration = (
                base_url
                + f"/configurations/{configuration2.id + 9999}/generic-configuration-actions"
            )
            response = self.client.get(
                url_get_for_non_existing_configuration,
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 404)

    def test_delete_generic_configuration_action_with_attachment_link(self):
        """Delete GenericConfigurationAction with an attachment link."""
        configuration_action = add_generic_configuration_action_model()
        _ = super().delete_object(
            url=f"{self.url}/{configuration_action.id}",
        )

    def test_http_response_not_found(self):
        """Make sure that the backend responds with 404 HTTP-Code if a resource was not found."""
        url = f"{self.url}/{fake.random_int()}"
        _ = super().http_code_404_when_resource_not_found(url)
