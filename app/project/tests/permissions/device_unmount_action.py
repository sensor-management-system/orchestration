"""Tests for the devices."""

from project import base_url
from project.api.models import Configuration
from project.api.models import Contact, User, Device
from project.api.models import DeviceMountAction
from project.api.models import DeviceUnmountAction
from project.api.models import Platform
from project.api.models.base_model import db
from project.tests.base import BaseTestCase
from project.tests.base import fake
from project.tests.base import generate_userinfo_data, create_token


def device_unmount_action_model(public=True, private=False, internal=False):
    device = Device(
        short_name=fake.pystr(),
        is_public=public,
        is_private=private,
        is_internal=internal,
    )
    parent_platform = Platform(
        short_name="device parent platform",
        is_public=public,
        is_private=private,
        is_internal=internal,
    )
    mock_jwt = generate_userinfo_data()
    contact = Contact(
        given_name=mock_jwt["given_name"],
        family_name=mock_jwt["family_name"],
        email=mock_jwt["email"],
    )
    user = User(subject=mock_jwt["sub"], contact=contact)
    configuration = Configuration(
        label=fake.pystr(), is_public=public, is_internal=internal,
    )
    device_mount_action = DeviceMountAction(
        begin_date=fake.date(),
        description="test mount device action model",
        offset_x=fake.coordinate(),
        offset_y=fake.coordinate(),
        offset_z=fake.coordinate(),
        created_by=user,
        device=device,
    )
    device_mount_action.parent_platform = parent_platform
    device_mount_action.configuration = configuration
    device_mount_action.contact = contact
    unmount_device_action = DeviceUnmountAction(
        end_date=fake.date(),
        description="test unmount device action model",
        created_by=user,
        device=device,
    )
    unmount_device_action.configuration = configuration
    unmount_device_action.contact = contact
    db.session.add_all(
        [
            device,
            parent_platform,
            contact,
            user,
            configuration,
            device_mount_action,
            unmount_device_action,
        ]
    )
    db.session.commit()
    action = (
        db.session.query(DeviceUnmountAction)
        .filter_by(id=unmount_device_action.id)
        .one()
    )
    return action, unmount_device_action


class TestUnmountDevicePermissions(BaseTestCase):
    """Tests for the Mount Device Permissions."""

    url = base_url + "/device-unmount-actions"
    object_type = "device_unmount_action"

    def test_unmount_a_public_device(self):
        """Ensure unmounting a public device will be listed."""
        action, unmount_device_action = device_unmount_action_model()
        self.assertEqual(action.description, unmount_device_action.description)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 1)

    def test_unmount_an_internal_device(self):
        """Ensure unmounting an internal device won't be listed unless user provide a valid JWT."""
        action, unmount_device_action = device_unmount_action_model(
            public=False, private=False, internal=True
        )
        self.assertEqual(action.description, unmount_device_action.description)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 0)

        # With a valid JWT
        access_headers = create_token()
        response = self.client.get(self.url, headers=access_headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 1)
