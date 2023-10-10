# SPDX-FileCopyrightText: 2021 - 2023
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Tests for the devices."""

import datetime
import json
import os
from unittest.mock import patch

import pytz
from flask import current_app

from project import base_url, idl
from project.api.models import (
    Configuration,
    Contact,
    CustomField,
    Device,
    DeviceAttachment,
    DeviceMountAction,
    DeviceParameter,
    DeviceParameterValueChangeAction,
    DeviceProperty,
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
from project.tests.models.test_device_calibration_action_model import (
    add_device_calibration_action,
)
from project.tests.models.test_generic_actions_models import (
    generate_device_action_model,
)
from project.tests.models.test_software_update_actions_model import (
    add_device_software_update_action_model,
)
from project.tests.models.test_user_model import add_user
from project.tests.permissions.test_platforms import IDL_USER_ACCOUNT
from project.tests.read_from_json import extract_data_from_json_file


class TestDeviceService(BaseTestCase):
    """Tests for the Device Service."""

    device_url = base_url + "/devices"
    contact_url = base_url + "/contacts"
    object_type = "device"
    json_data_url = os.path.join(test_file_path, "drafts", "devices_test_data.json")
    properties_url = base_url + "/device-properties"

    def setUp(self):
        """Set up for the tests."""
        super().setUp()
        contact1 = Contact(
            given_name="test", family_name="user", email="test.user@localhost"
        )
        contact2 = Contact(
            given_name="super", family_name="user", email="super.user@localhost"
        )
        self.normal_user = User(subject=contact1.email, contact=contact1)
        self.super_user = User(
            subject=contact2.email, contact=contact2, is_superuser=True
        )
        db.session.add_all([contact1, contact2, self.normal_user, self.super_user])

    def test_get_devices(self):
        """Ensure the GET /devices route behaves correctly."""
        response = self.client.get(self.device_url)
        self.assertEqual(response.status_code, 200)

    def test_add_device(self):
        """Ensure a new device can be added to the database."""
        devices_json = extract_data_from_json_file(self.json_data_url, "devices")

        device_data = {"data": {"type": "device", "attributes": devices_json[0]}}
        super().add_object(
            url=self.device_url, data_object=device_data, object_type=self.object_type
        )

    def test_add_device_non_valid_token(self):
        """Test the post request for adding a device, but without a valid token."""
        devices_json = extract_data_from_json_file(self.json_data_url, "devices")
        device_data = {"data": {"type": "device", "attributes": devices_json[0]}}
        with self.client:
            response = self.client.post(
                self.device_url,
                data=json.dumps(device_data),
                content_type="application/vnd.api+json",
                headers={"Authorization": "Bearer abcdefghij"},
            )
        self.assertEqual(response.status_code, 401)

    def test_add_device_contacts_relationship(self):
        """Ensure a new relationship between a device & contact can be created."""
        userinfo = generate_userinfo_data()
        contact_data = {
            "data": {
                "type": "contact",
                "attributes": {
                    "given_name": userinfo["given_name"],
                    "family_name": userinfo["family_name"],
                    "email": userinfo["email"],
                    "website": fake.url(),
                },
            }
        }
        contact = super().add_object(
            url=self.contact_url, data_object=contact_data, object_type="contact"
        )
        devices_json = extract_data_from_json_file(self.json_data_url, "devices")

        device_data = {
            "data": {
                "type": "device",
                "attributes": devices_json[0],
                "relationships": {
                    "contacts": {
                        "data": [{"type": "contact", "id": contact["data"]["id"]}]
                    }
                },
            },
        }
        data = super().add_object(
            url=self.device_url + "?include=contacts",
            data_object=device_data,
            object_type=self.object_type,
        )

        result_contact_ids = [
            x["id"] for x in data["data"]["relationships"]["contacts"]["data"]
        ]
        self.assertIn(contact["data"]["id"], result_contact_ids)

    def test_add_device_device_attachment_included(self):
        """Ensure that we can include attachments on getting a device."""
        # We want to create here a device, add two device attachments
        # and want to make sure that we can query the attachments
        # together with the device itself.

        device = Device(
            short_name="device",
            manufacturer_name=fake.company(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        db.session.add(device)

        attachment1 = DeviceAttachment(
            url="www.gfz-potsdam.de", label="GFZ", device=device
        )
        db.session.add(attachment1)
        attachment2 = DeviceAttachment(url="www.ufz.de", label="UFZ", device=device)
        db.session.add(attachment2)
        db.session.commit()

        with self.client:
            response = self.client.get(
                base_url + "/devices/" + str(device.id) + "?include=device_attachments",
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 200)

        response_data = response.get_json()

        self.assertEqual(response_data["data"]["id"], str(device.id))

        attachment_ids = [
            x["id"]
            for x in response_data["data"]["relationships"]["device_attachments"][
                "data"
            ]
        ]

        self.assertEqual(len(attachment_ids), 2)

        for attachment in [attachment1, attachment2]:
            self.assertIn(str(attachment.id), attachment_ids)

        included_attachments = {}

        for included_entry in response_data["included"]:
            if included_entry["type"] == "device_attachment":
                attachment_id = included_entry["id"]
                included_attachments[attachment_id] = included_entry

        self.assertEqual(len(included_attachments.keys()), 2)

        for attachment in [attachment1, attachment2]:
            self.assertIn(str(attachment.id), included_attachments.keys())
            self.assertEqual(
                attachment.url,
                included_attachments[str(attachment.id)]["attributes"]["url"],
            )
            self.assertEqual(
                attachment.label,
                included_attachments[str(attachment.id)]["attributes"]["label"],
            )

    def test_add_device_device_property_included(self):
        """Ensure that we can include properties on getting a device."""
        # We want to create here a device, add two device properties
        # and want to make sure that we can query the properties
        # together with the device itself.

        device = Device(
            short_name="device",
            manufacturer_name=fake.company(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        db.session.add(device)

        property1 = DeviceProperty(
            label="property1", property_name="device_property1", device=device
        )
        db.session.add(property1)
        property2 = DeviceProperty(
            label="property2", property_name="device_property2", device=device
        )
        db.session.add(property2)
        db.session.commit()

        with self.client:
            response = self.client.get(
                base_url + "/devices/" + str(device.id) + "?include=device_properties",
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 200)

        response_data = response.get_json()

        self.assertEqual(response_data["data"]["id"], str(device.id))

        property_ids = [
            x["id"]
            for x in response_data["data"]["relationships"]["device_properties"]["data"]
        ]

        self.assertEqual(len(property_ids), 2)

        for a_property in [property1, property2]:
            self.assertIn(str(a_property.id), property_ids)

        included_properties = {}

        for included_entry in response_data["included"]:
            if included_entry["type"] == "device_property":
                property_id = included_entry["id"]
                included_properties[property_id] = included_entry

        self.assertEqual(len(included_properties.keys()), 2)

        for a_property in [property1, property2]:
            self.assertIn(str(a_property.id), included_properties.keys())
            self.assertEqual(
                a_property.label,
                included_properties[str(a_property.id)]["attributes"]["label"],
            )

    def test_add_device_customfield_included(self):
        """Ensure that we can include customfields on getting a device."""
        device = Device(
            short_name="device",
            manufacturer_name=fake.company(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        db.session.add(device)

        customfield1 = CustomField(value="www.gfz-potsdam.de", key="GFZ", device=device)
        db.session.add(customfield1)
        customfield2 = CustomField(value="www.ufz.de", key="UFZ", device=device)
        db.session.add(customfield2)
        db.session.commit()

        with self.client:
            response = self.client.get(
                base_url + "/devices/" + str(device.id) + "?include=customfields",
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 200)

        response_data = response.get_json()

        self.assertEqual(response_data["data"]["id"], str(device.id))

        customfield_ids = [
            x["id"]
            for x in response_data["data"]["relationships"]["customfields"]["data"]
        ]

        self.assertEqual(len(customfield_ids), 2)

        for customfield in [customfield1, customfield2]:
            self.assertIn(str(customfield.id), customfield_ids)

        included_customfields = {}

        for included_entry in response_data["included"]:
            if included_entry["type"] == "customfield":
                customfield_id = included_entry["id"]
                included_customfields[customfield_id] = included_entry

        self.assertEqual(len(included_customfields.keys()), 2)

        for customfield in [customfield1, customfield2]:
            self.assertIn(str(customfield.id), included_customfields.keys())
            self.assertEqual(
                customfield.key,
                included_customfields[str(customfield.id)]["attributes"]["key"],
            )
            self.assertEqual(
                customfield.value,
                included_customfields[str(customfield.id)]["attributes"]["value"],
            )

    def test_http_response_not_found(self):
        """Make sure that the backend responds with 404 HTTP-Code if a resource was not found."""
        url = f"{self.device_url}/{fake.random_int()}"
        _ = super().http_code_404_when_resource_not_found(url)

    def test_delete_device_with_calibration_action(self):
        """Ensure that a device with a calibration_action can be deleted."""
        device_calibration_action = add_device_calibration_action()
        device_id = device_calibration_action.device_id
        # Only super users are allowed to delete
        with self.run_requests_as(self.super_user):
            _ = super().try_delete_object_with_status_code(
                url=f"{self.device_url}/{device_id}", expected_status_code=200
            )

    def test_delete_device_with_generic_action(self):
        """Ensure that a device with a generic action can be deleted."""
        device_action_model = generate_device_action_model()
        device_id = device_action_model.device_id
        with self.run_requests_as(self.super_user):
            _ = super().try_delete_object_with_status_code(
                url=f"{self.device_url}/{device_id}", expected_status_code=200
            )

    def test_delete_device_with_software_update_action(self):
        """Ensure that a device with  a software update action can be deleted."""
        device_action_model = add_device_software_update_action_model()
        device_id = device_action_model.device_id
        with self.run_requests_as(self.super_user):
            _ = super().try_delete_object_with_status_code(
                url=f"{self.device_url}/{device_id}", expected_status_code=200
            )

    def test_update_description_after_creation(self):
        """Make sure that update description field is set after post."""
        devices_json = extract_data_from_json_file(self.json_data_url, "devices")

        device_data = {"data": {"type": "device", "attributes": devices_json[0]}}
        result = super().add_object(
            url=self.device_url, data_object=device_data, object_type=self.object_type
        )
        result_id = result["data"]["id"]
        device = db.session.query(Device).filter_by(id=result_id).first()

        msg = "create;basic data"
        self.assertEqual(msg, device.update_description)

    def test_update_description_after_update(self):
        """Make sure that update description field is updated after patch."""
        devices_json = extract_data_from_json_file(self.json_data_url, "devices")

        device_data = {"data": {"type": "device", "attributes": devices_json[0]}}
        result = super().add_object(
            url=self.device_url, data_object=device_data, object_type=self.object_type
        )
        result_id = result["data"]["id"]

        user = add_user()
        user.is_superuser = True
        db.session.add(user)
        db.session.commit()

        with self.run_requests_as(user):
            with self.client:
                resp = self.client.patch(
                    self.device_url + "/" + result_id,
                    json={
                        "data": {
                            "id": result_id,
                            "type": "device",
                            "attributes": {
                                "long_name": "updated long name",
                            },
                        }
                    },
                    headers={"Content-Type": "application/vnd.api+json"},
                )
                self.assertEqual(resp.status_code, 200)

        device = db.session.query(Device).filter_by(id=result_id).first()

        msg = "update;basic data"
        self.assertEqual(msg, device.update_description)

    def test_update_description_after_adding_a_measured_quantity(self):
        """Make sure that update description field is set after post of a measured quantity."""
        user = add_user()
        device = Device(
            short_name=fake.pystr(),
            is_public=False,
            is_private=False,
            is_internal=True,
            created_by=user,
            updated_by=user,
        )
        db.session.add(device)
        db.session.commit()

        # Now as it is saved we can be sure that has an id
        self.assertTrue(device.id is not None)

        count_device_properties = (
            db.session.query(DeviceProperty)
            .filter_by(
                device_id=device.id,
            )
            .count()
        )
        # However, this new device for sure has no properties
        self.assertEqual(count_device_properties, 0)

        # Now we can write the request to add a device property
        payload = {
            "data": {
                "type": "device_property",
                "attributes": {
                    "label": "device property1",
                    "property_name": "device property name",
                    "compartment_name": "climate",
                    "sampling_media_name": "air",
                },
                "relationships": {
                    "device": {"data": {"type": "device", "id": str(device.id)}}
                },
            }
        }
        with self.client:
            url_post = base_url + "/device-properties"
            # You may want to look up self.add_object in the BaseTestCase
            # and compare if something doesn't work anymore
            response = self.client.post(
                url_post,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
                headers=create_token(),
            )
        # We expect that it worked and that we have a new entry
        self.assertEqual(response.status_code, 201)
        result_id = response.json["data"]["id"]
        result_device = db.session.query(Device).filter_by(id=result_id).first()

        msg = "create;measured quantity"
        self.assertEqual(msg, result_device.update_description)
        self.assertNotEqual(user.id, result_device.updated_by_id)

    def test_update_description_after_deleting_a_measured_quantity(self):
        """Make sure that update description field is set after deleting a measured quantity."""
        user = add_user()
        device = Device(
            short_name=fake.pystr(),
            is_public=False,
            is_private=False,
            is_internal=True,
            group_ids=IDL_USER_ACCOUNT.administrated_permission_groups,
            created_by=user,
            updated_by=user,
        )
        device_property = DeviceProperty(
            label="device property1",
            property_name="Test1",
            device=device,
        )
        db.session.add_all([device, device_property])
        db.session.commit()
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                response = self.client.delete(
                    self.properties_url + "/" + str(device_property.id),
                    content_type="application/vnd.api+json",
                    headers=create_token(),
                )

        self.assertEqual(response.status_code, 200)
        result_device = db.session.query(Device).filter_by(id=device.id).first()
        msg = "delete;measured quantity"
        self.assertEqual(msg, result_device.update_description)
        self.assertNotEqual(user.id, result_device.updated_by_id)

    def test_update_description_after_updating_a_measured_quantity(self):
        """Make sure that update description field is set after updating a measured quantity."""
        user = add_user()
        device = Device(
            short_name=fake.pystr(),
            is_public=False,
            is_private=False,
            is_internal=True,
            group_ids=IDL_USER_ACCOUNT.administrated_permission_groups,
            created_by=user,
            updated_by=user,
        )
        device_property = DeviceProperty(
            label="device property1",
            property_name="Test1",
            device=device,
        )
        db.session.add_all([device, device_property])
        db.session.commit()
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups_for_a_user:
            test_get_all_permission_groups_for_a_user.return_value = IDL_USER_ACCOUNT
            with self.client:
                response = self.client.patch(
                    self.properties_url + "/" + str(device_property.id),
                    json={
                        "data": {
                            "id": str(device_property.id),
                            "type": "device_property",
                            "attributes": {"label": "updated label"},
                        }
                    },
                    content_type="application/vnd.api+json",
                    headers=create_token(),
                )

        self.assertEqual(response.status_code, 200)
        result_device = db.session.query(Device).filter_by(id=device.id).first()
        msg = "update;measured quantity"
        self.assertEqual(msg, result_device.update_description)
        self.assertNotEqual(user.id, result_device.updated_by_id)

    def test_get_list_no_archived_devices_by_default(self):
        """Ensure that we don't list archived devices by default."""
        visible_device = Device(
            short_name="visible device",
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        archived_device = Device(
            short_name="archived device",
            is_public=True,
            is_private=False,
            is_internal=False,
            archived=True,
        )
        db.session.add_all([visible_device, archived_device])

        with self.client:
            response = self.client.get(self.device_url)
        self.assertEqual(response.status_code, 200)
        data = response.json["data"]
        # We have only one device, not the second one
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["attributes"]["short_name"], "visible device")
        self.assertEqual(data[0]["attributes"]["archived"], False)

    def test_get_list_with_archived_devices_by_flag(self):
        """Ensure that we can list archived devices if wished."""
        visible_device = Device(
            short_name="visible device",
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        archived_device = Device(
            short_name="archived device",
            is_public=True,
            is_private=False,
            is_internal=False,
            archived=True,
        )
        db.session.add_all([visible_device, archived_device])

        with self.client:
            response = self.client.get(self.device_url + "?hide_archived=false")
        self.assertEqual(response.status_code, 200)
        data = response.json["data"]
        # We have only one device, not the second one
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["attributes"]["short_name"], "visible device")
        self.assertEqual(data[0]["attributes"]["archived"], False)
        self.assertEqual(data[1]["attributes"]["short_name"], "archived device")
        self.assertEqual(data[1]["attributes"]["archived"], True)

    def test_delete_with_parameter_and_values(self):
        """
        Ensure we can delete a device with parameter & associated values.

        We don't want users to delete parameters with associated values,
        but once we need to delete the complete device it should be
        possible.
        """
        visible_device = Device(
            short_name="visible device",
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        parameter = DeviceParameter(
            device=visible_device,
            label="specialvalue",
            description="some value",
            unit_name="count",
            unit_uri="http://foo/count",
        )
        value = DeviceParameterValueChangeAction(
            device_parameter=parameter,
            contact=self.super_user.contact,
            date=datetime.datetime(2023, 5, 2, 15, 30, 00, tzinfo=pytz.utc),
            value="3",
        )
        db.session.add_all([visible_device, parameter, value])
        db.session.commit()

        url = f"{self.device_url}/{visible_device.id}"
        with self.run_requests_as(self.super_user):
            response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)

    def test_update_external_b2inst_metadata(self):
        """Make sure that we ask the system to update the external metadata after a patch."""
        devices_json = extract_data_from_json_file(self.json_data_url, "devices")

        device_data = {"data": {"type": "device", "attributes": devices_json[0]}}
        result = super().add_object(
            url=self.device_url, data_object=device_data, object_type=self.object_type
        )
        result_id = result["data"]["id"]

        user = add_user()
        user.is_superuser = True
        db.session.add(user)
        db.session.commit()

        device = db.session.query(Device).filter_by(id=result_id).first()
        device.b2inst_record_id = "123"
        db.session.add(device)
        db.session.commit()

        current_app.config.update({"B2INST_TOKEN": "123"})

        with self.run_requests_as(user):
            with self.client:
                with patch.object(
                    pidinst, "update_external_metadata"
                ) as update_external_metadata:
                    update_external_metadata.return_value = None
                    resp = self.client.patch(
                        self.device_url + "/" + result_id,
                        json={
                            "data": {
                                "id": result_id,
                                "type": "device",
                                "attributes": {
                                    "long_name": "updated long name",
                                },
                            }
                        },
                        headers={"Content-Type": "application/vnd.api+json"},
                    )
                    update_external_metadata.assert_called_once()
                    self.assertEqual(
                        update_external_metadata.call_args.args[0].id, device.id
                    )
        self.assertEqual(resp.status_code, 200)

    def test_update_external_b2inst_metadata_for_configuration(self):
        """Make sure that we ask the system to update the external metadata for configuration after a patch."""
        devices_json = extract_data_from_json_file(self.json_data_url, "devices")

        device_data = {"data": {"type": "device", "attributes": devices_json[0]}}
        result = super().add_object(
            url=self.device_url, data_object=device_data, object_type=self.object_type
        )
        result_id = result["data"]["id"]

        user = add_user()
        user.is_superuser = True
        db.session.add(user)
        db.session.commit()

        device = db.session.query(Device).filter_by(id=result_id).first()
        configuration = Configuration(label="Test config", b2inst_record_id="42")
        device_mount_action = DeviceMountAction(
            configuration=configuration,
            device=device,
            begin_contact=user.contact,
            begin_date=datetime.datetime(2022, 1, 1, 0, 0, 0, tzinfo=pytz.utc),
            offset_x=0,
            offset_y=0,
            offset_z=0,
        )
        db.session.add_all([configuration, device_mount_action])

        current_app.config.update({"B2INST_TOKEN": "123"})

        with self.run_requests_as(user):
            with self.client:
                with patch.object(
                    pidinst, "update_external_metadata"
                ) as update_external_metadata:
                    update_external_metadata.return_value = None
                    resp = self.client.patch(
                        self.device_url + "/" + result_id,
                        json={
                            "data": {
                                "id": result_id,
                                "type": "device",
                                "attributes": {
                                    "long_name": "updated long name",
                                },
                            }
                        },
                        headers={"Content-Type": "application/vnd.api+json"},
                    )
                    update_external_metadata.assert_called_once()
                    self.assertEqual(
                        update_external_metadata.call_args.args[0].id, configuration.id
                    )
        self.assertEqual(resp.status_code, 200)

    def test_zero_page_size_query_parameter(self):
        """Ensure we handle zero page sizes as successful."""
        resp = self.client.get(f"{self.device_url}?page[size]=0")
        self.assertEqual(resp.status_code, 200)

    def test_negative_page_size_query_parameter(self):
        """Ensure we handle negative page sizes as 4xx errors."""
        resp = self.client.get(f"{self.device_url}?page[size]=-1")
        self.assertEqual(resp.status_code, 400)

    def test_zero_page_number_query_parameter(self):
        """Ensure we handle zero page numbers as 4xx errors."""
        resp = self.client.get(f"{self.device_url}?page[number]=0")
        self.assertEqual(resp.status_code, 400)

    def test_negative_page_number_query_parameter(self):
        """Ensure we handle negative page numbers as 4xx errors."""
        resp = self.client.get(f"{self.device_url}?page[number]=-1")
        self.assertEqual(resp.status_code, 400)
