"""Tests for the static location action api."""

import datetime
import json

from project import base_url, db
from project.api.models import Configuration, Contact
from project.tests.base import BaseTestCase, create_token, fake, generate_userinfo_data
from project.tests.models.test_configuration_static_action_model import (
    add_static_location_begin_action_model,
)
from project.tests.models.test_configurations_model import generate_configuration_model


class TestConfigurationStaticLocationActionServices(BaseTestCase):
    """Tests for the ConfigurationStaticLocationAction endpoint."""

    url = base_url + "/static-location-actions"
    contact_url = base_url + "/contacts"
    object_type = "configuration_static_location_action"

    def test_get_configuration_static_location_action(self):
        """Ensure the List /configuration_static_location_action route behaves correctly."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        # no data yet
        self.assertEqual(response.json["data"], [])

    def test_get_device_calibration_action_collection(self):
        """Test retrieve a collection of configuration_static_location_action objects."""
        static_location_begin_action = add_static_location_begin_action_model(
            is_public=True, is_private=False, is_internal=False
        )
        with self.client:
            response = self.client.get(self.url)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            static_location_begin_action.begin_description,
            data["data"][0]["attributes"]["begin_description"],
        )

    def test_add_configuration_static_begin_location_action(self):
        """
        Ensure that we can create a new static location.

        Ensure POST a new configuration static location begin action
        can be added to the database.
        """
        data, _ = self.prepare_request_data(
            "test configuration_static_location_begin_action"
        )

        result = super().add_object(
            url=self.url,
            data_object=data,
            object_type=self.object_type,
        )

        configuration_id = result["data"]["relationships"]["configuration"]["data"][
            "id"
        ]
        configuration = (
            db.session.query(Configuration).filter_by(id=configuration_id).first()
        )
        self.assertEqual(
            configuration.update_description, "create;static location action"
        )
        # But we can't add another one with the very same settings, as
        # the exact configuration has already the location for the time slot
        self.try_add_object_with_status_code(
            url=self.url,
            data_object=data,
            expected_status_code=409,  # 409 => ConflictError
        )

    def test_post_configuration_static_begin_location_action_for_archived_configuration(
        self,
    ):
        """Ensure we can't add a location to an archived configuration."""
        data, _ = self.prepare_request_data(
            "test configuration_static_location_begin_action"
        )

        configuration_id = data["data"]["relationships"]["configuration"]["data"]["id"]

        configuration = (
            db.session.query(Configuration).filter_by(id=configuration_id).first()
        )
        configuration.archived = True
        db.session.add(configuration)
        db.session.commit()

        _ = super().try_add_object_with_status_code(
            url=self.url, data_object=data, expected_status_code=409
        )

    def prepare_request_data(self, description):
        """Return a payload to create a static location action later."""
        config = generate_configuration_model(
            is_public=True, is_private=False, is_internal=False
        )
        userinfo = generate_userinfo_data()
        contact = Contact(
            given_name=userinfo["given_name"],
            family_name=userinfo["family_name"],
            email=userinfo["email"],
        )
        db.session.add_all([contact, config])
        db.session.commit()
        data = {
            "data": {
                "type": self.object_type,
                "attributes": {
                    "begin_date": "2021-10-22T10:00:50.542Z",
                    "end_date": "2026-09-22T10:00:50.542Z",
                    "begin_description": description,
                    "end_description": "end",
                    "x": str(fake.coordinate()),
                    "y": str(fake.coordinate()),
                    "z": str(fake.coordinate()),
                    "epsg_code": None,
                    "elevation_datum_name": None,
                    "elevation_datum_uri": fake.uri(),
                },
                "relationships": {
                    "begin_contact": {"data": {"type": "contact", "id": contact.id}},
                    "end_contact": {"data": {"type": "contact", "id": contact.id}},
                    "configuration": {
                        "data": {"type": "configuration", "id": config.id}
                    },
                },
            }
        }
        return data, config

    def test_update_configuration_static_begin_location_action(self):
        """Ensure a configuration_static_begin_location_action can be updated."""
        static_location_begin_action = add_static_location_begin_action_model()
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
                "id": static_location_begin_action.id,
                "attributes": {
                    "end_description": "changed",
                    "end_date": "2023-10-22T10:00:50.542Z",
                },
                "relationships": {
                    "end_contact": {
                        "data": {"type": "contact", "id": contact["data"]["id"]}
                    },
                },
            }
        }

        result = super().update_object(
            url=f"{self.url}/{static_location_begin_action.id}",
            data_object=new_data,
            object_type=self.object_type,
        )
        configuration_id = result["data"]["relationships"]["configuration"]["data"][
            "id"
        ]
        configuration = (
            db.session.query(Configuration).filter_by(id=configuration_id).first()
        )
        self.assertEqual(
            configuration.update_description, "update;static location action"
        )

    def test_update_for_archived_configuration(self):
        """Ensure a configuration_static_begin_location_action can be updated."""
        static_location_begin_action = add_static_location_begin_action_model()

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
                "id": static_location_begin_action.id,
                "attributes": {
                    "end_description": "changed",
                    "end_date": "2023-10-22T10:00:50.542Z",
                },
                "relationships": {
                    "end_contact": {
                        "data": {"type": "contact", "id": contact["data"]["id"]}
                    },
                },
            }
        }
        static_location_begin_action.configuration.archived = True
        db.session.add(static_location_begin_action.configuration)
        db.session.commit()

        _ = super().try_update_object_with_status_code(
            url=f"{self.url}/{static_location_begin_action.id}",
            data_object=new_data,
            expected_status_code=409,
        )

    def test_update_configuration_static_begin_location_action_set_end_contact_to_none(
        self,
    ):
        """Ensure that we can reset the end_contact if necessary."""
        static_location_begin_action = add_static_location_begin_action_model()
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
        contact_result = super().add_object(
            url=self.contact_url, data_object=contact_data, object_type="contact"
        )
        contact = (
            db.session.query(Contact).filter_by(id=contact_result["data"]["id"]).one()
        )
        static_location_begin_action.end_contact = contact
        db.session.add_all([static_location_begin_action, contact])
        db.session.commit()
        new_data = {
            "data": {
                "type": self.object_type,
                "id": static_location_begin_action.id,
                "attributes": {
                    "end_description": "changed",
                    "end_date": "2023-10-22T10:00:50.542Z",
                },
                # And we want to set the contact back to None
                "relationships": {
                    # "end_contact": {
                    #    "data": {"type": "contact", "id": None}
                    # },
                    # "end_contact": None,
                    "end_contact": {"data": None},
                },
            }
        }

        _ = super().update_object(
            url=f"{self.url}/{static_location_begin_action.id}",
            data_object=new_data,
            object_type=self.object_type,
        )

    def test_update_configuration_static_location_fail_due_to_overlapping_times_for_locations(
        self,
    ):
        """Ensure that patching fails if there is already a location for the time."""
        static_location_begin_action1 = add_static_location_begin_action_model()
        static_location_begin_action2 = add_static_location_begin_action_model()
        static_location_begin_action1.begin_date = datetime.datetime(
            2023, 1, 1, 12, 0, 0
        )
        static_location_begin_action1.end_date = datetime.datetime(
            2023, 12, 31, 12, 0, 0
        )

        static_location_begin_action2.begin_date = datetime.datetime(
            2024, 1, 1, 12, 0, 0
        )
        static_location_begin_action2.end_date = datetime.datetime(
            2024, 12, 31, 12, 0, 0
        )
        static_location_begin_action2.configuration = (
            static_location_begin_action1.configuration
        )

        db.session.add_all(
            [static_location_begin_action1, static_location_begin_action2]
        )
        db.session.commit()

        updated_data = {
            "data": {
                "type": self.object_type,
                "id": static_location_begin_action1.id,
                "attributes": {
                    "begin_date": "2023-11-11T11:11:11.000Z",
                    "end_date": "2024-08-09T00:00:50.542Z",
                },
            }
        }

        _ = super().try_update_object_with_status_code(
            url=f"{self.url}/{static_location_begin_action1.id}",
            data_object=updated_data,
            expected_status_code=409,
        )

    def test_delete_configuration_static_begin_location_action(self):
        """Ensure a configuration_static_begin_location_action can be deleted."""
        static_location_begin_action = add_static_location_begin_action_model()
        configuration_id = static_location_begin_action.configuration_id

        _ = super().delete_object(
            url=f"{self.url}/{static_location_begin_action.id}",
        )
        configuration = (
            db.session.query(Configuration).filter_by(id=configuration_id).first()
        )
        self.assertEqual(
            configuration.update_description, "delete;static location action"
        )

    def test_delete_for_archived_configuration(self):
        """Ensure we can't delete a location for an archived configuration."""
        static_location_begin_action = add_static_location_begin_action_model()
        configuration = static_location_begin_action.configuration

        configuration.archived = True
        db.session.add(configuration)
        db.session.commit()

        with self.client:
            access_headers = create_token()
            response = self.client.delete(
                f"{self.url}/{static_location_begin_action.id}",
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
        self.assertEqual(response.status_code, 409)

    def test_filtered_by_configuration(self):
        """Ensure that filter by a specific configuration works well."""
        data1, config1 = self.prepare_request_data("test static_location_begin_action1")

        _ = super().add_object(
            url=self.url,
            data_object=data1,
            object_type=self.object_type,
        )
        data2, config2 = self.prepare_request_data("test static_location_begin_action2")

        _ = super().add_object(
            url=self.url,
            data_object=data2,
            object_type=self.object_type,
        )

        with self.client:
            response = self.client.get(
                self.url, content_type="application/vnd.api+json"
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 2)
        # Test only for the first one
        with self.client:
            url_get_for_config1 = (
                base_url + f"/configurations/{config1.id}/static-location-actions"
            )
            response = self.client.get(
                url_get_for_config1, content_type="application/vnd.api+json"
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 1)
        self.assertEqual(
            response.json["data"][0]["attributes"]["begin_description"],
            "test static_location_begin_action1",
        )

    def test_http_response_not_found(self):
        """Make sure that the backend responds with 404 HTTP-Code if a resource was not found."""
        url = f"{self.url}/{fake.random_int()}"
        _ = super().http_code_404_when_resource_not_found(url)
