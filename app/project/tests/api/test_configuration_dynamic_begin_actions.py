import json

from project import base_url, db
from project.api.models import Contact, Device, DeviceProperty
from project.tests.base import BaseTestCase, fake, generate_userinfo_data
from project.tests.models.test_configuration_dynamic_action_model import (
    add_dynamic_location_begin_action_model,
)
from project.tests.models.test_configurations_model import generate_configuration_model


class TestConfigurationDynamicLocationBeginActionServices(BaseTestCase):
    """Tests for the ConfigurationDynamicLocationBeginAction endpoint."""

    url = base_url + "/dynamic-location-begin-actions"
    contact_url = base_url + "/contacts"
    object_type = "configuration_dynamic_location_begin_action"

    def test_get_configuration_dynamic_location_action(self):
        """Ensure the List /configuration_dynamic_location_action route behaves correctly."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        # no data yet
        self.assertEqual(response.json["data"], [])

    def test_get_device_calibration_action_collection(self):
        """Test retrieve a collection of configuration_dynamic_location_action objects."""
        static_location_begin_action = add_dynamic_location_begin_action_model()
        with self.client:
            response = self.client.get(self.url)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            static_location_begin_action.description,
            data["data"][0]["attributes"]["description"],
        )

    def test_add_configuration_dynamic_begin_location_action(self):
        """
        Ensure POST a new configuration static location begin action
        can be added to the database.
        """
        device = Device(short_name="Device 555")
        x_property = DeviceProperty(
            device=device,
            measuring_range_min=fake.pyfloat(),
            measuring_range_max=fake.pyfloat(),
            failure_value=fake.pyfloat(),
            accuracy=fake.pyfloat(),
            label=fake.pystr(),
            unit_uri=fake.uri(),
            unit_name=fake.pystr(),
            compartment_uri=fake.uri(),
            compartment_name=fake.pystr(),
            property_uri=fake.uri(),
            property_name="Test x_property",
            sampling_media_uri=fake.uri(),
            sampling_media_name=fake.pystr(),
        )
        y_property = DeviceProperty(
            device=device,
            measuring_range_min=fake.pyfloat(),
            measuring_range_max=fake.pyfloat(),
            failure_value=fake.pyfloat(),
            accuracy=fake.pyfloat(),
            label=fake.pystr(),
            unit_uri=fake.uri(),
            unit_name=fake.pystr(),
            compartment_uri=fake.uri(),
            compartment_name=fake.pystr(),
            property_uri=fake.uri(),
            property_name="Test y_property",
            sampling_media_uri=fake.uri(),
            sampling_media_name=fake.pystr(),
        )
        z_property = DeviceProperty(
            device=device,
            measuring_range_min=fake.pyfloat(),
            measuring_range_max=fake.pyfloat(),
            failure_value=fake.pyfloat(),
            accuracy=fake.pyfloat(),
            label=fake.pystr(),
            unit_uri=fake.uri(),
            unit_name=fake.pystr(),
            compartment_uri=fake.uri(),
            compartment_name=fake.pystr(),
            property_uri=fake.uri(),
            property_name="Test z_property",
            sampling_media_uri=fake.uri(),
            sampling_media_name=fake.pystr(),
        )
        config = generate_configuration_model()
        userinfo = generate_userinfo_data()
        contact = Contact(
            given_name=userinfo["given_name"],
            family_name=userinfo["family_name"],
            email=userinfo["email"],
        )
        db.session.add_all(
            [device, x_property, y_property, z_property, contact, config]
        )
        db.session.commit()
        data = {
            "data": {
                "type": self.object_type,
                "attributes": {
                    "begin_date": fake.future_datetime().__str__(),
                    "description": "test",
                },
                "relationships": {
                    "contact": {"data": {"type": "contact", "id": contact.id}},
                    "x_property": {
                        "data": {"type": "device_property", "id": x_property.id}
                    },
                    "y_property": {
                        "data": {"type": "device_property", "id": y_property.id}
                    },
                    "z_property": {
                        "data": {"type": "device_property", "id": z_property.id}
                    },
                    "configuration": {
                        "data": {"type": "configuration", "id": config.id}
                    },
                },
            }
        }
        _ = super().add_object(
            url=f"{self.url}?include=configuration,contact,x_property,y_property,z_property",
            data_object=data,
            object_type=self.object_type,
        )

    def prepare_request_data_with_config(self, description):
        device = Device(short_name="Device 555")

        config = generate_configuration_model()
        userinfo = generate_userinfo_data()
        contact = Contact(
            given_name=userinfo["given_name"],
            family_name=userinfo["family_name"],
            email=userinfo["email"],
        )
        db.session.add_all([device, contact, config])
        db.session.commit()
        data = {
            "data": {
                "type": self.object_type,
                "attributes": {
                    "begin_date": fake.future_datetime().__str__(),
                    "description": description,
                },
                "relationships": {
                    "contact": {"data": {"type": "contact", "id": contact.id}},
                    "configuration": {
                        "data": {"type": "configuration", "id": config.id}
                    },
                },
            }
        }
        return data, config

    def test_update_configuration_dynamic_begin_location_action(self):
        """Ensure a configuration_dynamic_begin_location_action can be updated."""
        static_location_begin_action = add_dynamic_location_begin_action_model()
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
                "attributes": {"description": "changed",},
                "relationships": {
                    "contact": {
                        "data": {"type": "contact", "id": contact["data"]["id"]}
                    },
                },
            }
        }

        _ = super().update_object(
            url=f"{self.url}/{static_location_begin_action.id}?include=contact",
            data_object=new_data,
            object_type=self.object_type,
        )

    def test_delete_configuration_dynamic_begin_location_action(self):
        """Ensure a configuration_dynamic_begin_location_action can be deleted"""

        static_location_begin_action = add_dynamic_location_begin_action_model()

        _ = super().delete_object(url=f"{self.url}/{static_location_begin_action.id}",)

    def test_filtered_by_configuration(self):
        """Ensure that filter by a specific configuration works."""
        data1, config1 = self.prepare_request_data_with_config(
            "test dynamic_location_begin_action1"
        )

        _ = super().add_object(
            url=f"{self.url}?include=configuration,contact,x_property,y_property,z_property",
            data_object=data1,
            object_type=self.object_type,
        )
        data2, _ = self.prepare_request_data_with_config(
            "test dynamic_location_begin_action2"
        )

        _ = super().add_object(
            url=f"{self.url}?include=configuration,contact,x_property,y_property,z_property",
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
                base_url + f"/configurations/{config1.id}/dynamic-location-begin-action"
            )
            response = self.client.get(
                url_get_for_config1, content_type="application/vnd.api+json"
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 1)
        self.assertEqual(
            response.json["data"][0]["attributes"]["description"],
            "test dynamic_location_begin_action1",
        )

    def prepare_request_data_with_x_property(self, description):
        device = Device(short_name="Device 575")
        x_property = DeviceProperty(
            device=device,
            measuring_range_min=fake.pyfloat(),
            measuring_range_max=fake.pyfloat(),
            failure_value=fake.pyfloat(),
            accuracy=fake.pyfloat(),
            label=fake.pystr(),
            unit_uri=fake.uri(),
            unit_name=fake.pystr(),
            compartment_uri=fake.uri(),
            compartment_name=fake.pystr(),
            property_uri=fake.uri(),
            property_name="Test x_property",
            sampling_media_uri=fake.uri(),
            sampling_media_name=fake.pystr(),
        )
        config = generate_configuration_model()
        userinfo = generate_userinfo_data()
        contact = Contact(
            given_name=userinfo["given_name"],
            family_name=userinfo["family_name"],
            email=userinfo["email"],
        )
        db.session.add_all([device, contact, config, x_property])
        db.session.commit()
        data = {
            "data": {
                "type": self.object_type,
                "attributes": {
                    "begin_date": fake.future_datetime().__str__(),
                    "description": description,
                },
                "relationships": {
                    "contact": {"data": {"type": "contact", "id": contact.id}},
                    "x_property": {
                        "data": {"type": "device_property", "id": x_property.id}
                    },
                    "configuration": {
                        "data": {"type": "configuration", "id": config.id}
                    },
                },
            }
        }
        return data, x_property

    def test_filtered_by_x_property(self):
        """Ensure that filter by a specific device-property works."""
        data1, x_property1 = self.prepare_request_data_with_x_property(
            "test dynamic_location_begin_action1"
        )

        _ = super().add_object(
            url=f"{self.url}?include=configuration,contact,x_property",
            data_object=data1,
            object_type=self.object_type,
        )
        data2, _ = self.prepare_request_data_with_x_property(
            "test dynamic_location_begin_action2"
        )

        _ = super().add_object(
            url=f"{self.url}?include=configuration,contact,x_property",
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
                base_url
                + f"/device-properties/{x_property1.id}/dynamic-location-begin-actions-x"
            )
            response = self.client.get(
                url_get_for_config1, content_type="application/vnd.api+json"
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 1)
        self.assertEqual(
            response.json["data"][0]["attributes"]["description"],
            "test dynamic_location_begin_action1",
        )

    def test_http_response_not_found(self):
        """Make sure that the backend responds with 404 HTTP-Code if a resource was not found."""
        url = f"{self.url}/{fake.random_int()}"
        _ = super().http_code_404_when_resource_not_found(url)
