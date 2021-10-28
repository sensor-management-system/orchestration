"""Tests for the Platform-Permissions."""
import json

from project import base_url
from project.api.models import Contact, User, Platform
from project.api.models.base_model import db
from project.tests.base import BaseTestCase
from project.tests.base import fake
from project.tests.base import generate_token_data, create_token


class TestPlatformPermissions(BaseTestCase):
    """Tests for the platform Permissions."""

    platform_url = base_url + "/platforms"
    object_type = "platform"

    def test_add_public_platform(self):
        """Ensure a new platform can be public."""
        public_platform = Platform(
            id=15,
            short_name=fake.pystr(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        db.session.add(public_platform)
        db.session.commit()

        platform = db.session.query(Platform).filter_by(id=public_platform.id).one()
        self.assertEqual(platform.is_public, True)
        self.assertEqual(platform.is_internal, False)
        self.assertEqual(platform.is_private, False)

    def test_add_private_platform(self):
        """Ensure a new platform can be private."""
        private_platform = Platform(
            id=1,
            short_name=fake.pystr(),
            is_public=False,
            is_private=True,
            is_internal=False,
        )
        db.session.add(private_platform)
        db.session.commit()

        platform = db.session.query(Platform).filter_by(id=private_platform.id).one()
        self.assertEqual(platform.is_public, False)
        self.assertEqual(platform.is_internal, False)
        self.assertEqual(platform.is_private, True)

    def test_add_internal_platform_model(self):
        """Ensure a new platform model can be internal."""
        internal_platform = Platform(
            id=33,
            short_name=fake.pystr(),
            is_internal=True,
            is_public=False,
            is_private=False,
        )
        db.session.add(internal_platform)
        db.session.commit()

        platform = db.session.query(Platform).filter_by(id=internal_platform.id).one()
        self.assertEqual(platform.is_internal, True)
        self.assertEqual(platform.is_public, False)
        self.assertEqual(platform.is_private, False)

    def test_add_internal_platform(self):
        """Ensure a new platform can be added to api and is internal."""
        platform_data = {
            "data": {
                "type": "platform",
                "attributes": {
                    "short_name": fake.pystr(),
                    "is_public": False,
                    "is_internal": True,
                    "is_private": False,
                },
            }
        }
        access_headers = create_token()
        with self.client:
            response = self.client.post(
                self.platform_url,
                data=json.dumps(platform_data),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data["data"]["attributes"]["is_internal"], True)
        self.assertEqual(data["data"]["attributes"]["is_public"], False)
        self.assertEqual(data["data"]["attributes"]["is_private"], False)

    def test_get_as_anonymous_user(self):
        """Ensure anonymous user can only see public objects."""
        public_platform = Platform(
            id=15,
            short_name=fake.pystr(),
            is_private=False,
            is_internal=False,
            is_public=True,
        )

        internal_platform = Platform(
            id=33,
            short_name=fake.pystr(),
            is_public=False,
            is_private=False,
            is_internal=True,
        )
        private_platform = Platform(
            id=1,
            short_name=fake.pystr(),
            is_public=False,
            is_internal=False,
            is_private=True,
        )
        db.session.add_all([public_platform, internal_platform, private_platform])
        db.session.commit()

        response = self.client.get(self.platform_url)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertEqual(data["meta"]["count"], 1)
        self.assertEqual(data["data"][0]["id"], str(public_platform.id))

    def test_get_as_registered_user(self):
        """Ensure that a registered user can see public, internal, and only his own private objects"""
        public_platform = Platform(
            id=15,
            short_name=fake.pystr(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )

        internal_platform = Platform(
            id=33,
            short_name=fake.pystr(),
            is_public=False,
            is_private=False,
            is_internal=True,
        )
        private_platform = Platform(
            id=1,
            short_name=fake.pystr(),
            is_public=False,
            is_internal=False,
            is_private=True,
        )
        private_platform_1 = Platform(
            id=3,
            short_name=fake.pystr(),
            is_public=False,
            is_private=True,
            is_internal=False,
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
            [
                public_platform,
                internal_platform,
                private_platform,
                private_platform_1,
                contact,
                user,
                contact_1,
                user_1,
            ]
        )
        db.session.commit()

        private_platform.created_by_id = user.id
        private_platform_1.created_by_id = user_1.id

        token_data = {
            "sub": user.subject,
            "iss": "SMS unittest",
            "family_name": contact.family_name,
            "given_name": contact.given_name,
            "email": contact.email,
            "aud": "SMS",
        }
        access_headers = create_token(token_data)
        response = self.client.get(self.platform_url, headers=access_headers)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertEqual(data["meta"]["count"], 3)

    def test_add_platform_with_multiple_permission_values(self):
        """Make sure that is a a platform can't have multiple True permission values at the same time"""
        platform_data = {
            "data": {
                "type": "platform",
                "attributes": {
                    "short_name": fake.pystr(),
                    "is_public": True,
                    "is_internal": True,
                    "is_private": False,
                },
            }
        }
        access_headers = create_token()
        with self.client:
            response = self.client.post(
                self.platform_url,
                data=json.dumps(platform_data),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
        self.assertEqual(response.status_code, 409)

        device_data_1 = {
            "data": {
                "type": "platform",
                "attributes": {
                    "short_name": fake.pystr(),
                    "is_public": False,
                    "is_internal": True,
                    "is_private": True,
                },
            }
        }
        access_headers = create_token()
        with self.client:
            response = self.client.post(
                self.platform_url,
                data=json.dumps(device_data_1),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
        self.assertEqual(response.status_code, 409)

        device_data_2 = {
            "data": {
                "type": "platform",
                "attributes": {
                    "short_name": fake.pystr(),
                    "is_public": True,
                    "is_internal": True,
                    "is_private": True,
                },
            }
        }
        access_headers = create_token()
        with self.client:
            response = self.client.post(
                self.platform_url,
                data=json.dumps(device_data_2),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
        self.assertEqual(response.status_code, 409)

    def test_add_groups_ids(self):
        """Make sure that a platform with groups-ids can be created"""
        platform_data = {
            "data": {
                "type": "platform",
                "attributes": {
                    "short_name": fake.pystr(),
                    "is_public": False,
                    "is_internal": True,
                    "is_private": False,
                    "group_ids": [12],
                },
            }
        }
        access_headers = create_token()
        with self.client:
            response = self.client.post(
                self.platform_url,
                data=json.dumps(platform_data),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )

        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 201)

        self.assertEqual(data["data"]["attributes"]["group_ids"], [12])
