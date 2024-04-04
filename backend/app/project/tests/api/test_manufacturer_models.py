# SPDX-FileCopyrightText: 2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Tests for the manufacturer model endpoints."""

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


@fixtures.register("user1", scope=lambda: db.session)
@fixtures.use(["contact1"])
def create_user1(contact1):
    """Create a normal user to use it in the tests."""
    result = User(contact=contact1, subject=contact1.email)
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


@fixtures.register("export_control_contact", scope=lambda: db.session)
def create_export_control_contact():
    """Create a contact that can be used to make an export control user."""
    result = Contact(
        given_name="export", family_name="contact", email="super.contact@localhost"
    )
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


@fixtures.register("manufacturer_model1", scope=lambda: db.session)
def create_manufacturer_model1():
    """Create a manufacturer model."""
    result = ManufacturerModel(
        manufacturer_name="TRUEBENER GmbH",
        model="SMT 100",
        external_system_name=None,
        external_system_url=None,
    )
    db.session.add(result)
    db.session.commit()
    return result


@fixtures.register("manufacturer_model2", scope=lambda: db.session)
def create_manufacturer_model2():
    """Create another manufacturer model."""
    result = ManufacturerModel(
        manufacturer_name="Campbell",
        model="CRS 1000",
        external_system_name=None,
        external_system_url=None,
    )
    db.session.add(result)
    db.session.commit()
    return result


@fixtures.register("export_control_of_manufacturer_model1", scope=lambda: db.session)
@fixtures.use(["manufacturer_model1"])
def create_export_control_of_manufacturer_model1(manufacturer_model1):
    """Create the export control data for the manufacturer model1."""
    result = ExportControl(
        manufacturer_model=manufacturer_model1,
        internal_note="internal only",
        dual_use=False,
        additional_information="Don't worry",
    )
    db.session.add(result)
    db.session.commit()
    return result


class TestManuafacturerModels(BaseTestCase):
    """Test the api for the manufacturer models."""

    url = base_url + "/manufacturer-models"

    def test_get_list_empty(self):
        """Ensure we can get the empty list."""
        response = self.client.get(self.url)
        self.expect(response.status_code).to_equal(200)
        self.expect(response.json["data"]).to_equal([])

    @fixtures.use(["manufacturer_model1", "manufacturer_model2"])
    def test_get_list_with_content(self, manufacturer_model1, manufacturer_model2):
        """Ensure we can get the content."""
        response = self.client.get(self.url)
        self.expect(response.status_code).to_equal(200)
        data = response.json["data"]
        self.expect(len).of(data).to_equal(2)
        self.expect(data[0]["attributes"]).to_equal(
            {
                "manufacturer_name": manufacturer_model1.manufacturer_name,
                "model": manufacturer_model1.model,
                "external_system_name": None,
                "external_system_url": None,
            }
        )
        self.expect(data[0]["attributes"]["model"]).to_equal("SMT 100")
        self.expect(data[1]["attributes"]["model"]).to_equal("CRS 1000")

    def test_get_one_non_existing(self):
        """Ensure we return a 404 response if the element doesn't exist."""
        response = self.client.get(self.url + "/123456789")
        self.expect(response.status_code).to_equal(404)

    @fixtures.use(["manufacturer_model1"])
    def test_get_one_with_data(self, manufacturer_model1):
        """Ensure we can get a one element."""
        response = self.client.get(self.url + f"/{manufacturer_model1.id}")
        self.expect(response.status_code).to_equal(200)
        data = response.json["data"]
        self.expect(data["type"]).to_equal("manufacturer_model")
        self.expect(data["id"]).to_equal(str(manufacturer_model1.id))
        self.expect(data["attributes"]).to_equal(
            {
                "manufacturer_name": manufacturer_model1.manufacturer_name,
                "model": manufacturer_model1.model,
                "external_system_name": None,
                "external_system_url": None,
            }
        )

    def test_post_not_allowed_no_user(self):
        """Ensure we can't post if we have no user."""
        response = self.client.post(
            self.url,
            json.dumps(
                {
                    "data": {
                        "type": "manufacturer_model",
                        "attributes": {
                            "manufacturer_name": "Fancy",
                            "model": "super fancy",
                            "external_system_name": None,
                            "external_system_url": None,
                        },
                    }
                }
            ),
            content_type="application/vnd.api+json",
        )
        self.expect(response.status_code).to_equal(401)

    @fixtures.use(["user1"])
    def test_post_not_allowed_normal_user(self, user1):
        """Ensure we can't post if we are normal user."""
        with self.run_requests_as(user1):
            response = self.client.post(
                self.url,
                json.dumps(
                    {
                        "data": {
                            "type": "manufacturer_model",
                            "attributes": {
                                "manufacturer_name": "Fancy",
                                "model": "super fancy",
                                "external_system_name": None,
                                "external_system_url": None,
                            },
                        }
                    }
                ),
                content_type="application/vnd.api+json",
            )
        self.expect(response.status_code).to_equal(403)

    @fixtures.use(["super_user"])
    def test_post_not_allowed_super_user(self, super_user):
        """Ensure we can't post even if we are super user."""
        with self.run_requests_as(super_user):
            response = self.client.post(
                self.url,
                json.dumps(
                    {
                        "data": {
                            "type": "manufacturer_model",
                            "attributes": {
                                "manufacturer_name": "Fancy",
                                "model": "super fancy",
                                "external_system_name": None,
                                "external_system_url": None,
                            },
                        }
                    }
                ),
                content_type="application/vnd.api+json",
            )
        self.expect(response.status_code).to_equal(403)

    @fixtures.use(["export_control_user"])
    def test_post_not_allowed_export_control_user(self, export_control_user):
        """Ensure we can't post even if we are export control user."""
        with self.run_requests_as(export_control_user):
            response = self.client.post(
                self.url,
                json.dumps(
                    {
                        "data": {
                            "type": "manufacturer_model",
                            "attributes": {
                                "manufacturer_name": "Fancy",
                                "model": "super fancy",
                                "external_system_name": None,
                                "external_system_url": None,
                            },
                        }
                    }
                ),
                content_type="application/vnd.api+json",
            )
        self.expect(response.status_code).to_equal(403)

    @fixtures.use(["super_user", "manufacturer_model1"])
    def test_patch_not_allowed(self, super_user, manufacturer_model1):
        """Ensure we can't patch even if we are a super user."""
        with self.run_requests_as(super_user):
            response = self.client.patch(
                f"{self.url}/{manufacturer_model1.id}",
                json.dumps(
                    {
                        "data": {
                            "id": f"{manufacturer_model1.id}",
                            "type": "manufacturer_model",
                            "attributes": {"model": "fancy"},
                        }
                    }
                ),
                content_type="application/vnd.api+json",
            )
        self.expect(response.status_code).to_equal(403)

    @fixtures.use(["super_user", "manufacturer_model1"])
    def test_delete_not_allowed(self, super_user, manufacturer_model1):
        """Ensure we can't delete even if we are a super user."""
        with self.run_requests_as(super_user):
            response = self.client.delete(f"{self.url}/{manufacturer_model1.id}")
        self.expect(response.status_code).to_equal(403)

    def test_openapi_docs(self):
        """Ensure we have the GET endpoints documented in the openapi document."""
        response = self.client.get(f"{base_url}/openapi.json")
        self.expect(response.status_code).to_equal(200)
        endpoints = response.json["paths"]
        for expected_endpoint in [
            "/manufacturer-models",
            "/manufacturer-models/{manufacturer_model_id}",
        ]:
            self.expect(expected_endpoint).to_be_in(endpoints.keys())
            self.expect(endpoints[expected_endpoint].keys()).to_have_length(1)
            self.expect(endpoints[expected_endpoint].keys()).to_include("get")

    @fixtures.use(["export_control_of_manufacturer_model1"])
    def test_get_list_export_control_can_be_included(
        self, export_control_of_manufacturer_model1
    ):
        """Ensure we can include the export control information for the list."""
        response = self.client.get(self.url + "?include=export_control")
        self.expect(response.status_code).to_equal(200)
        included = response.json["included"]
        self.expect(len).of(included).to_equal(1)
        self.expect(included[0]["id"]).to_equal(
            str(export_control_of_manufacturer_model1.id)
        )
        self.expect(included[0]["type"]).to_equal("export_control")
        self.expect(included[0]["attributes"]["dual_use"]).to_equal(False)
        self.expect(included[0]["attributes"]["additional_information"]).to_equal(
            export_control_of_manufacturer_model1.additional_information
        )
        self.expect(included[0]["attributes"].keys()).not_.to_include("internal_note")

    @fixtures.use(["export_control_of_manufacturer_model1"])
    def test_get_one_export_control_can_be_included(
        self, export_control_of_manufacturer_model1
    ):
        """Ensure we can include the export control information for the list."""
        manufacturer_model_id = (
            export_control_of_manufacturer_model1.manufacturer_model_id
        )
        url = self.url + f"/{manufacturer_model_id}?include=export_control"
        response = self.client.get(url)
        self.expect(response.status_code).to_equal(200)
        included = response.json["included"]
        self.expect(len).of(included).to_equal(1)
        self.expect(included[0]["id"]).to_equal(
            str(export_control_of_manufacturer_model1.id)
        )
        self.expect(included[0]["type"]).to_equal("export_control")
        self.expect(included[0]["attributes"]["dual_use"]).to_equal(False)
        self.expect(included[0]["attributes"]["additional_information"]).to_equal(
            export_control_of_manufacturer_model1.additional_information
        )
        self.expect(included[0]["attributes"].keys()).not_.to_include("internal_note")


