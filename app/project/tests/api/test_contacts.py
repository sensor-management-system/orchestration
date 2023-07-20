# SPDX-FileCopyrightText: 2021 - 2023
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Tests for the api for contacts."""

import json
import os
from unittest.mock import patch

from flask import current_app

from project import base_url
from project.api.models import (
    Configuration,
    ConfigurationContactRole,
    Contact,
    Device,
    DeviceContactRole,
    Platform,
    PlatformContactRole,
    User,
)
from project.api.models.base_model import db
from project.extensions.instances import pidinst
from project.tests.base import (
    BaseTestCase,
    create_token,
    fake,
    generate_userinfo_data,
    test_file_path,
)
from project.tests.permissions import create_a_test_contact


class TestContactServices(BaseTestCase):
    """Test class contact services."""

    url = base_url + "/contacts"
    object_type = "contact"
    json_data_url = os.path.join(test_file_path, "drafts", "contacts_test_data.json")

    def test_get_contacts(self):
        """Ensure the /contacts route behaves correctly."""
        with self.client:
            response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["data"], [])

    def test_get_collection_of_contacts(self):
        """Ensure contact get collection behaves correctly."""
        contact = create_a_test_contact()
        with self.client:
            response = self.client.get(self.url)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(contact.email, data["data"][0]["attributes"]["email"])

    def test_post_a_contact(self):
        """Ensure post a contact behaves correctly."""
        self.assertEqual(db.session.query(Contact).count(), 0)
        self.assertEqual(db.session.query(User).count(), 0)

        userinfo = generate_userinfo_data()
        contact = {
            "given_name": fake.first_name(),
            "family_name": fake.last_name(),
            "email": fake.unique.email(),
        }

        data = {"data": {"type": "contact", "attributes": contact}}
        access_headers = create_token(userinfo)
        with self.client:
            response = self.client.post(
                self.url,
                data=json.dumps(data),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
        self.assertEqual(response.status_code, 201)
        contacts = db.session.query(Contact).all()

        # First one is the one we inserted by the token (before the
        # post request logic) for the user.
        # The second one is the entry we created for the new contact.
        self.assertEqual(len(contacts), 2)

        contact_by_system = contacts[0]
        contact_by_request = contacts[1]

        self.assertEqual(contact_by_request.given_name, contact["given_name"])
        self.assertEqual(contact_by_request.family_name, contact["family_name"])
        self.assertEqual(contact_by_request.email, contact["email"])
        # This is an important thing!
        # Here the created_by_id points to the user that created it,
        # so that we can check for the edit permission later.
        self.assertEqual(contact_by_request.created_by_id, contact_by_system.user.id)

        self.assertEqual(contact_by_system.given_name, userinfo["given_name"])
        self.assertEqual(contact_by_system.family_name, userinfo["family_name"])
        # self.assertEqual(contact_by_system.email, userinfo["email"])
        # And the one created by the system itself (by adding the user
        # of the request), we don't have this field.
        self.assertIsNone(contact_by_system.created_by_id)

    def test_update_contact_as_self(self):
        """
        Ensure update contact behaves correctly.

        This is the request with the user that the contact belongs to.
        """
        contact = create_a_test_contact()
        user = User(contact=contact, subject=contact.email)
        db.session.add(user)
        db.session.commit()
        contact_updated = {
            "data": {
                "type": "contact",
                "id": contact.id,
                "attributes": {
                    "given_name": "updated",
                    "organization": "Helmholtz",
                },
            }
        }
        with self.run_requests_as(user):
            with self.client:
                response = self.client.patch(
                    f"{self.url}/{contact.id}",
                    data=json.dumps(contact_updated),
                    content_type="application/vnd.api+json",
                )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["data"]["attributes"]["given_name"], "updated")
        self.assertEqual(
            response.json["data"]["attributes"]["organization"], "Helmholtz"
        )

    def test_update_contact_as_superuser(self):
        """
        Ensure update contact behaves correctly.

        This is the request with the a super user (differnt from contact).
        """
        contact = create_a_test_contact()
        super_user_contact = create_a_test_contact()
        super_user = User(
            contact=super_user_contact,
            subject=super_user_contact.email,
            is_superuser=True,
        )
        db.session.add(super_user)
        db.session.commit()
        contact_updated = {
            "data": {
                "type": "contact",
                "id": contact.id,
                "attributes": {
                    "given_name": "updated",
                },
            }
        }
        with self.run_requests_as(super_user):
            with self.client:
                response = self.client.patch(
                    f"{self.url}/{contact.id}",
                    data=json.dumps(contact_updated),
                    content_type="application/vnd.api+json",
                )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["data"]["attributes"]["given_name"], "updated")

    def test_update_contact_as_creator(self):
        """
        Ensure update contact behaves correctly.

        This is the request with the a differnt user that created the contact.
        """
        contact = create_a_test_contact()
        other_contact = create_a_test_contact()
        user = User(contact=other_contact, subject=other_contact.email)
        contact.created_by = user
        db.session.add_all([user, contact])
        db.session.commit()
        contact_updated = {
            "data": {
                "type": "contact",
                "id": contact.id,
                "attributes": {
                    "given_name": "updated",
                },
            }
        }
        with self.run_requests_as(user):
            with self.client:
                response = self.client.patch(
                    f"{self.url}/{contact.id}",
                    data=json.dumps(contact_updated),
                    content_type="application/vnd.api+json",
                )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["data"]["attributes"]["given_name"], "updated")

    def test_update_contact_not_as_creator(self):
        """
        Ensure update contact behaves correctly.

        This is the request with the a differnt user that created the contact.
        """
        contact = create_a_test_contact()
        first_other_contact = create_a_test_contact()
        second_other_contact = create_a_test_contact()
        first_user = User(
            contact=first_other_contact, subject=first_other_contact.email
        )
        second_user = User(
            contact=second_other_contact, subject=second_other_contact.email
        )
        contact.created_by = first_user
        db.session.add_all(
            [first_user, second_user, first_other_contact, second_user, contact]
        )
        db.session.commit()
        contact_updated = {
            "data": {
                "type": "contact",
                "id": contact.id,
                "attributes": {
                    "given_name": "updated",
                },
            }
        }
        with self.run_requests_as(second_user):
            with self.client:
                response = self.client.patch(
                    f"{self.url}/{contact.id}",
                    data=json.dumps(contact_updated),
                    content_type="application/vnd.api+json",
                )
        self.assertEqual(response.status_code, 403)

    def test_update_contact_system_contact(self):
        """
        Ensure update contact behaves correctly.

        This is the request with the a differnt user for an automatically
        created contact.
        """
        contact = create_a_test_contact()
        other_contact = create_a_test_contact()
        user = User(contact=other_contact, subject=other_contact.email)
        db.session.add_all([user, other_contact])
        db.session.commit()
        contact_updated = {
            "data": {
                "type": "contact",
                "id": contact.id,
                "attributes": {
                    "given_name": "updated",
                },
            }
        }
        with self.run_requests_as(user):
            with self.client:
                response = self.client.patch(
                    f"{self.url}/{contact.id}",
                    data=json.dumps(contact_updated),
                    content_type="application/vnd.api+json",
                )
        self.assertEqual(response.status_code, 403)

    def test_delete_contact_as_superuser(self):
        """Ensure remove contact behaves correctly for a superuser."""
        contact = create_a_test_contact()
        super_user_contact = create_a_test_contact()
        super_user = User(
            contact=super_user_contact,
            subject=super_user_contact.email,
            is_superuser=True,
        )
        db.session.add(super_user)
        db.session.commit()

        with self.run_requests_as(super_user):
            with self.client:
                response = self.client.delete(
                    f"{self.url}/{contact.id}",
                    content_type="application/vnd.api+json",
                )
        self.assertEqual(response.status_code, 200)

    def test_delete_contact_as_creator(self):
        """Ensure remove contact behaves correctly for a creator of that contact."""
        contact = create_a_test_contact()
        other_contact = create_a_test_contact()
        user = User(contact=other_contact, subject=other_contact.email)
        contact.created_by = user
        db.session.add_all([user, contact])
        db.session.commit()

        with self.run_requests_as(user):
            with self.client:
                response = self.client.delete(
                    f"{self.url}/{contact.id}",
                    content_type="application/vnd.api+json",
                )
        self.assertEqual(response.status_code, 200)

    def test_delete_contact_not_as_creator(self):
        """Ensure a normal user can't remove a contact."""
        contact = create_a_test_contact()
        other_contact = create_a_test_contact()
        user = User(contact=other_contact, subject=other_contact.email)
        db.session.add_all([user])
        db.session.commit()

        with self.run_requests_as(user):
            with self.client:
                response = self.client.delete(
                    f"{self.url}/{contact.id}",
                    content_type="application/vnd.api+json",
                )
        self.assertEqual(response.status_code, 403)

    def test_http_response_not_found(self):
        """Make sure that the backend responds with 404 HTTP-Code if a resource was not found."""
        url = f"{self.url}/{fake.random_int()}"
        _ = super().http_code_404_when_resource_not_found(url)

    def test_post_duplicated_orcids(self):
        """Make sure we can't add a orcid for a second time."""
        userinfo = generate_userinfo_data()
        contact_data1 = {
            "given_name": fake.first_name(),
            "family_name": fake.last_name(),
            "email": fake.unique.email(),
            "orcid": "0000-0000-0000-0001",
        }
        contact_data2 = {
            "given_name": fake.first_name(),
            "family_name": fake.last_name(),
            "email": fake.unique.email(),
            "orcid": "0000-0000-0000-0001",
        }

        data = {"data": {"type": "contact", "attributes": contact_data1}}
        access_headers = create_token(userinfo)
        with self.client:
            response = self.client.post(
                self.url,
                data=json.dumps(data),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
        self.assertEqual(response.status_code, 201)
        # And for the second one
        data = {"data": {"type": "contact", "attributes": contact_data2}}
        access_headers = create_token(userinfo)
        with self.client:
            response = self.client.post(
                self.url,
                data=json.dumps(data),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
        self.assertEqual(response.status_code, 409)

    def test_post_duplicated_email(self):
        """Make sure we can't add an email for a second time."""
        userinfo = generate_userinfo_data()
        contact_data1 = {
            "given_name": fake.first_name(),
            "family_name": fake.last_name(),
            "email": "fake@unique.email",
        }
        contact_data2 = {
            "given_name": fake.first_name(),
            "family_name": fake.last_name(),
            "email": "fake@unique.email",
        }

        data = {"data": {"type": "contact", "attributes": contact_data1}}
        access_headers = create_token(userinfo)
        with self.client:
            response = self.client.post(
                self.url,
                data=json.dumps(data),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
        self.assertEqual(response.status_code, 201)
        # And for the second one
        data = {"data": {"type": "contact", "attributes": contact_data2}}
        access_headers = create_token(userinfo)
        with self.client:
            response = self.client.post(
                self.url,
                data=json.dumps(data),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
        self.assertEqual(response.status_code, 409)

    def test_patch_to_duplicated_orcids(self):
        """Make sure we can't insert an orcid for a second time by patch."""
        contact1 = Contact(
            given_name=fake.first_name(),
            family_name=fake.last_name(),
            email=fake.unique.email(),
            orcid="0000-0000-0000-0001",
        )
        contact2 = Contact(
            given_name=fake.first_name(),
            family_name=fake.last_name(),
            email=fake.unique.email(),
        )
        super_user = User(contact=contact1, is_superuser=True, subject=contact1.email)
        db.session.add_all([contact1, contact2, super_user])
        db.session.commit()
        contact_data = {
            "orcid": "0000-0000-0000-0001",
        }

        # We try to update the orcid of the second contact.
        # But when it is equal to an existing one, we should see the error.
        data = {
            "data": {"type": "contact", "id": contact2.id, "attributes": contact_data}
        }
        with self.client:
            with self.run_requests_as(super_user):
                response = self.client.patch(
                    f"{self.url}/{contact2.id}",
                    data=json.dumps(data),
                    content_type="application/vnd.api+json",
                )
        self.assertEqual(response.status_code, 409)

    def test_patch_to_duplicated_emails(self):
        """Make sure we can't insert an email for a second time by patch."""
        contact1 = Contact(
            given_name=fake.first_name(),
            family_name=fake.last_name(),
            email=fake.unique.email(),
        )
        contact2 = Contact(
            given_name=fake.first_name(),
            family_name=fake.last_name(),
            email=fake.unique.email(),
        )
        super_user = User(contact=contact1, is_superuser=True, subject=contact1.email)
        db.session.add_all([contact1, contact2, super_user])
        db.session.commit()
        contact_data = {
            "email": contact1.email,
        }

        # We try to update the mail of the second contact.
        # But when it is equal to an existing one, we should see the error.
        data = {
            "data": {"type": "contact", "id": contact2.id, "attributes": contact_data}
        }
        with self.client:
            with self.run_requests_as(super_user):
                response = self.client.patch(
                    f"{self.url}/{contact2.id}",
                    data=json.dumps(data),
                    content_type="application/vnd.api+json",
                )
        self.assertEqual(response.status_code, 409)

    def test_contact_creation_with_organization(self):
        """Ensure that we try to set the organization for new contacts."""
        user_data = {
            "given_name": "Test",
            "family_name": "User",
            "email": "test.user@gfz-potsdam.de",
            "sub": "tuser@gfz-potsdam.de",
        }
        token = create_token(user_data)
        self.assertEqual(0, db.session.query(Contact).count())

        self.client.get(
            base_url + "/devices",
            headers=token,
            content_type="application/vnd.api+json",
        )
        self.assertEqual(1, db.session.query(Contact).count())

        contact = db.session.query(Contact).first()

        self.assertEqual(contact.given_name, "Test")
        self.assertEqual(contact.family_name, "User")
        self.assertEqual(contact.email, "test.user@gfz-potsdam.de")
        # And we want to make sure that we can set the organization if
        # we have it in our list.
        self.assertEqual(
            contact.organization,
            "Helmholtz Centre Potsdam - German Research Centre for Geosciences GFZ",
        )

    def test_contact_creation_without_known_organization(self):
        """Ensure that we still add the contact, even if the organzation is unknow."""
        user_data = {
            "given_name": "Test",
            "family_name": "User",
            "email": "test.user@abcdef.foo",
            "sub": "tuser@abcdef.foo",
        }
        token = create_token(user_data)
        self.assertEqual(0, db.session.query(Contact).count())

        self.client.get(
            base_url + "/devices",
            headers=token,
            content_type="application/vnd.api+json",
        )
        self.assertEqual(1, db.session.query(Contact).count())

        contact = db.session.query(Contact).first()

        self.assertEqual(contact.given_name, "Test")
        self.assertEqual(contact.family_name, "User")
        self.assertEqual(contact.email, "test.user@abcdef.foo")
        self.assertIsNone(contact.organization)

    def test_update_external_metadata_for_device_after_patch_of_contact(self):
        """Ensure we trigger the update of external metadata if we update a contact with a device."""
        contact = Contact(
            given_name="Test", family_name="User", email="test.user@localhost"
        )
        super_user = User(contact=contact, subject=contact.email, is_superuser=True)
        device = Device(short_name="Test device", b2inst_record_id="42")
        device_contact_role = DeviceContactRole(
            device=device,
            contact=contact,
            role_name="Owner",
            role_uri="https://localhost/cv/roles/1",
        )
        db.session.add_all([contact, super_user, device, device_contact_role])
        db.session.commit()

        payload = {
            "data": {
                "type": "contact",
                "id": str(contact.id),
                "attributes": {
                    "family_name": "married",
                },
            }
        }
        current_app.config.update({"B2INST_TOKEN": "123"})
        with self.run_requests_as(super_user):
            with patch.object(
                pidinst, "update_external_metadata"
            ) as update_external_metadata:
                update_external_metadata.return_value = None
                resp = self.client.patch(
                    f"{self.url}/{contact.id}",
                    data=json.dumps(payload),
                    content_type="application/vnd.api+json",
                )
                update_external_metadata.assert_called_once()
                self.assertEqual(
                    update_external_metadata.call_args.args[0].id, device.id
                )
            self.assertEqual(resp.status_code, 200)

    def test_update_external_metadata_for_platform_after_patch_of_contact(self):
        """Ensure we trigger the update of external metadata if we update a contact with a platform."""
        contact = Contact(
            given_name="Test", family_name="User", email="test.user@localhost"
        )
        super_user = User(contact=contact, subject=contact.email, is_superuser=True)
        platform = Platform(short_name="Test platform", b2inst_record_id="42")
        platform_contact_role = PlatformContactRole(
            platform=platform,
            contact=contact,
            role_name="Owner",
            role_uri="https://localhost/cv/roles/1",
        )
        db.session.add_all([contact, super_user, platform, platform_contact_role])
        db.session.commit()

        payload = {
            "data": {
                "type": "contact",
                "id": str(contact.id),
                "attributes": {
                    "family_name": "married",
                },
            }
        }
        current_app.config.update({"B2INST_TOKEN": "123"})
        with self.run_requests_as(super_user):
            with patch.object(
                pidinst, "update_external_metadata"
            ) as update_external_metadata:
                update_external_metadata.return_value = None
                resp = self.client.patch(
                    f"{self.url}/{contact.id}",
                    data=json.dumps(payload),
                    content_type="application/vnd.api+json",
                )
                update_external_metadata.assert_called_once()
                self.assertEqual(
                    update_external_metadata.call_args.args[0].id, platform.id
                )
            self.assertEqual(resp.status_code, 200)

    def test_update_external_metadata_for_configuration_after_patch_of_contact(self):
        """Ensure we trigger the update of external metadata if we update a contact with a configuration."""
        contact = Contact(
            given_name="Test", family_name="User", email="test.user@localhost"
        )
        super_user = User(contact=contact, subject=contact.email, is_superuser=True)
        configuration = Configuration(label="Test configuration", b2inst_record_id="42")
        configuration_contact_role = ConfigurationContactRole(
            configuration=configuration,
            contact=contact,
            role_name="Owner",
            role_uri="https://localhost/cv/roles/1",
        )
        db.session.add_all(
            [contact, super_user, configuration, configuration_contact_role]
        )
        db.session.commit()

        payload = {
            "data": {
                "type": "contact",
                "id": str(contact.id),
                "attributes": {
                    "family_name": "married",
                },
            }
        }
        current_app.config.update({"B2INST_TOKEN": "123"})
        with self.run_requests_as(super_user):
            with patch.object(
                pidinst, "update_external_metadata"
            ) as update_external_metadata:
                update_external_metadata.return_value = None
                resp = self.client.patch(
                    f"{self.url}/{contact.id}",
                    data=json.dumps(payload),
                    content_type="application/vnd.api+json",
                )
                update_external_metadata.assert_called_once()
                self.assertEqual(
                    update_external_metadata.call_args.args[0].id, configuration.id
                )
            self.assertEqual(resp.status_code, 200)

    def test_update_external_metadata_for_device_after_delete_of_contact(self):
        """Ensure we trigger the update of external metadata if we delete a contact with a device."""
        contact1 = Contact(
            given_name="Test1", family_name="User", email="test1.user@localhost"
        )
        contact2 = Contact(
            given_name="Test2", family_name="User", email="test2.user@localhost"
        )
        super_user = User(contact=contact2, subject=contact2.email, is_superuser=True)
        device = Device(short_name="Test device", b2inst_record_id="42")
        device_contact_role = DeviceContactRole(
            device=device,
            contact=contact1,
            role_name="Owner",
            role_uri="https://localhost/cv/roles/1",
        )
        db.session.add_all(
            [contact1, contact2, super_user, device, device_contact_role]
        )
        db.session.commit()

        current_app.config.update({"B2INST_TOKEN": "123"})
        with self.run_requests_as(super_user):
            with patch.object(
                pidinst, "update_external_metadata"
            ) as update_external_metadata:
                update_external_metadata.return_value = None
                resp = self.client.delete(
                    f"{self.url}/{contact1.id}",
                )
                update_external_metadata.assert_called_once()
                self.assertEqual(
                    update_external_metadata.call_args.args[0].id, device.id
                )
            self.assertEqual(resp.status_code, 200)

    def test_update_external_metadata_for_platform_after_delete_of_contact(self):
        """Ensure we trigger the update of external metadata if we delete a contact with a platform."""
        contact1 = Contact(
            given_name="Test1", family_name="User", email="test1.user@localhost"
        )
        contact2 = Contact(
            given_name="Test2", family_name="User", email="test2.user@localhost"
        )
        super_user = User(contact=contact2, subject=contact2.email, is_superuser=True)
        platform = Platform(short_name="Test platform", b2inst_record_id="42")
        platform_contact_role = PlatformContactRole(
            platform=platform,
            contact=contact1,
            role_name="Owner",
            role_uri="https://localhost/cv/roles/1",
        )
        db.session.add_all(
            [contact1, contact2, super_user, platform, platform_contact_role]
        )
        db.session.commit()

        current_app.config.update({"B2INST_TOKEN": "123"})
        with self.run_requests_as(super_user):
            with patch.object(
                pidinst, "update_external_metadata"
            ) as update_external_metadata:
                update_external_metadata.return_value = None
                resp = self.client.delete(
                    f"{self.url}/{contact1.id}",
                )
                update_external_metadata.assert_called_once()
                self.assertEqual(
                    update_external_metadata.call_args.args[0].id, platform.id
                )
            self.assertEqual(resp.status_code, 200)

    def test_update_external_metadata_for_configuration_after_delete_of_contact(self):
        """Ensure we trigger the update of external metadata if we delete a contact with a configuration."""
        contact1 = Contact(
            given_name="Test1", family_name="User", email="test1.user@localhost"
        )
        contact2 = Contact(
            given_name="Test2", family_name="User", email="test2.user@localhost"
        )
        super_user = User(contact=contact2, subject=contact2.email, is_superuser=True)
        configuration = Configuration(label="Test configuration", b2inst_record_id="42")
        configuration_contact_role = ConfigurationContactRole(
            configuration=configuration,
            contact=contact1,
            role_name="Owner",
            role_uri="https://localhost/cv/roles/1",
        )
        db.session.add_all(
            [contact1, contact2, super_user, configuration, configuration_contact_role]
        )
        db.session.commit()

        current_app.config.update({"B2INST_TOKEN": "123"})
        with self.run_requests_as(super_user):
            with patch.object(
                pidinst, "update_external_metadata"
            ) as update_external_metadata:
                update_external_metadata.return_value = None
                resp = self.client.delete(
                    f"{self.url}/{contact1.id}",
                )
                update_external_metadata.assert_called_once()
                self.assertEqual(
                    update_external_metadata.call_args.args[0].id, configuration.id
                )
            self.assertEqual(resp.status_code, 200)
