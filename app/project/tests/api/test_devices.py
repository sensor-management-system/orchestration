"""Tests for the devices."""

from project import base_url
from project.api.models.base_model import db
from project.api.models.customfield import CustomField
from project.api.models.device import Device
from project.api.models.device_attachment import DeviceAttachment
from project.api.models.device_property import DeviceProperty
from project.tests.base import BaseTestCase
from project.tests.base import fake, generate_token_data
from project.tests.read_from_json import extract_data_from_json_file


class TestDeviceService(BaseTestCase):
    """Tests for the Device Service."""

    device_url = base_url + "/devices"
    contact_url = base_url + "/contacts"
    object_type = "device"
    json_data_url = "/usr/src/app/project/tests/drafts/devices_test_data.json"

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

    def test_add_device_contacts_relationship(self):
        """Ensure a new relationship between a device & contact can be created."""
        jwt1 = generate_token_data()
        contact_data = {
            "data": {
                "type": "contact",
                "attributes": {
                    "given_name": jwt1["given_name"],
                    "family_name": jwt1["family_name"],
                    "email": jwt1["email"],
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

        device = Device(short_name="device")
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

    def test_add_device_device_attachment_relationship(self):
        """Ensure that we can work with the attachment relationship."""
        device = Device(short_name="device")
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
                base_url
                + "/devices/"
                + str(device.id)
                + "/relationships/device-attachments",
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 200)

        response_data = response.get_json()

        # it seems that this relationships are plain integer values
        # so we convert them explicitly
        attachment_ids = [str(x["id"]) for x in response_data["data"]]

        self.assertEqual(len(attachment_ids), 2)

        for attachment in [attachment1, attachment2]:
            self.assertIn(str(attachment.id), attachment_ids)

    def test_add_device_device_property_included(self):
        """Ensure that we can include properties on getting a device."""
        # We want to create here a device, add two device properties
        # and want to make sure that we can query the properties
        # together with the device itself.

        device = Device(short_name="device")
        db.session.add(device)

        property1 = DeviceProperty(label="property1", device=device)
        db.session.add(property1)
        property2 = DeviceProperty(label="property2", device=device)
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

    def test_add_device_device_property_relationship(self):
        """Ensure that we can work with the property relationship."""
        device = Device(short_name="device")
        db.session.add(device)

        property1 = DeviceProperty(label="property1", device=device)
        db.session.add(property1)
        property2 = DeviceProperty(label="property2", device=device)
        db.session.add(property2)
        db.session.commit()

        with self.client:
            response = self.client.get(
                base_url
                + "/devices/"
                + str(device.id)
                + "/relationships/device-properties",
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 200)

        response_data = response.get_json()

        # it seems that this relationships are plain integer values
        # so we convert them explicitly
        property_ids = [str(x["id"]) for x in response_data["data"]]

        self.assertEqual(len(property_ids), 2)

        for a_property in [property1, property2]:
            self.assertIn(str(a_property.id), property_ids)

    def test_add_device_customfield_included(self):
        """Ensure that we can include customfields on getting a device."""
        device = Device(short_name="device")
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

    def test_add_device_customfield_relationship(self):
        """Ensure that we can work with the customfield relationship."""
        device = Device(short_name="device")
        db.session.add(device)

        customfield1 = CustomField(value="www.gfz-potsdam.de", key="GFZ", device=device)
        db.session.add(customfield1)
        customfield2 = CustomField(value="www.ufz.de", key="UFZ", device=device)
        db.session.add(customfield2)
        db.session.commit()

        with self.client:
            response = self.client.get(
                base_url + "/devices/" + str(device.id) + "/relationships/customfields",
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 200)

        response_data = response.get_json()

        # it seems that this relationships are plain integer values
        # so we convert them explicitly
        customfield_ids = [str(x["id"]) for x in response_data["data"]]

        self.assertEqual(len(customfield_ids), 2)

        for customfield in [customfield1, customfield2]:
            self.assertIn(str(customfield.id), customfield_ids)