class TestKeepingManufacturerModelsUpToDateByDevices(BaseTestCase):
    """Test cases to keep the manufacturer model table up to date by handling devices."""

    url = base_url + "/devices"

    @fixtures.use(["super_user"])
    def test_add_manufacturer_model_entry_by_adding_internal_device(self, super_user):
        """Ensure we can add a manufacturer model when adding an internal device."""
        self.expect(db.session.query(ManufacturerModel).count()).to_equal(0)

        payload = {
            "data": {
                "type": "device",
                "attributes": {
                    "short_name": "fancy device",
                    "manufacturer_name": "TRUEBENER GmbH",
                    "model": "SMT 100",
                    "is_internal": True,
                    "is_private": False,
                    "is_public": False,
                    "group_ids": ["1"],
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

        all_manufacturer_models = db.session.query(ManufacturerModel).all()

        self.expect(len).of(all_manufacturer_models).to_equal(1)
        manufacturer_model = all_manufacturer_models[0]
        self.expect(manufacturer_model.manufacturer_name).to_equal(
            payload["data"]["attributes"]["manufacturer_name"]
        )
        self.expect(manufacturer_model.model).to_equal(
            payload["data"]["attributes"]["model"]
        )
        self.expect(manufacturer_model.external_system_name).to_equal(None)
        self.expect(manufacturer_model.external_system_url).to_equal(None)

    @fixtures.use(["super_user"])
    def test_add_manufacturer_model_entry_by_adding_public_device(self, super_user):
        """Ensure we can add a manufacturer model when adding a public device."""
        self.expect(db.session.query(ManufacturerModel).count()).to_equal(0)

        payload = {
            "data": {
                "type": "device",
                "attributes": {
                    "short_name": "fancy device",
                    "manufacturer_name": "TRUEBENER GmbH",
                    "model": "SMT 100",
                    "is_internal": False,
                    "is_private": False,
                    "is_public": True,
                    "group_ids": ["1"],
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

        all_manufacturer_models = db.session.query(ManufacturerModel).all()

        self.expect(len).of(all_manufacturer_models).to_equal(1)
        manufacturer_model = all_manufacturer_models[0]
        self.expect(manufacturer_model.manufacturer_name).to_equal(
            payload["data"]["attributes"]["manufacturer_name"]
        )
        self.expect(manufacturer_model.model).to_equal(
            payload["data"]["attributes"]["model"]
        )
        self.expect(manufacturer_model.external_system_name).to_equal(None)
        self.expect(manufacturer_model.external_system_url).to_equal(None)

    @fixtures.use(["super_user"])
    def test_add_manufacturer_model_entry_by_adding_private_device(self, super_user):
        """Ensure we can add a manufacturer model when adding a private device."""
        self.expect(db.session.query(ManufacturerModel).count()).to_equal(0)

        payload = {
            "data": {
                "type": "device",
                "attributes": {
                    "short_name": "fancy device",
                    "manufacturer_name": "TRUEBENER GmbH",
                    "model": "SMT 100",
                    "is_internal": False,
                    "is_private": True,
                    "is_public": False,
                },
                # The "created_by" relationship will be filled by the
                # system automatically.
            }
        }
        with self.run_requests_as(super_user):
            response = self.client.post(
                self.url,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.expect(response.status_code).to_equal(201)

        all_manufacturer_models = db.session.query(ManufacturerModel).all()

        self.expect(len).of(all_manufacturer_models).to_equal(1)
        manufacturer_model = all_manufacturer_models[0]
        self.expect(manufacturer_model.manufacturer_name).to_equal(
            payload["data"]["attributes"]["manufacturer_name"]
        )
        self.expect(manufacturer_model.model).to_equal(
            payload["data"]["attributes"]["model"]
        )
        self.expect(manufacturer_model.external_system_name).to_equal(None)
        self.expect(manufacturer_model.external_system_url).to_equal(None)

    @fixtures.use(["super_user"])
    def test_dont_add_manufacturer_model_entry_without_model(self, super_user):
        """Ensure we don't add a manufacturer model without a model."""
        self.expect(db.session.query(ManufacturerModel).count()).to_equal(0)

        payload = {
            "data": {
                "type": "device",
                "attributes": {
                    "short_name": "fancy device",
                    "manufacturer_name": "TRUEBENER GmbH",
                    "is_internal": True,
                    "is_private": False,
                    "is_public": False,
                    "group_ids": ["1"],
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
        self.expect(db.session.query(ManufacturerModel).count()).to_equal(0)

    @fixtures.use(["super_user"])
    def test_dont_add_manufacturer_model_entry_without_name(self, super_user):
        """Ensure we don't add a manufacturer model without a name."""
        self.expect(db.session.query(ManufacturerModel).count()).to_equal(0)

        payload = {
            "data": {
                "type": "device",
                "attributes": {
                    "short_name": "fancy device",
                    "manufacturer_name": "",
                    "model": "SMT 100",
                    "is_internal": True,
                    "is_private": False,
                    "is_public": False,
                    "group_ids": ["1"],
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
        self.expect(db.session.query(ManufacturerModel).count()).to_equal(0)

    @fixtures.use(["super_user"])
    def test_stay_with_existing_manufacturer_model_entry_on_post(self, super_user):
        """Ensure we don't need to add a manufacturer model if there exists an entry."""
        manufacturer_model = ManufacturerModel(
            manufacturer_name="TRUEBENER GmbH", model="SMT 100"
        )
        db.session.add(manufacturer_model)
        db.session.commit()

        payload = {
            "data": {
                "type": "device",
                "attributes": {
                    "short_name": "fancy device",
                    "manufacturer_name": "TRUEBENER GmbH",
                    "model": "SMT 100",
                    "is_internal": True,
                    "is_private": False,
                    "is_public": False,
                    "group_ids": ["1"],
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

        all_manufacturer_models = db.session.query(ManufacturerModel).all()
        self.expect(len).of(all_manufacturer_models).to_equal(1)

    @fixtures.use(["super_user"])
    def test_remove_manufacturer_model_if_no_usage_left(self, super_user):
        """Ensure we remove a manufacturer model that is no longer in use."""
        device = Device(
            short_name="fancy device",
            manufacturer_name="TRUEBENER GmbH",
            model="SMT 100",
            is_internal=True,
            is_private=False,
            is_public=False,
            group_ids=["1"],
        )
        manufacturer_model = ManufacturerModel(
            manufacturer_name=device.manufacturer_name,
            model=device.model,
        )
        db.session.add_all([device, manufacturer_model])
        db.session.commit()

        with self.run_requests_as(super_user):
            response = self.client.delete(f"{self.url}/{device.id}")
        self.expect(response.status_code).to_equal(200)

        self.expect(db.session.query(ManufacturerModel).count()).to_equal(0)

    @fixtures.use(["super_user"])
    def test_dont_remove_manufacturer_model_if_other_device(self, super_user):
        """Ensure we don't remove a manufacturer model if there is another device that fits."""
        device1 = Device(
            short_name="fancy device",
            manufacturer_name="TRUEBENER GmbH",
            model="SMT 100",
            is_internal=True,
            is_private=False,
            is_public=False,
            group_ids=["1"],
        )
        device2 = Device(
            short_name="other device",
            manufacturer_name="TRUEBENER GmbH",
            model="SMT 100",
            is_internal=True,
            is_private=False,
            is_public=False,
            group_ids=["2"],
        )
        manufacturer_model = ManufacturerModel(
            manufacturer_name=device1.manufacturer_name,
            model=device1.model,
        )
        db.session.add_all([device1, device2, manufacturer_model])
        db.session.commit()

        with self.run_requests_as(super_user):
            response = self.client.delete(f"{self.url}/{device1.id}")
        self.expect(response.status_code).to_equal(200)

        self.expect(db.session.query(ManufacturerModel).count()).to_equal(1)

    @fixtures.use(["super_user"])
    def test_dont_remove_manufacturer_model_if_other_platform(self, super_user):
        """Ensure we don't remove a manufacturer model if there is another platform that fits."""
        device = Device(
            short_name="fancy device",
            manufacturer_name="TRUEBENER GmbH",
            model="SMT 100",
            is_internal=True,
            is_private=False,
            is_public=False,
            group_ids=["1"],
        )
        platform = Platform(
            short_name="other platform",
            manufacturer_name="TRUEBENER GmbH",
            model="SMT 100",
            is_internal=True,
            is_private=False,
            is_public=False,
            group_ids=["2"],
        )
        manufacturer_model = ManufacturerModel(
            manufacturer_name=device.manufacturer_name,
            model=device.model,
        )
        db.session.add_all([device, platform, manufacturer_model])
        db.session.commit()

        with self.run_requests_as(super_user):
            response = self.client.delete(f"{self.url}/{device.id}")
        self.expect(response.status_code).to_equal(200)

        self.expect(db.session.query(ManufacturerModel).count()).to_equal(1)

    @fixtures.use(["super_user"])
    def test_dont_remove_manufacturer_model_if_external_system(self, super_user):
        """Ensure we don't automatically remove manufacturer models that refer to external systems."""
        device = Device(
            short_name="fancy device",
            manufacturer_name="TRUEBENER GmbH",
            model="SMT 100",
            is_internal=True,
            is_private=False,
            is_public=False,
            group_ids=["1"],
        )
        manufacturer_model = ManufacturerModel(
            manufacturer_name=device.manufacturer_name,
            model=device.model,
            external_system_name="GIPP",
            external_system_url="https://gipp.gfz-potsdam.de/instrumentcategories/view/4",
        )
        db.session.add_all([device, manufacturer_model])
        db.session.commit()

        with self.run_requests_as(super_user):
            response = self.client.delete(f"{self.url}/{device.id}")
        self.expect(response.status_code).to_equal(200)

        self.expect(db.session.query(ManufacturerModel).count()).to_equal(1)

    @fixtures.use(["super_user"])
    def test_dont_remove_manufacturer_model_if_already_export_control_information(
        self, super_user
    ):
        """Ensure we don't automatically remove entries for that we have export control data."""
        device = Device(
            short_name="fancy device",
            manufacturer_name="TRUEBENER GmbH",
            model="SMT 100",
            is_internal=True,
            is_private=False,
            is_public=False,
            group_ids=["1"],
        )
        manufacturer_model = ManufacturerModel(
            manufacturer_name=device.manufacturer_name,
            model=device.model,
        )
        export_control = ExportControl(
            manufacturer_model=manufacturer_model, dual_use=True
        )
        db.session.add_all([device, manufacturer_model, export_control])
        db.session.commit()

        with self.run_requests_as(super_user):
            response = self.client.delete(f"{self.url}/{device.id}")
        self.expect(response.status_code).to_equal(200)

        self.expect(db.session.query(ManufacturerModel).count()).to_equal(1)

    @fixtures.use(["super_user"])
    def test_dont_remove_manufacturer_model_if_already_export_control_attachment(
        self, super_user
    ):
        """Ensure we don't automatically remove entries for that we have an export control attachment."""
        device = Device(
            short_name="fancy device",
            manufacturer_name="TRUEBENER GmbH",
            model="SMT 100",
            is_internal=True,
            is_private=False,
            is_public=False,
            group_ids=["1"],
        )
        manufacturer_model = ManufacturerModel(
            manufacturer_name=device.manufacturer_name,
            model=device.model,
        )
        export_control_attachment = ExportControlAttachment(
            manufacturer_model=manufacturer_model,
            label="GFZ",
            url="http://gfz-potsdam.de",
            is_export_control_only=False,
        )
        db.session.add_all([device, manufacturer_model, export_control_attachment])
        db.session.commit()

        with self.run_requests_as(super_user):
            response = self.client.delete(f"{self.url}/{device.id}")
        self.expect(response.status_code).to_equal(200)

        self.expect(db.session.query(ManufacturerModel).count()).to_equal(1)

    @fixtures.use(["super_user"])
    def test_update_removes_old_and_adds_new_manufacturer_model_entry(self, super_user):
        """Ensure that we create a new manufacturer model entry and remove the old one."""
        device = Device(
            short_name="fancy device",
            manufacturer_name="TRUEBENER GmbH",
            model="SMT 100",
            is_internal=True,
            is_private=False,
            is_public=False,
            group_ids=["1"],
        )
        manufacturer_model = ManufacturerModel(
            manufacturer_name=device.manufacturer_name,
            model=device.model,
        )
        db.session.add_all([device, manufacturer_model])
        db.session.commit()

        first_manufacturer_model_id = manufacturer_model.id

        with self.run_requests_as(super_user):
            response = self.client.patch(
                f"{self.url}/{device.id}",
                data=json.dumps(
                    {
                        "data": {
                            "type": "device",
                            "id": str(device.id),
                            "attributes": {
                                "model": "SMT 100 x",
                            },
                        }
                    }
                ),
                content_type="application/vnd.api+json",
            )
        self.expect(response.status_code).to_equal(200)

        all_manufacturer_models = db.session.query(ManufacturerModel).all()

        self.expect(len).of(all_manufacturer_models).to_equal(1)
        self.expect(all_manufacturer_models[0].model).to_equal("SMT 100 x")
        self.expect(all_manufacturer_models[0].id).not_.to_equal(
            first_manufacturer_model_id
        )

    @fixtures.use(["super_user"])
    def test_update_doesnt_remove_old_if_external_system(self, super_user):
        """Ensure that we don't remove the old entry if it is linked to an external system."""
        device = Device(
            short_name="fancy device",
            manufacturer_name="TRUEBENER GmbH",
            model="SMT 100",
            is_internal=True,
            is_private=False,
            is_public=False,
            group_ids=["1"],
        )
        manufacturer_model = ManufacturerModel(
            manufacturer_name=device.manufacturer_name,
            model=device.model,
            external_system_name="GIPP",
            external_system_url="https://gipp.gfz-potsdam.de",
        )
        db.session.add_all([device, manufacturer_model])
        db.session.commit()

        first_manufacturer_model_id = manufacturer_model.id

        with self.run_requests_as(super_user):
            response = self.client.patch(
                f"{self.url}/{device.id}",
                data=json.dumps(
                    {
                        "data": {
                            "type": "device",
                            "id": str(device.id),
                            "attributes": {
                                "model": "SMT 100 x",
                            },
                        }
                    }
                ),
                content_type="application/vnd.api+json",
            )
        self.expect(response.status_code).to_equal(200)

        all_manufacturer_models = db.session.query(ManufacturerModel).all()

        self.expect(len).of(all_manufacturer_models).to_equal(2)
        self.expect(all_manufacturer_models[0].model).to_equal("SMT 100")
        self.expect(all_manufacturer_models[1].model).to_equal("SMT 100 x")
        self.expect(all_manufacturer_models[1].id).not_.to_equal(
            first_manufacturer_model_id
        )

    @fixtures.use(["super_user"])
    def test_update_doesnt_remove_old_if_export_control_information(self, super_user):
        """Ensure that we don't remove the old entry if we have export control data for it."""
        device = Device(
            short_name="fancy device",
            manufacturer_name="TRUEBENER GmbH",
            model="SMT 100",
            is_internal=True,
            is_private=False,
            is_public=False,
            group_ids=["1"],
        )
        manufacturer_model = ManufacturerModel(
            manufacturer_name=device.manufacturer_name,
            model=device.model,
        )
        export_control = ExportControl(
            manufacturer_model=manufacturer_model,
            dual_use=True,
        )
        db.session.add_all([device, manufacturer_model, export_control])
        db.session.commit()

        first_manufacturer_model_id = manufacturer_model.id

        with self.run_requests_as(super_user):
            response = self.client.patch(
                f"{self.url}/{device.id}",
                data=json.dumps(
                    {
                        "data": {
                            "type": "device",
                            "id": str(device.id),
                            "attributes": {
                                "model": "SMT 100 x",
                            },
                        }
                    }
                ),
                content_type="application/vnd.api+json",
            )
        self.expect(response.status_code).to_equal(200)

        all_manufacturer_models = db.session.query(ManufacturerModel).all()

        self.expect(len).of(all_manufacturer_models).to_equal(2)
        self.expect(all_manufacturer_models[0].model).to_equal("SMT 100")
        self.expect(all_manufacturer_models[1].model).to_equal("SMT 100 x")
        self.expect(all_manufacturer_models[1].id).not_.to_equal(
            first_manufacturer_model_id
        )

    @fixtures.use(["super_user"])
    def test_update_doesnt_remove_old_if_export_control_attachment(self, super_user):
        """Ensure that we don't remove the old entry if we have an export control attachment."""
        device = Device(
            short_name="fancy device",
            manufacturer_name="TRUEBENER GmbH",
            model="SMT 100",
            is_internal=True,
            is_private=False,
            is_public=False,
            group_ids=["1"],
        )
        manufacturer_model = ManufacturerModel(
            manufacturer_name=device.manufacturer_name,
            model=device.model,
        )
        export_control_attachment = ExportControlAttachment(
            manufacturer_model=manufacturer_model,
            label="GFZ",
            url="http://gfz-potsdam.de",
            is_export_control_only=False,
        )
        db.session.add_all([device, manufacturer_model, export_control_attachment])
        db.session.commit()

        first_manufacturer_model_id = manufacturer_model.id

        with self.run_requests_as(super_user):
            response = self.client.patch(
                f"{self.url}/{device.id}",
                data=json.dumps(
                    {
                        "data": {
                            "type": "device",
                            "id": str(device.id),
                            "attributes": {
                                "model": "SMT 100 x",
                            },
                        }
                    }
                ),
                content_type="application/vnd.api+json",
            )
        self.expect(response.status_code).to_equal(200)

        all_manufacturer_models = db.session.query(ManufacturerModel).all()

        self.expect(len).of(all_manufacturer_models).to_equal(2)
        self.expect(all_manufacturer_models[0].model).to_equal("SMT 100")
        self.expect(all_manufacturer_models[1].model).to_equal("SMT 100 x")
        self.expect(all_manufacturer_models[1].id).not_.to_equal(
            first_manufacturer_model_id
        )

    @fixtures.use(["super_user"])
    def test_update_doesnt_remove_old_if_other_device(self, super_user):
        """Ensure that we don't remove the old entry if we have another device for it."""
        device1 = Device(
            short_name="fancy device",
            manufacturer_name="TRUEBENER GmbH",
            model="SMT 100",
            is_internal=True,
            is_private=False,
            is_public=False,
            group_ids=["1"],
        )
        device2 = Device(
            short_name="other device",
            manufacturer_name="TRUEBENER GmbH",
            model="SMT 100",
            is_internal=True,
            is_private=False,
            is_public=False,
            group_ids=["2"],
        )
        manufacturer_model = ManufacturerModel(
            manufacturer_name=device1.manufacturer_name,
            model=device1.model,
        )
        db.session.add_all([device1, device2, manufacturer_model])
        db.session.commit()

        first_manufacturer_model_id = manufacturer_model.id

        with self.run_requests_as(super_user):
            response = self.client.patch(
                f"{self.url}/{device1.id}",
                data=json.dumps(
                    {
                        "data": {
                            "type": "device",
                            "id": str(device1.id),
                            "attributes": {
                                "model": "SMT 100 x",
                            },
                        }
                    }
                ),
                content_type="application/vnd.api+json",
            )
        self.expect(response.status_code).to_equal(200)

        all_manufacturer_models = db.session.query(ManufacturerModel).all()

        self.expect(len).of(all_manufacturer_models).to_equal(2)
        self.expect(all_manufacturer_models[0].model).to_equal("SMT 100")
        self.expect(all_manufacturer_models[1].model).to_equal("SMT 100 x")
        self.expect(all_manufacturer_models[1].id).not_.to_equal(
            first_manufacturer_model_id
        )

    @fixtures.use(["super_user"])
    def test_update_doesnt_remove_old_if_other_platform(self, super_user):
        """Ensure that we don't remove the old entry if we have another platform for it."""
        device = Device(
            short_name="fancy device",
            manufacturer_name="TRUEBENER GmbH",
            model="SMT 100",
            is_internal=True,
            is_private=False,
            is_public=False,
            group_ids=["1"],
        )
        platform = Platform(
            short_name="other platform",
            manufacturer_name="TRUEBENER GmbH",
            model="SMT 100",
            is_internal=True,
            is_private=False,
            is_public=False,
            group_ids=["2"],
        )
        manufacturer_model = ManufacturerModel(
            manufacturer_name=device.manufacturer_name,
            model=device.model,
        )
        db.session.add_all([device, platform, manufacturer_model])
        db.session.commit()

        first_manufacturer_model_id = manufacturer_model.id

        with self.run_requests_as(super_user):
            response = self.client.patch(
                f"{self.url}/{device.id}",
                data=json.dumps(
                    {
                        "data": {
                            "type": "device",
                            "id": str(device.id),
                            "attributes": {
                                "model": "SMT 100 x",
                            },
                        }
                    }
                ),
                content_type="application/vnd.api+json",
            )
        self.expect(response.status_code).to_equal(200)

        all_manufacturer_models = db.session.query(ManufacturerModel).all()

        self.expect(len).of(all_manufacturer_models).to_equal(2)
        self.expect(all_manufacturer_models[0].model).to_equal("SMT 100")
        self.expect(all_manufacturer_models[1].model).to_equal("SMT 100 x")
        self.expect(all_manufacturer_models[1].id).not_.to_equal(
            first_manufacturer_model_id
        )


class TestKeepingManufacturerModelsUpToDateByPlatforms(BaseTestCase):
    """Test cases to keep the manufacturer model table up to date by handling platforms."""

    url = base_url + "/platforms"

    @fixtures.use(["super_user"])
    def test_add_manufacturer_model_entry_by_adding_internal_platform(self, super_user):
        """Ensure we can add a manufacturer model when adding an internal platform."""
        self.expect(db.session.query(ManufacturerModel).count()).to_equal(0)

        payload = {
            "data": {
                "type": "platform",
                "attributes": {
                    "short_name": "fancy platform",
                    "manufacturer_name": "TRUEBENER GmbH",
                    "model": "SMT 100",
                    "is_internal": True,
                    "is_private": False,
                    "is_public": False,
                    "group_ids": ["1"],
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

        all_manufacturer_models = db.session.query(ManufacturerModel).all()

        self.expect(len).of(all_manufacturer_models).to_equal(1)
        manufacturer_model = all_manufacturer_models[0]
        self.expect(manufacturer_model.manufacturer_name).to_equal(
            payload["data"]["attributes"]["manufacturer_name"]
        )
        self.expect(manufacturer_model.model).to_equal(
            payload["data"]["attributes"]["model"]
        )
        self.expect(manufacturer_model.external_system_name).to_equal(None)
        self.expect(manufacturer_model.external_system_url).to_equal(None)

    @fixtures.use(["super_user"])
    def test_add_manufacturer_model_entry_by_adding_public_platform(self, super_user):
        """Ensure we can add a manufacturer model when adding a public platform."""
        self.expect(db.session.query(ManufacturerModel).count()).to_equal(0)

        payload = {
            "data": {
                "type": "platform",
                "attributes": {
                    "short_name": "fancy platform",
                    "manufacturer_name": "TRUEBENER GmbH",
                    "model": "SMT 100",
                    "is_internal": False,
                    "is_private": False,
                    "is_public": True,
                    "group_ids": ["1"],
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

        all_manufacturer_models = db.session.query(ManufacturerModel).all()

        self.expect(len).of(all_manufacturer_models).to_equal(1)
        manufacturer_model = all_manufacturer_models[0]
        self.expect(manufacturer_model.manufacturer_name).to_equal(
            payload["data"]["attributes"]["manufacturer_name"]
        )
        self.expect(manufacturer_model.model).to_equal(
            payload["data"]["attributes"]["model"]
        )
        self.expect(manufacturer_model.external_system_name).to_equal(None)
        self.expect(manufacturer_model.external_system_url).to_equal(None)

    @fixtures.use(["super_user"])
    def test_add_manufacturer_model_entry_by_adding_private_platform(self, super_user):
        """Ensure we can add a manufacturer model when adding a private platform."""
        self.expect(db.session.query(ManufacturerModel).count()).to_equal(0)

        payload = {
            "data": {
                "type": "platform",
                "attributes": {
                    "short_name": "fancy platform",
                    "manufacturer_name": "TRUEBENER GmbH",
                    "model": "SMT 100",
                    "is_internal": False,
                    "is_private": True,
                    "is_public": False,
                },
                # "created_by" relationship will be set by the system.
            }
        }
        with self.run_requests_as(super_user):
            response = self.client.post(
                self.url,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.expect(response.status_code).to_equal(201)

        all_manufacturer_models = db.session.query(ManufacturerModel).all()

        self.expect(len).of(all_manufacturer_models).to_equal(1)
        manufacturer_model = all_manufacturer_models[0]
        self.expect(manufacturer_model.manufacturer_name).to_equal(
            payload["data"]["attributes"]["manufacturer_name"]
        )
        self.expect(manufacturer_model.model).to_equal(
            payload["data"]["attributes"]["model"]
        )
        self.expect(manufacturer_model.external_system_name).to_equal(None)
        self.expect(manufacturer_model.external_system_url).to_equal(None)

    @fixtures.use(["super_user"])
    def test_dont_add_manufacturer_model_entry_without_model(self, super_user):
        """Ensure we don't add a manufacturer model without a model."""
        self.expect(db.session.query(ManufacturerModel).count()).to_equal(0)

        payload = {
            "data": {
                "type": "platform",
                "attributes": {
                    "short_name": "fancy platform",
                    "manufacturer_name": "TRUEBENER GmbH",
                    "is_internal": True,
                    "is_private": False,
                    "is_public": False,
                    "group_ids": ["1"],
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
        self.expect(db.session.query(ManufacturerModel).count()).to_equal(0)

    @fixtures.use(["super_user"])
    def test_dont_add_manufacturer_model_entry_without_name(self, super_user):
        """Ensure we don't add a manufacturer model without a name."""
        self.expect(db.session.query(ManufacturerModel).count()).to_equal(0)

        payload = {
            "data": {
                "type": "platform",
                "attributes": {
                    "short_name": "fancy platform",
                    "manufacturer_name": "",
                    "model": "SMT 100",
                    "is_internal": True,
                    "is_private": False,
                    "is_public": False,
                    "group_ids": ["1"],
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
        self.expect(db.session.query(ManufacturerModel).count()).to_equal(0)

    @fixtures.use(["super_user"])
    def test_stay_with_existing_manufacturer_model_entry_on_post(self, super_user):
        """Ensure we don't need to add a manufacturer model if there exists an entry."""
        manufacturer_model = ManufacturerModel(
            manufacturer_name="TRUEBENER GmbH", model="SMT 100"
        )
        db.session.add(manufacturer_model)
        db.session.commit()

        payload = {
            "data": {
                "type": "platform",
                "attributes": {
                    "short_name": "fancy platform",
                    "manufacturer_name": "TRUEBENER GmbH",
                    "model": "SMT 100",
                    "is_internal": True,
                    "is_private": False,
                    "is_public": False,
                    "group_ids": ["1"],
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

        all_manufacturer_models = db.session.query(ManufacturerModel).all()
        self.expect(len).of(all_manufacturer_models).to_equal(1)

    @fixtures.use(["super_user"])
    def test_remove_manufacturer_model_if_no_usage_left(self, super_user):
        """Ensure we remove a manufacturer model that is no longer in use."""
        platform = Platform(
            short_name="fancy platform",
            manufacturer_name="TRUEBENER GmbH",
            model="SMT 100",
            is_internal=True,
            is_private=False,
            is_public=False,
            group_ids=["1"],
        )
        manufacturer_model = ManufacturerModel(
            manufacturer_name=platform.manufacturer_name,
            model=platform.model,
        )
        db.session.add_all([platform, manufacturer_model])
        db.session.commit()

        with self.run_requests_as(super_user):
            response = self.client.delete(f"{self.url}/{platform.id}")
        self.expect(response.status_code).to_equal(200)

        self.expect(db.session.query(ManufacturerModel).count()).to_equal(0)

    @fixtures.use(["super_user"])
    def test_dont_remove_manufacturer_model_if_other_platform(self, super_user):
        """Ensure we don't remove a manufacturer model if there is another platform that fits."""
        platform1 = Platform(
            short_name="fancy platform",
            manufacturer_name="TRUEBENER GmbH",
            model="SMT 100",
            is_internal=True,
            is_private=False,
            is_public=False,
            group_ids=["1"],
        )
        platform2 = Platform(
            short_name="other platform",
            manufacturer_name="TRUEBENER GmbH",
            model="SMT 100",
            is_internal=True,
            is_private=False,
            is_public=False,
            group_ids=["2"],
        )
        manufacturer_model = ManufacturerModel(
            manufacturer_name=platform1.manufacturer_name,
            model=platform1.model,
        )
        db.session.add_all([platform1, platform2, manufacturer_model])
        db.session.commit()

        with self.run_requests_as(super_user):
            response = self.client.delete(f"{self.url}/{platform1.id}")
        self.expect(response.status_code).to_equal(200)

        self.expect(db.session.query(ManufacturerModel).count()).to_equal(1)

    @fixtures.use(["super_user"])
    def test_dont_remove_manufacturer_model_if_other_device(self, super_user):
        """Ensure we don't remove a manufacturer model if there is another device that fits."""
        platform = Platform(
            short_name="fancy platform",
            manufacturer_name="TRUEBENER GmbH",
            model="SMT 100",
            is_internal=True,
            is_private=False,
            is_public=False,
            group_ids=["1"],
        )
        device = Device(
            short_name="other device",
            manufacturer_name="TRUEBENER GmbH",
            model="SMT 100",
            is_internal=True,
            is_private=False,
            is_public=False,
            group_ids=["2"],
        )
        manufacturer_model = ManufacturerModel(
            manufacturer_name=platform.manufacturer_name,
            model=platform.model,
        )
        db.session.add_all([platform, device, manufacturer_model])
        db.session.commit()

        with self.run_requests_as(super_user):
            response = self.client.delete(f"{self.url}/{platform.id}")
        self.expect(response.status_code).to_equal(200)

        self.expect(db.session.query(ManufacturerModel).count()).to_equal(1)

    @fixtures.use(["super_user"])
    def test_dont_remove_manufacturer_model_if_external_system(self, super_user):
        """Ensure we don't automatically remove manufacturer models that refer to external systems."""
        platform = Platform(
            short_name="fancy platform",
            manufacturer_name="TRUEBENER GmbH",
            model="SMT 100",
            is_internal=True,
            is_private=False,
            is_public=False,
            group_ids=["1"],
        )
        manufacturer_model = ManufacturerModel(
            manufacturer_name=platform.manufacturer_name,
            model=platform.model,
            external_system_name="GIPP",
            external_system_url="https://gipp.gfz-potsdam.de/instrumentcategories/view/4",
        )
        db.session.add_all([platform, manufacturer_model])
        db.session.commit()

        with self.run_requests_as(super_user):
            response = self.client.delete(f"{self.url}/{platform.id}")
        self.expect(response.status_code).to_equal(200)

        self.expect(db.session.query(ManufacturerModel).count()).to_equal(1)

    @fixtures.use(["super_user"])
    def test_dont_remove_manufacturer_model_if_already_export_control_information(
        self, super_user
    ):
        """Ensure we don't automatically remove entries for that we have export control data."""
        platform = Platform(
            short_name="fancy platform",
            manufacturer_name="TRUEBENER GmbH",
            model="SMT 100",
            is_internal=True,
            is_private=False,
            is_public=False,
            group_ids=["1"],
        )
        manufacturer_model = ManufacturerModel(
            manufacturer_name=platform.manufacturer_name,
            model=platform.model,
        )
        export_control = ExportControl(
            manufacturer_model=manufacturer_model, dual_use=True
        )
        db.session.add_all([platform, manufacturer_model, export_control])
        db.session.commit()

        with self.run_requests_as(super_user):
            response = self.client.delete(f"{self.url}/{platform.id}")
        self.expect(response.status_code).to_equal(200)

        self.expect(db.session.query(ManufacturerModel).count()).to_equal(1)

    @fixtures.use(["super_user"])
    def test_dont_remove_manufacturer_model_if_already_export_control_attachment(
        self, super_user
    ):
        """Ensure we don't automatically remove entries for that we have export control attachments."""
        platform = Platform(
            short_name="fancy platform",
            manufacturer_name="TRUEBENER GmbH",
            model="SMT 100",
            is_internal=True,
            is_private=False,
            is_public=False,
            group_ids=["1"],
        )
        manufacturer_model = ManufacturerModel(
            manufacturer_name=platform.manufacturer_name,
            model=platform.model,
        )
        export_control_attachment = ExportControlAttachment(
            manufacturer_model=manufacturer_model,
            label="GFZ",
            url="http://gfz-potsdam.de",
            is_export_control_only=False,
        )
        db.session.add_all([platform, manufacturer_model, export_control_attachment])
        db.session.commit()

        with self.run_requests_as(super_user):
            response = self.client.delete(f"{self.url}/{platform.id}")
        self.expect(response.status_code).to_equal(200)

        self.expect(db.session.query(ManufacturerModel).count()).to_equal(1)

    @fixtures.use(["super_user"])
    def test_update_removes_old_and_adds_new_manufacturer_model_entry(self, super_user):
        """Ensure that we create a new manufacturer model entry and remove the old one."""
        platform = Platform(
            short_name="fancy platform",
            manufacturer_name="TRUEBENER GmbH",
            model="SMT 100",
            is_internal=True,
            is_private=False,
            is_public=False,
            group_ids=["1"],
        )
        manufacturer_model = ManufacturerModel(
            manufacturer_name=platform.manufacturer_name,
            model=platform.model,
        )
        db.session.add_all([platform, manufacturer_model])
        db.session.commit()

        first_manufacturer_model_id = manufacturer_model.id

        with self.run_requests_as(super_user):
            response = self.client.patch(
                f"{self.url}/{platform.id}",
                data=json.dumps(
                    {
                        "data": {
                            "type": "platform",
                            "id": str(platform.id),
                            "attributes": {
                                "model": "SMT 100 x",
                            },
                        }
                    }
                ),
                content_type="application/vnd.api+json",
            )
        self.expect(response.status_code).to_equal(200)

        all_manufacturer_models = db.session.query(ManufacturerModel).all()

        self.expect(len).of(all_manufacturer_models).to_equal(1)
        self.expect(all_manufacturer_models[0].model).to_equal("SMT 100 x")
        self.expect(all_manufacturer_models[0].id).not_.to_equal(
            first_manufacturer_model_id
        )

    @fixtures.use(["super_user"])
    def test_update_doesnt_remove_old_if_external_system(self, super_user):
        """Ensure that we don't remove the old entry if it is linked to an external system."""
        platform = Platform(
            short_name="fancy platform",
            manufacturer_name="TRUEBENER GmbH",
            model="SMT 100",
            is_internal=True,
            is_private=False,
            is_public=False,
            group_ids=["1"],
        )
        manufacturer_model = ManufacturerModel(
            manufacturer_name=platform.manufacturer_name,
            model=platform.model,
            external_system_name="GIPP",
            external_system_url="https://gipp.gfz-potsdam.de",
        )
        db.session.add_all([platform, manufacturer_model])
        db.session.commit()

        first_manufacturer_model_id = manufacturer_model.id

        with self.run_requests_as(super_user):
            response = self.client.patch(
                f"{self.url}/{platform.id}",
                data=json.dumps(
                    {
                        "data": {
                            "type": "platform",
                            "id": str(platform.id),
                            "attributes": {
                                "model": "SMT 100 x",
                            },
                        }
                    }
                ),
                content_type="application/vnd.api+json",
            )
        self.expect(response.status_code).to_equal(200)

        all_manufacturer_models = db.session.query(ManufacturerModel).all()

        self.expect(len).of(all_manufacturer_models).to_equal(2)
        self.expect(all_manufacturer_models[0].model).to_equal("SMT 100")
        self.expect(all_manufacturer_models[1].model).to_equal("SMT 100 x")
        self.expect(all_manufacturer_models[1].id).not_.to_equal(
            first_manufacturer_model_id
        )

    @fixtures.use(["super_user"])
    def test_update_doesnt_remove_old_if_export_control_information(self, super_user):
        """Ensure that we don't remove the old entry if we have export control data for it."""
        platform = Platform(
            short_name="fancy platform",
            manufacturer_name="TRUEBENER GmbH",
            model="SMT 100",
            is_internal=True,
            is_private=False,
            is_public=False,
            group_ids=["1"],
        )
        manufacturer_model = ManufacturerModel(
            manufacturer_name=platform.manufacturer_name,
            model=platform.model,
        )
        export_control = ExportControl(
            manufacturer_model=manufacturer_model,
            dual_use=True,
        )
        db.session.add_all([platform, manufacturer_model, export_control])
        db.session.commit()

        first_manufacturer_model_id = manufacturer_model.id

        with self.run_requests_as(super_user):
            response = self.client.patch(
                f"{self.url}/{platform.id}",
                data=json.dumps(
                    {
                        "data": {
                            "type": "platform",
                            "id": str(platform.id),
                            "attributes": {
                                "model": "SMT 100 x",
                            },
                        }
                    }
                ),
                content_type="application/vnd.api+json",
            )
        self.expect(response.status_code).to_equal(200)

        all_manufacturer_models = db.session.query(ManufacturerModel).all()

        self.expect(len).of(all_manufacturer_models).to_equal(2)
        self.expect(all_manufacturer_models[0].model).to_equal("SMT 100")
        self.expect(all_manufacturer_models[1].model).to_equal("SMT 100 x")
        self.expect(all_manufacturer_models[1].id).not_.to_equal(
            first_manufacturer_model_id
        )

    @fixtures.use(["super_user"])
    def test_update_doesnt_remove_old_if_export_control_attachment(self, super_user):
        """Ensure that we don't remove the old entry if we have export control attachments for it."""
        platform = Platform(
            short_name="fancy platform",
            manufacturer_name="TRUEBENER GmbH",
            model="SMT 100",
            is_internal=True,
            is_private=False,
            is_public=False,
            group_ids=["1"],
        )
        manufacturer_model = ManufacturerModel(
            manufacturer_name=platform.manufacturer_name,
            model=platform.model,
        )
        export_control_attachment = ExportControlAttachment(
            manufacturer_model=manufacturer_model,
            label="GFZ",
            url="http://gfz-potsdam.de",
            is_export_control_only=False,
        )
        db.session.add_all([platform, manufacturer_model, export_control_attachment])
        db.session.commit()

        first_manufacturer_model_id = manufacturer_model.id

        with self.run_requests_as(super_user):
            response = self.client.patch(
                f"{self.url}/{platform.id}",
                data=json.dumps(
                    {
                        "data": {
                            "type": "platform",
                            "id": str(platform.id),
                            "attributes": {
                                "model": "SMT 100 x",
                            },
                        }
                    }
                ),
                content_type="application/vnd.api+json",
            )
        self.expect(response.status_code).to_equal(200)

        all_manufacturer_models = db.session.query(ManufacturerModel).all()

        self.expect(len).of(all_manufacturer_models).to_equal(2)
        self.expect(all_manufacturer_models[0].model).to_equal("SMT 100")
        self.expect(all_manufacturer_models[1].model).to_equal("SMT 100 x")
        self.expect(all_manufacturer_models[1].id).not_.to_equal(
            first_manufacturer_model_id
        )

    @fixtures.use(["super_user"])
    def test_update_doesnt_remove_old_if_other_platform(self, super_user):
        """Ensure that we don't remove the old entry if we have another platform for it."""
        platform1 = Platform(
            short_name="fancy platform",
            manufacturer_name="TRUEBENER GmbH",
            model="SMT 100",
            is_internal=True,
            is_private=False,
            is_public=False,
            group_ids=["1"],
        )
        platform2 = Platform(
            short_name="other platform",
            manufacturer_name="TRUEBENER GmbH",
            model="SMT 100",
            is_internal=True,
            is_private=False,
            is_public=False,
            group_ids=["2"],
        )
        manufacturer_model = ManufacturerModel(
            manufacturer_name=platform1.manufacturer_name,
            model=platform1.model,
        )
        db.session.add_all([platform1, platform2, manufacturer_model])
        db.session.commit()

        first_manufacturer_model_id = manufacturer_model.id

        with self.run_requests_as(super_user):
            response = self.client.patch(
                f"{self.url}/{platform1.id}",
                data=json.dumps(
                    {
                        "data": {
                            "type": "platform",
                            "id": str(platform1.id),
                            "attributes": {
                                "model": "SMT 100 x",
                            },
                        }
                    }
                ),
                content_type="application/vnd.api+json",
            )
        self.expect(response.status_code).to_equal(200)

        all_manufacturer_models = db.session.query(ManufacturerModel).all()

        self.expect(len).of(all_manufacturer_models).to_equal(2)
        self.expect(all_manufacturer_models[0].model).to_equal("SMT 100")
        self.expect(all_manufacturer_models[1].model).to_equal("SMT 100 x")
        self.expect(all_manufacturer_models[1].id).not_.to_equal(
            first_manufacturer_model_id
        )

    @fixtures.use(["super_user"])
    def test_update_doesnt_remove_old_if_other_device(self, super_user):
        """Ensure that we don't remove the old entry if we have another device for it."""
        platform = Platform(
            short_name="fancy platform",
            manufacturer_name="TRUEBENER GmbH",
            model="SMT 100",
            is_internal=True,
            is_private=False,
            is_public=False,
            group_ids=["1"],
        )
        device = Device(
            short_name="other device",
            manufacturer_name="TRUEBENER GmbH",
            model="SMT 100",
            is_internal=True,
            is_private=False,
            is_public=False,
            group_ids=["2"],
        )
        manufacturer_model = ManufacturerModel(
            manufacturer_name=platform.manufacturer_name,
            model=platform.model,
        )
        db.session.add_all([platform, device, manufacturer_model])
        db.session.commit()

        first_manufacturer_model_id = manufacturer_model.id

        with self.run_requests_as(super_user):
            response = self.client.patch(
                f"{self.url}/{platform.id}",
                data=json.dumps(
                    {
                        "data": {
                            "type": "platform",
                            "id": str(platform.id),
                            "attributes": {
                                "model": "SMT 100 x",
                            },
                        }
                    }
                ),
                content_type="application/vnd.api+json",
            )
        self.expect(response.status_code).to_equal(200)

        all_manufacturer_models = db.session.query(ManufacturerModel).all()

        self.expect(len).of(all_manufacturer_models).to_equal(2)
        self.expect(all_manufacturer_models[0].model).to_equal("SMT 100")
        self.expect(all_manufacturer_models[1].model).to_equal("SMT 100 x")
        self.expect(all_manufacturer_models[1].id).not_.to_equal(
            first_manufacturer_model_id
        )
