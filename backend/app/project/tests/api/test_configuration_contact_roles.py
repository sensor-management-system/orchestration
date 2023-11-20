# SPDX-FileCopyrightText: 2022 - 2023
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Test classes for the configuration contact roles."""

import json
from unittest.mock import patch

from flask import current_app

from project import base_url
from project.api.models import Configuration, ConfigurationContactRole, Contact, User
from project.api.models.base_model import db
from project.extensions.instances import pidinst
from project.tests.base import BaseTestCase, fake, generate_userinfo_data


def add_a_contact():
    """Add a test contact."""
    userinfo = generate_userinfo_data()
    contact = Contact(
        given_name=userinfo["given_name"],
        family_name=userinfo["family_name"],
        email=userinfo["email"],
    )
    db.session.add(contact)
    db.session.commit()
    return contact


def add_a_configuration():
    """Add a test configuration."""
    configuration = Configuration(label=fake.pystr(), is_public=True)
    db.session.add(configuration)
    db.session.commit()
    return configuration


def add_configuration_contact_role():
    """Add a test configuration contact role."""
    contact = add_a_contact()
    configuration = add_a_configuration()
    configuration_contact_role = ConfigurationContactRole(
        role_name=fake.pystr(),
        role_uri=fake.url(),
        configuration=configuration,
        contact=contact,
    )
    db.session.add(configuration_contact_role)
    db.session.commit()
    return configuration_contact_role


class TestConfigurationContactRolesServices(BaseTestCase):
    """Test configurationContactRoles services."""

    url = base_url + "/configuration-contact-roles"
    object_type = "configuration_contact_role"

    def test_get_configuration_contact_role(self):
        """Ensure the /configuration-contact-roles route behaves correctly."""
        with self.client:
            response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["data"], [])

    def test_get_collection_of_configuration_contact_role(self):
        """Ensure configuration-contact-roles get collection behaves correctly."""
        configuration_contact_role = add_configuration_contact_role()

        with self.client:
            response = self.client.get(self.url)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            configuration_contact_role.role_name,
            data["data"][0]["attributes"]["role_name"],
        )

    def test_post_a_configuration_contact_role(self):
        """Ensure post a configuration_contact_role behaves correctly."""
        contact = add_a_contact()
        configuration = add_a_configuration()
        attributes = {
            "role_name": fake.pystr(),
            "role_uri": fake.url(),
        }
        relationships = {
            "configuration": {
                "data": {"id": configuration.id, "type": "configuration"}
            },
            "contact": {"data": {"id": contact.id, "type": "contact"}},
        }
        data = {
            "data": {
                "type": self.object_type,
                "attributes": attributes,
                "relationships": relationships,
            }
        }
        url = f"{self.url}?include=configuration,contact"
        result = super().add_object(
            url=url, data_object=data, object_type=self.object_type
        )
        configuration_id = result["data"]["relationships"]["configuration"]["data"][
            "id"
        ]
        configuration = (
            db.session.query(Configuration).filter_by(id=configuration_id).first()
        )
        self.assertEqual(configuration.update_description, "create;contact")

    def test_update_a_contact_role(self):
        """Ensure update configuration_contact_role behaves correctly."""
        configuration_contact_role = add_configuration_contact_role()
        contact_updated = {
            "data": {
                "type": self.object_type,
                "id": configuration_contact_role.id,
                "attributes": {
                    "role_name": "updated",
                },
            }
        }
        result = super().update_object(
            url=f"{self.url}/{configuration_contact_role.id}",
            data_object=contact_updated,
            object_type=self.object_type,
        )
        configuration_id = result["data"]["relationships"]["configuration"]["data"][
            "id"
        ]
        configuration = (
            db.session.query(Configuration).filter_by(id=configuration_id).first()
        )
        self.assertEqual(configuration.update_description, "update;contact")

    def test_delete_a_contact(self):
        """Ensure remove configuration_contact_role behaves correctly."""
        configuration_contact_role = add_configuration_contact_role()
        configuration_id = configuration_contact_role.configuration_id

        _ = super().delete_object(
            url=f"{self.url}/{configuration_contact_role.id}",
        )
        configuration = (
            db.session.query(Configuration).filter_by(id=configuration_id).first()
        )
        self.assertEqual(configuration.update_description, "delete;contact")

    def test_http_response_not_found(self):
        """Make sure that the backend responds with 404 HTTP-Code if a resource was not found."""
        url = f"{self.url}/{fake.random_int()}"
        _ = super().http_code_404_when_resource_not_found(url)

    def test_delete_related_contact(self):
        """Ensure we don't have orphans if we delete the contact."""
        configuration_contact_role = add_configuration_contact_role()
        configuration_contact_role_id = configuration_contact_role.id
        self.assertIsNotNone(configuration_contact_role_id)
        db.session.delete(configuration_contact_role.contact)
        db.session.commit()

        # It should remove the contact role as well.
        reloaded = (
            db.session.query(ConfigurationContactRole)
            .filter_by(id=configuration_contact_role_id)
            .first()
        )
        self.assertIsNone(reloaded)

    def test_delete_related_configuration(self):
        """Ensure we don't have orphans if we delete the configuration."""
        configuration_contact_role = add_configuration_contact_role()
        configuration_contact_role_id = configuration_contact_role.id
        self.assertIsNotNone(configuration_contact_role_id)
        db.session.delete(configuration_contact_role.configuration)
        db.session.commit()

        # It should remove the contact role as well.
        reloaded = (
            db.session.query(ConfigurationContactRole)
            .filter_by(id=configuration_contact_role_id)
            .first()
        )
        self.assertIsNone(reloaded)

    def test_update_external_metadata_after_post_of_contact_role(self):
        """Ensure we ask the system to update external metadata after posting the contact role."""
        contact = add_a_contact()
        configuration = add_a_configuration()
        configuration.b2inst_record_id = "42"
        db.session.add(configuration)
        db.session.commit()

        attributes = {
            "role_name": fake.pystr(),
            "role_uri": fake.url(),
        }
        relationships = {
            "configuration": {
                "data": {"id": configuration.id, "type": "configuration"}
            },
            "contact": {"data": {"id": contact.id, "type": "contact"}},
        }
        data = {
            "data": {
                "type": self.object_type,
                "attributes": attributes,
                "relationships": relationships,
            }
        }
        url = f"{self.url}?include=configuration,contact"
        current_app.config.update({"B2INST_TOKEN": "123"})

        with patch.object(
            pidinst, "update_external_metadata"
        ) as update_external_metadata:
            update_external_metadata.return_value = None
            super().add_object(url=url, data_object=data, object_type=self.object_type)
            update_external_metadata.assert_called_once()
            self.assertEqual(
                update_external_metadata.call_args.args[0].id, configuration.id
            )

    def test_update_external_metadata_after_patch_of_contact_role(self):
        """Ensure we ask the system to update external metadata after patching the contact role."""
        configuration_contact_role = add_configuration_contact_role()
        contact_updated = {
            "data": {
                "type": self.object_type,
                "id": configuration_contact_role.id,
                "attributes": {
                    "role_name": "updated",
                },
            }
        }
        configuration = configuration_contact_role.configuration
        configuration.b2inst_record_id = "42"
        db.session.add(configuration)
        db.session.commit()

        current_app.config.update({"B2INST_TOKEN": "123"})

        with patch.object(
            pidinst, "update_external_metadata"
        ) as update_external_metadata:
            update_external_metadata.return_value = None
            super().update_object(
                url=f"{self.url}/{configuration_contact_role.id}",
                data_object=contact_updated,
                object_type=self.object_type,
            )
            update_external_metadata.assert_called_once()
            self.assertEqual(
                update_external_metadata.call_args.args[0].id, configuration.id
            )

    def test_update_external_metadata_after_delete_of_contact_role(self):
        """Ensure we ask the system to update external metadata after deleting the contact role."""
        configuration_contact_role = add_configuration_contact_role()
        configuration = configuration_contact_role.configuration
        configuration.b2inst_record_id = "42"
        db.session.add(configuration)
        db.session.commit()

        current_app.config.update({"B2INST_TOKEN": "123"})

        with patch.object(
            pidinst, "update_external_metadata"
        ) as update_external_metadata:
            update_external_metadata.return_value = None
            super().delete_object(
                url=f"{self.url}/{configuration_contact_role.id}",
            )
            update_external_metadata.assert_called_once()
            self.assertEqual(
                update_external_metadata.call_args.args[0].id, configuration.id
            )

    def test_ensure_unique_constraint_on_post(self):
        """Ensure that we have a unique constraint for role, configuration and contact."""
        contact = Contact(
            given_name="A", family_name="Contact", email="a.contact@localhost"
        )
        super_user = User(contact=contact, subject=contact.email, is_superuser=True)

        configuration = Configuration(label="test configuration")
        role_name = "Owner"
        role_uri = "https://cv/roles/1"

        contact_role = ConfigurationContactRole(
            contact=contact,
            configuration=configuration,
            role_name=role_name,
            role_uri=role_uri,
        )

        db.session.add_all([contact, super_user, configuration, contact_role])
        db.session.commit()

        payload = {
            "data": {
                "type": "configuration_contact_role",
                "attributes": {
                    "role_name": role_name,
                    "role_uri": role_uri,
                },
                "relationships": {
                    "configuration": {
                        "data": {
                            "id": configuration.id,
                            "type": "configuration",
                        },
                    },
                    "contact": {"data": {"id": contact.id, "type": "contact"}},
                },
            }
        }

        with self.run_requests_as(super_user):
            response = self.client.post(
                self.url,
                json=payload,
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 409)

    def test_ensure_unique_constraint_on_patch(self):
        """Ensure that we have a unique constraint for role, configuration and contact also for changes."""
        contact = Contact(
            given_name="A", family_name="Contact", email="a.contact@localhost"
        )
        super_user = User(contact=contact, subject=contact.email, is_superuser=True)

        configuration = Configuration(label="test configuration")
        role_name1 = "Owner"
        role_uri1 = "https://cv/roles/1"

        contact_role1 = ConfigurationContactRole(
            contact=contact,
            configuration=configuration,
            role_name=role_name1,
            role_uri=role_uri1,
        )

        role_name2 = "PI"
        role_uri2 = "https://cv/roles/2"

        contact_role2 = ConfigurationContactRole(
            contact=contact,
            configuration=configuration,
            role_name=role_name2,
            role_uri=role_uri2,
        )

        db.session.add_all(
            [contact, super_user, configuration, contact_role1, contact_role2]
        )
        db.session.commit()

        # It is not possible to add this for the very same configuration, contact & role.
        payload = {
            "data": {
                "type": "configuration_contact_role",
                "id": contact_role2.id,
                "attributes": {
                    "role_name": role_name1,
                    "role_uri": role_uri1,
                },
                "relationships": {
                    "configuration": {
                        "data": {
                            "id": configuration.id,
                            "type": "configuration",
                        },
                    },
                    "contact": {"data": {"id": contact.id, "type": "contact"}},
                },
            }
        }

        with self.run_requests_as(super_user):
            response = self.client.patch(
                f"{self.url}/{contact_role2.id}",
                json=payload,
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 409)
