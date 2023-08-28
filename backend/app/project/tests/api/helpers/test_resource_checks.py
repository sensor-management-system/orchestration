# SPDX-FileCopyrightText: 2022
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Luca Johannes Nendel <luca-johannes.nendel@ufz.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Tests for various resource tests."""
import dateutil.parser

from project import base_url
from project.api.models import (
    Configuration,
    Contact,
    Device,
    DeviceMountAction,
    DeviceProperty,
)
from project.api.models.base_model import db
from project.tests.base import BaseTestCase, create_token, fake, generate_userinfo_data
from project.tests.models.test_configurations_model import generate_configuration_model


class TestDevicePropertyValidator(BaseTestCase):
    """
    Validator tests for device properties.

    It mainly tests the usages in dynamic locations actions - and
    that they can't be deleted.
    """

    url = base_url + "/dynamic-location-actions"
    object_type = "configuration_dynamic_location_action"

    def test_validate_property_dynamic_location_action_deletion(self):
        """Ensure that a property used by a dynamic_location_action can't be deleted."""
        device = Device(short_name="Device 69", is_public=True)
        property = DeviceProperty(
            device=device,
            accuracy=fake.pyfloat(),
            label=fake.pystr(),
            unit_uri=fake.uri(),
            unit_name=fake.pystr(),
            property_uri=fake.uri(),
            property_name="Test property",
        )

        config = generate_configuration_model()
        userinfo = generate_userinfo_data()
        contact = Contact(
            given_name=userinfo["given_name"],
            family_name=userinfo["family_name"],
            email=userinfo["email"],
        )
        db.session.add_all([device, property, contact, config])
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
                        "data": {"type": "device_property", "id": property.id}
                    },
                    "y_property": {
                        "data": {"type": "device_property", "id": property.id}
                    },
                    "z_property": {
                        "data": {"type": "device_property", "id": property.id}
                    },
                    "configuration": {
                        "data": {"type": "configuration", "id": config.id}
                    },
                },
            }
        }
        # Make sure that we have the device mount action for the x properties.
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
        access_headers = create_token()
        # Check if we can delete the device property
        with self.client:
            response = self.client.delete(
                base_url + "/device-properties/" + str(property.id),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
        self.assertEqual(response.status_code, 409)

    def test_validate_property_dynamic_location_action_deletion_without_action(self):
        """Ensure that a property not used by a dynamic_location_action can be deleted."""
        device = Device(short_name="Device 69", is_public=True)
        property = DeviceProperty(
            device=device,
            accuracy=fake.pyfloat(),
            label=fake.pystr(),
            unit_uri=fake.uri(),
            unit_name=fake.pystr(),
            property_uri=fake.uri(),
            property_name="Test property",
        )

        db.session.add_all([device, property])
        db.session.commit()
        db.session.commit()

        access_headers = create_token()
        # Check if we can delete the device property
        with self.client:
            response = self.client.delete(
                base_url + "/device-properties/" + str(property.id),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
        self.assertEqual(response.status_code, 200)
