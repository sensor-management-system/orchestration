import json

from project import base_url
from project.api.models import Contact, Configuration
from project.api.models.base_model import db
from project.api.models.contact_role import ConfigurationContactRole
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


def add_a_configuration():
    configuration = Configuration(label=fake.pystr(), is_public=True)
    db.session.add(configuration)
    db.session.commit()
    return configuration


def add_configuration_contact_role():
    contact = add_a_contact()
    configuration = add_a_configuration()
    configuration_contact_role = ConfigurationContactRole(
        role_name=fake.pystr(), role_uri=fake.url(), configuration=configuration, contact=contact
    )
    db.session.add(configuration_contact_role)
    db.session.commit()
    return configuration_contact_role


class TestConfigurationContactRolesServices(BaseTestCase):
    """
    Test ConfigurationContactRoles Services
    """

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
            configuration_contact_role.role_name, data["data"][0]["attributes"]["role_name"]
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
            "configuration": {"data": {"id": configuration.id, "type": "configuration"}},
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
        result= super().add_object(url=url, data_object=data, object_type=self.object_type)
        configuration_id = result["data"]["relationships"]["configuration"]["data"]["id"]
        configuration = db.session.query(Configuration).filter_by(id=configuration_id).first()
        self.assertEqual(configuration.update_description, "create;contact")

    def test_update_a_contact_role(self):
        """Ensure update configuration_contact_role behaves correctly."""
        configuration_contact_role = add_configuration_contact_role()
        contact_updated = {
            "data": {
                "type": self.object_type,
                "id": configuration_contact_role.id,
                "attributes": {"role_name": "updated",},
            }
        }
        result = super().update_object(
            url=f"{self.url}/{configuration_contact_role.id}",
            data_object=contact_updated,
            object_type=self.object_type,
        )
        configuration_id = result["data"]["relationships"]["configuration"]["data"]["id"]
        configuration = db.session.query(Configuration).filter_by(id=configuration_id).first()
        self.assertEqual(configuration.update_description, "update;contact")

    def test_delete_a_contact(self):
        """Ensure remove configuration_contact_role behaves correctly."""

        configuration_contact_role = add_configuration_contact_role()
        configuration_id = configuration_contact_role.configuration_id

        _ = super().delete_object(url=f"{self.url}/{configuration_contact_role.id}",)
        configuration = (
            db.session.query(Configuration).filter_by(id=configuration_id).first()
        )
        self.assertEqual(
            configuration.update_description, "delete;contact"
        )

    def test_http_response_not_found(self):
        """Make sure that the backend responds with 404 HTTP-Code if a resource was not found."""
        url = f"{self.url}/{fake.random_int()}"
        _ = super().http_code_404_when_resource_not_found(url)
