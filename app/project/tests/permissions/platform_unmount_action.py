from project import base_url
from project.api.models import Configuration
from project.api.models import Contact, User
from project.api.models import Platform
from project.api.models import PlatformMountAction
from project.api.models import PlatformUnmountAction
from project.api.models.base_model import db
from project.tests.base import BaseTestCase
from project.tests.base import fake
from project.tests.base import generate_token_data, create_token


def platform_unmount_action_model(public=True, private=False, internal=False):
    platform = Platform(
        short_name="Test platform",
        is_public=public,
        is_private=private,
        is_internal=internal,
    )
    mock_jwt = generate_token_data()
    contact = Contact(
        given_name=mock_jwt["given_name"],
        family_name=mock_jwt["family_name"],
        email=mock_jwt["email"],
    )
    user = User(subject=mock_jwt["sub"], contact=contact)
    configuration = Configuration(
        label=fake.pystr(), is_public=public, is_internal=internal,
    )
    platform_mount_action = PlatformMountAction(
        begin_date=fake.date(),
        description="test mount internal platform action model",
        offset_x=fake.coordinate(),
        offset_y=fake.coordinate(),
        offset_z=fake.coordinate(),
        created_by=user,
        platform=platform,
    )
    platform_mount_action.configuration = configuration
    platform_mount_action.contact = contact
    platform_unmount_action = PlatformUnmountAction(
        end_date=fake.date(),
        description="test unmount platform action model",
        created_by=user,
        platform=platform,
    )
    platform_unmount_action.configuration = configuration
    platform_unmount_action.contact = contact
    db.session.add_all(
        [
            platform,
            contact,
            user,
            configuration,
            platform_mount_action,
            platform_unmount_action,
        ]
    )
    db.session.commit()
    action = (
        db.session.query(PlatformUnmountAction)
        .filter_by(id=platform_unmount_action.id)
        .one()
    )
    return action, platform_unmount_action


class TestMountPlatformPermissions(BaseTestCase):
    """Tests for the Unmount Platform Permissions."""

    url = base_url + "/platform-unmount-actions"
    object_type = "platform_unmount_action"

    def test_unmount_a_public_platform(self):
        """Ensure unmounting a public platform will be listed."""
        action, platform_unmount_action = platform_unmount_action_model()
        self.assertEqual(action.description, platform_unmount_action.description)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 1)

    def test_unmount_an_internal_platform_model(self):
        """Ensure unmounting an internal platform won't be listed unless user provide a valid JWT."""
        action, platform_unmount_action = platform_unmount_action_model(
            public=False, private=False, internal=True
        )
        self.assertEqual(action.description, platform_unmount_action.description)

        # Without a valid JWT -> Will not be listed.
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 0)

        # With a valid JWT
        access_headers = create_token()
        response = self.client.get(self.url, headers=access_headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 1)
