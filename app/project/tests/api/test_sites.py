"""Tests for the api & permissions for the sites."""

from unittest.mock import patch

from project import base_url
from project.api.models import Configuration, Contact, Site, SiteContactRole, User
from project.api.models.base_model import db
from project.extensions.idl.models.user_account import UserAccount
from project.extensions.instances import idl
from project.tests.base import BaseTestCase


class TestSiteApi(BaseTestCase):
    """Tests for the sites."""

    sites_url = base_url + "/sites"

    def setUp(self):
        """Set up some data for the tests."""
        super().setUp()
        self.normal_contact = Contact(
            given_name="normal", family_name="contact", email="normal.contact@somewhere"
        )
        self.super_contact = Contact(
            given_name="super", family_name="contact", email="super.contact@somewhere"
        )
        self.normal_user = User(
            contact=self.normal_contact,
            subject=self.normal_contact.email,
        )
        self.super_user = User(
            contact=self.super_contact,
            subject=self.super_contact.email,
            is_superuser=True,
        )
        self.internal_site = Site(
            label="internal",
            is_internal=True,
            is_public=False,
            created_by=self.normal_user,
            updated_by=self.normal_user,
        )
        self.public_site = Site(
            label="public",
            is_internal=False,
            is_public=True,
            created_by=self.normal_user,
            updated_by=self.normal_user,
        )

        db.session.add_all(
            [
                self.internal_site,
                self.public_site,
                self.normal_contact,
                self.normal_user,
                self.super_contact,
                self.super_user,
            ]
        )
        db.session.commit()

    def test_query_list_anonymous(self):
        """Ensure anoymous user can't query internal sites."""
        resp = self.client.get(self.sites_url)
        self.assertEqual(resp.status_code, 200)
        data_list = resp.json["data"]
        self.assertEqual(len(data_list), 1)
        self.assertTrue(data_list[0]["attributes"]["is_public"])
        self.assertFalse(data_list[0]["attributes"]["is_internal"])

    def test_query_list_user(self):
        """Ensure normal user can query internal and public sites."""
        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.sites_url)
        self.assertEqual(resp.status_code, 200)
        data_list = resp.json["data"]
        self.assertEqual(len(data_list), 2)
        self.assertTrue(data_list[0]["attributes"]["is_internal"])
        self.assertFalse(data_list[0]["attributes"]["is_public"])
        self.assertTrue(data_list[1]["attributes"]["is_public"])
        self.assertFalse(data_list[1]["attributes"]["is_internal"])

    def test_query_list_no_archived_by_default(self):
        """Ensure that we don't return archvied sites normally."""
        self.public_site.archived = True
        db.session.add(self.public_site)
        db.session.commit()

        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.sites_url)
        self.assertEqual(resp.status_code, 200)
        data_list = resp.json["data"]
        self.assertEqual(len(data_list), 1)
        self.assertTrue(data_list[0]["attributes"]["is_internal"])
        self.assertFalse(data_list[0]["attributes"]["is_public"])

    def test_query_list_include_archived_if_requested(self):
        """Ensure that we can include archived sites."""
        self.public_site.archived = True
        db.session.add(self.public_site)
        db.session.commit()

        with self.run_requests_as(self.normal_user):
            resp = self.client.get(self.sites_url + "?hide_archived=false")
        self.assertEqual(resp.status_code, 200)
        data_list = resp.json["data"]
        self.assertEqual(len(data_list), 2)
        self.assertTrue(data_list[0]["attributes"]["is_internal"])
        self.assertFalse(data_list[0]["attributes"]["is_public"])
        self.assertTrue(data_list[1]["attributes"]["is_public"])
        self.assertFalse(data_list[1]["attributes"]["is_internal"])
        self.assertTrue(data_list[1]["attributes"]["archived"])

    def test_post_without_default_visibility(self):
        """Ensure that internal is the visibility if nothing else is given."""
        payload = {"data": {"type": "site", "attributes": {"label": "some new site"}}}

        with self.run_requests_as(self.super_user):
            resp = self.client.post(
                self.sites_url,
                json=payload,
                headers={"Content-Type": "application/vnd.api+json"},
            )
        self.assertEqual(resp.status_code, 201)
        data_entry = resp.json["data"]
        self.assertTrue(data_entry["attributes"]["is_internal"])
        self.assertFalse(data_entry["attributes"]["is_public"])

    def test_post_public_visibility(self):
        """Ensure that we stay with public visibility if given."""
        payload = {
            "data": {
                "type": "site",
                "attributes": {
                    "label": "some new site",
                    "is_public": True,
                },
            }
        }

        with self.run_requests_as(self.super_user):
            resp = self.client.post(
                self.sites_url,
                json=payload,
                headers={"Content-Type": "application/vnd.api+json"},
            )
        self.assertEqual(resp.status_code, 201)
        data_entry = resp.json["data"]
        self.assertTrue(data_entry["attributes"]["is_public"])
        self.assertFalse(data_entry["attributes"]["is_internal"])

    def test_post_without_user(self):
        """Ensure we need a user to create sites."""
        payload = {
            "data": {
                "type": "site",
                "attributes": {
                    "label": "some new site",
                    "is_public": True,
                },
            }
        }

        resp = self.client.post(
            self.sites_url,
            json=payload,
            headers={"Content-Type": "application/vnd.api+json"},
        )
        self.assertEqual(resp.status_code, 401)

    def test_after_post_has_created_by_id(self):
        """Ensure that we save the id of the user that created the site."""
        payload = {
            "data": {
                "type": "site",
                "attributes": {
                    "label": "some new site",
                },
            }
        }

        with self.run_requests_as(self.super_user):
            resp = self.client.post(
                self.sites_url,
                json=payload,
                headers={"Content-Type": "application/vnd.api+json"},
            )
        self.assertEqual(resp.status_code, 201)
        data_entry = resp.json["data"]
        self.assertEqual(
            data_entry["relationships"]["created_by"]["data"]["id"],
            str(self.super_user.id),
        )

    def test_after_post_has_one_contact(self):
        """Ensure we add the user as owner contact for the site."""
        payload = {
            "data": {
                "type": "site",
                "attributes": {
                    "label": "some new site",
                },
            }
        }

        with self.run_requests_as(self.super_user):
            resp = self.client.post(
                self.sites_url,
                json=payload,
                headers={"Content-Type": "application/vnd.api+json"},
            )
        self.assertEqual(resp.status_code, 201)
        data_entry = resp.json["data"]
        new_id = data_entry["id"]

        contact_roles = (
            db.session.query(SiteContactRole).filter_by(site_id=new_id).all()
        )
        self.assertEqual(len(contact_roles), 1)
        self.assertEqual(contact_roles[0].contact, self.super_contact)
        self.assertEqual(contact_roles[0].role_name, "Owner")

    def test_after_post_updated_at_and_by(self):
        """Ensure that we set the updated by id & updated at fields also after post."""
        payload = {
            "data": {
                "type": "site",
                "attributes": {
                    "label": "some new site",
                },
            }
        }

        with self.run_requests_as(self.super_user):
            resp = self.client.post(
                self.sites_url,
                json=payload,
                headers={"Content-Type": "application/vnd.api+json"},
            )
        self.assertEqual(resp.status_code, 201)
        data_entry = resp.json["data"]
        new_id = data_entry["id"]
        new_site = db.session.query(Site).filter_by(id=new_id).first()

        self.assertEqual(new_site.updated_by, self.super_user)
        self.assertTrue(new_site.updated_at >= new_site.created_at)

    def test_after_post_update_description(self):
        """Ensure that we set the update description after post."""
        payload = {
            "data": {
                "type": "site",
                "attributes": {
                    "label": "some new site",
                },
            }
        }

        with self.run_requests_as(self.super_user):
            resp = self.client.post(
                self.sites_url,
                json=payload,
                headers={"Content-Type": "application/vnd.api+json"},
            )
        self.assertEqual(resp.status_code, 201)
        data_entry = resp.json["data"]
        new_id = data_entry["id"]
        new_site = db.session.query(Site).filter_by(id=new_id).first()

        self.assertEqual(new_site.update_description, "create;basic data")

    def test_get_one_404(self):
        """Ensure we get a 404 response if we try to get a site that doesn't exist."""
        resp = self.client.get(self.sites_url + "/9999999999999")
        self.assertEqual(resp.status_code, 404)

    def test_get_one_internal_anonymous(self):
        """Ensure we can't get an internal site without login."""
        resp = self.client.get(f"{self.sites_url}/{self.internal_site.id}")
        self.assertIn(resp.status_code, [401, 403])

    def test_get_one_internal_user(self):
        """Ensure we can get an internal site with login."""
        with self.run_requests_as(self.normal_user):
            resp = self.client.get(f"{self.sites_url}/{self.internal_site.id}")
            self.assertEqual(resp.status_code, 200)

    def test_get_one_public_anonymous(self):
        """Ensure we can get an public site without login."""
        resp = self.client.get(f"{self.sites_url}/{self.public_site.id}")
        self.assertEqual(resp.status_code, 200)

    def test_get_one_schema(self):
        """Ensure we can have all the fields we want to have in the response."""
        resp = self.client.get(f"{self.sites_url}/{self.public_site.id}")
        self.assertEqual(resp.status_code, 200)
        data_entry = resp.json["data"]

        attribute_fields = [
            "label",
            "description",
            "geometry",
            "epsg_code",
            "is_internal",
            "is_public",
            "group_ids",
            "archived",
            "street",
            "street_number",
            "city",
            "zip_code",
            "country",
            "building",
            "room",
            "created_at",
            "updated_at",
        ]
        for field in attribute_fields:
            self.assertIn(field, data_entry["attributes"].keys())

        relationships = {
            "created_by": dict,
            "updated_by": dict,
        }
        for field, type_ in relationships.items():
            self.assertIn(field, data_entry["relationships"].keys())
            self.assertEqual(type(data_entry["relationships"][field]["data"]), type_)

    def test_patch_anonymous(self):
        """Ensure we don't allow patch requests for anonymous users."""
        payload = {
            "id": self.public_site.id,
            "type": "public",
            "attributes": {"description": "Some more useful desciption"},
        }

        resp = self.client.patch(
            f"{self.sites_url}/{self.public_site.id}", json=payload
        )
        self.assertEqual(resp.status_code, 401)

    def test_patch_archived(self):
        """Ensure we don't allow to patch archived sites."""
        self.public_site.archived = True
        db.session.add(self.public_site)
        db.session.commit()

        payload = {
            "data": {
                "id": self.public_site.id,
                "type": "site",
                "attributes": {"description": "Some more useful desciption"},
            }
        }

        with self.run_requests_as(self.normal_user):
            resp = self.client.patch(
                f"{self.sites_url}/{self.public_site.id}",
                json=payload,
                headers={"Content-Type": "application/vnd.api+json"},
            )
        self.assertEqual(resp.status_code, 403)

    def test_patch_super_user(self):
        """Ensure we allow super users to patch sites."""
        description = "Some more useful description"
        payload = {
            "data": {
                "id": self.public_site.id,
                "type": "site",
                "attributes": {"description": description},
            }
        }

        with self.run_requests_as(self.super_user):
            resp = self.client.patch(
                f"{self.sites_url}/{self.public_site.id}",
                json=payload,
                headers={"Content-Type": "application/vnd.api+json"},
            )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json["data"]["attributes"]["description"], description)

    def test_patch_group_admin(self):
        """Ensure we allow group admins to patch sites."""
        self.public_site.group_ids = ["123"]
        db.session.add(self.public_site)
        db.session.commit()
        description = "Some more useful description"
        payload = {
            "data": {
                "id": self.public_site.id,
                "type": "site",
                "attributes": {"description": description},
            }
        }

        with self.run_requests_as(self.normal_user):
            with patch.object(idl, "get_all_permission_groups_for_a_user") as idl_mock:
                idl_mock.return_value = UserAccount(
                    id=1,
                    username="mock",
                    administrated_permission_groups=["123"],
                    membered_permission_groups=[],
                )
                resp = self.client.patch(
                    f"{self.sites_url}/{self.public_site.id}",
                    json=payload,
                    headers={"Content-Type": "application/vnd.api+json"},
                )
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(
                resp.json["data"]["attributes"]["description"], description
            )

    def test_patch_group_member(self):
        """Ensure we allow group members to patch sites."""
        self.public_site.group_ids = ["123"]
        db.session.add(self.public_site)
        db.session.commit()
        description = "Some more useful description"
        payload = {
            "data": {
                "id": self.public_site.id,
                "type": "site",
                "attributes": {"description": description},
            }
        }

        with self.run_requests_as(self.normal_user):
            with patch.object(idl, "get_all_permission_groups_for_a_user") as idl_mock:
                idl_mock.return_value = UserAccount(
                    id=1,
                    username="mock",
                    administrated_permission_groups=[],
                    membered_permission_groups=["123"],
                )
                resp = self.client.patch(
                    f"{self.sites_url}/{self.public_site.id}",
                    json=payload,
                    headers={"Content-Type": "application/vnd.api+json"},
                )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json["data"]["attributes"]["description"], description)

    def test_patch_no_group_member(self):
        """Ensure we don't allow non group members to patch sites."""
        self.public_site.group_ids = ["123"]
        db.session.add(self.public_site)
        db.session.commit()
        description = "Some more useful description"
        payload = {
            "data": {
                "id": self.public_site.id,
                "type": "site",
                "attributes": {"description": description},
            }
        }

        with self.run_requests_as(self.normal_user):
            with patch.object(idl, "get_all_permission_groups_for_a_user") as idl_mock:
                idl_mock.return_value = UserAccount(
                    id=1,
                    username="mock",
                    administrated_permission_groups=[],
                    membered_permission_groups=[],
                )
                resp = self.client.patch(
                    f"{self.sites_url}/{self.public_site.id}",
                    json=payload,
                    headers={"Content-Type": "application/vnd.api+json"},
                )
        self.assertEqual(resp.status_code, 403)

    def test_patch_updated_by_id_is_set(self):
        """Ensure we set the user id for the update."""
        description = "Some more useful description"
        payload = {
            "data": {
                "id": self.public_site.id,
                "type": "site",
                "attributes": {"description": description},
            }
        }

        with self.run_requests_as(self.super_user):
            resp = self.client.patch(
                f"{self.sites_url}/{self.public_site.id}",
                json=payload,
                headers={"Content-Type": "application/vnd.api+json"},
            )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(
            resp.json["data"]["relationships"]["updated_by"]["data"]["id"],
            str(self.super_user.id),
        )

    def test_patch_update_description(self):
        """Ensure we update the update description when patching."""
        self.public_site.update_description = "random data"
        db.session.add(self.public_site)
        db.session.commit()

        description = "Some more useful description"
        payload = {
            "data": {
                "id": self.public_site.id,
                "type": "site",
                "attributes": {"description": description},
            }
        }

        with self.run_requests_as(self.super_user):
            resp = self.client.patch(
                f"{self.sites_url}/{self.public_site.id}",
                json=payload,
                headers={"Content-Type": "application/vnd.api+json"},
            )
        self.assertEqual(resp.status_code, 200)
        reloaded_site = db.session.query(Site).filter_by(id=self.public_site.id).first()
        self.assertEqual(reloaded_site.update_description, "update;basic data")

    def test_delete_anonymous(self):
        """Ensure we don't allow deletion without login."""
        resp = self.client.delete(f"{self.sites_url}/{self.public_site.id}")
        self.assertEqual(resp.status_code, 401)

    def test_delete_by_super_user(self):
        """Ensure we allow deletion for super users."""
        site_id = self.public_site.id
        with self.run_requests_as(self.super_user):
            resp = self.client.delete(f"{self.sites_url}/{site_id}")
        self.assertEqual(resp.status_code, 200)

        self.assertEqual(db.session.query(Site).filter_by(id=site_id).first(), None)

    def test_delete_by_normal_user(self):
        """Ensure we don't allow deletion for normal users."""
        with self.run_requests_as(self.normal_user):
            resp = self.client.delete(f"{self.sites_url}/{self.public_site.id}")
        self.assertEqual(resp.status_code, 403)

    def test_delete_with_associated_configurations(self):
        """Ensure we can't delete a site when there is a configuration associated."""
        configuration = Configuration(
            label="abc", is_public=True, is_internal=False, site=self.public_site
        )
        db.session.add(configuration)
        db.session.commit()
        site_id = self.public_site.id
        with self.run_requests_as(self.super_user):
            resp = self.client.delete(f"{self.sites_url}/{site_id}")
        self.assertEqual(resp.status_code, 409)

    def test_post_site_type(self):
        """Ensure that we can post the site type."""
        payload = {
            "data": {
                "type": "site",
                "attributes": {
                    "label": "some new site",
                    "is_public": True,
                    "site_type_name": "Example site",
                    "site_type_uri": "https://cv/sites/123",
                },
            }
        }

        with self.run_requests_as(self.super_user):
            resp = self.client.post(
                self.sites_url,
                json=payload,
                headers={"Content-Type": "application/vnd.api+json"},
            )
        self.assertEqual(resp.status_code, 201)
        data_entry = resp.json["data"]
        self.assertEqual(data_entry["attributes"]["site_type_name"], "Example site")
        self.assertEqual(
            data_entry["attributes"]["site_type_uri"], "https://cv/sites/123"
        )

    def test_post_site_usage(self):
        """Ensure that we can post the site usage."""
        payload = {
            "data": {
                "type": "site",
                "attributes": {
                    "label": "some new site",
                    "is_public": True,
                    "site_usage_name": "Example usage",
                    "site_usage_uri": "https://cv/usages/123",
                },
            }
        }

        with self.run_requests_as(self.super_user):
            resp = self.client.post(
                self.sites_url,
                json=payload,
                headers={"Content-Type": "application/vnd.api+json"},
            )
        self.assertEqual(resp.status_code, 201)
        data_entry = resp.json["data"]
        self.assertEqual(data_entry["attributes"]["site_usage_name"], "Example usage")
        self.assertEqual(
            data_entry["attributes"]["site_usage_uri"], "https://cv/usages/123"
        )

    def test_post_elevation(self):
        """Ensure that we can post the elevation."""
        payload = {
            "data": {
                "type": "site",
                "attributes": {
                    "label": "some new site",
                    "is_public": True,
                    "elevation_datum_name": "mean sea level (Atlantic)",
                    "elevation_datum_uri": "https://cv/elevation/45",
                    "elevation": 42.0,
                },
            }
        }

        with self.run_requests_as(self.super_user):
            resp = self.client.post(
                self.sites_url,
                json=payload,
                headers={"Content-Type": "application/vnd.api+json"},
            )
        self.assertEqual(resp.status_code, 201)
        data_entry = resp.json["data"]
        self.assertEqual(
            data_entry["attributes"]["elevation_datum_name"],
            "mean sea level (Atlantic)",
        )
        self.assertEqual(
            data_entry["attributes"]["elevation_datum_uri"], "https://cv/elevation/45"
        )
        self.assertEqual(data_entry["attributes"]["elevation"], 42.0)
