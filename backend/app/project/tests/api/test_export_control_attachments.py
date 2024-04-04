# SPDX-FileCopyrightText: 2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Tests for the export control attachment endpoints."""

import json
from unittest.mock import patch

from project import base_url
from project.api.models import (
    Contact,
    Device,
    ExportControl,
    ExportControlAttachment,
    ManufacturerModel,
    Platform,
    User,
)
from project.api.models.base_model import db
from project.tests.base import BaseTestCase, Fixtures
from project.views import download_files

fixtures = Fixtures()


@fixtures.register("contact1", scope=lambda: db.session)
def create_contact1():
    """Create a single contact so that it can be used within the tests."""
    result = Contact(
        given_name="first", family_name="contact", email="first.contact@localhost"
    )
    db.session.add(result)
    db.session.commit()
    return result


@fixtures.register("export_control_contact", scope=lambda: db.session)
def create_export_control_contact():
    """Create a contact that can be used to make an export control user."""
    result = Contact(
        given_name="export", family_name="contact", email="super.contact@localhost"
    )
    db.session.add(result)
    db.session.commit()
    return result


@fixtures.register("super_user_contact", scope=lambda: db.session)
def create_super_user_contact():
    """Create a contact that can be used to make a super user."""
    result = Contact(
        given_name="super", family_name="contact", email="super.contact@localhost"
    )
    db.session.add(result)
    db.session.commit()
    return result


@fixtures.register("user1", scope=lambda: db.session)
@fixtures.use(["contact1"])
def create_user1(contact1):
    """Create a normal user to use it in the tests."""
    result = User(contact=contact1, subject=contact1.email)
    db.session.add(result)
    db.session.commit()
    return result


@fixtures.register("export_control_user", scope=lambda: db.session)
@fixtures.use(["export_control_contact"])
def create_export_control_user(export_control_contact):
    """Create an export control user to use it in the tests."""
    result = User(
        contact=export_control_contact,
        subject=export_control_contact.email,
        is_export_control=True,
    )
    db.session.add(result)
    db.session.commit()
    return result


@fixtures.register("super_user", scope=lambda: db.session)
@fixtures.use(["super_user_contact"])
def create_super_user(super_user_contact):
    """Create super user to use it in the tests."""
    result = User(
        contact=super_user_contact, subject=super_user_contact.email, is_superuser=True
    )
    db.session.add(result)
    db.session.commit()
    return result


@fixtures.register("manufacturer_model1", scope=lambda: db.session)
def create_manufacturer_model1():
    """Create the manufacturer model1."""
    result = ManufacturerModel(manufacturer_name="TRUEBENER GmbH", model="SMT 100")
    db.session.add(result)
    db.session.commit()
    return result


@fixtures.register("public_attachment_of_manufacturer_model1", scope=lambda: db.session)
@fixtures.use(["manufacturer_model1"])
def create_public_attachment_of_manufacturer_model1(manufacturer_model1):
    """Create a public visible attachment for the manufacturer model1."""
    result = ExportControlAttachment(
        manufacturer_model=manufacturer_model1,
        url="https://gfz-potsdam.de",
        label="GFZ",
        is_export_control_only=False,
    )
    db.session.add(result)
    db.session.commit()
    return result


@fixtures.register(
    "internal_attachment_of_manufacturer_model1", scope=lambda: db.session
)
@fixtures.use(["manufacturer_model1"])
def create_internal_attachment_of_manufacturer_model1(manufacturer_model1):
    """Create a non public visible attachment for the manufacturer model1."""
    result = ExportControlAttachment(
        manufacturer_model=manufacturer_model1,
        url="https://gfz-potsdam.de",
        label="GFZ",
        is_export_control_only=True,
    )
    db.session.add(result)
    db.session.commit()
    return result


@fixtures.register("manufacturer_model2", scope=lambda: db.session)
def create_manufacturer_model2():
    """Create the manufacturer model2."""
    result = ManufacturerModel(manufacturer_name="Campbell", model="CRS 1000")
    db.session.add(result)
    db.session.commit()
    return result


