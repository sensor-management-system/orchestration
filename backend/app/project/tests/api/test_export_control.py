# SPDX-FileCopyrightText: 2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Tests for the export control endpoints."""

import json

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


@fixtures.register("export_control_of_manufacturer_model1", scope=lambda: db.session)
@fixtures.use(["manufacturer_model1"])
def create_export_control_of_manufacturer_model1(manufacturer_model1):
    """Create an export control entry for the manufacturer model1."""
    result = ExportControl(
        manufacturer_model=manufacturer_model1,
        dual_use=False,
        additional_information="No need for an SMT 100",
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


@fixtures.register("export_control_of_manufacturer_model2", scope=lambda: db.session)
@fixtures.use(["manufacturer_model2"])
def create_export_control_of_manufacturer_model2(manufacturer_model2):
    """Create an export control entry for the manufacturer model2."""
    result = ExportControl(
        manufacturer_model=manufacturer_model2,
        dual_use=None,
        additional_information="Still need to be checked",
        internal_note="we have to wait for the manufacturer to answer",
    )
    db.session.add(result)
    db.session.commit()
    return result


class TestExportControl(BaseTestCase):
    """Test class for the export control api."""

    url = base_url + "/export-control"

    def test_get_list_empty(self):
        """Ensure we can get an empty list."""
        response = self.client.get(self.url)
        self.expect(response.status_code).to_equal(200)
        self.expect(response.json["data"]).to_equal([])

    @fixtures.use(
        [
            "export_control_of_manufacturer_model1",
            "export_control_of_manufacturer_model2",
        ]
    )
    def test_get_list_with_content(
        self,
        export_control_of_manufacturer_model1,
        export_control_of_manufacturer_model2,
    ):
        """Ensure we can get the basic information publically."""
        response = self.client.get(self.url)
        self.expect(response.status_code).to_equal(200)
        data = response.json["data"]
        self.expect(len).of(data).to_equal(2)
        self.expect(data[0]["attributes"]["dual_use"]).to_equal(False)
        self.expect(data[1]["attributes"]["dual_use"]).to_equal(None)
        # But ensure that we don't give out the internal_note without a user.
        self.expect(data[1]["attributes"].keys()).not_.to_include("internal_note")

    @fixtures.use(["user1", "export_control_of_manufacturer_model2"])
    def test_get_list_with_content_for_normal_user(
        self, user1, export_control_of_manufacturer_model2
    ):
        """Ensure we don't deliver internal information to a normal user."""
        with self.run_requests_as(user1):
            response = self.client.get(self.url)
        self.expect(response.status_code).to_equal(200)
        data = response.json["data"]
        self.expect(len).of(data).to_equal(1)
        self.expect(data[0]["attributes"]["dual_use"]).to_equal(None)
        self.expect(data[0]["attributes"].keys()).not_.to_include("internal_note")

    @fixtures.use(["export_control_user", "export_control_of_manufacturer_model2"])
    def test_get_list_with_content_for_export_control_user(
        self, export_control_user, export_control_of_manufacturer_model2
    ):
        """Ensure we can get the internal information if we are an export control user."""
        with self.run_requests_as(export_control_user):
            response = self.client.get(self.url)
        self.expect(response.status_code).to_equal(200)
        data = response.json["data"]
        self.expect(len).of(data).to_equal(1)
        self.expect(data[0]["attributes"]["dual_use"]).to_equal(None)
        self.expect(data[0]["attributes"]["internal_note"]).to_equal(
            export_control_of_manufacturer_model2.internal_note
        )

    @fixtures.use(["super_user", "export_control_of_manufacturer_model2"])
    def test_get_list_with_content_for_super_user(
        self, super_user, export_control_of_manufacturer_model2
    ):
        """Ensure we can get the internal information if we are a super user."""
        with self.run_requests_as(super_user):
            response = self.client.get(self.url)
        self.expect(response.status_code).to_equal(200)
        data = response.json["data"]
        self.expect(len).of(data).to_equal(1)
        self.expect(data[0]["attributes"]["dual_use"]).to_equal(None)
        self.expect(data[0]["attributes"]["internal_note"]).to_equal(
            export_control_of_manufacturer_model2.internal_note
        )

    @fixtures.use(["manufacturer_model1"])
    def test_post_no_user(self, manufacturer_model1):
        """Ensure we can't post without a user."""
        payload = {
            "data": {
                "type": "export_control",
                "attributes": {
                    "dual_use": False,
                    "additional_information": "No need to worry",
                },
                "relationships": {
                    "manufacturer_model": {
                        "data": {
                            "id": str(manufacturer_model1.id),
                            "type": "manufacturer_model",
                        }
                    }
                },
            }
        }
        response = self.client.post(
            self.url, data=json.dumps(payload), content_type="application/vnd.api+json"
        )
        self.expect(response.status_code).to_equal(401)

    @fixtures.use(["user1", "manufacturer_model1"])
    def test_post_normal_user(self, user1, manufacturer_model1):
        """Ensure we can't post with a normal user."""
        payload = {
            "data": {
                "type": "export_control",
                "attributes": {
                    "dual_use": False,
                    "additional_information": "No need to worry",
                },
                "relationships": {
                    "manufacturer_model": {
                        "data": {
                            "id": str(manufacturer_model1.id),
                            "type": "manufacturer_model",
                        }
                    }
                },
            }
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
        """Ensure we can post with an export control user."""
        payload = {
            "data": {
                "type": "export_control",
                "attributes": {
                    "dual_use": False,
                    "additional_information": "No need to worry",
                },
                "relationships": {
                    "manufacturer_model": {
                        "data": {
                            "id": str(manufacturer_model1.id),
                            "type": "manufacturer_model",
                        }
                    }
                },
            }
        }
        with self.run_requests_as(export_control_user):
            response = self.client.post(
                self.url,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.expect(response.status_code).to_equal(201)

        data = response.json["data"]

        self.expect(data["relationships"]["created_by"]["data"]["id"]).to_equal(
            str(export_control_user.id)
        )
        self.expect(data["relationships"]["updated_by"]["data"]["id"]).to_equal(
            str(export_control_user.id)
        )

        self.expect(data["attributes"]["created_at"]).to_be_a_datetime_string()
        self.expect(data["attributes"]["updated_at"]).to_be_a_datetime_string()

    @fixtures.use(["super_user", "manufacturer_model1"])
    def test_post_super_user(self, super_user, manufacturer_model1):
        """Ensure we can post with a super user."""
        payload = {
            "data": {
                "type": "export_control",
                "attributes": {
                    "dual_use": False,
                    "additional_information": "No need to worry",
                },
                "relationships": {
                    "manufacturer_model": {
                        "data": {
                            "id": str(manufacturer_model1.id),
                            "type": "manufacturer_model",
                        }
                    }
                },
            }
        }
        with self.run_requests_as(super_user):
            response = self.client.post(
                self.url,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.expect(response.status_code).to_equal(201)

        data = response.json["data"]

        self.expect(data["relationships"]["created_by"]["data"]["id"]).to_equal(
            str(super_user.id)
        )
        self.expect(data["relationships"]["updated_by"]["data"]["id"]).to_equal(
            str(super_user.id)
        )

        self.expect(data["attributes"]["created_at"]).to_be_a_datetime_string()
        self.expect(data["attributes"]["updated_at"]).to_be_a_datetime_string()

    @fixtures.use(["export_control_of_manufacturer_model1"])
    def test_delete_no_user(self, export_control_of_manufacturer_model1):
        """Ensure we can't delete if we have no user."""
        response = self.client.delete(
            f"{self.url}/{export_control_of_manufacturer_model1.id}"
        )
        self.expect(response.status_code).to_equal(401)

    @fixtures.use(["user1", "export_control_of_manufacturer_model1"])
    def test_delete_normal_user(self, user1, export_control_of_manufacturer_model1):
        """Ensure we can't delete if we have a normal user."""
        with self.run_requests_as(user1):
            response = self.client.delete(
                f"{self.url}/{export_control_of_manufacturer_model1.id}"
            )
        self.expect(response.status_code).to_equal(403)

    @fixtures.use(["export_control_user", "export_control_of_manufacturer_model1"])
    def test_delete_export_control_user(
        self, export_control_user, export_control_of_manufacturer_model1
    ):
        """Ensure we can delete if we have an export control user."""
        with self.run_requests_as(export_control_user):
            response = self.client.delete(
                f"{self.url}/{export_control_of_manufacturer_model1.id}"
            )
        self.expect(response.status_code).to_equal(200)
        self.expect(
            db.session.query(ExportControl)
            .filter_by(id=export_control_of_manufacturer_model1.id)
            .first()
        ).to_equal(None)

    @fixtures.use(["super_user", "export_control_of_manufacturer_model1"])
    def test_delete_super_user(self, super_user, export_control_of_manufacturer_model1):
        """Ensure we can delete if we have a super user."""
        with self.run_requests_as(super_user):
            response = self.client.delete(
                f"{self.url}/{export_control_of_manufacturer_model1.id}"
            )
        self.expect(response.status_code).to_equal(200)
        self.expect(
            db.session.query(ExportControl)
            .filter_by(id=export_control_of_manufacturer_model1.id)
            .first()
        ).to_equal(None)

    def test_get_one_non_existing(self):
        """Ensure we 404 for a nonexisting id.."""
        response = self.client.get(self.url + "/123456789")
        self.expect(response.status_code).to_equal(404)

    @fixtures.use(["export_control_of_manufacturer_model2"])
    def test_get_one_no_user(
        self,
        export_control_of_manufacturer_model2,
    ):
        """Ensure we can get the basic information publically."""
        response = self.client.get(
            self.url + f"/{export_control_of_manufacturer_model2.id}"
        )
        self.expect(response.status_code).to_equal(200)
        data = response.json["data"]
        self.expect(data["attributes"]["dual_use"]).to_equal(None)
        self.expect(data["attributes"].keys()).not_.to_include("internal_note")

    @fixtures.use(["user1", "export_control_of_manufacturer_model2"])
    def test_get_one_normal_user(self, user1, export_control_of_manufacturer_model2):
        """Ensure we don't deliver internal information to a normal user."""
        with self.run_requests_as(user1):
            response = self.client.get(
                self.url + f"/{export_control_of_manufacturer_model2.id}"
            )
        self.expect(response.status_code).to_equal(200)
        data = response.json["data"]
        self.expect(data["attributes"]["dual_use"]).to_equal(None)
        self.expect(data["attributes"].keys()).not_.to_include("internal_note")

    @fixtures.use(["export_control_user", "export_control_of_manufacturer_model2"])
    def test_get_one_export_control_user(
        self, export_control_user, export_control_of_manufacturer_model2
    ):
        """Ensure we can get the internal information if we are an export control user."""
        with self.run_requests_as(export_control_user):
            response = self.client.get(
                self.url + f"/{export_control_of_manufacturer_model2.id}"
            )
        self.expect(response.status_code).to_equal(200)
        data = response.json["data"]
        self.expect(data["attributes"]["dual_use"]).to_equal(None)
        self.expect(data["attributes"]["internal_note"]).to_equal(
            export_control_of_manufacturer_model2.internal_note
        )

    @fixtures.use(["super_user", "export_control_of_manufacturer_model2"])
    def test_get_one_with_content_for_super_user(
        self, super_user, export_control_of_manufacturer_model2
    ):
        """Ensure we can get the internal information if we are a super user."""
        with self.run_requests_as(super_user):
            response = self.client.get(
                self.url + f"/{export_control_of_manufacturer_model2.id}"
            )
        self.expect(response.status_code).to_equal(200)
        data = response.json["data"]
        self.expect(data["attributes"]["dual_use"]).to_equal(None)
        self.expect(data["attributes"]["internal_note"]).to_equal(
            export_control_of_manufacturer_model2.internal_note
        )

    @fixtures.use(["export_control_of_manufacturer_model1"])
    def test_patch_no_user(self, export_control_of_manufacturer_model1):
        """Ensure we can't patch without a user."""
        payload = {
            "data": {
                "type": "export_control",
                "id": str(export_control_of_manufacturer_model1.id),
                "attributes": {
                    "dual_use": True,
                },
            }
        }
        response = self.client.patch(
            self.url + f"/{export_control_of_manufacturer_model1.id}",
            data=json.dumps(payload),
            content_type="application/vnd.api+json",
        )
        self.expect(response.status_code).to_equal(401)

    @fixtures.use(["user1", "export_control_of_manufacturer_model1"])
    def test_patch_normal_user(self, user1, export_control_of_manufacturer_model1):
        """Ensure we can't patch with a normal user."""
        payload = {
            "data": {
                "type": "export_control",
                "id": str(export_control_of_manufacturer_model1.id),
                "attributes": {
                    "dual_use": True,
                },
            }
        }
        with self.run_requests_as(user1):
            response = self.client.patch(
                self.url + f"/{export_control_of_manufacturer_model1.id}",
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.expect(response.status_code).to_equal(403)

    @fixtures.use(["export_control_user", "export_control_of_manufacturer_model1"])
    def test_patch_export_control_user(
        self, export_control_user, export_control_of_manufacturer_model1
    ):
        """Ensure we can patch with an export control user."""
        payload = {
            "data": {
                "type": "export_control",
                "id": str(export_control_of_manufacturer_model1.id),
                "attributes": {
                    "dual_use": True,
                },
            }
        }
        with self.run_requests_as(export_control_user):
            response = self.client.patch(
                self.url + f"/{export_control_of_manufacturer_model1.id}",
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.expect(response.status_code).to_equal(200)

        data = response.json["data"]

        self.expect(data["relationships"]["updated_by"]["data"]["id"]).to_equal(
            str(export_control_user.id)
        )

        self.expect(data["attributes"]["updated_at"]).to_be_a_datetime_string()

    @fixtures.use(["super_user", "export_control_of_manufacturer_model1"])
    def test_patch_super_user(self, super_user, export_control_of_manufacturer_model1):
        """Ensure we can patch with a super user."""
        payload = {
            "data": {
                "type": "export_control",
                "id": str(export_control_of_manufacturer_model1.id),
                "attributes": {
                    "dual_use": True,
                },
            }
        }
        with self.run_requests_as(super_user):
            response = self.client.patch(
                self.url + f"/{export_control_of_manufacturer_model1.id}",
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.expect(response.status_code).to_equal(200)

        data = response.json["data"]

        self.expect(data["relationships"]["updated_by"]["data"]["id"]).to_equal(
            str(super_user.id)
        )

        self.expect(data["attributes"]["updated_at"]).to_be_a_datetime_string()

    @fixtures.use(
        [
            "export_control_of_manufacturer_model1",
            "export_control_of_manufacturer_model2",
        ]
    )
    def test_get_list_prefiltered_by_manufacturer_model(
        self,
        export_control_of_manufacturer_model1,
        export_control_of_manufacturer_model2,
    ):
        """Ensure we can prefilter using the manufacturer models."""
        url1 = "/".join(
            [
                base_url,
                "manufacturer-models",
                str(export_control_of_manufacturer_model1.manufacturer_model_id),
                "export-control",
            ]
        )
        response1 = self.client.get(url1)
        self.expect(response1.status_code).to_equal(200)
        data1 = response1.json["data"]
        self.expect(len).of(data1).to_equal(1)
        self.expect(data1[0]["id"]).to_equal(
            str(export_control_of_manufacturer_model1.id)
        )

        url2 = "/".join(
            [
                base_url,
                "manufacturer-models",
                str(export_control_of_manufacturer_model2.manufacturer_model_id),
                "export-control",
            ]
        )
        response2 = self.client.get(url2)
        self.expect(response2.status_code).to_equal(200)
        data2 = response2.json["data"]
        self.expect(len).of(data2).to_equal(1)
        self.expect(data2[0]["id"]).to_equal(
            str(export_control_of_manufacturer_model2.id)
        )

        url3 = f"{base_url}/manufacturer-models/9999999/export-control"
        response3 = self.client.get(url3)
        self.expect(response3.status_code).to_equal(404)

    @fixtures.use(
        [
            "export_control_of_manufacturer_model1",
            "export_control_of_manufacturer_model2",
        ]
    )
    def test_get_list_prefiltered_by_manufacturer_model_id(
        self,
        export_control_of_manufacturer_model1,
        export_control_of_manufacturer_model2,
    ):
        """Ensure we can prefilter using the manufacturer model id filter."""
        url1 = "".join(
            [
                self.url,
                "?filter[manufacturer_model_id]=",
                str(export_control_of_manufacturer_model1.manufacturer_model_id),
            ]
        )
        response1 = self.client.get(url1)
        self.expect(response1.status_code).to_equal(200)
        data1 = response1.json["data"]
        self.expect(len).of(data1).to_equal(1)
        self.expect(data1[0]["id"]).to_equal(
            str(export_control_of_manufacturer_model1.id)
        )

        url2 = "".join(
            [
                self.url,
                "?filter[manufacturer_model_id]=",
                str(export_control_of_manufacturer_model2.manufacturer_model_id),
            ]
        )
        response2 = self.client.get(url2)
        self.expect(response2.status_code).to_equal(200)
        data2 = response2.json["data"]
        self.expect(len).of(data2).to_equal(1)
        self.expect(data2[0]["id"]).to_equal(
            str(export_control_of_manufacturer_model2.id)
        )

        url3 = f"{self.url}?filter[manufacturer_model_id]=9999999"
        response3 = self.client.get(url3)
        self.expect(response3.status_code).to_equal(200)
        data3 = response3.json["data"]
        self.expect(len).of(data3).to_equal(0)

    @fixtures.use(
        [
            "export_control_of_manufacturer_model1",
            "export_control_of_manufacturer_model2",
        ]
    )
    def test_get_list_prefiltered_by_platform(
        self,
        export_control_of_manufacturer_model1,
        export_control_of_manufacturer_model2,
    ):
        """Ensure we can prefilter using the platform."""
        manufacturer_model1 = export_control_of_manufacturer_model1.manufacturer_model
        manufacturer_model2 = export_control_of_manufacturer_model2.manufacturer_model
        platform1 = Platform(
            short_name="platform1",
            manufacturer_name=manufacturer_model1.manufacturer_name,
            model=manufacturer_model1.model,
            is_public=True,
            is_internal=False,
            is_private=False,
            group_ids=["1"],
        )
        platform2 = Platform(
            short_name="platform2",
            manufacturer_name=manufacturer_model2.manufacturer_name,
            model=manufacturer_model2.model,
            is_public=True,
            is_internal=False,
            is_private=False,
            group_ids=["2"],
        )
        platform3 = Platform(
            short_name="platform3",
            manufacturer_name="super fancy gmbh",
            model="fancy extreme",
            is_public=True,
            is_internal=False,
            is_private=False,
            group_ids=["3"],
        )
        db.session.add_all([platform1, platform2, platform3])
        db.session.commit()

        url1 = "/".join(
            [
                base_url,
                "platforms",
                str(platform1.id),
                "export-control",
            ]
        )
        response1 = self.client.get(url1)
        self.expect(response1.status_code).to_equal(200)
        data1 = response1.json["data"]
        self.expect(len).of(data1).to_equal(1)
        self.expect(data1[0]["id"]).to_equal(
            str(export_control_of_manufacturer_model1.id)
        )

        url2 = "/".join(
            [
                base_url,
                "platforms",
                str(platform2.id),
                "export-control",
            ]
        )
        response2 = self.client.get(url2)
        self.expect(response2.status_code).to_equal(200)
        data2 = response2.json["data"]
        self.expect(len).of(data2).to_equal(1)
        self.expect(data2[0]["id"]).to_equal(
            str(export_control_of_manufacturer_model2.id)
        )

        url3 = "/".join(
            [
                base_url,
                "platforms",
                str(platform3.id),
                "export-control",
            ]
        )
        response3 = self.client.get(url3)
        self.expect(response3.status_code).to_equal(200)
        data3 = response3.json["data"]
        self.expect(len).of(data3).to_equal(0)

        url4 = f"{base_url}/platoforms/9999999/export-control"
        response4 = self.client.get(url4)
        self.expect(response4.status_code).to_equal(404)

    @fixtures.use(
        [
            "export_control_of_manufacturer_model1",
            "export_control_of_manufacturer_model2",
        ]
    )
    def test_get_list_prefiltered_by_device(
        self,
        export_control_of_manufacturer_model1,
        export_control_of_manufacturer_model2,
    ):
        """Ensure we can prefilter using the device."""
        manufacturer_model1 = export_control_of_manufacturer_model1.manufacturer_model
        manufacturer_model2 = export_control_of_manufacturer_model2.manufacturer_model
        device1 = Device(
            short_name="device1",
            manufacturer_name=manufacturer_model1.manufacturer_name,
            model=manufacturer_model1.model,
            is_public=True,
            is_internal=False,
            is_private=False,
            group_ids=["1"],
        )
        device2 = Device(
            short_name="device2",
            manufacturer_name=manufacturer_model2.manufacturer_name,
            model=manufacturer_model2.model,
            is_public=True,
            is_internal=False,
            is_private=False,
            group_ids=["2"],
        )
        device3 = Device(
            short_name="device3",
            manufacturer_name="super fancy gmbh",
            model="fancy extreme",
            is_public=True,
            is_internal=False,
            is_private=False,
            group_ids=["3"],
        )
        db.session.add_all([device1, device2, device3])
        db.session.commit()

        url1 = "/".join(
            [
                base_url,
                "devices",
                str(device1.id),
                "export-control",
            ]
        )
        response1 = self.client.get(url1)
        self.expect(response1.status_code).to_equal(200)
        data1 = response1.json["data"]
        self.expect(len).of(data1).to_equal(1)
        self.expect(data1[0]["id"]).to_equal(
            str(export_control_of_manufacturer_model1.id)
        )

        url2 = "/".join(
            [
                base_url,
                "devices",
                str(device2.id),
                "export-control",
            ]
        )
        response2 = self.client.get(url2)
        self.expect(response2.status_code).to_equal(200)
        data2 = response2.json["data"]
        self.expect(len).of(data2).to_equal(1)
        self.expect(data2[0]["id"]).to_equal(
            str(export_control_of_manufacturer_model2.id)
        )

        url3 = "/".join(
            [
                base_url,
                "devices",
                str(device3.id),
                "export-control",
            ]
        )
        response3 = self.client.get(url3)
        self.expect(response3.status_code).to_equal(200)
        data3 = response3.json["data"]
        self.expect(len).of(data3).to_equal(0)

        url4 = f"{base_url}/platoforms/9999999/export-control"
        response4 = self.client.get(url4)
        self.expect(response4.status_code).to_equal(404)

    def test_openapi_docs(self):
        """Ensure we have the endoints documented in the openapi specs."""
        response = self.client.get(f"{base_url}/openapi.json")
        self.expect(response.status_code).to_equal(200)
        endpoints = response.json["paths"]
        expected_methods_by_endpoints = {
            "/export-control": ["get", "post"],
            "/export-control/{export_control_id}": ["get", "patch", "delete"],
        }
        for endpoint, expected_methods in expected_methods_by_endpoints.items():
            self.expect(endpoint).to_be_in(endpoints.keys())
            for method in expected_methods:
                self.expect(endpoints[endpoint].keys()).to_include(method)

    @fixtures.use(["export_control_user", "export_control_of_manufacturer_model1"])
    def test_delete_can_remove_no_longer_used_manufacturer_model(
        self, export_control_user, export_control_of_manufacturer_model1
    ):
        """Ensure we delete the manufacturer model entry if it is no longer in use."""
        with self.run_requests_as(export_control_user):
            response = self.client.delete(
                f"{self.url}/{export_control_of_manufacturer_model1.id}"
            )
        self.expect(response.status_code).to_equal(200)
        self.expect(
            db.session.query(ExportControl)
            .filter_by(id=export_control_of_manufacturer_model1.id)
            .first()
        ).to_equal(None)

        self.expect(
            db.session.query(ManufacturerModel)
            .filter_by(id=export_control_of_manufacturer_model1.manufacturer_model_id)
            .first()
        ).to_equal(None)

    @fixtures.use(["export_control_user", "export_control_of_manufacturer_model1"])
    def test_delete_cant_remove_manufacturer_model_if_used_by_external_system(
        self, export_control_user, export_control_of_manufacturer_model1
    ):
        """Ensure we dont't delete the manufacturer model entry if it refers to an external system."""
        manufacturer_model = export_control_of_manufacturer_model1.manufacturer_model
        manufacturer_model.external_system_name = "GIPP"
        manufacturer_model.external_system_url = (
            "https://gipp.gfz-potsdam.de/instrumentcategory/123"
        )

        db.session.add(manufacturer_model)
        db.session.commit()

        with self.run_requests_as(export_control_user):
            response = self.client.delete(
                f"{self.url}/{export_control_of_manufacturer_model1.id}"
            )
        self.expect(response.status_code).to_equal(200)
        self.expect(
            db.session.query(ExportControl)
            .filter_by(id=export_control_of_manufacturer_model1.id)
            .first()
        ).to_equal(None)

        # The manufacturer model is still there.
        self.expect(
            db.session.query(ManufacturerModel)
            .filter_by(id=export_control_of_manufacturer_model1.manufacturer_model_id)
            .first()
        ).to_equal(manufacturer_model)

    @fixtures.use(["export_control_user", "export_control_of_manufacturer_model1"])
    def test_delete_cant_remove_manufacturer_model_if_used_by_device(
        self, export_control_user, export_control_of_manufacturer_model1
    ):
        """Ensure we dont't delete the manufacturer model entry if it refers to a device."""
        manufacturer_model = export_control_of_manufacturer_model1.manufacturer_model

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
                f"{self.url}/{export_control_of_manufacturer_model1.id}"
            )
        self.expect(response.status_code).to_equal(200)
        self.expect(
            db.session.query(ExportControl)
            .filter_by(id=export_control_of_manufacturer_model1.id)
            .first()
        ).to_equal(None)

        # The manufacturer model is still there.
        self.expect(
            db.session.query(ManufacturerModel)
            .filter_by(id=export_control_of_manufacturer_model1.manufacturer_model_id)
            .first()
        ).to_equal(manufacturer_model)

    @fixtures.use(["export_control_user", "export_control_of_manufacturer_model1"])
    def test_delete_cant_remove_manufacturer_model_if_used_by_platform(
        self, export_control_user, export_control_of_manufacturer_model1
    ):
        """Ensure we dont't delete the manufacturer model entry if it refers to a platform."""
        manufacturer_model = export_control_of_manufacturer_model1.manufacturer_model

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
                f"{self.url}/{export_control_of_manufacturer_model1.id}"
            )
        self.expect(response.status_code).to_equal(200)
        self.expect(
            db.session.query(ExportControl)
            .filter_by(id=export_control_of_manufacturer_model1.id)
            .first()
        ).to_equal(None)

        # The manufacturer model is still there.
        self.expect(
            db.session.query(ManufacturerModel)
            .filter_by(id=export_control_of_manufacturer_model1.manufacturer_model_id)
            .first()
        ).to_equal(manufacturer_model)

    @fixtures.use(["export_control_user", "export_control_of_manufacturer_model1"])
    def test_delete_cant_remove_manufacturer_model_if_used_by_attachment(
        self, export_control_user, export_control_of_manufacturer_model1
    ):
        """Ensure we dont't delete the manufacturer model entry if it refers to an attachment."""
        manufacturer_model = export_control_of_manufacturer_model1.manufacturer_model

        attachment = ExportControlAttachment(
            label="test",
            url="https://gfz-potsdam.de",
            manufacturer_model=manufacturer_model,
            is_export_control_only=True,
        )

        db.session.add(attachment)
        db.session.commit()

        with self.run_requests_as(export_control_user):
            response = self.client.delete(
                f"{self.url}/{export_control_of_manufacturer_model1.id}"
            )
        self.expect(response.status_code).to_equal(200)
        self.expect(
            db.session.query(ExportControl)
            .filter_by(id=export_control_of_manufacturer_model1.id)
            .first()
        ).to_equal(None)

        # The manufacturer model is still there.
        self.expect(
            db.session.query(ManufacturerModel)
            .filter_by(id=export_control_of_manufacturer_model1.manufacturer_model_id)
            .first()
        ).to_equal(manufacturer_model)

    @fixtures.use(
        [
            "export_control_user",
            "export_control_of_manufacturer_model1",
            "manufacturer_model2",
        ]
    )
    def test_patch_move_to_other_manufacturer_model(
        self,
        export_control_user,
        export_control_of_manufacturer_model1,
        manufacturer_model2,
    ):
        """Ensure we can't change the associated manufacturer model of an export control dataset via the api."""
        payload = {
            "data": {
                "type": "export_control",
                "id": str(export_control_of_manufacturer_model1.id),
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
                self.url + f"/{export_control_of_manufacturer_model1.id}",
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.expect(response.status_code).to_equal(409)

    @fixtures.use(["export_control_user", "export_control_of_manufacturer_model1"])
    def test_dont_allow_to_add_two_export_control_data_for_same_manufacturer_model(
        self, export_control_user, export_control_of_manufacturer_model1
    ):
        """Ensure we can't add 2 export control information for the same manufacturer model."""
        payload = {
            "data": {
                "type": "export_control",
                "attributes": {
                    "dual_use": False,
                    "additional_information": "No need to worry",
                },
                "relationships": {
                    "manufacturer_model": {
                        "data": {
                            "id": str(
                                export_control_of_manufacturer_model1.manufacturer_model_id
                            ),
                            "type": "manufacturer_model",
                        }
                    }
                },
            }
        }
        with self.run_requests_as(export_control_user):
            response = self.client.post(
                self.url,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.expect(response.status_code).to_equal(409)
