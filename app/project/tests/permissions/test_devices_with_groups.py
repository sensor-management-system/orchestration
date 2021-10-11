"""Tests for the devices."""
import json

from project import base_url
from project.api.models import Contact, User, Device
from project.api.models.base_model import db
from project.tests.base import BaseTestCase
from project.tests.base import generate_token_data, create_token


class TestDeviceService(BaseTestCase):
    """Tests for the Device Service."""

    device_url = base_url + "/devices"
    contact_url = base_url + "/contacts"
    object_type = "device"

    def test_add_public_device(self):
        """Ensure a new device can be public."""
        public_sensor = Device(
            id=15,
            short_name="public device",
        )
        db.session.add(public_sensor)
        db.session.commit()

        public_sensor.is_internal = False
        public_sensor.is_public = True
        public_sensor.is_private = False

        device = db.session.query(Device).filter_by(id=public_sensor.id).one()
        self.assertEqual(device.is_public, True)
        self.assertEqual(device.is_internal, False)
        self.assertEqual(device.is_private, False)

    def test_add_private_device(self):
        """Ensure a new device can be private."""
        private_sensor = Device(
            id=1,
            short_name="private device",
        )
        db.session.add(private_sensor)
        db.session.commit()

        private_sensor.is_internal = False
        private_sensor.is_public = False
        private_sensor.is_private = True

        device = db.session.query(Device).filter_by(id=private_sensor.id).one()
        self.assertEqual(device.is_public, False)
        self.assertEqual(device.is_internal, False)
        self.assertEqual(device.is_private, True)

    def test_add_device(self):
        """Ensure a new device can be added and by default is internal."""
        internal_sensor = Device(
            id=33,
            short_name="internal device",
        )
        db.session.add(internal_sensor)
        db.session.commit()

        device = db.session.query(Device).filter_by(id=internal_sensor.id).one()
        self.assertEqual(device.is_internal, True)
        self.assertEqual(device.is_public, False)
        self.assertEqual(device.is_private, False)

    def test_get_as_anonymous_user(self):
        """Ensure anonymous user can only see public objects."""
        public_sensor = Device(
            id=15,
            short_name="device_short_name test2",
        )

        internal_sensor = Device(
            id=33,
            short_name="device_short_name test2",
        )
        private_sensor = Device(
            id=1,
            short_name="private device",
        )
        db.session.add_all([public_sensor, internal_sensor, private_sensor])
        db.session.commit()

        public_sensor.is_internal = False
        public_sensor.is_public = True
        public_sensor.is_private = False

        private_sensor.is_internal = False
        private_sensor.is_private = True
        private_sensor.is_public = False

        response = self.client.get(self.device_url)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertEqual(data["meta"]["count"], 1)
        self.assertEqual(data["data"][0]["id"], str(public_sensor.id))

    def test_get_as_registered_user(self):
        """Ensure that a registered user can see public, internal, and only his own private objects"""
        public_sensor = Device(
            id=15,
            short_name="device_short_name test2",
        )

        internal_sensor = Device(
            id=33,
            short_name="device_short_name test2",
        )
        private_sensor = Device(
            id=1,
            short_name="private device",
        )
        private_sensor_1 = Device(
            id=3,
            short_name="private device",
        )
        mock_jwt = generate_token_data()
        contact = Contact(
            given_name=mock_jwt["given_name"],
            family_name=mock_jwt["family_name"],
            email=mock_jwt["email"],
        )

        mock_jwt_1 = generate_token_data()
        contact_1 = Contact(
            given_name=mock_jwt_1["given_name"],
            family_name=mock_jwt_1["family_name"],
            email=mock_jwt_1["email"],
        )

        user = User(subject="test_user@test.test", contact=contact)
        user_1 = User(subject="test_user1@test.test", contact=contact_1)
        db.session.add_all(
            [public_sensor, internal_sensor, private_sensor, private_sensor_1, contact, user, contact_1, user_1])
        db.session.commit()

        public_sensor.is_internal = False
        public_sensor.is_public = True
        public_sensor.is_private = False

        private_sensor.is_internal = False
        private_sensor.is_private = True
        private_sensor.is_public = False
        private_sensor.created_by_id = user.id

        private_sensor_1.is_internal = False
        private_sensor_1.is_private = True
        private_sensor_1.is_public = False
        private_sensor_1.created_by_id = user_1.id

        token_data = {"sub": user.subject,
                      "iss": "SMS unittest",
                      "family_name": contact.family_name,
                      "given_name": contact.given_name,
                      "email": contact.email,
                      "aud": "SMS"
                      }
        access_headers = create_token(token_data)
        response = self.client.get(self.device_url, headers=access_headers)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertEqual(data["meta"]["count"], 3)

    # def test_add_device_with_multipel_view_status(self):
    #     """Make Sure that is a an object can't have tow status at the same time"""
    #     device_data = {"data": {"type": "device", "attributes": {
    #         "short_name": "Test device",
    #         "is_public": True,
    #         "is_internal": True,
    #         "is_private": False
    #     }}}
    #     access_headers = create_token()
    #     with self.client:
    #         response = self.client.post(
    #             self.device_url,
    #             data=json.dumps(device_data),
    #             content_type="application/vnd.api+json",
    #             headers=access_headers,
    #         )
    #     data = json.loads(response.data.decode())
    #     print(data)

# TODO
# Write more tests and fix validate methode so that is still works
# even if attribute is None