@fixtures.register("public_attachment_of_manufacturer_model2", scope=lambda: db.session)
@fixtures.use(["manufacturer_model2"])
def create_public_attachment_of_manufacturer_model2(manufacturer_model2):
    """Create a public visible attachment for the manufacturer model2."""
    result = ExportControlAttachment(
        manufacturer_model=manufacturer_model2,
        url="https://ufz.de",
        label="UFZ",
        is_export_control_only=False,
    )
    db.session.add(result)
    db.session.commit()
    return result


class TestExportControlAttachments(BaseTestCase):
    """Test class for the export control attachments."""

    url = base_url + "/export-control-attachments"

    def test_get_list_empty(self):
        """Ensure we can get the empty list."""
        response = self.client.get(self.url)
        self.expect(response.status_code).to_equal(200)
        self.expect(response.json["data"]).to_equal([])

    @fixtures.use(
        [
            "public_attachment_of_manufacturer_model1",
            "public_attachment_of_manufacturer_model2",
        ]
    )
    def test_get_list_content(
        self,
        public_attachment_of_manufacturer_model1,
        public_attachment_of_manufacturer_model2,
    ):
        """Ensure we can list the public attachments."""
        response = self.client.get(self.url)
        self.expect(response.status_code).to_equal(200)
        data = response.json["data"]
        self.expect(data[0]["id"]).to_equal(
            str(public_attachment_of_manufacturer_model1.id)
        )
        self.expect(data[0]["attributes"]["label"]).to_equal("GFZ")
        self.expect(data[1]["id"]).to_equal(
            str(public_attachment_of_manufacturer_model2.id)
        )
        self.expect(data[1]["attributes"]["label"]).to_equal("UFZ")

    @fixtures.use(["internal_attachment_of_manufacturer_model1"])
    def test_get_list_content_internal_without_user(
        self, internal_attachment_of_manufacturer_model1
    ):
        """Ensure we don't list internal attachments without a user."""
        response = self.client.get(self.url)
        self.expect(response.status_code).to_equal(200)
        self.expect(response.json["data"]).to_equal([])

    @fixtures.use(["user1", "internal_attachment_of_manufacturer_model1"])
    def test_get_list_content_internal_with_normal_user(
        self, user1, internal_attachment_of_manufacturer_model1
    ):
        """Ensure we don't list internal attachments for normal users."""
        with self.run_requests_as(user1):
            response = self.client.get(self.url)
        self.expect(response.status_code).to_equal(200)
        self.expect(response.json["data"]).to_equal([])

    @fixtures.use(["export_control_user", "internal_attachment_of_manufacturer_model1"])
    def test_get_list_content_internal_with_export_control_user(
        self, export_control_user, internal_attachment_of_manufacturer_model1
    ):
        """Ensure we list internal attachments for export control users."""
        with self.run_requests_as(export_control_user):
            response = self.client.get(self.url)
        self.expect(response.status_code).to_equal(200)
        data = response.json["data"]
        self.expect(len).of(data).to_equal(1)
        self.expect(data[0]["id"]).to_equal(
            str(internal_attachment_of_manufacturer_model1.id)
        )

    @fixtures.use(["super_user", "internal_attachment_of_manufacturer_model1"])
    def test_get_list_content_internal_with_super_user(
        self, super_user, internal_attachment_of_manufacturer_model1
    ):
        """Ensure we list internal attachments for super users."""
        with self.run_requests_as(super_user):
            response = self.client.get(self.url)
        self.expect(response.status_code).to_equal(200)
        data = response.json["data"]
        self.expect(len).of(data).to_equal(1)
        self.expect(data[0]["id"]).to_equal(
            str(internal_attachment_of_manufacturer_model1.id)
        )

    @fixtures.use(
        [
            "public_attachment_of_manufacturer_model1",
            "public_attachment_of_manufacturer_model2",
        ]
    )
    def test_get_list_prefiltered_by_manufacturer_model(
        self,
        public_attachment_of_manufacturer_model1,
        public_attachment_of_manufacturer_model2,
    ):
        """Ensure we can prefilter using the manufacturer models."""
        url1 = "/".join(
            [
                base_url,
                "manufacturer-models",
                str(public_attachment_of_manufacturer_model1.manufacturer_model_id),
                "export-control-attachments",
            ]
        )
        response1 = self.client.get(url1)
        self.expect(response1.status_code).to_equal(200)
        data1 = response1.json["data"]
        self.expect(len).of(data1).to_equal(1)
        self.expect(data1[0]["id"]).to_equal(
            str(public_attachment_of_manufacturer_model1.id)
        )

        url2 = "/".join(
            [
                base_url,
                "manufacturer-models",
                str(public_attachment_of_manufacturer_model2.manufacturer_model_id),
                "export-control-attachments",
            ]
        )
        response2 = self.client.get(url2)
        self.expect(response2.status_code).to_equal(200)
        data2 = response2.json["data"]
        self.expect(len).of(data2).to_equal(1)
        self.expect(data2[0]["id"]).to_equal(
            str(public_attachment_of_manufacturer_model2.id)
        )

        url3 = f"{base_url}/manufacturer-models/9999999/export-control-attachments"
        response3 = self.client.get(url3)
        self.expect(response3.status_code).to_equal(404)

    @fixtures.use(
        [
            "public_attachment_of_manufacturer_model1",
            "public_attachment_of_manufacturer_model2",
        ]
    )
    def test_get_list_prefiltered_by_manufacturer_model_id(
        self,
        public_attachment_of_manufacturer_model1,
        public_attachment_of_manufacturer_model2,
    ):
        """Ensure we can prefilter using the manufacturer model id filter."""
        url1 = "".join(
            [
                self.url,
                "?filter[manufacturer_model_id]=",
                str(public_attachment_of_manufacturer_model1.manufacturer_model_id),
            ]
        )
        response1 = self.client.get(url1)
        self.expect(response1.status_code).to_equal(200)
        data1 = response1.json["data"]
        self.expect(len).of(data1).to_equal(1)
        self.expect(data1[0]["id"]).to_equal(
            str(public_attachment_of_manufacturer_model1.id)
        )

        url2 = "".join(
            [
                self.url,
                "?filter[manufacturer_model_id]=",
                str(public_attachment_of_manufacturer_model2.manufacturer_model_id),
            ]
        )
        response2 = self.client.get(url2)
        self.expect(response2.status_code).to_equal(200)
        data2 = response2.json["data"]
        self.expect(len).of(data2).to_equal(1)
        self.expect(data2[0]["id"]).to_equal(
            str(public_attachment_of_manufacturer_model2.id)
        )

        url3 = "".join(
            [
                self.url,
                "?filter[manufacturer_model_id]=9999999",
            ]
        )
        response3 = self.client.get(url3)
        self.expect(response3.status_code).to_equal(200)
        data3 = response3.json["data"]
        self.expect(len).of(data3).to_equal(0)

    def test_get_one_non_existing(self):
        """Ensure we return a 404 response if the export attachment doesn't exist."""
        response = self.client.get(f"{self.url}/123456789")
        self.expect(response.status_code).to_equal(404)

    @fixtures.use(["public_attachment_of_manufacturer_model1"])
    def test_get_one_public(self, public_attachment_of_manufacturer_model1):
        """Ensure we allow get on public attachments."""
        response = self.client.get(
            f"{self.url}/{public_attachment_of_manufacturer_model1.id}"
        )
        self.expect(response.status_code).to_equal(200)
        data = response.json["data"]
        self.expect(data["id"]).to_equal(
            str(public_attachment_of_manufacturer_model1.id)
        )
        self.expect(data["attributes"]["label"]).to_equal("GFZ")

    @fixtures.use(["internal_attachment_of_manufacturer_model1"])
    def test_get_one_internal_no_user(self, internal_attachment_of_manufacturer_model1):
        """Ensure we restrict get on internal attachments without a user."""
        response = self.client.get(
            f"{self.url}/{internal_attachment_of_manufacturer_model1.id}"
        )
        self.expect(response.status_code).to_equal(401)

    @fixtures.use(["user1", "internal_attachment_of_manufacturer_model1"])
    def test_get_one_internal_normal_user(
        self, user1, internal_attachment_of_manufacturer_model1
    ):
        """Ensure we restrict get on internal attachments for normal users."""
        with self.run_requests_as(user1):
            response = self.client.get(
                f"{self.url}/{internal_attachment_of_manufacturer_model1.id}"
            )
        self.expect(response.status_code).to_equal(403)

    @fixtures.use(["export_control_user", "internal_attachment_of_manufacturer_model1"])
    def test_get_one_internal_export_control_user(
        self, export_control_user, internal_attachment_of_manufacturer_model1
    ):
        """Ensure we allow get on internal attachments for export control users."""
        with self.run_requests_as(export_control_user):
            response = self.client.get(
                f"{self.url}/{internal_attachment_of_manufacturer_model1.id}"
            )
        self.expect(response.status_code).to_equal(200)
        data = response.json["data"]
        self.expect(data["id"]).to_equal(
            str(internal_attachment_of_manufacturer_model1.id)
        )
        self.expect(data["attributes"]["label"]).to_equal("GFZ")

    @fixtures.use(["super_user", "internal_attachment_of_manufacturer_model1"])
    def test_get_one_internal_super_user(
        self, super_user, internal_attachment_of_manufacturer_model1
    ):
        """Ensure we allow get on internal attachments for super users."""
        with self.run_requests_as(super_user):
            response = self.client.get(
                f"{self.url}/{internal_attachment_of_manufacturer_model1.id}"
            )
        self.expect(response.status_code).to_equal(200)
        data = response.json["data"]
        self.expect(data["id"]).to_equal(
            str(internal_attachment_of_manufacturer_model1.id)
        )
        self.expect(data["attributes"]["label"]).to_equal("GFZ")

    @fixtures.use(["manufacturer_model1"])
    def test_post_no_user(self, manufacturer_model1):
        """Ensure we can't post if we don't have a user."""
        payload = {
            "data": {
                "type": "export_control_attachment",
                "attributes": {
                    "label": "GFZ",
                    "url": "https://gfz-potsdam.de",
                    "is_export_control_only": False,
                },
                "relationships": {
                    "manufacturer_model": {
                        "data": {
                            "id": manufacturer_model1.id,
                            "type": "manufacturer_model",
                        }
                    }
                },
            },
        }
        response = self.client.post(
            self.url,
            data=json.dumps(payload),
            content_type="application/vnd.api+json",
        )
        self.expect(response.status_code).to_equal(401)

    @fixtures.use(["user1", "manufacturer_model1"])
    def test_post_normal_user(self, user1, manufacturer_model1):
        """Ensure we can't post if we are a normal user."""
        payload = {
            "data": {
                "type": "export_control_attachment",
                "attributes": {
                    "label": "GFZ",
                    "url": "https://gfz-potsdam.de",
                    "is_export_control_only": False,
                },
                "relationships": {
                    "manufacturer_model": {
                        "data": {
                            "id": manufacturer_model1.id,
                            "type": "manufacturer_model",
                        }
                    }
                },
            },
        }
        with self.run_requests_as(user1):
            response = self.client.post(
                self.url,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.expect(response.status_code).to_equal(403)

    @fixtures.use(["export_control_user", "manufacturer_model1"])
    def test_post_export_control_user(self, export_control_user, manufacturer_model1):
        """Ensure we can post if we are export control user."""
        payload = {
            "data": {
                "type": "export_control_attachment",
                "attributes": {
                    "label": "GFZ",
                    "url": "https://gfz-potsdam.de",
                    "is_export_control_only": False,
                },
                "relationships": {
                    "manufacturer_model": {
                        "data": {
                            "id": manufacturer_model1.id,
                            "type": "manufacturer_model",
                        }
                    }
                },
            },
        }
        with self.run_requests_as(export_control_user):
            response = self.client.post(
                self.url,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.expect(response.status_code).to_equal(201)
        loaded_attachment = (
            db.session.query(ExportControlAttachment)
            .filter_by(id=response.json["data"]["id"])
            .first()
        )
        self.expect(loaded_attachment.created_by_id).to_equal(export_control_user.id)
        self.expect(loaded_attachment.updated_by_id).to_equal(export_control_user.id)
        self.expect(loaded_attachment.created_at).not_.to_be(None)
        self.expect(loaded_attachment.updated_at).not_.to_be(None)

    @fixtures.use(["super_user", "manufacturer_model1"])
    def test_post_super_user(self, super_user, manufacturer_model1):
        """Ensure we can post if we are export control user."""
        payload = {
            "data": {
                "type": "export_control_attachment",
                "attributes": {
                    "label": "GFZ",
                    "url": "https://gfz-potsdam.de",
                    "is_export_control_only": False,
                },
                "relationships": {
                    "manufacturer_model": {
                        "data": {
                            "id": manufacturer_model1.id,
                            "type": "manufacturer_model",
                        }
                    }
                },
            },
        }
        with self.run_requests_as(super_user):
            response = self.client.post(
                self.url,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.expect(response.status_code).to_equal(201)
        loaded_attachment = (
            db.session.query(ExportControlAttachment)
            .filter_by(id=response.json["data"]["id"])
            .first()
        )
        self.expect(loaded_attachment.created_by_id).to_equal(super_user.id)
        self.expect(loaded_attachment.updated_by_id).to_equal(super_user.id)
        self.expect(loaded_attachment.created_at).not_.to_be(None)
        self.expect(loaded_attachment.updated_at).not_.to_be(None)

    @fixtures.use(["public_attachment_of_manufacturer_model1"])
    def test_patch_no_user(self, public_attachment_of_manufacturer_model1):
        """Ensure we can't patch without a user."""
        payload = {
            "data": {
                "id": str(public_attachment_of_manufacturer_model1.id),
                "type": "export_control_attachment",
                "attributes": {
                    "label": "fancy",
                },
            }
        }
        response = self.client.patch(
            f"{self.url}/{public_attachment_of_manufacturer_model1.id}",
            data=json.dumps(payload),
            content_type="application/vnd.api+json",
        )
        self.expect(response.status_code).to_equal(401)

    @fixtures.use(["user1", "public_attachment_of_manufacturer_model1"])
    def test_patch_normal_user(self, user1, public_attachment_of_manufacturer_model1):
        """Ensure we can't patch with a normal user."""
        payload = {
            "data": {
                "id": str(public_attachment_of_manufacturer_model1.id),
                "type": "export_control_attachment",
                "attributes": {
                    "label": "fancy",
                },
            }
        }
        with self.run_requests_as(user1):
            response = self.client.patch(
                f"{self.url}/{public_attachment_of_manufacturer_model1.id}",
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.expect(response.status_code).to_equal(403)

    @fixtures.use(["export_control_user", "public_attachment_of_manufacturer_model1"])
    def test_patch_export_control_user(
        self, export_control_user, public_attachment_of_manufacturer_model1
    ):
        """Ensure we can patch with an export control user."""
        payload = {
            "data": {
                "id": str(public_attachment_of_manufacturer_model1.id),
                "type": "export_control_attachment",
                "attributes": {
                    "label": "fancy",
                },
            }
        }
        with self.run_requests_as(export_control_user):
            response = self.client.patch(
                f"{self.url}/{public_attachment_of_manufacturer_model1.id}",
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.expect(response.status_code).to_equal(200)
        loaded_attachment = (
            db.session.query(ExportControlAttachment)
            .filter_by(id=public_attachment_of_manufacturer_model1.id)
            .first()
        )
        self.expect(loaded_attachment.updated_by_id).to_equal(export_control_user.id)
        self.expect(loaded_attachment.updated_at).not_.to_be(None)

    @fixtures.use(["super_user", "public_attachment_of_manufacturer_model1"])
    def test_patch_super_user(
        self, super_user, public_attachment_of_manufacturer_model1
    ):
        """Ensure we can patch with an export control user."""
        payload = {
            "data": {
                "id": str(public_attachment_of_manufacturer_model1.id),
                "type": "export_control_attachment",
                "attributes": {
                    "label": "fancy",
                },
            }
        }
        with self.run_requests_as(super_user):
            response = self.client.patch(
                f"{self.url}/{public_attachment_of_manufacturer_model1.id}",
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.expect(response.status_code).to_equal(200)
        loaded_attachment = (
            db.session.query(ExportControlAttachment)
            .filter_by(id=public_attachment_of_manufacturer_model1.id)
            .first()
        )
        self.expect(loaded_attachment.updated_by_id).to_equal(super_user.id)
        self.expect(loaded_attachment.updated_at).not_.to_be(None)

    @fixtures.use(["public_attachment_of_manufacturer_model1"])
    def test_delete_no_user(self, public_attachment_of_manufacturer_model1):
        """Ensure we can't delete without a user."""
        response = self.client.delete(
            f"{self.url}/{public_attachment_of_manufacturer_model1.id}",
        )
        self.expect(response.status_code).to_equal(401)

    @fixtures.use(["user1", "public_attachment_of_manufacturer_model1"])
    def test_delete_normal_user(self, user1, public_attachment_of_manufacturer_model1):
        """Ensure we can't delete with a normal user."""
        with self.run_requests_as(user1):
            response = self.client.delete(
                f"{self.url}/{public_attachment_of_manufacturer_model1.id}",
            )
        self.expect(response.status_code).to_equal(403)

    @fixtures.use(["export_control_user", "public_attachment_of_manufacturer_model1"])
    def test_delete_export_control_user(
        self, export_control_user, public_attachment_of_manufacturer_model1
    ):
        """Ensure we can delete with an export control user."""
        with self.run_requests_as(export_control_user):
            response = self.client.delete(
                f"{self.url}/{public_attachment_of_manufacturer_model1.id}",
            )
        self.expect(response.status_code).to_equal(200)

    @fixtures.use(["super_user", "public_attachment_of_manufacturer_model1"])
    def test_delete_super_user(
        self, super_user, public_attachment_of_manufacturer_model1
    ):
        """Ensure we can delete with an export control user."""
        with self.run_requests_as(super_user):
            response = self.client.delete(
                f"{self.url}/{public_attachment_of_manufacturer_model1.id}",
            )
        self.expect(response.status_code).to_equal(200)

    def test_download_get_not_found(self):
        """Ensure that we return 404 for non existing attachments."""
        url = f"{self.url}/123456789/file/somefile.txt"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    @fixtures.use(["internal_attachment_of_manufacturer_model1"])
    def test_download_get_internal_no_user(
        self, internal_attachment_of_manufacturer_model1
    ):
        """Ensure that we require a user for internal attachments."""
        url = f"{self.url}/{internal_attachment_of_manufacturer_model1.id}/file/somefile.txt"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    @fixtures.use(["user1", "internal_attachment_of_manufacturer_model1"])
    def test_download_get_internal_normal_user(
        self, user1, internal_attachment_of_manufacturer_model1
    ):
        """Ensure that we don't expose internal attachments to normal users."""
        url = f"{self.url}/{internal_attachment_of_manufacturer_model1.id}/file/somefile.txt"
        with self.run_requests_as(user1):
            response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    @fixtures.use(["public_attachment_of_manufacturer_model1"])
    def test_download_get_redirect_for_public_attachment(
        self, public_attachment_of_manufacturer_model1
    ):
        """Ensure that we can redirect for attachments that are not internal."""
        url = f"{self.url}/{public_attachment_of_manufacturer_model1.id}/file/somefile.txt"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    @fixtures.use(["manufacturer_model1"])
    def test_download_get_content_public_no_user(self, manufacturer_model1):
        """Get the content for a public device."""
        attachment = ExportControlAttachment(
            manufacturer_model=manufacturer_model1,
            label="gfz",
            # url will not be used.
            url="http://localhost/.../file.txt",
            internal_url="http://minio:8080/.../file.txt",
            is_export_control_only=False,
        )
        db.session.add_all([attachment])
        db.session.commit()

        url = f"{self.url}/{attachment.id}/file/somefile.txt"
        with patch.object(download_files, "build_response") as build_response_mock:
            with patch.object(
                download_files, "get_content_type"
            ) as get_content_type_mock:
                build_response_mock.return_value = "some text"
                get_content_type_mock.return_value = "plain/text"

                response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "plain/text")
        self.assertEqual(response.text, "some text")

    @fixtures.use(["export_control_user", "manufacturer_model1"])
    def test_download_get_content_internal_with_export_control_user(
        self, export_control_user, manufacturer_model1
    ):
        """Get the content for an internal url with an export control user."""
        attachment = ExportControlAttachment(
            manufacturer_model=manufacturer_model1,
            label="gfz",
            # url will not be used.
            url="http://localhost/.../file.txt",
            internal_url="http://minio:8080/.../file.txt",
            is_export_control_only=True,
        )
        db.session.add_all([attachment])
        db.session.commit()

        url = f"{self.url}/{attachment.id}/file/somefile.txt"
        with patch.object(download_files, "build_response") as build_response_mock:
            with patch.object(
                download_files, "get_content_type"
            ) as get_content_type_mock:
                build_response_mock.return_value = "some text"
                get_content_type_mock.return_value = "plain/text"

                with self.run_requests_as(export_control_user):
                    response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "plain/text")
        self.assertEqual(response.text, "some text")

    @fixtures.use(["super_user", "manufacturer_model1"])
    def test_download_get_content_internal_with_super_user(
        self, super_user, manufacturer_model1
    ):
        """Get the content for an internal url with an export control user."""
        attachment = ExportControlAttachment(
            manufacturer_model=manufacturer_model1,
            label="gfz",
            # url will not be used.
            url="http://localhost/.../file.txt",
            internal_url="http://minio:8080/.../file.txt",
            is_export_control_only=True,
        )
        db.session.add_all([attachment])
        db.session.commit()

        url = f"{self.url}/{attachment.id}/file/somefile.txt"
        with patch.object(download_files, "build_response") as build_response_mock:
            with patch.object(
                download_files, "get_content_type"
            ) as get_content_type_mock:
                build_response_mock.return_value = "some text"
                get_content_type_mock.return_value = "plain/text"

                with self.run_requests_as(super_user):
                    response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "plain/text")
        self.assertEqual(response.text, "some text")

    @fixtures.use(["export_control_user", "public_attachment_of_manufacturer_model1"])
    def test_delete_can_remove_no_longer_used_manufacturer_model(
        self, export_control_user, public_attachment_of_manufacturer_model1
    ):
        """Ensure we can delete the manufacturer model entry if it is no longer in use."""
        with self.run_requests_as(export_control_user):
            response = self.client.delete(
                f"{self.url}/{public_attachment_of_manufacturer_model1.id}",
            )
        self.expect(response.status_code).to_equal(200)

        self.expect(
            db.session.query(ManufacturerModel)
            .filter_by(
                id=public_attachment_of_manufacturer_model1.manufacturer_model_id
            )
            .first()
        ).to_equal(None)

    @fixtures.use(["export_control_user", "public_attachment_of_manufacturer_model1"])
    def test_delete_cant_remove_manufacturer_model_if_used_by_external_system(
        self, export_control_user, public_attachment_of_manufacturer_model1
    ):
        """Ensure we can't delete the manufacturer model entry if it refers to an external system."""
        manufacturer_model = public_attachment_of_manufacturer_model1.manufacturer_model
        manufacturer_model.external_system_name = "GIPP"
        manufacturer_model.external_system_url = (
            "https://gipp.gfz-potsdam.de/instrumentcategory/123"
        )

        db.session.add(manufacturer_model)
        db.session.commit()

        with self.run_requests_as(export_control_user):
            response = self.client.delete(
                f"{self.url}/{public_attachment_of_manufacturer_model1.id}",
            )
        self.expect(response.status_code).to_equal(200)

        self.expect(
            db.session.query(ManufacturerModel)
            .filter_by(
                id=public_attachment_of_manufacturer_model1.manufacturer_model_id
            )
            .first()
        ).to_equal(manufacturer_model)

    @fixtures.use(["export_control_user", "public_attachment_of_manufacturer_model1"])
    def test_delete_cant_remove_manufacturer_model_if_used_by_device(
        self, export_control_user, public_attachment_of_manufacturer_model1
    ):
        """Ensure we can't delete the manufacturer model entry if it refers to a device."""
        manufacturer_model = public_attachment_of_manufacturer_model1.manufacturer_model

        device = Device(
            short_name="test device",
            is_public=True,
            is_internal=False,
            is_private=False,
            group_ids=[1],
            manufacturer_name=manufacturer_model.manufacturer_name,
            model=manufacturer_model.model,
        )

        db.session.add(device)
        db.session.commit()

        with self.run_requests_as(export_control_user):
            response = self.client.delete(
                f"{self.url}/{public_attachment_of_manufacturer_model1.id}",
            )
        self.expect(response.status_code).to_equal(200)

        self.expect(
            db.session.query(ManufacturerModel)
            .filter_by(
                id=public_attachment_of_manufacturer_model1.manufacturer_model_id
            )
            .first()
        ).to_equal(manufacturer_model)

    @fixtures.use(["export_control_user", "public_attachment_of_manufacturer_model1"])
    def test_delete_cant_remove_manufacturer_model_if_used_by_platform(
        self, export_control_user, public_attachment_of_manufacturer_model1
    ):
        """Ensure we can't delete the manufacturer model entry if it refers to a platform."""
        manufacturer_model = public_attachment_of_manufacturer_model1.manufacturer_model

        platform = Platform(
            short_name="test platform",
            is_public=True,
            is_internal=False,
            is_private=False,
            group_ids=[1],
            manufacturer_name=manufacturer_model.manufacturer_name,
            model=manufacturer_model.model,
        )

        db.session.add(platform)
        db.session.commit()

        with self.run_requests_as(export_control_user):
            response = self.client.delete(
                f"{self.url}/{public_attachment_of_manufacturer_model1.id}",
            )
        self.expect(response.status_code).to_equal(200)

        self.expect(
            db.session.query(ManufacturerModel)
            .filter_by(
                id=public_attachment_of_manufacturer_model1.manufacturer_model_id
            )
            .first()
        ).to_equal(manufacturer_model)

    @fixtures.use(["export_control_user", "public_attachment_of_manufacturer_model1"])
    def test_delete_cant_remove_manufacturer_model_if_used_by_export_control_data(
        self, export_control_user, public_attachment_of_manufacturer_model1
    ):
        """Ensure we can't delete the manufacturer model entry if it refers to export control data."""
        manufacturer_model = public_attachment_of_manufacturer_model1.manufacturer_model

        export_control = ExportControl(
            manufacturer_model=manufacturer_model,
            dual_use=True,
        )

        db.session.add(export_control)
        db.session.commit()

        with self.run_requests_as(export_control_user):
            response = self.client.delete(
                f"{self.url}/{public_attachment_of_manufacturer_model1.id}",
            )
        self.expect(response.status_code).to_equal(200)

        self.expect(
            db.session.query(ManufacturerModel)
            .filter_by(
                id=public_attachment_of_manufacturer_model1.manufacturer_model_id
            )
            .first()
        ).to_equal(manufacturer_model)

    @fixtures.use(
        [
            "export_control_user",
            "public_attachment_of_manufacturer_model1",
            "manufacturer_model2",
        ]
    )
    def test_patch_move_to_other_manufacturer_model(
        self,
        export_control_user,
        public_attachment_of_manufacturer_model1,
        manufacturer_model2,
    ):
        """Ensure we can't change the associated manufacturer model of an attachment via the api."""
        payload = {
            "data": {
                "type": "export_control_attachment",
                "id": str(public_attachment_of_manufacturer_model1.id),
                "relationships": {
                    "manufacturer_model": {
                        "data": {
                            "type": "manufacturer_model",
                            "id": str(manufacturer_model2.id),
                        }
                    }
                },
            }
        }
        with self.run_requests_as(export_control_user):
            response = self.client.patch(
                self.url + f"/{public_attachment_of_manufacturer_model1.id}",
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.expect(response.status_code).to_equal(409)
