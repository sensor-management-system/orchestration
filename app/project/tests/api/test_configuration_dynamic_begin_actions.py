import json

import dateutil.parser

from project import base_url, db
from project.api.models import (
    Configuration,
    Contact,
    Device,
    DeviceMountAction,
    DeviceProperty,
    User,
)
from project.tests.base import BaseTestCase, create_token, fake, generate_userinfo_data
from project.tests.models.test_configuration_dynamic_action_model import (
    add_dynamic_location_begin_action_model,
)
from project.tests.models.test_configurations_model import generate_configuration_model


class TestConfigurationDynamicLocationBeginActionServices(BaseTestCase):
    """Tests for the ConfigurationDynamicLocationBeginAction endpoint."""

    url = base_url + "/dynamic-location-actions"
    contact_url = base_url + "/contacts"
    object_type = "configuration_dynamic_location_action"

    def test_get_configuration_dynamic_location_action(self):
        """Ensure the List /configuration_dynamic_location_action route behaves correctly."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        # no data yet
        self.assertEqual(response.json["data"], [])

    def test_get_device_calibration_action_collection(self):
        """Test retrieve a collection of configuration_dynamic_location_action objects."""
        dynamic_location_begin_action = add_dynamic_location_begin_action_model(
            is_public=True, is_private=False, is_internal=False
        )
        with self.client:
            response = self.client.get(self.url)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            dynamic_location_begin_action.begin_description,
            data["data"][0]["attributes"]["begin_description"],
        )

    def test_add_configuration_dynamic_begin_location_action(self):
        """Ensure a new configuration dynamic location can be added to the database."""
        device = Device(
            short_name="Device 555",
            manufacturer_name=fake.pystr(),
            is_public=False,
            is_private=False,
            is_internal=True,
        )
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
                    "begin_date": "2021-08-22T10:00:50.542Z",
                    "end_date": "2021-10-22T10:00:50.542Z",
                    "begin_description": "beginning",
                    "end_description": "finishing",
                },
                "relationships": {
                    "begin_contact": {"data": {"type": "contact", "id": contact.id}},
                    "end_contact": {"data": {"type": "contact", "id": contact.id}},
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
        # Make sure that we have the device mount action for the xyz properties.
        device_mount_action = DeviceMountAction(
            device=device,
            configuration=config,
            begin_contact=contact,
            begin_date=dateutil.parser.parse(data["data"]["attributes"]["begin_date"]),
        )
        db.session.add(device_mount_action)
        db.session.commit()

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
            configuration.update_description, "create;dynamic location action"
        )

    def test_add_for_archived_configuration(self):
        """Ensure we can't add a location for an archived configuration."""
        device = Device(
            short_name="Device 555",
            is_public=False,
            is_private=False,
            is_internal=True,
        )
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
        config.archived = True
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
                    "begin_date": "2021-08-22T10:00:50.542Z",
                    "end_date": "2021-10-22T10:00:50.542Z",
                    "begin_description": "beginning",
                    "end_description": "finishing",
                },
                "relationships": {
                    "begin_contact": {"data": {"type": "contact", "id": contact.id}},
                    "end_contact": {"data": {"type": "contact", "id": contact.id}},
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
        # Make sure that we have the device mount action for the xyz properties.
        device_mount_action = DeviceMountAction(
            device=device,
            configuration=config,
            begin_contact=contact,
            begin_date=dateutil.parser.parse(data["data"]["attributes"]["begin_date"]),
        )
        db.session.add(device_mount_action)
        db.session.commit()

        _ = super().try_add_object_with_status_code(
            url=self.url, data_object=data, expected_status_code=409
        )

    def test_add_for_archived_device(self):
        """Ensure we can't add a location for an archived configuration."""
        device = Device(
            short_name="Device 555",
            is_public=False,
            is_private=False,
            is_internal=True,
            archived=True,
        )
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
                    "begin_date": "2021-08-22T10:00:50.542Z",
                    "end_date": "2021-10-22T10:00:50.542Z",
                    "begin_description": "beginning",
                    "end_description": "finishing",
                },
                "relationships": {
                    "begin_contact": {"data": {"type": "contact", "id": contact.id}},
                    "end_contact": {"data": {"type": "contact", "id": contact.id}},
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
        # Make sure that we have the device mount action for the xyz properties.
        device_mount_action = DeviceMountAction(
            device=device,
            configuration=config,
            begin_contact=contact,
            begin_date=dateutil.parser.parse(data["data"]["attributes"]["begin_date"]),
        )
        db.session.add(device_mount_action)
        db.session.commit()

        _ = super().try_add_object_with_status_code(
            url=self.url, data_object=data, expected_status_code=409
        )

    def test_add_configuration_dynamic_begin_location_action_without_mount_action(self):
        """
        Ensure POST fails if there is no mount action for the xyz properties.

        This is part of the more advanced validation & we want to make sure
        that those run.
        """
        device = Device(
            short_name="Device 555",
            is_public=False,
            is_private=False,
            is_internal=True,
        )
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
                    "begin_date": "2021-08-22T10:00:50.542Z",
                    "end_date": "2021-10-22T10:00:50.542Z",
                    "begin_description": "beginning",
                    "end_description": "finishing",
                },
                "relationships": {
                    "begin_contact": {"data": {"type": "contact", "id": contact.id}},
                    "end_contact": {"data": {"type": "contact", "id": contact.id}},
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
        access_headers = create_token()
        with self.client:
            response = self.client.post(
                self.url,
                data=json.dumps(data),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
        self.assertEqual(response.status_code, 409)

    def prepare_request_data_with_config(self, description):
        """Create some request data to add a location action."""
        device = Device(
            short_name="Device 555",
            manufacturer_name=fake.pystr(),
            is_public=False,
            is_private=False,
            is_internal=True,
        )

        config = generate_configuration_model(
            is_public=True, is_private=False, is_internal=False
        )
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
                    "begin_date": "2021-08-22T10:00:50.542Z",
                    "end_date": "2021-10-23T10:00:50.542Z",
                    "begin_description": description,
                    "end_description": description,
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

    def test_update_configuration_dynamic_begin_location_action(self):
        """Ensure a configuration_dynamic_begin_location_action can be updated."""
        dynamic_location_begin_action = add_dynamic_location_begin_action_model()
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
        # This block for the device mount actions is just to make sure
        # that all the device properties have mounts for the timepoints.
        device_mounts_by_device_ids = {}
        contact_instance = (
            db.session.query(Contact).filter_by(id=contact["data"]["id"]).one()
        )
        for device_property in [
            dynamic_location_begin_action.x_property,
            dynamic_location_begin_action.y_property,
            dynamic_location_begin_action.z_property,
        ]:
            if device_property:
                device = device_property.device
                device_id = device.id
                if device_id not in device_mounts_by_device_ids.keys():
                    mount_action = DeviceMountAction(
                        device=device,
                        configuration=dynamic_location_begin_action.configuration,
                        begin_date=dynamic_location_begin_action.begin_date,
                        begin_contact=contact_instance,
                    )
                    db.session.add(mount_action)
                    db.session.commit()
                    device_mounts_by_device_ids[device_id] = mount_action
        new_data = {
            "data": {
                "type": self.object_type,
                "id": dynamic_location_begin_action.id,
                "attributes": {
                    "end_description": "stopped",
                    "end_date": "2021-10-22T10:00:50.542Z",
                },
                "relationships": {
                    "end_contact": {
                        "data": {"type": "contact", "id": contact["data"]["id"]}
                    },
                },
            }
        }

        result = super().update_object(
            url=f"{self.url}/{dynamic_location_begin_action.id}",
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
            configuration.update_description, "update;dynamic location action"
        )

    def test_update_archived_configuration(self):
        """Ensure that we can't change for archived configurations."""
        dynamic_location_begin_action = add_dynamic_location_begin_action_model()
        dynamic_location_begin_action.configuration.archived = True
        db.session.add(dynamic_location_begin_action.configuration)
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
        # This block for the device mount actions is just to make sure
        # that all the device properties have mounts for the timepoints.
        device_mounts_by_device_ids = {}
        contact_instance = (
            db.session.query(Contact).filter_by(id=contact["data"]["id"]).one()
        )
        for device_property in [
            dynamic_location_begin_action.x_property,
            dynamic_location_begin_action.y_property,
            dynamic_location_begin_action.z_property,
        ]:
            if device_property:
                device = device_property.device
                device_id = device.id
                if device_id not in device_mounts_by_device_ids.keys():
                    mount_action = DeviceMountAction(
                        device=device,
                        configuration=dynamic_location_begin_action.configuration,
                        begin_date=dynamic_location_begin_action.begin_date,
                        begin_contact=contact_instance,
                    )
                    db.session.add(mount_action)
                    db.session.commit()
                    device_mounts_by_device_ids[device_id] = mount_action
        new_data = {
            "data": {
                "type": self.object_type,
                "id": dynamic_location_begin_action.id,
                "attributes": {
                    "end_description": "stopped",
                    "end_date": "2021-10-22T10:00:50.542Z",
                },
                "relationships": {
                    "end_contact": {
                        "data": {"type": "contact", "id": contact["data"]["id"]}
                    },
                },
            }
        }

        _ = super().try_update_object_with_status_code(
            url=f"{self.url}/{dynamic_location_begin_action.id}",
            data_object=new_data,
            expected_status_code=409,
        )

    def test_update_archived_device(self):
        """Ensure that we can't change for archived devices."""
        dynamic_location_begin_action = add_dynamic_location_begin_action_model()
        dynamic_location_begin_action.x_property.device.archived = True
        db.session.add(dynamic_location_begin_action.x_property.device)
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
        # This block for the device mount actions is just to make sure
        # that all the device properties have mounts for the timepoints.
        device_mounts_by_device_ids = {}
        contact_instance = (
            db.session.query(Contact).filter_by(id=contact["data"]["id"]).one()
        )
        for device_property in [
            dynamic_location_begin_action.x_property,
            dynamic_location_begin_action.y_property,
            dynamic_location_begin_action.z_property,
        ]:
            if device_property:
                device = device_property.device
                device_id = device.id
                if device_id not in device_mounts_by_device_ids.keys():
                    mount_action = DeviceMountAction(
                        device=device,
                        configuration=dynamic_location_begin_action.configuration,
                        begin_date=dynamic_location_begin_action.begin_date,
                        begin_contact=contact_instance,
                    )
                    db.session.add(mount_action)
                    db.session.commit()
                    device_mounts_by_device_ids[device_id] = mount_action
        new_data = {
            "data": {
                "type": self.object_type,
                "id": dynamic_location_begin_action.id,
                "attributes": {
                    "end_description": "stopped",
                    "end_date": "2021-10-22T10:00:50.542Z",
                },
                "relationships": {
                    "end_contact": {
                        "data": {"type": "contact", "id": contact["data"]["id"]}
                    },
                },
            }
        }

        _ = super().try_update_object_with_status_code(
            url=f"{self.url}/{dynamic_location_begin_action.id}",
            data_object=new_data,
            expected_status_code=409,
        )

    def test_update_configuration_dynamic_begin_location_action_fail(self):
        """Ensure we validate the mounts for the xzy properties."""
        dynamic_location_begin_action = add_dynamic_location_begin_action_model()
        contact = Contact(
            family_name="Bob", given_name="Meister", email="bob.meister@localhost"
        )
        superuser = User(contact=contact, is_superuser=True, subject=contact.email)
        db.session.add_all([contact, superuser])
        db.session.commit()
        # We don't add the mount action here, so the patch request will fail.
        new_data = {
            "data": {
                "type": self.object_type,
                "id": dynamic_location_begin_action.id,
                "attributes": {
                    "end_description": "stopped",
                    "end_date": "2021-10-22T10:00:50.542Z",
                },
                "relationships": {
                    "end_contact": {
                        "data": {
                            "type": "contact",
                            "id": contact.id,
                        }
                    },
                },
            }
        }

        with self.run_requests_as(superuser):
            with self.client:
                response = self.client.patch(
                    f"{self.url}/{dynamic_location_begin_action.id}",
                    data=json.dumps(new_data),
                    content_type="application/vnd.api+json",
                )
        self.assertEqual(response.status_code, 409)

    def test_update_configuration_dynamic_begin_location_action_set_end_contact_to_none(
        self,
    ):
        """Ensure that we can reset the end_contact if necessary."""
        dynamic_location_begin_action = add_dynamic_location_begin_action_model()
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
        dynamic_location_begin_action.end_contact = contact
        db.session.add_all([dynamic_location_begin_action, contact])
        db.session.commit()
        # This block for the device mount actions is just to make sure
        # that all the device properties have mounts for the timepoints.
        device_mounts_by_device_ids = {}
        for device_property in [
            dynamic_location_begin_action.x_property,
            dynamic_location_begin_action.y_property,
            dynamic_location_begin_action.z_property,
        ]:
            if device_property:
                device = device_property.device
                device_id = device.id
                if device_id not in device_mounts_by_device_ids.keys():
                    mount_action = DeviceMountAction(
                        device=device,
                        configuration=dynamic_location_begin_action.configuration,
                        begin_date=dynamic_location_begin_action.begin_date,
                        begin_contact=contact,
                    )
                    db.session.add(mount_action)
                    db.session.commit()
                    device_mounts_by_device_ids[device_id] = mount_action
        new_data = {
            "data": {
                "type": self.object_type,
                "id": dynamic_location_begin_action.id,
                "attributes": {
                    "end_description": "stopped",
                    "end_date": "2021-10-22T10:00:50.542Z",
                },
                "relationships": {
                    "end_contact": {
                        "data": None,
                    },
                },
            }
        }

        _ = super().update_object(
            url=f"{self.url}/{dynamic_location_begin_action.id}",
            data_object=new_data,
            object_type=self.object_type,
        )

    def test_delete_configuration_dynamic_begin_location_action(self):
        """Ensure a configuration_dynamic_begin_location_action can be deleted."""
        dynamic_location_begin_action = add_dynamic_location_begin_action_model()
        configuration_id = dynamic_location_begin_action.configuration_id

        _ = super().delete_object(
            url=f"{self.url}/{dynamic_location_begin_action.id}",
        )
        configuration = (
            db.session.query(Configuration).filter_by(id=configuration_id).first()
        )
        self.assertEqual(
            configuration.update_description, "delete;dynamic location action"
        )

    def test_delete_archived_configuration(self):
        """Ensure we can't delete for an archived configuration."""
        dynamic_location_begin_action = add_dynamic_location_begin_action_model()
        dynamic_location_begin_action.configuration.archived = True
        db.session.add(dynamic_location_begin_action.configuration)
        db.session.commit()

        access_headers = create_token()
        with self.client:
            response = self.client.delete(
                f"{self.url}/{dynamic_location_begin_action.id}",
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
        self.assertEqual(response.status_code, 409)

    def test_delete_archived_device(self):
        """Ensure we can't delete for an archived device."""
        dynamic_location_begin_action = add_dynamic_location_begin_action_model()
        dynamic_location_begin_action.x_property.device.archived = True
        db.session.add(dynamic_location_begin_action.x_property.device)
        db.session.commit()

        access_headers = create_token()
        with self.client:
            response = self.client.delete(
                f"{self.url}/{dynamic_location_begin_action.id}",
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
        self.assertEqual(response.status_code, 409)

    def test_filtered_by_configuration(self):
        """Ensure that filter by a specific configuration works."""
        data1, config1 = self.prepare_request_data_with_config(
            "test dynamic_location_begin_action1"
        )

        _ = super().add_object(
            url=self.url,
            data_object=data1,
            object_type=self.object_type,
        )
        data2, _ = self.prepare_request_data_with_config(
            "test dynamic_location_begin_action2"
        )

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
                base_url + f"/configurations/{config1.id}/dynamic-location-actions"
            )
            response = self.client.get(
                url_get_for_config1, content_type="application/vnd.api+json"
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 1)
        self.assertEqual(
            response.json["data"][0]["attributes"]["begin_description"],
            "test dynamic_location_begin_action1",
        )

    def prepare_request_data_with_x_property(self, description):
        """Prepare some payloads to add/update an x property."""
        device = Device(
            short_name="Device 575",
            manufacturer_name=fake.pystr(),
            is_public=False,
            is_private=False,
            is_internal=True,
        )
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
        config = generate_configuration_model(
            is_public=True, is_private=False, is_internal=False
        )
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
                    "begin_description": description,
                },
                "relationships": {
                    "begin_contact": {"data": {"type": "contact", "id": contact.id}},
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

    def ensure_device_mount_action_exists(self, data1, x_property1):
        """Help to add a device mount action for the dynamic location property."""
        # As we use a device property here, we need to make sure that
        # its device is also mounted on the configuration.
        configuration = (
            db.session.query(Configuration)
            .filter_by(id=data1["data"]["relationships"]["configuration"]["data"]["id"])
            .one()
        )
        contact = (
            db.session.query(Contact)
            .filter_by(id=data1["data"]["relationships"]["begin_contact"]["data"]["id"])
            .one()
        )
        device_mount_action = DeviceMountAction(
            device=x_property1.device,
            configuration=configuration,
            begin_contact=contact,
            begin_date=dateutil.parser.parse(data1["data"]["attributes"]["begin_date"]),
        )
        db.session.add(device_mount_action)
        db.session.commit()

    def test_filtered_by_x_property(self):
        """Ensure that filter by a specific device-property works."""
        data1, x_property1 = self.prepare_request_data_with_x_property(
            "test dynamic_location_begin_action1"
        )
        self.ensure_device_mount_action_exists(data1, x_property1)

        _ = super().add_object(
            url=self.url,
            data_object=data1,
            object_type=self.object_type,
        )
        data2, x_property2 = self.prepare_request_data_with_x_property(
            "test dynamic_location_begin_action2"
        )
        self.ensure_device_mount_action_exists(data2, x_property2)

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
                base_url
                + f"/device-properties/{x_property1.id}/dynamic-location-actions-x"
            )
            response = self.client.get(
                url_get_for_config1, content_type="application/vnd.api+json"
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 1)
        self.assertEqual(
            response.json["data"][0]["attributes"]["begin_description"],
            "test dynamic_location_begin_action1",
        )

    def test_http_response_not_found(self):
        """Make sure that the backend responds with 404 HTTP-Code if a resource was not found."""
        url = f"{self.url}/{fake.random_int()}"
        _ = super().http_code_404_when_resource_not_found(url)
