# SPDX-FileCopyrightText: 2021 - 2024
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Tests for the api for device calibration attachments."""

import json

from project import base_url, db
from project.api.models import (
    Contact,
    Device,
    DeviceAttachment,
    DeviceCalibrationAction,
    User,
)
from project.extensions.instances import mqtt
from project.tests.base import BaseTestCase, Fixtures, fake
from project.tests.models.test_device_calibration_attachment_model import (
    add_device_calibration_attachment,
)

fixtures = Fixtures()


@fixtures.register("contact1", scope=lambda: db.session)
def create_contact1():
    """Create a single contact so that it can be used within the tests."""
    result = Contact(
        given_name="first", family_name="contact", email="first.contact@localhost"
    )
    db.session.add(result)
    db.session.commit()
    return result


@fixtures.register("user1", scope=lambda: db.session)
@fixtures.use(["contact1"])
def create_user1(contact1):
    """Create a normal user to use it in the tests."""
    result = User(contact=contact1, subject=contact1.email)
    db.session.add(result)
    db.session.commit()
    return result


class TestDeviceCalibrationAttachment(BaseTestCase):
    """Tests for the DeviceCalibrationAttachment endpoints."""

    url = base_url + "/device-calibration-attachments"
    object_type = "device_calibration_attachment"

    def test_get_generic_device_action_attachment(self):
        """Ensure the GET /device_calibration_attachment route reachable."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        # no data yet
        self.assertEqual(response.json["data"], [])

    def test_get_device_calibration_action_attachment_collection(self):
        """Test retrieve a collection of DeviceCalibrationAttachment objects."""
        device_calibration_attachment = add_device_calibration_attachment()
        device = device_calibration_attachment.action.device
        device.is_public = True
        device.is_internal = False

        db.session.add(device)
        db.session.commit()

        with self.client:
            response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        # should be only one
        self.assertEqual(response.json["meta"]["count"], 1)
        self.assertEqual(
            response.json["data"][0]["id"], str(device_calibration_attachment.id)
        )

    def test_get_device_calibration_action_attachment_collection_internal(self):
        """Ensure we don't show entries of internal devices without user."""
        device_calibration_attachment = add_device_calibration_attachment()
        device = device_calibration_attachment.action.device
        self.assertTrue(device.is_internal)

        db.session.add(device)
        db.session.commit()

        with self.client:
            response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        # Should be empty as we don't give a user => internal device is not
        # visible anymore.
        self.assertEqual(response.json["meta"]["count"], 0)

    @fixtures.use
    def test_post_generic_device_action_attachment(self, contact1, user1):
        """Create DeviceCalibrationAttachment."""
        device = Device(
            short_name="Device 1",
            manufacturer_name=fake.company(),
            is_public=False,
            is_private=False,
            is_internal=True,
        )

        db.session.add(device)
        db.session.commit()
        attachment = DeviceAttachment(
            label=fake.pystr(), url=fake.url(), device_id=device.id
        )
        device_calibration_action = DeviceCalibrationAction(
            description="Test DeviceCalibrationAction",
            current_calibration_date=fake.date(),
            next_calibration_date=fake.date(),
            device=device,
            contact=contact1,
        )
        db.session.add_all([device, attachment, device_calibration_action])
        db.session.commit()
        data = {
            "data": {
                "type": self.object_type,
                "attributes": {},
                "relationships": {
                    "action": {
                        "data": {
                            "type": "device_calibration_action",
                            "id": device_calibration_action.id,
                        }
                    },
                    "attachment": {
                        "data": {"type": "device_attachment", "id": attachment.id}
                    },
                },
            }
        }
        with self.run_requests_as(user1):
            _ = super().add_object(
                url=f"{self.url}?include=action,attachment",
                data_object=data,
                object_type=self.object_type,
            )
        # And ensure that we trigger the mqtt.
        mqtt.publish.assert_called_once()
        call_args = mqtt.publish.call_args[0]

        self.expect(call_args[0]).to_equal("sms/post-device-calibration-attachment")
        notification_data = json.loads(call_args[1])["data"]
        self.expect(notification_data["type"]).to_equal("device_calibration_attachment")
        self.expect(
            notification_data["relationships"]["action"]["data"]["id"]
        ).to_equal(str(device_calibration_action.id))
        self.expect(str).of(notification_data["id"]).to_match(r"\d+")

    @fixtures.use
    def test_update_generic_device_action_attachment(self, user1):
        """Update DeviceCalibrationAttachment."""
        device_calibration_attachment = add_device_calibration_attachment()
        device = Device(
            short_name="Device new",
            manufacturer_name=fake.company(),
            is_public=False,
            is_private=False,
            is_internal=True,
        )
        db.session.add(device)
        db.session.commit()
        attachment = DeviceAttachment(
            label=fake.pystr(), url=fake.url(), device_id=device.id
        )
        db.session.add_all([attachment])
        db.session.commit()
        data = {
            "data": {
                "type": self.object_type,
                "id": device_calibration_attachment.id,
                "attributes": {},
                "relationships": {
                    "attachment": {
                        "data": {"type": "device_attachment", "id": attachment.id}
                    },
                },
            }
        }
        with self.run_requests_as(user1):
            _ = super().update_object(
                url=f"{self.url}/{device_calibration_attachment.id}?include=attachment",
                data_object=data,
                object_type=self.object_type,
            )
        # And ensure that we trigger the mqtt.
        mqtt.publish.assert_called_once()
        call_args = mqtt.publish.call_args[0]

        self.expect(call_args[0]).to_equal("sms/patch-device-calibration-attachment")
        notification_data = json.loads(call_args[1])["data"]
        self.expect(notification_data["type"]).to_equal("device_calibration_attachment")
        self.expect(
            notification_data["relationships"]["attachment"]["data"]["id"]
        ).to_equal(str(attachment.id))
        self.expect(
            notification_data["relationships"]["action"]["data"]["id"]
        ).to_equal(str(device_calibration_attachment.action_id))

    def test_delete_generic_device_action_attachment(self):
        """Delete DeviceCalibrationAttachment."""
        dca = add_device_calibration_attachment()
        _ = super().delete_object(
            url=f"{self.url}/{dca.id}",
        )
        # And ensure that we trigger the mqtt.
        mqtt.publish.assert_called_once()
        call_args = mqtt.publish.call_args[0]

        self.expect(call_args[0]).to_equal("sms/delete-device-calibration-attachment")
        self.expect(json.loads).of(call_args[1]).to_equal(
            {"data": {"type": "device_calibration_attachment", "id": str(dca.id)}}
        )

    def test_http_response_not_found(self):
        """Make sure that the backend responds with 404 HTTP-Code if a resource was not found."""
        url = f"{self.url}/{fake.random_int()}"
        _ = super().http_code_404_when_resource_not_found(url)
