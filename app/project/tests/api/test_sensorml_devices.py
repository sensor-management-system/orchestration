"""Tests to extract sensorML for devices."""

import datetime
import pathlib
import pickle
import xml

import pytz
from flask import current_app

from project import base_url
from project.api.models import (
    Configuration,
    Contact,
    Device,
    DeviceAttachment,
    DeviceCalibrationAction,
    DeviceContactRole,
    DeviceMountAction,
    DeviceProperty,
    DeviceSoftwareUpdateAction,
    GenericDeviceAction,
    User,
)
from project.api.models.base_model import db
from project.tests.base import BaseTestCase


class TestSensorMLDevice(BaseTestCase):
    """Test class for the sensor ML transformation for devices."""

    url = base_url + "/devices"

    def setUp(self):
        """Set up data for the tests."""
        super().setUp()
        path_this_file = pathlib.Path(__file__)
        path_pickle_schema = (
            path_this_file.parent / "helpers" / "sensorml_schema_validator.pickle"
        )

        with path_pickle_schema.open("rb") as infile:
            self.schema = pickle.load(infile)

        self.device = Device(
            is_public=True,
            is_private=False,
            is_internal=False,
            short_name="dummy device",
        )
        db.session.add_all([self.device])
        db.session.commit()

    def test_get_non_existing(self):
        """Ensure we get an 404 if the device doesn't exist."""
        with self.client:
            resp = self.client.get(f"{self.url}/9999999999/sensorml")
        self.assertEqual(resp.status_code, 404)

    def test_get_internal_device_without_user(self):
        """Ensure we don't show sensorML for internal devices without a user."""
        self.device.is_internal = True
        self.device.is_public = False
        db.session.add_all([self.device])
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.device.id}/sensorml")
        self.assertEqual(resp.status_code, 401)

    def test_get_internal_device_with_user(self):
        """Ensure we don't show sensorML for internal devices without a user."""
        self.device.is_internal = True
        self.device.is_public = False
        contact = Contact(given_name="Given", family_name="Fam", email="given@family")
        user = User(subject=contact.email, contact=contact)
        db.session.add_all([self.device, contact, user])
        db.session.commit()

        with self.run_requests_as(user):
            with self.client:
                resp = self.client.get(f"{self.url}/{self.device.id}/sensorml")
        self.assertEqual(resp.status_code, 200)

    def test_get_private_device_with_different_user(self):
        """Ensure we don't show sensorML for private devices without a user."""
        contact1 = Contact(given_name="Given", family_name="Fam", email="given@family")
        user1 = User(subject=contact1.email, contact=contact1)
        self.device.is_private = True
        self.device.is_public = False
        self.device.created_by = user1
        contact2 = Contact(
            given_name="Given J.", family_name="Fam", email="given.j@family"
        )
        user2 = User(subject=contact2.email, contact=contact2)
        db.session.add_all([self.device, contact1, user1, contact2, user2])
        db.session.commit()

        with self.run_requests_as(user2):
            with self.client:
                resp = self.client.get(f"{self.url}/{self.device.id}/sensorml")
        self.assertEqual(resp.status_code, 403)

    def test_get_private_device_with_super_user(self):
        """Ensure we show sensorML for private devices to a superuser."""
        contact1 = Contact(given_name="Given", family_name="Fam", email="given@family")
        user1 = User(subject=contact1.email, contact=contact1)
        self.device.is_private = True
        self.device.is_public = False
        self.device.created_by = user1
        contact2 = Contact(
            given_name="Given J.", family_name="Fam", email="given.j@family"
        )
        user2 = User(subject=contact2.email, contact=contact2, is_superuser=True)
        db.session.add_all([self.device, contact1, user1, contact2, user2])
        db.session.commit()

        with self.run_requests_as(user2):
            with self.client:
                resp = self.client.get(f"{self.url}/{self.device.id}/sensorml")
        self.assertEqual(resp.status_code, 200)

    def test_get_private_device_with_owner(self):
        """Ensure we show sensorML for private devices to the owner."""
        contact1 = Contact(given_name="Given", family_name="Fam", email="given@family")
        user1 = User(subject=contact1.email, contact=contact1)
        self.device.is_private = True
        self.device.is_public = False
        self.device.created_by = user1
        db.session.add_all([self.device, contact1, user1])
        db.session.commit()

        with self.run_requests_as(user1):
            with self.client:
                resp = self.client.get(f"{self.url}/{self.device.id}/sensorml")
        self.assertEqual(resp.status_code, 200)

    def test_get_public_device_no_contacts_no_events(self):
        """
        Test with a device without contacts nor events.

        The public device should be visible for everyone.
        But a basic device doesn't has contacts yet (the backend
        api creates one, but in our test we don't have one), nor
        events.

        But we can test the id & the short name.
        """
        with self.client:
            resp = self.client.get(f"{self.url}/{self.device.id}/sensorml")
        self.assertEqual(resp.status_code, 200)
        xml_text = resp.text
        self.schema.validate(xml_text)
        root = xml.etree.ElementTree.fromstring(resp.text)
        gml_id = root.attrib.get("{http://www.opengis.net/gml/3.2}id")
        self.assertEqual(gml_id, f"device_{self.device.id}")
        sml_identification = root.find(
            "{http://www.opengis.net/sensorml/2.0}identification"
        )
        sml_identifier_list = sml_identification.find(
            "{http://www.opengis.net/sensorml/2.0}IdentifierList"
        )
        sml_identifiers = sml_identifier_list.findall(
            "{http://www.opengis.net/sensorml/2.0}identifier"
        )
        self.assertEqual(len(sml_identifiers), 1)
        sml_identifier = sml_identifiers[0]
        sml_term = sml_identifier.find("{http://www.opengis.net/sensorml/2.0}Term")
        sml_term_definition = sml_term.attrib.get("definition")
        self.assertEqual(
            sml_term_definition, "http://sensorml.com/ont/swe/property/ShortName"
        )
        sml_term_label = sml_term.find(
            "{http://www.opengis.net/sensorml/2.0}label"
        ).text
        self.assertEqual(sml_term_label, "Short Name")
        sml_term_value = sml_term.find(
            "{http://www.opengis.net/sensorml/2.0}value"
        ).text
        self.assertEqual(sml_term_value, self.device.short_name)

    def test_get_public_device_with_pid(self):
        """Check that we give out the pid."""
        self.device.persistent_identifier = "12345/test.abc.1234-4567"

        db.session.add(self.device)
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.device.id}/sensorml")

        self.assertEqual(resp.status_code, 200)
        xml_text = resp.text
        self.schema.validate(xml_text)
        root = xml.etree.ElementTree.fromstring(resp.text)
        sml_identification = root.find(
            "{http://www.opengis.net/sensorml/2.0}identification"
        )
        sml_identifier_list = sml_identification.find(
            "{http://www.opengis.net/sensorml/2.0}IdentifierList"
        )
        sml_identifiers = sml_identifier_list.findall(
            "{http://www.opengis.net/sensorml/2.0}identifier"
        )
        self.assertEqual(len(sml_identifiers), 2)
        sml_identifier_pid = sml_identifiers[0]

        self.assertEqual(
            sml_identifier_pid.find(
                "{http://www.opengis.net/sensorml/2.0}Term"
            ).attrib.get("definition"),
            "http://sensorml.com/ont/swe/property/Identifier",
        )
        self.assertEqual(
            sml_identifier_pid.find("{http://www.opengis.net/sensorml/2.0}Term")
            .find("{http://www.opengis.net/sensorml/2.0}label")
            .text,
            "handle",
        )
        self.assertEqual(
            sml_identifier_pid.find("{http://www.opengis.net/sensorml/2.0}Term")
            .find("{http://www.opengis.net/sensorml/2.0}value")
            .text,
            self.device.persistent_identifier,
        )

    def test_get_public_device_contacts(self):
        """Test with a device with some contacts."""
        owner_name = "Owner"
        owner_uri = current_app.config["CV_URL"] + "/contactroles/4/"
        pi_name = "PI"
        pi_uri = current_app.config["CV_URL"] + "/contactroles/5/"
        contact1 = Contact(
            given_name="Given",
            family_name="Fam",
            email="given@family",
            website="https://given.fam/index.html",
            organization="Dummy organization",
        )
        contact2 = Contact(given_name="Homer J", family_name="S", email="homer.j@fix")
        contact_role1 = DeviceContactRole(
            contact=contact1,
            device=self.device,
            role_name=owner_name,
            role_uri=owner_uri,
        )
        contact_role2 = DeviceContactRole(
            contact=contact2, device=self.device, role_name=pi_name, role_uri=pi_uri
        )

        db.session.add_all([contact1, contact2, contact_role1, contact_role2])
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.device.id}/sensorml")
        self.assertEqual(resp.status_code, 200)
        xml_text = resp.text
        self.schema.validate(xml_text)
        root = xml.etree.ElementTree.fromstring(resp.text)
        sml_contacts = root.find("{http://www.opengis.net/sensorml/2.0}contacts")
        sml_contact_list = sml_contacts.find(
            "{http://www.opengis.net/sensorml/2.0}ContactList"
        )
        sml_contact_entries = sml_contact_list.findall(
            "{http://www.opengis.net/sensorml/2.0}contact"
        )
        self.assertEqual(len(sml_contact_entries), 2)
        first_contact = sml_contact_entries[0]
        second_contact = sml_contact_entries[1]

        self.assertEqual(
            first_contact.find("{http://www.isotc211.org/2005/gmd}CI_ResponsibleParty")
            .find("{http://www.isotc211.org/2005/gmd}individualName")
            .find("{http://www.isotc211.org/2005/gco}CharacterString")
            .text,
            f"{contact1.given_name} {contact1.family_name}",
        )
        self.assertEqual(
            first_contact.find("{http://www.isotc211.org/2005/gmd}CI_ResponsibleParty")
            .find("{http://www.isotc211.org/2005/gmd}organisationName")
            .find("{http://www.isotc211.org/2005/gco}CharacterString")
            .text,
            "Dummy organization",
        )
        self.assertEqual(
            first_contact.find("{http://www.isotc211.org/2005/gmd}CI_ResponsibleParty")
            .find("{http://www.isotc211.org/2005/gmd}contactInfo")
            .find("{http://www.isotc211.org/2005/gmd}CI_Contact")
            .find("{http://www.isotc211.org/2005/gmd}address")
            .find("{http://www.isotc211.org/2005/gmd}CI_Address")
            .find("{http://www.isotc211.org/2005/gmd}electronicMailAddress")
            .find("{http://www.isotc211.org/2005/gco}CharacterString")
            .text,
            contact1.email,
        )
        self.assertEqual(
            first_contact.attrib.get("{http://www.w3.org/1999/xlink}arcrole"),
            contact_role1.role_uri,
        )
        self.assertEqual(
            first_contact.find("{http://www.isotc211.org/2005/gmd}CI_ResponsibleParty")
            .find("{http://www.isotc211.org/2005/gmd}role")
            .find("{http://www.isotc211.org/2005/gmd}CI_RoleCode")
            .attrib.get("codeList"),
            current_app.config["CV_URL"] + "/contactroles",
        )
        self.assertEqual(
            first_contact.find("{http://www.isotc211.org/2005/gmd}CI_ResponsibleParty")
            .find("{http://www.isotc211.org/2005/gmd}role")
            .find("{http://www.isotc211.org/2005/gmd}CI_RoleCode")
            .attrib.get("codeListValue"),
            "4",
        )

        self.assertEqual(
            first_contact.find("{http://www.isotc211.org/2005/gmd}CI_ResponsibleParty")
            .find("{http://www.isotc211.org/2005/gmd}contactInfo")
            .find("{http://www.isotc211.org/2005/gmd}CI_Contact")
            .find("{http://www.isotc211.org/2005/gmd}onlineResource")
            .find("{http://www.isotc211.org/2005/gmd}CI_OnlineResource")
            .find("{http://www.isotc211.org/2005/gmd}linkage")
            .find("{http://www.isotc211.org/2005/gmd}URL")
            .text,
            contact1.website,
        )

        self.assertEqual(
            second_contact.find("{http://www.isotc211.org/2005/gmd}CI_ResponsibleParty")
            .find("{http://www.isotc211.org/2005/gmd}individualName")
            .find("{http://www.isotc211.org/2005/gco}CharacterString")
            .text,
            f"{contact2.given_name} {contact2.family_name}",
        )
        self.assertEqual(
            second_contact.find("{http://www.isotc211.org/2005/gmd}CI_ResponsibleParty")
            .find("{http://www.isotc211.org/2005/gmd}contactInfo")
            .find("{http://www.isotc211.org/2005/gmd}CI_Contact")
            .find("{http://www.isotc211.org/2005/gmd}address")
            .find("{http://www.isotc211.org/2005/gmd}CI_Address")
            .find("{http://www.isotc211.org/2005/gmd}electronicMailAddress")
            .find("{http://www.isotc211.org/2005/gco}CharacterString")
            .text,
            contact2.email,
        )
        self.assertEqual(
            second_contact.attrib.get("{http://www.w3.org/1999/xlink}arcrole"),
            contact_role2.role_uri,
        )
        self.assertEqual(
            second_contact.find("{http://www.isotc211.org/2005/gmd}CI_ResponsibleParty")
            .find("{http://www.isotc211.org/2005/gmd}role")
            .find("{http://www.isotc211.org/2005/gmd}CI_RoleCode")
            .attrib.get("codeList"),
            current_app.config["CV_URL"] + "/contactroles",
        )
        self.assertEqual(
            second_contact.find("{http://www.isotc211.org/2005/gmd}CI_ResponsibleParty")
            .find("{http://www.isotc211.org/2005/gmd}role")
            .find("{http://www.isotc211.org/2005/gmd}CI_RoleCode")
            .attrib.get("codeListValue"),
            "5",
        )

    def test_get_public_device_with_long_name(self):
        """Check that we give out the long name."""
        self.device.long_name = "some long name"

        db.session.add(self.device)
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.device.id}/sensorml")

        self.assertEqual(resp.status_code, 200)
        xml_text = resp.text
        self.schema.validate(xml_text)
        root = xml.etree.ElementTree.fromstring(resp.text)
        sml_identification = root.find(
            "{http://www.opengis.net/sensorml/2.0}identification"
        )
        sml_identifier_list = sml_identification.find(
            "{http://www.opengis.net/sensorml/2.0}IdentifierList"
        )
        sml_identifiers = sml_identifier_list.findall(
            "{http://www.opengis.net/sensorml/2.0}identifier"
        )
        self.assertEqual(len(sml_identifiers), 2)
        sml_identifier_long_name = sml_identifiers[0]
        sml_identifier_short_name = sml_identifiers[1]

        self.assertEqual(
            sml_identifier_long_name.find(
                "{http://www.opengis.net/sensorml/2.0}Term"
            ).attrib.get("definition"),
            "http://sensorml.com/ont/swe/property/LongName",
        )
        self.assertEqual(
            sml_identifier_long_name.find("{http://www.opengis.net/sensorml/2.0}Term")
            .find("{http://www.opengis.net/sensorml/2.0}label")
            .text,
            "Long Name",
        )
        self.assertEqual(
            sml_identifier_long_name.find("{http://www.opengis.net/sensorml/2.0}Term")
            .find("{http://www.opengis.net/sensorml/2.0}value")
            .text,
            self.device.long_name,
        )

        self.assertEqual(
            sml_identifier_short_name.find(
                "{http://www.opengis.net/sensorml/2.0}Term"
            ).attrib.get("definition"),
            "http://sensorml.com/ont/swe/property/ShortName",
        )
        self.assertEqual(
            sml_identifier_short_name.find("{http://www.opengis.net/sensorml/2.0}Term")
            .find("{http://www.opengis.net/sensorml/2.0}label")
            .text,
            "Short Name",
        )
        self.assertEqual(
            sml_identifier_short_name.find("{http://www.opengis.net/sensorml/2.0}Term")
            .find("{http://www.opengis.net/sensorml/2.0}value")
            .text,
            self.device.short_name,
        )

    def test_get_public_device_with_model(self):
        """Check that we give out the model number."""
        self.device.model = "0815"

        db.session.add(self.device)
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.device.id}/sensorml")

        self.assertEqual(resp.status_code, 200)
        xml_text = resp.text
        self.schema.validate(xml_text)
        root = xml.etree.ElementTree.fromstring(resp.text)
        sml_identification = root.find(
            "{http://www.opengis.net/sensorml/2.0}identification"
        )
        sml_identifier_list = sml_identification.find(
            "{http://www.opengis.net/sensorml/2.0}IdentifierList"
        )
        sml_identifiers = sml_identifier_list.findall(
            "{http://www.opengis.net/sensorml/2.0}identifier"
        )
        self.assertEqual(len(sml_identifiers), 2)
        sml_identifier_model_number = sml_identifiers[1]

        self.assertEqual(
            sml_identifier_model_number.find(
                "{http://www.opengis.net/sensorml/2.0}Term"
            ).attrib.get("definition"),
            "http://sensorml.com/ont/swe/property/ModelNumber",
        )
        self.assertEqual(
            sml_identifier_model_number.find(
                "{http://www.opengis.net/sensorml/2.0}Term"
            )
            .find("{http://www.opengis.net/sensorml/2.0}label")
            .text,
            "Model Number",
        )
        self.assertEqual(
            sml_identifier_model_number.find(
                "{http://www.opengis.net/sensorml/2.0}Term"
            )
            .find("{http://www.opengis.net/sensorml/2.0}value")
            .text,
            self.device.model,
        )

    def test_get_public_device_with_status(self):
        """Check that we give out the status."""
        self.device.status_name = "In use"

        db.session.add(self.device)
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.device.id}/sensorml")

        self.assertEqual(resp.status_code, 200)
        xml_text = resp.text
        self.schema.validate(xml_text)
        root = xml.etree.ElementTree.fromstring(resp.text)
        sml_identification = root.find(
            "{http://www.opengis.net/sensorml/2.0}identification"
        )
        sml_identifier_list = sml_identification.find(
            "{http://www.opengis.net/sensorml/2.0}IdentifierList"
        )
        sml_identifiers = sml_identifier_list.findall(
            "{http://www.opengis.net/sensorml/2.0}identifier"
        )
        self.assertEqual(len(sml_identifiers), 2)
        sml_identifier_status_name = sml_identifiers[1]

        self.assertEqual(
            sml_identifier_status_name.find(
                "{http://www.opengis.net/sensorml/2.0}Term"
            ).attrib.get("definition"),
            "http://sensorml.com/ont/swe/property/SystemStatus",
        )
        self.assertEqual(
            sml_identifier_status_name.find("{http://www.opengis.net/sensorml/2.0}Term")
            .find("{http://www.opengis.net/sensorml/2.0}label")
            .text,
            "System Status",
        )
        self.assertEqual(
            sml_identifier_status_name.find("{http://www.opengis.net/sensorml/2.0}Term")
            .find("{http://www.opengis.net/sensorml/2.0}value")
            .text,
            self.device.status_name,
        )

    def test_get_public_device_with_serial_number(self):
        """Check that we give out the serial number."""
        self.device.serial_number = "1234"

        db.session.add(self.device)
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.device.id}/sensorml")

        self.assertEqual(resp.status_code, 200)
        xml_text = resp.text
        self.schema.validate(xml_text)
        root = xml.etree.ElementTree.fromstring(resp.text)
        sml_identification = root.find(
            "{http://www.opengis.net/sensorml/2.0}identification"
        )
        sml_identifier_list = sml_identification.find(
            "{http://www.opengis.net/sensorml/2.0}IdentifierList"
        )
        sml_identifiers = sml_identifier_list.findall(
            "{http://www.opengis.net/sensorml/2.0}identifier"
        )
        self.assertEqual(len(sml_identifiers), 2)
        sml_identifier_serial_number = sml_identifiers[1]

        self.assertEqual(
            sml_identifier_serial_number.find(
                "{http://www.opengis.net/sensorml/2.0}Term"
            ).attrib.get("definition"),
            "http://sensorml.com/ont/swe/property/SerialNumber",
        )
        self.assertEqual(
            sml_identifier_serial_number.find(
                "{http://www.opengis.net/sensorml/2.0}Term"
            )
            .find("{http://www.opengis.net/sensorml/2.0}label")
            .text,
            "Serial Number",
        )
        self.assertEqual(
            sml_identifier_serial_number.find(
                "{http://www.opengis.net/sensorml/2.0}Term"
            )
            .find("{http://www.opengis.net/sensorml/2.0}value")
            .text,
            self.device.serial_number,
        )

    def test_get_public_device_with_manufacturer(self):
        """Check that we give out the manufacturer."""
        self.device.manufacturer_name = "XYZ Coop"

        db.session.add(self.device)
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.device.id}/sensorml")

        self.assertEqual(resp.status_code, 200)
        xml_text = resp.text
        self.schema.validate(xml_text)
        root = xml.etree.ElementTree.fromstring(resp.text)
        sml_identification = root.find(
            "{http://www.opengis.net/sensorml/2.0}identification"
        )
        sml_identifier_list = sml_identification.find(
            "{http://www.opengis.net/sensorml/2.0}IdentifierList"
        )
        sml_identifiers = sml_identifier_list.findall(
            "{http://www.opengis.net/sensorml/2.0}identifier"
        )
        self.assertEqual(len(sml_identifiers), 2)
        sml_identifier_manufacturer_name = sml_identifiers[1]

        self.assertEqual(
            sml_identifier_manufacturer_name.find(
                "{http://www.opengis.net/sensorml/2.0}Term"
            ).attrib.get("definition"),
            "http://sensorml.com/ont/swe/property/Manufacturer",
        )
        self.assertEqual(
            sml_identifier_manufacturer_name.find(
                "{http://www.opengis.net/sensorml/2.0}Term"
            )
            .find("{http://www.opengis.net/sensorml/2.0}label")
            .text,
            "Manufacturer",
        )
        self.assertEqual(
            sml_identifier_manufacturer_name.find(
                "{http://www.opengis.net/sensorml/2.0}Term"
            )
            .find("{http://www.opengis.net/sensorml/2.0}value")
            .text,
            self.device.manufacturer_name,
        )

    def test_get_public_device_with_device_type(self):
        """Check that we give out the device type."""
        self.device.device_type_name = "Barometer"

        db.session.add(self.device)
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.device.id}/sensorml")

        self.assertEqual(resp.status_code, 200)
        xml_text = resp.text
        self.schema.validate(xml_text)
        root = xml.etree.ElementTree.fromstring(resp.text)
        sml_classification = root.find(
            "{http://www.opengis.net/sensorml/2.0}classification"
        )
        sml_classifier_list = sml_classification.find(
            "{http://www.opengis.net/sensorml/2.0}ClassifierList"
        )
        sml_classifiers = sml_classifier_list.findall(
            "{http://www.opengis.net/sensorml/2.0}classifier"
        )
        self.assertEqual(len(sml_classifiers), 1)
        sml_classifier_device_type = sml_classifiers[0]

        self.assertEqual(
            sml_classifier_device_type.find(
                "{http://www.opengis.net/sensorml/2.0}Term"
            ).attrib.get("definition"),
            "http://sensorml.com/ont/swe/property/SensorType",
        )
        self.assertEqual(
            sml_classifier_device_type.find("{http://www.opengis.net/sensorml/2.0}Term")
            .find("{http://www.opengis.net/sensorml/2.0}label")
            .text,
            "sensor type",
        )
        self.assertEqual(
            sml_classifier_device_type.find("{http://www.opengis.net/sensorml/2.0}Term")
            .find("{http://www.opengis.net/sensorml/2.0}value")
            .text,
            self.device.device_type_name,
        )

    def test_get_public_device_with_description(self):
        """Check that we give out the description."""
        self.device.description = "Some long description"

        db.session.add(self.device)
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.device.id}/sensorml")

        self.assertEqual(resp.status_code, 200)
        xml_text = resp.text
        self.schema.validate(xml_text)
        root = xml.etree.ElementTree.fromstring(resp.text)
        sml_description = root.find("{http://www.opengis.net/gml/3.2}description")
        self.assertEqual(sml_description.text, self.device.description)

    def test_get_public_device_with_website(self):
        """Check that we give out the website."""
        self.device.website = "https://gfz-potsdam.de"

        db.session.add(self.device)
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.device.id}/sensorml")

        self.assertEqual(resp.status_code, 200)
        xml_text = resp.text
        self.schema.validate(xml_text)
        root = xml.etree.ElementTree.fromstring(resp.text)
        sml_documentation = root.find(
            "{http://www.opengis.net/sensorml/2.0}documentation"
        )
        sml_document_list = sml_documentation.find(
            "{http://www.opengis.net/sensorml/2.0}DocumentList"
        )
        sml_documents = sml_document_list.findall(
            "{http://www.opengis.net/sensorml/2.0}document"
        )
        self.assertEqual(len(sml_documents), 1)
        sml_document_website = sml_documents[0]

        self.assertEqual(
            sml_document_website.attrib.get("{http://www.w3.org/1999/xlink}arcrole"),
            "Website",
        )
        self.assertEqual(
            sml_document_website.find(
                "{http://www.isotc211.org/2005/gmd}CI_OnlineResource"
            )
            .find("{http://www.isotc211.org/2005/gmd}linkage")
            .find("{http://www.isotc211.org/2005/gmd}URL")
            .text,
            self.device.website,
        )

    def test_get_public_device_with_attachments(self):
        """Check that we give out the attachments."""
        attachment = DeviceAttachment(
            device=self.device, url="https://ufz.de", label="UFZ-Page"
        )

        db.session.add(attachment)
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.device.id}/sensorml")

        self.assertEqual(resp.status_code, 200)
        xml_text = resp.text
        self.schema.validate(xml_text)
        root = xml.etree.ElementTree.fromstring(resp.text)
        sml_documentation = root.find(
            "{http://www.opengis.net/sensorml/2.0}documentation"
        )
        sml_document_list = sml_documentation.find(
            "{http://www.opengis.net/sensorml/2.0}DocumentList"
        )
        sml_documents = sml_document_list.findall(
            "{http://www.opengis.net/sensorml/2.0}document"
        )
        self.assertEqual(len(sml_documents), 1)
        sml_document_website = sml_documents[0]

        self.assertEqual(
            sml_document_website.attrib.get("{http://www.w3.org/1999/xlink}arcrole"),
            "Attachment",
        )
        self.assertEqual(
            sml_document_website.find(
                "{http://www.isotc211.org/2005/gmd}CI_OnlineResource"
            )
            .find("{http://www.isotc211.org/2005/gmd}linkage")
            .find("{http://www.isotc211.org/2005/gmd}URL")
            .text,
            attachment.url,
        )
        self.assertEqual(
            sml_document_website.find(
                "{http://www.isotc211.org/2005/gmd}CI_OnlineResource"
            )
            .find("{http://www.isotc211.org/2005/gmd}name")
            .find("{http://www.isotc211.org/2005/gco}CharacterString")
            .text,
            attachment.label,
        )
        self.assertEqual(
            sml_document_website.find(
                "{http://www.isotc211.org/2005/gmd}CI_OnlineResource"
            ).attrib.get("id"),
            f"Attachment_{attachment.id}_of_PhysicalSystem_device_{self.device.id}",
        )

    def test_get_public_device_with_device_properties(self):
        """Check that we give out the device properties."""
        air_temperature_uri = current_app.config["CV_URL"] + "/measuredquantity/4/"
        device_property = DeviceProperty(
            device=self.device,
            sampling_media_name="Weather",
            property_name="Air temperature",
            property_uri=air_temperature_uri,
            unit_name="°C",
            label="Air temp",
        )

        db.session.add(device_property)
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.device.id}/sensorml")

        self.assertEqual(resp.status_code, 200)
        xml_text = resp.text
        self.schema.validate(xml_text)
        root = xml.etree.ElementTree.fromstring(resp.text)
        sml_output = root.find("{http://www.opengis.net/sensorml/2.0}outputs")
        sml_output_list = sml_output.find(
            "{http://www.opengis.net/sensorml/2.0}OutputList"
        )
        sml_outputs = sml_output_list.findall(
            "{http://www.opengis.net/sensorml/2.0}output"
        )
        self.assertEqual(len(sml_outputs), 1)
        sml_output_air_temp = sml_outputs[0]

        self.assertEqual(
            sml_output_air_temp.attrib.get("name"),
            device_property.property_name.replace(" ", "_"),
        )
        self.assertEqual(
            sml_output_air_temp.find(
                "{http://www.opengis.net/swe/2.0}Quantity"
            ).attrib.get("definition"),
            device_property.property_uri,
        )
        self.assertEqual(
            sml_output_air_temp.find("{http://www.opengis.net/swe/2.0}Quantity")
            .find("{http://www.opengis.net/swe/2.0}label")
            .text,
            device_property.label,
        )
        self.assertEqual(
            sml_output_air_temp.find("{http://www.opengis.net/swe/2.0}Quantity")
            .find("{http://www.opengis.net/swe/2.0}uom")
            .attrib.get("code"),
            device_property.unit_name,
        )

    def test_get_public_device_with_device_properties_without_unit(self):
        """Check that we give out the device properties also without unit."""
        air_temperature_uri = current_app.config["CV_URL"] + "/measuredquantity/4/"
        device_property = DeviceProperty(
            device=self.device,
            sampling_media_name="Weather",
            property_name="Air temperature",
            property_uri=air_temperature_uri,
            label="Air temp",
        )

        db.session.add(device_property)
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.device.id}/sensorml")

        self.assertEqual(resp.status_code, 200)
        xml_text = resp.text
        self.schema.validate(xml_text)
        root = xml.etree.ElementTree.fromstring(resp.text)
        sml_output = root.find("{http://www.opengis.net/sensorml/2.0}outputs")
        sml_output_list = sml_output.find(
            "{http://www.opengis.net/sensorml/2.0}OutputList"
        )
        sml_outputs = sml_output_list.findall(
            "{http://www.opengis.net/sensorml/2.0}output"
        )
        self.assertEqual(len(sml_outputs), 1)
        sml_output_air_temp = sml_outputs[0]

        self.assertEqual(
            sml_output_air_temp.attrib.get("name"),
            device_property.property_name.replace(" ", "_"),
        )
        self.assertEqual(
            sml_output_air_temp.find(
                "{http://www.opengis.net/swe/2.0}Quantity"
            ).attrib.get("definition"),
            device_property.property_uri,
        )
        self.assertEqual(
            sml_output_air_temp.find("{http://www.opengis.net/swe/2.0}Quantity")
            .find("{http://www.opengis.net/swe/2.0}label")
            .text,
            device_property.label,
        )
        self.assertEqual(
            sml_output_air_temp.find("{http://www.opengis.net/swe/2.0}Quantity")
            .find("{http://www.opengis.net/swe/2.0}uom")
            .attrib,
            {},
        )

    def test_get_public_device_with_device_properties_without_label(self):
        """Check that we give out the device properties also without label."""
        air_temperature_uri = current_app.config["CV_URL"] + "/measuredquantity/4/"
        device_property = DeviceProperty(
            device=self.device,
            sampling_media_name="Weather",
            property_name="Air temperature",
            property_uri=air_temperature_uri,
        )

        db.session.add(device_property)
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.device.id}/sensorml")

        self.assertEqual(resp.status_code, 200)
        xml_text = resp.text
        self.schema.validate(xml_text)
        root = xml.etree.ElementTree.fromstring(resp.text)
        sml_output = root.find("{http://www.opengis.net/sensorml/2.0}outputs")
        sml_output_list = sml_output.find(
            "{http://www.opengis.net/sensorml/2.0}OutputList"
        )
        sml_outputs = sml_output_list.findall(
            "{http://www.opengis.net/sensorml/2.0}output"
        )
        self.assertEqual(len(sml_outputs), 1)
        sml_output_air_temp = sml_outputs[0]

        self.assertEqual(
            sml_output_air_temp.attrib.get("name"),
            device_property.property_name.replace(" ", "_"),
        )
        self.assertEqual(
            sml_output_air_temp.find(
                "{http://www.opengis.net/swe/2.0}Quantity"
            ).attrib.get("definition"),
            device_property.property_uri,
        )
        self.assertIsNone(
            sml_output_air_temp.find("{http://www.opengis.net/swe/2.0}Quantity")
            .find("{http://www.opengis.net/swe/2.0}label")
            .text,
        )
        self.assertEqual(
            sml_output_air_temp.find("{http://www.opengis.net/swe/2.0}Quantity")
            .find("{http://www.opengis.net/swe/2.0}uom")
            .attrib,
            {},
        )

    def test_get_public_device_with_device_properties_without_property_uri(self):
        """Check that we give out the device properties also without property uri."""
        device_property = DeviceProperty(
            device=self.device,
            property_name="Air temperature",
        )

        db.session.add(device_property)
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.device.id}/sensorml")

        self.assertEqual(resp.status_code, 200)
        xml_text = resp.text
        self.schema.validate(xml_text)
        root = xml.etree.ElementTree.fromstring(resp.text)
        sml_output = root.find("{http://www.opengis.net/sensorml/2.0}outputs")
        sml_output_list = sml_output.find(
            "{http://www.opengis.net/sensorml/2.0}OutputList"
        )
        sml_outputs = sml_output_list.findall(
            "{http://www.opengis.net/sensorml/2.0}output"
        )
        self.assertEqual(len(sml_outputs), 1)
        sml_output_air_temp = sml_outputs[0]

        self.assertEqual(
            sml_output_air_temp.attrib.get("name"),
            device_property.property_name.replace(" ", "_"),
        )
        self.assertIsNone(
            sml_output_air_temp.find(
                "{http://www.opengis.net/swe/2.0}Quantity"
            ).attrib.get("definition"),
        )
        self.assertIsNone(
            sml_output_air_temp.find("{http://www.opengis.net/swe/2.0}Quantity")
            .find("{http://www.opengis.net/swe/2.0}label")
            .text,
        )
        self.assertEqual(
            sml_output_air_temp.find("{http://www.opengis.net/swe/2.0}Quantity")
            .find("{http://www.opengis.net/swe/2.0}uom")
            .attrib,
            {},
        )

    def test_get_public_device_with_empty_device_property(self):
        """Check that we give out the device properties also without property uri."""
        device_property = DeviceProperty(
            device=self.device,
            property_name="",
        )

        db.session.add(device_property)
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.device.id}/sensorml")

        self.assertEqual(resp.status_code, 200)
        xml_text = resp.text
        self.schema.validate(xml_text)
        root = xml.etree.ElementTree.fromstring(resp.text)
        sml_output = root.find("{http://www.opengis.net/sensorml/2.0}outputs")
        self.assertIsNone(sml_output)

    def test_get_public_device_with_mount(self):
        """Check that we give out the device mount."""
        configuration = Configuration(label="Test config")
        contact = Contact(given_name="Given", family_name="Fam", email="given@family")
        device_mount = DeviceMountAction(
            device=self.device,
            configuration=configuration,
            begin_date=datetime.datetime(year=2022, month=12, day=24, tzinfo=pytz.utc),
            begin_contact=contact,
            end_date=datetime.datetime(year=2022, month=12, day=25, tzinfo=pytz.utc),
            begin_description="Mount of device on test config",
        )

        db.session.add_all([configuration, device_mount, contact])
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.device.id}/sensorml")

        self.assertEqual(resp.status_code, 200)
        xml_text = resp.text
        self.schema.validate(xml_text)
        root = xml.etree.ElementTree.fromstring(resp.text)
        sml_history = root.find("{http://www.opengis.net/sensorml/2.0}history")
        sml_event_list = sml_history.find(
            "{http://www.opengis.net/sensorml/2.0}EventList"
        )
        sml_events = sml_event_list.findall(
            "{http://www.opengis.net/sensorml/2.0}event"
        )
        self.assertEqual(len(sml_events), 1)

        sml_mount_event = sml_events[0]

        self.assertEqual(
            sml_mount_event.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}classification")
            .find("{http://www.opengis.net/sensorml/2.0}ClassifierList")
            .find("{http://www.opengis.net/sensorml/2.0}classifier")
            .find("{http://www.opengis.net/sensorml/2.0}Term")
            .attrib.get("definition"),
            "Mount",
        )
        self.assertEqual(
            sml_mount_event.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}classification")
            .find("{http://www.opengis.net/sensorml/2.0}ClassifierList")
            .find("{http://www.opengis.net/sensorml/2.0}classifier")
            .find("{http://www.opengis.net/sensorml/2.0}Term")
            .find("{http://www.opengis.net/sensorml/2.0}label")
            .text,
            f"Mounted to {configuration.label}",
        )
        self.assertEqual(
            sml_mount_event.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}classification")
            .find("{http://www.opengis.net/sensorml/2.0}ClassifierList")
            .find("{http://www.opengis.net/sensorml/2.0}classifier")
            .find("{http://www.opengis.net/sensorml/2.0}Term")
            .find("{http://www.opengis.net/sensorml/2.0}value")
            .text,
            "Mount",
        )
        self.assertEqual(
            sml_mount_event.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}time")
            .find("{http://www.opengis.net/gml/3.2}TimePeriod")
            .attrib.get("{http://www.opengis.net/gml/3.2}id"),
            f"TimePeriodForDeviceMountAction_{device_mount.id}_of_device_{self.device.id}",
        )
        self.assertEqual(
            sml_mount_event.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}time")
            .find("{http://www.opengis.net/gml/3.2}TimePeriod")
            .find("{http://www.opengis.net/gml/3.2}description")
            .text,
            device_mount.begin_description,
        )
        self.assertEqual(
            sml_mount_event.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}time")
            .find("{http://www.opengis.net/gml/3.2}TimePeriod")
            .find("{http://www.opengis.net/gml/3.2}begin")
            .find("{http://www.opengis.net/gml/3.2}TimeInstant")
            .find("{http://www.opengis.net/gml/3.2}timePosition")
            .text,
            "2022-12-24T00:00:00+00:00",
        )
        self.assertEqual(
            sml_mount_event.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}time")
            .find("{http://www.opengis.net/gml/3.2}TimePeriod")
            .find("{http://www.opengis.net/gml/3.2}end")
            .find("{http://www.opengis.net/gml/3.2}TimeInstant")
            .find("{http://www.opengis.net/gml/3.2}timePosition")
            .text,
            "2022-12-25T00:00:00+00:00",
        )

    def test_get_public_device_with_mount_without_end(self):
        """Check that we give out the device mount without an end date."""
        configuration = Configuration(label="Test config")
        contact = Contact(given_name="Given", family_name="Fam", email="given@family")
        device_mount = DeviceMountAction(
            device=self.device,
            configuration=configuration,
            begin_date=datetime.datetime(year=2022, month=12, day=24, tzinfo=pytz.utc),
            begin_contact=contact,
            begin_description="Mount of device on test config",
        )

        db.session.add_all([configuration, device_mount, contact])
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.device.id}/sensorml")

        self.assertEqual(resp.status_code, 200)
        xml_text = resp.text
        self.schema.validate(xml_text)
        root = xml.etree.ElementTree.fromstring(resp.text)
        sml_history = root.find("{http://www.opengis.net/sensorml/2.0}history")
        sml_event_list = sml_history.find(
            "{http://www.opengis.net/sensorml/2.0}EventList"
        )
        sml_events = sml_event_list.findall(
            "{http://www.opengis.net/sensorml/2.0}event"
        )
        self.assertEqual(len(sml_events), 1)

        sml_mount_event = sml_events[0]

        self.assertEqual(
            len(
                sml_mount_event.find("{http://www.opengis.net/sensorml/2.0}Event")
                .find("{http://www.opengis.net/sensorml/2.0}time")
                .find("{http://www.opengis.net/gml/3.2}TimePeriod")
                .find("{http://www.opengis.net/gml/3.2}end")
                .findall("{http://www.opengis.net/gml/3.2}TimeInstant")
            ),
            0,
        )

    def test_get_public_device_with_mount_without_description(self):
        """Check that we give out the device mount without a description."""
        configuration = Configuration(label="Test config")
        contact = Contact(given_name="Given", family_name="Fam", email="given@family")
        device_mount = DeviceMountAction(
            device=self.device,
            configuration=configuration,
            begin_date=datetime.datetime(year=2022, month=12, day=24, tzinfo=pytz.utc),
            begin_contact=contact,
        )

        db.session.add_all([configuration, device_mount, contact])
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.device.id}/sensorml")

        self.assertEqual(resp.status_code, 200)
        xml_text = resp.text
        self.schema.validate(xml_text)
        root = xml.etree.ElementTree.fromstring(resp.text)
        sml_history = root.find("{http://www.opengis.net/sensorml/2.0}history")
        sml_event_list = sml_history.find(
            "{http://www.opengis.net/sensorml/2.0}EventList"
        )
        sml_events = sml_event_list.findall(
            "{http://www.opengis.net/sensorml/2.0}event"
        )
        self.assertEqual(len(sml_events), 1)

        sml_mount_event = sml_events[0]

        self.assertIsNone(
            sml_mount_event.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}time")
            .find("{http://www.opengis.net/gml/3.2}TimePeriod")
            .find("{http://www.opengis.net/gml/3.2}description")
            .text,
        )

    def test_get_public_device_with_mount_without_configuration_label(self):
        """Check that we give out the device mount without a configuration label."""
        configuration = Configuration()
        contact = Contact(given_name="Given", family_name="Fam", email="given@family")
        device_mount = DeviceMountAction(
            device=self.device,
            configuration=configuration,
            begin_date=datetime.datetime(year=2022, month=12, day=24, tzinfo=pytz.utc),
            begin_contact=contact,
        )

        db.session.add_all([configuration, device_mount, contact])
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.device.id}/sensorml")

        self.assertEqual(resp.status_code, 200)
        xml_text = resp.text
        self.schema.validate(xml_text)
        root = xml.etree.ElementTree.fromstring(resp.text)
        sml_history = root.find("{http://www.opengis.net/sensorml/2.0}history")
        sml_event_list = sml_history.find(
            "{http://www.opengis.net/sensorml/2.0}EventList"
        )
        sml_events = sml_event_list.findall(
            "{http://www.opengis.net/sensorml/2.0}event"
        )
        self.assertEqual(len(sml_events), 1)

        sml_mount_event = sml_events[0]

        self.assertEqual(
            sml_mount_event.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}classification")
            .find("{http://www.opengis.net/sensorml/2.0}ClassifierList")
            .find("{http://www.opengis.net/sensorml/2.0}classifier")
            .find("{http://www.opengis.net/sensorml/2.0}Term")
            .find("{http://www.opengis.net/sensorml/2.0}label")
            .text,
            f"Mounted to configuration {configuration.id}",
        )

    def test_get_public_device_with_calibration_action(self):
        """Check that we give out the calibration action."""
        contact = Contact(given_name="Given", family_name="Fam", email="given@family")
        calibration_action = DeviceCalibrationAction(
            device=self.device,
            current_calibration_date=datetime.datetime(
                year=2022, month=12, day=24, tzinfo=pytz.utc
            ),
            next_calibration_date=datetime.datetime(
                year=2022, month=12, day=25, tzinfo=pytz.utc
            ),
            contact=contact,
            formula="x+y",
            value=42.0,
            description="Some desc",
        )

        db.session.add_all([contact, calibration_action])
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.device.id}/sensorml")

        self.assertEqual(resp.status_code, 200)
        xml_text = resp.text
        self.schema.validate(xml_text)
        root = xml.etree.ElementTree.fromstring(resp.text)

        sml_history = root.find("{http://www.opengis.net/sensorml/2.0}history")
        sml_event_list = sml_history.find(
            "{http://www.opengis.net/sensorml/2.0}EventList"
        )
        sml_events = sml_event_list.findall(
            "{http://www.opengis.net/sensorml/2.0}event"
        )
        self.assertEqual(len(sml_events), 1)

        sml_calibration_event = sml_events[0]

        self.assertEqual(
            sml_calibration_event.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}classification")
            .find("{http://www.opengis.net/sensorml/2.0}ClassifierList")
            .find("{http://www.opengis.net/sensorml/2.0}classifier")
            .find("{http://www.opengis.net/sensorml/2.0}Term")
            .attrib.get("definition"),
            "Calibration",
        )
        self.assertEqual(
            sml_calibration_event.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}classification")
            .find("{http://www.opengis.net/sensorml/2.0}ClassifierList")
            .find("{http://www.opengis.net/sensorml/2.0}classifier")
            .find("{http://www.opengis.net/sensorml/2.0}Term")
            .find("{http://www.opengis.net/sensorml/2.0}label")
            .text,
            "Calibration",
        )
        self.assertEqual(
            sml_calibration_event.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}classification")
            .find("{http://www.opengis.net/sensorml/2.0}ClassifierList")
            .find("{http://www.opengis.net/sensorml/2.0}classifier")
            .find("{http://www.opengis.net/sensorml/2.0}Term")
            .find("{http://www.opengis.net/sensorml/2.0}value")
            .text,
            str(calibration_action.value),
        )
        self.assertEqual(
            sml_calibration_event.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}time")
            .find("{http://www.opengis.net/gml/3.2}TimeInstant")
            .attrib.get("{http://www.opengis.net/gml/3.2}id"),
            f"TimeInstantForCalibration_{calibration_action.id}_of_device_{self.device.id}",
        )
        self.assertEqual(
            sml_calibration_event.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}time")
            .find("{http://www.opengis.net/gml/3.2}TimeInstant")
            .find("{http://www.opengis.net/gml/3.2}timePosition")
            .text,
            "2022-12-24T00:00:00+00:00",
        )

    def test_get_public_device_with_calibration_action_without_value(self):
        """Check that we give out the calibration action even without a value."""
        contact = Contact(given_name="Given", family_name="Fam", email="given@family")
        calibration_action = DeviceCalibrationAction(
            device=self.device,
            current_calibration_date=datetime.datetime(
                year=2022, month=12, day=24, tzinfo=pytz.utc
            ),
            next_calibration_date=datetime.datetime(
                year=2022, month=12, day=25, tzinfo=pytz.utc
            ),
            contact=contact,
            formula="x+y",
            description="Some desc",
        )

        db.session.add_all([contact, calibration_action])
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.device.id}/sensorml")

        self.assertEqual(resp.status_code, 200)
        xml_text = resp.text
        self.schema.validate(xml_text)
        root = xml.etree.ElementTree.fromstring(resp.text)

        sml_history = root.find("{http://www.opengis.net/sensorml/2.0}history")
        sml_event_list = sml_history.find(
            "{http://www.opengis.net/sensorml/2.0}EventList"
        )
        sml_events = sml_event_list.findall(
            "{http://www.opengis.net/sensorml/2.0}event"
        )
        self.assertEqual(len(sml_events), 1)

        sml_calibration_event = sml_events[0]

        self.assertIsNone(
            sml_calibration_event.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}classification")
            .find("{http://www.opengis.net/sensorml/2.0}ClassifierList")
            .find("{http://www.opengis.net/sensorml/2.0}classifier")
            .find("{http://www.opengis.net/sensorml/2.0}Term")
            .find("{http://www.opengis.net/sensorml/2.0}value")
            .text,
        )

    def test_get_public_device_with_generic_action(self):
        """Check that we give out the generic action."""
        contact = Contact(given_name="Given", family_name="Fam", email="given@family")
        device_maintenance_uri = current_app.config["CV_URL"] + "/actiontypes/5/"
        device_action = GenericDeviceAction(
            device=self.device,
            begin_date=datetime.datetime(year=2022, month=12, day=24, tzinfo=pytz.utc),
            end_date=datetime.datetime(year=2022, month=12, day=25, tzinfo=pytz.utc),
            contact=contact,
            description="Some desc",
            action_type_name="Device Maintenance",
            action_type_uri=device_maintenance_uri,
        )

        db.session.add_all([contact, device_action])
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.device.id}/sensorml")

        self.assertEqual(resp.status_code, 200)
        xml_text = resp.text
        self.schema.validate(xml_text)
        root = xml.etree.ElementTree.fromstring(resp.text)

        sml_history = root.find("{http://www.opengis.net/sensorml/2.0}history")
        sml_event_list = sml_history.find(
            "{http://www.opengis.net/sensorml/2.0}EventList"
        )
        sml_events = sml_event_list.findall(
            "{http://www.opengis.net/sensorml/2.0}event"
        )
        self.assertEqual(len(sml_events), 1)

        sml_action_event = sml_events[0]

        self.assertEqual(
            sml_action_event.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}classification")
            .find("{http://www.opengis.net/sensorml/2.0}ClassifierList")
            .find("{http://www.opengis.net/sensorml/2.0}classifier")
            .find("{http://www.opengis.net/sensorml/2.0}Term")
            .attrib.get("definition"),
            device_action.action_type_uri,
        )
        self.assertEqual(
            sml_action_event.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}classification")
            .find("{http://www.opengis.net/sensorml/2.0}ClassifierList")
            .find("{http://www.opengis.net/sensorml/2.0}classifier")
            .find("{http://www.opengis.net/sensorml/2.0}Term")
            .find("{http://www.opengis.net/sensorml/2.0}label")
            .text,
            device_action.action_type_name,
        )
        self.assertEqual(
            sml_action_event.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}classification")
            .find("{http://www.opengis.net/sensorml/2.0}ClassifierList")
            .find("{http://www.opengis.net/sensorml/2.0}classifier")
            .find("{http://www.opengis.net/sensorml/2.0}Term")
            .find("{http://www.opengis.net/sensorml/2.0}value")
            .text,
            device_action.action_type_name,
        )
        self.assertEqual(
            sml_action_event.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}time")
            .find("{http://www.opengis.net/gml/3.2}TimePeriod")
            .attrib.get("{http://www.opengis.net/gml/3.2}id"),
            f"TimePeriodForDeviceMaintenance_{device_action.id}_of_device_{self.device.id}",
        )
        self.assertEqual(
            sml_action_event.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}time")
            .find("{http://www.opengis.net/gml/3.2}TimePeriod")
            .find("{http://www.opengis.net/gml/3.2}begin")
            .find("{http://www.opengis.net/gml/3.2}TimeInstant")
            .find("{http://www.opengis.net/gml/3.2}timePosition")
            .text,
            "2022-12-24T00:00:00+00:00",
        )
        self.assertEqual(
            sml_action_event.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}time")
            .find("{http://www.opengis.net/gml/3.2}TimePeriod")
            .find("{http://www.opengis.net/gml/3.2}description")
            .text,
            device_action.description,
        )
        self.assertEqual(
            sml_action_event.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}time")
            .find("{http://www.opengis.net/gml/3.2}TimePeriod")
            .find("{http://www.opengis.net/gml/3.2}end")
            .find("{http://www.opengis.net/gml/3.2}TimeInstant")
            .find("{http://www.opengis.net/gml/3.2}timePosition")
            .text,
            "2022-12-25T00:00:00+00:00",
        )

    def test_get_public_device_with_generic_action_without_end_date(self):
        """Check that we give out the generic action without an end date."""
        contact = Contact(given_name="Given", family_name="Fam", email="given@family")
        device_maintenance_uri = current_app.config["CV_URL"] + "/actiontypes/5/"
        device_action = GenericDeviceAction(
            device=self.device,
            begin_date=datetime.datetime(year=2022, month=12, day=24, tzinfo=pytz.utc),
            contact=contact,
            description="Some desc",
            action_type_name="Device Maintenance",
            action_type_uri=device_maintenance_uri,
        )

        db.session.add_all([contact, device_action])
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.device.id}/sensorml")

        self.assertEqual(resp.status_code, 200)
        xml_text = resp.text
        self.schema.validate(xml_text)
        root = xml.etree.ElementTree.fromstring(resp.text)

        sml_history = root.find("{http://www.opengis.net/sensorml/2.0}history")
        sml_event_list = sml_history.find(
            "{http://www.opengis.net/sensorml/2.0}EventList"
        )
        sml_events = sml_event_list.findall(
            "{http://www.opengis.net/sensorml/2.0}event"
        )
        self.assertEqual(len(sml_events), 1)

        sml_action_event = sml_events[0]

        self.assertEqual(
            len(
                sml_action_event.find("{http://www.opengis.net/sensorml/2.0}Event")
                .find("{http://www.opengis.net/sensorml/2.0}time")
                .find("{http://www.opengis.net/gml/3.2}TimePeriod")
                .find("{http://www.opengis.net/gml/3.2}end")
                .findall("{http://www.opengis.net/gml/3.2}TimeInstant")
            ),
            0,
        )

    def test_get_public_device_with_generic_action_without_description(self):
        """Check that we give out the generic action without description."""
        contact = Contact(given_name="Given", family_name="Fam", email="given@family")
        device_maintenance_uri = current_app.config["CV_URL"] + "/actiontypes/5/"
        device_action = GenericDeviceAction(
            device=self.device,
            begin_date=datetime.datetime(year=2022, month=12, day=24, tzinfo=pytz.utc),
            contact=contact,
            action_type_name="Device Maintenance",
            action_type_uri=device_maintenance_uri,
        )

        db.session.add_all([contact, device_action])
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.device.id}/sensorml")

        self.assertEqual(resp.status_code, 200)
        xml_text = resp.text
        self.schema.validate(xml_text)
        root = xml.etree.ElementTree.fromstring(resp.text)

        sml_history = root.find("{http://www.opengis.net/sensorml/2.0}history")
        sml_event_list = sml_history.find(
            "{http://www.opengis.net/sensorml/2.0}EventList"
        )
        sml_events = sml_event_list.findall(
            "{http://www.opengis.net/sensorml/2.0}event"
        )
        self.assertEqual(len(sml_events), 1)

        sml_action_event = sml_events[0]

        self.assertIsNone(
            sml_action_event.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}time")
            .find("{http://www.opengis.net/gml/3.2}TimePeriod")
            .find("{http://www.opengis.net/gml/3.2}description")
            .text,
        )

    def test_get_public_device_with_generic_action_without_action_type_uri(self):
        """Check that we give out the generic action without action type uri."""
        contact = Contact(given_name="Given", family_name="Fam", email="given@family")
        device_action = GenericDeviceAction(
            device=self.device,
            begin_date=datetime.datetime(year=2022, month=12, day=24, tzinfo=pytz.utc),
            contact=contact,
            action_type_name="Device Maintenance",
        )

        db.session.add_all([contact, device_action])
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.device.id}/sensorml")

        self.assertEqual(resp.status_code, 200)
        xml_text = resp.text
        self.schema.validate(xml_text)
        root = xml.etree.ElementTree.fromstring(resp.text)

        sml_history = root.find("{http://www.opengis.net/sensorml/2.0}history")
        sml_event_list = sml_history.find(
            "{http://www.opengis.net/sensorml/2.0}EventList"
        )
        sml_events = sml_event_list.findall(
            "{http://www.opengis.net/sensorml/2.0}event"
        )
        self.assertEqual(len(sml_events), 1)

        sml_action_event = sml_events[0]

        self.assertEqual(
            sml_action_event.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}classification")
            .find("{http://www.opengis.net/sensorml/2.0}ClassifierList")
            .find("{http://www.opengis.net/sensorml/2.0}classifier")
            .find("{http://www.opengis.net/sensorml/2.0}Term")
            .attrib.get("definition"),
            "Action",
        )

    def test_get_public_device_with_software_update_action(self):
        """Check that we give out the software update action."""
        contact = Contact(given_name="Given", family_name="Fam", email="given@family")
        firmware_uri = current_app.config["CV_URL"] + "/softwaretypes/1/"
        update_action = DeviceSoftwareUpdateAction(
            device=self.device,
            update_date=datetime.datetime(year=2022, month=12, day=24, tzinfo=pytz.utc),
            contact=contact,
            description="Some desc",
            software_type_name="Firmware",
            software_type_uri=firmware_uri,
        )

        db.session.add_all([contact, update_action])
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.device.id}/sensorml")

        self.assertEqual(resp.status_code, 200)
        xml_text = resp.text
        self.schema.validate(xml_text)
        root = xml.etree.ElementTree.fromstring(resp.text)

        sml_history = root.find("{http://www.opengis.net/sensorml/2.0}history")
        sml_event_list = sml_history.find(
            "{http://www.opengis.net/sensorml/2.0}EventList"
        )
        sml_events = sml_event_list.findall(
            "{http://www.opengis.net/sensorml/2.0}event"
        )
        self.assertEqual(len(sml_events), 1)

        sml_update_event = sml_events[0]

        self.assertEqual(
            sml_update_event.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}classification")
            .find("{http://www.opengis.net/sensorml/2.0}ClassifierList")
            .find("{http://www.opengis.net/sensorml/2.0}classifier")
            .find("{http://www.opengis.net/sensorml/2.0}Term")
            .attrib.get("definition"),
            update_action.software_type_uri,
        )
        self.assertEqual(
            sml_update_event.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}classification")
            .find("{http://www.opengis.net/sensorml/2.0}ClassifierList")
            .find("{http://www.opengis.net/sensorml/2.0}classifier")
            .find("{http://www.opengis.net/sensorml/2.0}Term")
            .find("{http://www.opengis.net/sensorml/2.0}label")
            .text,
            update_action.software_type_name,
        )
        self.assertEqual(
            sml_update_event.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}classification")
            .find("{http://www.opengis.net/sensorml/2.0}ClassifierList")
            .find("{http://www.opengis.net/sensorml/2.0}classifier")
            .find("{http://www.opengis.net/sensorml/2.0}Term")
            .find("{http://www.opengis.net/sensorml/2.0}value")
            .text,
            update_action.software_type_name,
        )
        self.assertEqual(
            sml_update_event.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}time")
            .find("{http://www.opengis.net/gml/3.2}TimeInstant")
            .attrib.get("{http://www.opengis.net/gml/3.2}id"),
            f"TimeInstantForFirmwareUpdate_{update_action.id}_of_device_{self.device.id}",
        )
        self.assertEqual(
            sml_update_event.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}time")
            .find("{http://www.opengis.net/gml/3.2}TimeInstant")
            .find("{http://www.opengis.net/gml/3.2}timePosition")
            .text,
            "2022-12-24T00:00:00+00:00",
        )

    def test_get_public_device_with_software_update_action_without_software_type_uri(
        self,
    ):
        """Check that we give out the software update action without software type uri."""
        contact = Contact(given_name="Given", family_name="Fam", email="given@family")
        update_action = DeviceSoftwareUpdateAction(
            device=self.device,
            update_date=datetime.datetime(year=2022, month=12, day=24, tzinfo=pytz.utc),
            contact=contact,
            description="Some desc",
            software_type_name="Firmware",
        )

        db.session.add_all([contact, update_action])
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.device.id}/sensorml")

        self.assertEqual(resp.status_code, 200)
        xml_text = resp.text
        self.schema.validate(xml_text)
        root = xml.etree.ElementTree.fromstring(resp.text)

        sml_history = root.find("{http://www.opengis.net/sensorml/2.0}history")
        sml_event_list = sml_history.find(
            "{http://www.opengis.net/sensorml/2.0}EventList"
        )
        sml_events = sml_event_list.findall(
            "{http://www.opengis.net/sensorml/2.0}event"
        )
        self.assertEqual(len(sml_events), 1)

        sml_update_event = sml_events[0]

        self.assertEqual(
            sml_update_event.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}classification")
            .find("{http://www.opengis.net/sensorml/2.0}ClassifierList")
            .find("{http://www.opengis.net/sensorml/2.0}classifier")
            .find("{http://www.opengis.net/sensorml/2.0}Term")
            .attrib.get("definition"),
            "SoftwareUpdate",
        )
