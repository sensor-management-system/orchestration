"""Tests for the Configuration-Permissions."""
import json

from project import base_url
from project.api.models import Contact, User, Configuration
from project.api.models.base_model import db
from project.tests.base import BaseTestCase
from project.tests.base import fake
from project.tests.base import generate_token_data, create_token


class TestConfigurationPermissions(BaseTestCase):
    """Tests for the configuration Permissions."""

    configuration_url = base_url + "/configurations"
    object_type = "configuration"

    def test_add_public_configuration(self):
        """Ensure a new configuration can be public."""
        public_config = Configuration(
            id=15, label="public configuration", is_public=True, is_internal=False,
        )
        db.session.add(public_config)
        db.session.commit()

        configuration = (
            db.session.query(Configuration).filter_by(id=public_config.id).one()
        )
        self.assertEqual(configuration.is_public, True)
        self.assertEqual(configuration.is_internal, False)

    def test_add_configuration_model(self):
        """Ensure a new configuration model can be internal."""
        internal_config = Configuration(
            id=33, label="internal configuration", is_internal=True, is_public=False,
        )
        db.session.add(internal_config)
        db.session.commit()

        configuration = (
            db.session.query(Configuration).filter_by(id=internal_config.id).one()
        )
        self.assertEqual(configuration.is_internal, True)
        self.assertEqual(configuration.is_public, False)

    def test_add_configuration(self):
        """Ensure a new configuration can be added to api and is internal."""
        configuration_data = {
            "data": {
                "type": "configuration",
                "attributes": {
                    "label": fake.pystr(),
                    "is_public": False,
                    "is_internal": True,
                },
            }
        }
        access_headers = create_token()
        with self.client:
            response = self.client.post(
                self.configuration_url,
                data=json.dumps(configuration_data),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data["data"]["attributes"]["is_internal"], True)
        self.assertEqual(data["data"]["attributes"]["is_public"], False)

    def test_get_all_as_anonymous_user(self):
        """Ensure anonymous user can only see public objects."""
        public_config = Configuration(
            id=15, label=fake.pystr(), is_internal=False, is_public=True
        )

        internal_config = Configuration(
            id=33, label=fake.pystr(), is_public=False, is_internal=True
        )

        db.session.add_all([public_config, internal_config])
        db.session.commit()

        response = self.client.get(self.configuration_url)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertEqual(data["meta"]["count"], 1)
        self.assertEqual(data["data"][0]["id"], str(public_config.id))

    def test_get_an_internal_config__as_anonymous_user(self):
        """Ensure anonymous user can't access an internal configuration."""
        internal_config = Configuration(
            label=fake.pystr(), is_public=False, is_internal=True
        )

        db.session.add(internal_config)
        db.session.commit()
        url = f"{self.configuration_url}/{internal_config.id}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_get_as_registered_user(self):
        """Ensure that a registered user can see public, internal, and only his own private objects"""
        public_config = Configuration(
            id=15, label=fake.pystr(), is_public=True, is_internal=False,
        )

        internal_config = Configuration(
            id=33, label=fake.pystr(), is_public=False, is_internal=True,
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
            [public_config, internal_config, contact, user, contact_1, user_1]
        )
        db.session.commit()

        token_data = {
            "sub": user.subject,
            "iss": "SMS unittest",
            "family_name": contact.family_name,
            "given_name": contact.given_name,
            "email": contact.email,
            "aud": "SMS",
        }
        access_headers = create_token(token_data)
        response = self.client.get(self.configuration_url, headers=access_headers)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertEqual(data["meta"]["count"], 2)

    def test_add_configuration_with_multiple_true_permission_values(self):
        """Make sure that a configuration can't have multiple True permission values at the same time"""
        configuration_data = {
            "data": {
                "type": "configuration",
                "attributes": {
                    "label": fake.pystr(),
                    "is_public": True,
                    "is_internal": True,
                },
            }
        }
        access_headers = create_token()
        with self.client:
            response = self.client.post(
                self.configuration_url,
                data=json.dumps(configuration_data),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
        self.assertEqual(response.status_code, 409)

    def test_add_groups_ids(self):
        """Make sure that a configuration with groups-ids can be created"""
        device_data = {
            "data": {
                "type": "configuration",
                "attributes": {
                    "label": fake.pystr(),
                    "is_public": False,
                    "is_internal": True,
                    "group_ids": [12],
                },
            }
        }
        access_headers = create_token()
        with self.client:
            response = self.client.post(
                self.configuration_url,
                data=json.dumps(device_data),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )

        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 201)

        self.assertEqual(data["data"]["attributes"]["group_ids"], [12])
