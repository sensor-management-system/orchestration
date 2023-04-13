# SPDX-FileCopyrightText: 2022
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

import json

from project import base_url
from project.api.models import Contact, Platform
from project.api.models.base_model import db
from project.api.models.contact_role import PlatformContactRole
from project.tests.base import BaseTestCase, fake, generate_userinfo_data


def add_a_contact():
    userinfo = generate_userinfo_data()
    contact = Contact(
        given_name=userinfo["given_name"],
        family_name=userinfo["family_name"],
        email=userinfo["email"],
    )
    db.session.add(contact)
    db.session.commit()
    return contact


def add_a_platform():
    platform = Platform(
        short_name=fake.pystr(), manufacturer_name=fake.company(), is_public=True
    )
    db.session.add(platform)
    db.session.commit()
    return platform


def add_platform_contact_role():
    contact = add_a_contact()
    platform = add_a_platform()
    platform_contact_role = PlatformContactRole(
        role_name=fake.pystr(), role_uri=fake.url(), platform=platform, contact=contact
    )
    db.session.add(platform_contact_role)
    db.session.commit()
    return platform_contact_role


class TestPlatformContactRolesServices(BaseTestCase):
    """
    Test PlatformContactRoles Services
    """

    url = base_url + "/platform-contact-roles"
    object_type = "platform_contact_role"

    def test_get_platform_contact_role(self):
        """Ensure the /platform-contact-roles route behaves correctly."""
        with self.client:
            response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["data"], [])

    def test_get_collection_of_platform_contact_role(self):
        """Ensure platform-contact-roles get collection behaves correctly."""

        platform_contact_role = add_platform_contact_role()

        with self.client:
            response = self.client.get(self.url)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            platform_contact_role.role_name, data["data"][0]["attributes"]["role_name"]
        )

    def test_post_a_platform_contact_role(self):
        """Ensure post a platform_contact_role behaves correctly."""
        contact = add_a_contact()
        platform = add_a_platform()
        attributes = {
            "role_name": fake.pystr(),
            "role_uri": fake.url(),
        }
        relationships = {
            "platform": {"data": {"id": platform.id, "type": "platform"}},
            "contact": {"data": {"id": contact.id, "type": "contact"}},
        }
        data = {
            "data": {
                "type": self.object_type,
                "attributes": attributes,
                "relationships": relationships,
            }
        }
        url = f"{self.url}?include=platform,contact"
        result = super().add_object(
            url=url, data_object=data, object_type=self.object_type
        )
        platform_id = result["data"]["relationships"]["platform"]["data"]["id"]
        platform = db.session.query(Platform).filter_by(id=platform_id).first()
        self.assertEqual(platform.update_description, "create;contact")

    def test_update_a_contact_role(self):
        """Ensure update platform_contact_role behaves correctly."""
        platform_contact_role = add_platform_contact_role()
        contact_updated = {
            "data": {
                "type": self.object_type,
                "id": platform_contact_role.id,
                "attributes": {
                    "role_name": "updated",
                },
            }
        }
        result = super().update_object(
            url=f"{self.url}/{platform_contact_role.id}",
            data_object=contact_updated,
            object_type=self.object_type,
        )
        platform_id = result["data"]["relationships"]["platform"]["data"]["id"]
        platform = db.session.query(Platform).filter_by(id=platform_id).first()
        self.assertEqual(platform.update_description, "update;contact")

    def test_delete_a_contact_role(self):
        """Ensure remove platform_contact_role behaves correctly."""

        platform_contact_role = add_platform_contact_role()
        platform_id = platform_contact_role.platform_id
        _ = super().delete_object(
            url=f"{self.url}/{platform_contact_role.id}",
        )
        platform = db.session.query(Platform).filter_by(id=platform_id).first()
        self.assertEqual(platform.update_description, "delete;contact")

    def test_http_response_not_found(self):
        """Make sure that the backend responds with 404 HTTP-Code if a resource was not found."""
        url = f"{self.url}/{fake.random_int()}"
        _ = super().http_code_404_when_resource_not_found(url)

    def test_delete_related_contact(self):
        """Ensure we don't have orphans if we delete the contact."""
        platform_contact_role = add_platform_contact_role()
        platform_contact_role_id = platform_contact_role.id
        self.assertIsNotNone(platform_contact_role_id)
        db.session.delete(platform_contact_role.contact)
        db.session.commit()

        # It should remove the contact role as well.
        reloaded = (
            db.session.query(PlatformContactRole)
            .filter_by(id=platform_contact_role_id)
            .first()
        )
        self.assertIsNone(reloaded)

    def test_delete_related_platform(self):
        """Ensure we don't have orphans if we delete the platform."""
        platform_contact_role = add_platform_contact_role()
        platform_contact_role_id = platform_contact_role.id
        self.assertIsNotNone(platform_contact_role_id)
        db.session.delete(platform_contact_role.platform)
        db.session.commit()

        # It should remove the contact role as well.
        reloaded = (
            db.session.query(PlatformContactRole)
            .filter_by(id=platform_contact_role_id)
            .first()
        )
        self.assertIsNone(reloaded)
