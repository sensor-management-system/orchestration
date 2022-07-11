import json

from project import base_url
from project.api.models import Contact, Device
from project.api.models.base_model import db
from project.api.models.contact_role import DeviceContactRole
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


def add_a_device():
    device = Device(short_name=fake.pystr(), manufacturer_name=fake.company(),is_public=True)
    db.session.add(device)
    db.session.commit()
    return device


def add_device_contact_roles():
    contact = add_a_contact()
    device = add_a_device()
    device_contact_roles = DeviceContactRole(
        role_name=fake.pystr(), role_uri=fake.url(), device=device, contact=contact
    )
    db.session.add(device_contact_roles)
    db.session.commit()
    return device_contact_roles


class TestDeviceContactRolesServices(BaseTestCase):
    """
    Test DeviceContactRoles Services
    """

    url = base_url + "/device-contact-roles"
    object_type = "device_contact_role"

    def test_get_device_contact_roles(self):
        """Ensure the /device-contact-roles route behaves correctly."""
        with self.client:
            response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["data"], [])

    def test_get_collection_of_device_contact_roles(self):
        """Ensure device-contact-roles get collection behaves correctly."""

        device_contact_roles = add_device_contact_roles()

        with self.client:
            response = self.client.get(self.url)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            device_contact_roles.role_name, data["data"][0]["attributes"]["role_name"]
        )

    def test_post_a_device_contact_role(self):
        """Ensure post a device_contact_roles behaves correctly."""
        contact = add_a_contact()
        device = add_a_device()
        attributes = {
            "role_name": fake.pystr(),
            "role_uri": fake.url(),
        }
        relationships = {
            "device": {"data": {"id": device.id, "type": "device"}},
            "contact": {"data": {"id": contact.id, "type": "contact"}},
        }
        data = {
            "data": {
                "type": self.object_type,
                "attributes": attributes,
                "relationships": relationships,
            }
        }
        url = f"{self.url}?include=device,contact"
        super().add_object(url=url, data_object=data, object_type=self.object_type)

    def test_update_a_contact_role(self):
        """Ensure update device_contact_roles behaves correctly."""
        device_contact_roles = add_device_contact_roles()
        contact_updated = {
            "data": {
                "type": self.object_type,
                "id": device_contact_roles.id,
                "attributes": {"role_name": "updated",},
            }
        }
        _ = super().update_object(
            url=f"{self.url}/{device_contact_roles.id}",
            data_object=contact_updated,
            object_type=self.object_type,
        )

    def test_delete_a_contact_role(self):
        """Ensure remove device_contact_roles behaves correctly."""

        device_contact_roles = add_device_contact_roles()
        _ = super().delete_object(url=f"{self.url}/{device_contact_roles.id}",)

    def test_http_response_not_found(self):
        """Make sure that the backend responds with 404 HTTP-Code if a resource was not found."""
        url = f"{self.url}/{fake.random_int()}"
        _ = super().http_code_404_when_resource_not_found(url)
