import json

from project import base_url
from project.api.models import Contact, Platform
from project.api.models.base_model import db
from project.api.models.contact_role import PlatformContactRole
from project.tests.base import (
    BaseTestCase,
    generate_userinfo_data,
    fake,
)


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
    platform = Platform(short_name=fake.pystr())
    db.session.add(platform)
    db.session.commit()
    return platform


def add_platform_contact_roles():
    contact = add_a_contact()
    platform = add_a_platform()
    platform_contact_roles = PlatformContactRole(
        role_name=fake.pystr(), role_uri=fake.url(), platform=platform, contact=contact
    )
    db.session.add(platform_contact_roles)
    db.session.commit()
    return platform_contact_roles


class TestPlatformContactRolesServices(BaseTestCase):
    """
    Test PlatformContactRoles Services
    """

    url = base_url + "/platform-contact-roles"
    object_type = "platform_contact_role"

    def test_get_platform_contact_roles(self):
        """Ensure the /platform-contact-roles route behaves correctly."""
        with self.client:
            response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["data"], [])

    def test_get_collection_of_platform_contact_roles(self):
        """Ensure platform-contact-roles get collection behaves correctly."""

        platform_contact_roles = add_platform_contact_roles()

        with self.client:
            response = self.client.get(self.url)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            platform_contact_roles.role_name, data["data"][0]["attributes"]["role_name"]
        )

    def test_post_a_platform_contact_roles(self):
        """Ensure post a platform_contact_roles behaves correctly."""
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
        super().add_object(url=url, data_object=data, object_type=self.object_type)

    def test_update_a_contact(self):
        """Ensure update platform_contact_roles behaves correctly."""
        platform_contact_roles = add_platform_contact_roles()
        contact_updated = {
            "data": {
                "type": self.object_type,
                "id": platform_contact_roles.id,
                "attributes": {"role_name": "updated",},
            }
        }
        _ = super().update_object(
            url=f"{self.url}/{platform_contact_roles.id}",
            data_object=contact_updated,
            object_type=self.object_type,
        )

    def test_delete_a_contacts(self):
        """Ensure remove platform_contact_roles behaves correctly."""

        platform_contact_roles = add_platform_contact_roles()
        _ = super().delete_object(url=f"{self.url}/{platform_contact_roles.id}",)

    def test_http_response_not_found(self):
        """Make sure that the backend responds with 404 HTTP-Code if a resource was not found."""
        url = f"{self.url}/{fake.random_int()}"
        _ = super().http_code_404_when_resource_not_found(url)
