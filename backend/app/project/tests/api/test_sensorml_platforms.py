# SPDX-FileCopyrightText: 2023 - 2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Tests to extract sensorML for platforms."""

import datetime
import pathlib
import pickle
import xml

import pytz
from flask import current_app

from project import base_url
from project.api.helpers.dictutils import dict_from_kv_list
from project.api.models import (
    Configuration,
    Contact,
    ExportControl,
    ExportControlAttachment,
    GenericPlatformAction,
    ManufacturerModel,
    Platform,
    PlatformAttachment,
    PlatformContactRole,
    PlatformMountAction,
    PlatformParameter,
    PlatformParameterValueChangeAction,
    PlatformSoftwareUpdateAction,
    User,
)
from project.api.models.base_model import db
from project.tests.base import BaseTestCase


class TestSensorMLPlatform(BaseTestCase):
    """Test class for the sensor ML transformation for platforms."""

    url = base_url + "/platforms"

    @classmethod
    def setUpClass(cls):
        """Set up data that we can reuse between all the test cases."""
        path_this_file = pathlib.Path(__file__)
        path_pickle_schema = (
            path_this_file.parent / "helpers" / "sensorml_schema_validator.pickle"
        )

        with path_pickle_schema.open("rb") as infile:
            cls.schema = pickle.load(infile)

    def setUp(self):
        """Set up data for the tests."""
        super().setUp()

        self.platform = Platform(
            is_public=True,
            is_private=False,
            is_internal=False,
            short_name="dummy platform",
        )
        db.session.add_all([self.platform])
        db.session.commit()

    def test_get_non_existing(self):
        """Ensure we get an 404 if the platform doesn't exist."""
        with self.client:
            resp = self.client.get(f"{self.url}/9999999999/sensorml")
        self.assertEqual(resp.status_code, 404)

    def test_get_internal_platform_without_user(self):
        """Ensure we don't show sensorML for internal platforms without a user."""
        self.platform.is_internal = True
        self.platform.is_public = False
        db.session.add_all([self.platform])
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.platform.id}/sensorml")
        self.assertEqual(resp.status_code, 401)

    def test_get_internal_platform_with_user(self):
        """Ensure we don't show sensorML for internal platforms without a user."""
        self.platform.is_internal = True
        self.platform.is_public = False
        contact = Contact(given_name="Given", family_name="Fam", email="given@family")
        user = User(subject=contact.email, contact=contact)
        db.session.add_all([self.platform, contact, user])
        db.session.commit()

        with self.run_requests_as(user):
            with self.client:
                resp = self.client.get(f"{self.url}/{self.platform.id}/sensorml")
        self.assertEqual(resp.status_code, 200)

    def test_get_private_platform_with_different_user(self):
        """Ensure we don't show sensorML for private platforms without a user."""
        contact1 = Contact(given_name="Given", family_name="Fam", email="given@family")
        user1 = User(subject=contact1.email, contact=contact1)
        self.platform.is_private = True
        self.platform.is_public = False
        self.platform.created_by = user1
        contact2 = Contact(
            given_name="Given J.", family_name="Fam", email="given.j@family"
        )
        user2 = User(subject=contact2.email, contact=contact2)
        db.session.add_all([self.platform, contact1, user1, contact2, user2])
        db.session.commit()

        with self.run_requests_as(user2):
            with self.client:
                resp = self.client.get(f"{self.url}/{self.platform.id}/sensorml")
        self.assertEqual(resp.status_code, 403)

    def test_get_private_platform_with_super_user(self):
        """Ensure we show sensorML for private platforms to a superuser."""
        contact1 = Contact(given_name="Given", family_name="Fam", email="given@family")
        user1 = User(subject=contact1.email, contact=contact1)
        self.platform.is_private = True
        self.platform.is_public = False
        self.platform.created_by = user1
        contact2 = Contact(
            given_name="Given J.", family_name="Fam", email="given.j@family"
        )
        user2 = User(subject=contact2.email, contact=contact2, is_superuser=True)
        db.session.add_all([self.platform, contact1, user1, contact2, user2])
        db.session.commit()

        with self.run_requests_as(user2):
            with self.client:
                resp = self.client.get(f"{self.url}/{self.platform.id}/sensorml")
        self.assertEqual(resp.status_code, 200)

    def test_get_private_platform_with_owner(self):
        """Ensure we show sensorML for private platforms to the owner."""
        contact1 = Contact(given_name="Given", family_name="Fam", email="given@family")
        user1 = User(subject=contact1.email, contact=contact1)
        self.platform.is_private = True
        self.platform.is_public = False
        self.platform.created_by = user1
        db.session.add_all([self.platform, contact1, user1])
        db.session.commit()

        with self.run_requests_as(user1):
            with self.client:
                resp = self.client.get(f"{self.url}/{self.platform.id}/sensorml")
        self.assertEqual(resp.status_code, 200)

    def test_get_public_platform_no_contacts_no_events(self):
        """
        Test with a platform without contacts nor events.

        The public platform should be visible for everyone.
        But a basic platform doesn't has contacts yet (the backend
        api creates one, but in our test we don't have one), nor
        events.

        But we can test the id & the short name.
        """
        with self.client:
            resp = self.client.get(f"{self.url}/{self.platform.id}/sensorml")
        self.assertEqual(resp.status_code, 200)
        xml_text = resp.text
        self.expect(xml_text).to_start_with('<?xml version="1.0" encoding="UTF-8"?>\n')
        self.schema.validate(xml_text)
        root = xml.etree.ElementTree.fromstring(resp.text)

        schema_locations = dict_from_kv_list(
            root.attrib[
                "{http://www.w3.org/2001/XMLSchema-instance}schemaLocation"
            ].split(" ")
        )

        self.expect(schema_locations["http://www.opengis.net/sensorml/2.0"]).to_equal(
            "http://schemas.opengis.net/sensorML/2.0/sensorML.xsd"
        )

        gml_id = root.attrib.get("{http://www.opengis.net/gml/3.2}id")
        self.assertEqual(gml_id, f"platform_{self.platform.id}")
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
        self.assertEqual(sml_term_value, self.platform.short_name)

        # The short name is also included as gml:name
        self.assertEqual(
            root.find("{http://www.opengis.net/gml/3.2}name").text,
            self.platform.short_name,
        )

    def test_get_public_platform_contacts(self):
        """Test with a platform with some contacts."""
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
        contact_role1 = PlatformContactRole(
            contact=contact1,
            platform=self.platform,
            role_name=owner_name,
            role_uri=owner_uri,
        )
        contact_role2 = PlatformContactRole(
            contact=contact2, platform=self.platform, role_name=pi_name, role_uri=pi_uri
        )

        db.session.add_all([contact1, contact2, contact_role1, contact_role2])
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.platform.id}/sensorml")
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

    def test_get_public_platform_with_long_name(self):
        """Check that we give out the long name."""
        self.platform.long_name = "some long name"

        db.session.add(self.platform)
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.platform.id}/sensorml")

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
            self.platform.long_name,
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
            self.platform.short_name,
        )

    def test_get_public_platform_with_pid(self):
        """Check that we give out the pid."""
        self.platform.persistent_identifier = "12345/test.abc.1234-4567"

        db.session.add(self.platform)
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.platform.id}/sensorml")

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
            self.platform.persistent_identifier,
        )

    def test_get_public_platform_with_model(self):
        """Check that we give out the model number."""
        self.platform.model = "0815"

        db.session.add(self.platform)
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.platform.id}/sensorml")

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
            self.platform.model,
        )

    def test_get_public_platform_with_status(self):
        """Check that we give out the status."""
        self.platform.status_name = "In use"

        db.session.add(self.platform)
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.platform.id}/sensorml")

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
            self.platform.status_name,
        )

    def test_get_public_platform_with_serial_number(self):
        """Check that we give out the serial number."""
        self.platform.serial_number = "1234"

        db.session.add(self.platform)
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.platform.id}/sensorml")

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
            self.platform.serial_number,
        )

    def test_get_public_platform_with_manufacturer(self):
        """Check that we give out the manufacturer."""
        self.platform.manufacturer_name = "XYZ Coop"

        db.session.add(self.platform)
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.platform.id}/sensorml")

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
            self.platform.manufacturer_name,
        )

    def test_get_public_platform_with_platform_type(self):
        """Check that we give out the platform type."""
        self.platform.platform_type_name = "Barometer"

        db.session.add(self.platform)
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.platform.id}/sensorml")

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
        sml_classifier_platform_type = sml_classifiers[0]

        self.assertEqual(
            sml_classifier_platform_type.find(
                "{http://www.opengis.net/sensorml/2.0}Term"
            ).attrib.get("definition"),
            "http://sensorml.com/ont/swe/property/PlatformType",
        )
        self.assertEqual(
            sml_classifier_platform_type.find(
                "{http://www.opengis.net/sensorml/2.0}Term"
            )
            .find("{http://www.opengis.net/sensorml/2.0}label")
            .text,
            "platform type",
        )
        self.assertEqual(
            sml_classifier_platform_type.find(
                "{http://www.opengis.net/sensorml/2.0}Term"
            )
            .find("{http://www.opengis.net/sensorml/2.0}value")
            .text,
            self.platform.platform_type_name,
        )

    def test_get_public_platform_with_country(self):
        """Check that we give out the country."""
        self.platform.country = "Germany"

        db.session.add(self.platform)
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.platform.id}/sensorml")

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
        # First one is short name
        sml_identifier_country = sml_identifiers[1]

        self.assertEqual(
            sml_identifier_country.find(
                "{http://www.opengis.net/sensorml/2.0}Term"
            ).attrib.get("definition"),
            "http://sensorml.com/ont/misb0601/identifier/Country_of_Manufacture",
        )
        self.assertEqual(
            sml_identifier_country.find("{http://www.opengis.net/sensorml/2.0}Term")
            .find("{http://www.opengis.net/sensorml/2.0}label")
            .text,
            "Country of Manufacture",
        )
        self.assertEqual(
            sml_identifier_country.find("{http://www.opengis.net/sensorml/2.0}Term")
            .find("{http://www.opengis.net/sensorml/2.0}value")
            .text,
            self.platform.country,
        )

    def test_get_public_platform_with_description(self):
        """Check that we give out the description."""
        self.platform.description = "Some long description"

        db.session.add(self.platform)
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.platform.id}/sensorml")

        self.assertEqual(resp.status_code, 200)
        xml_text = resp.text
        self.schema.validate(xml_text)
        root = xml.etree.ElementTree.fromstring(resp.text)
        sml_description = root.find("{http://www.opengis.net/gml/3.2}description")
        self.assertEqual(sml_description.text, self.platform.description)

    def test_get_public_platform_with_website(self):
        """Check that we give out the website."""
        self.platform.website = "https://gfz-potsdam.de"

        db.session.add(self.platform)
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.platform.id}/sensorml")

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
            self.platform.website,
        )

    def test_get_public_platform_with_platform_parameters(self):
        """Check that we give out the platform parameters."""
        parameter = PlatformParameter(
            unit_name="°C",
            unit_uri="https://cv/units/1",
            label="Fan start temperature",
            description="Temperature on that the fan starts",
            platform=self.platform,
        )
        db.session.add(parameter)
        db.session.commit()

        with self.client:
            resp = self.client.get(f"{self.url}/{self.platform.id}/sensorml")

        self.expect(resp.status_code).to_equal(200)
        xml_text = resp.text
        self.schema.validate(xml_text)
        root = xml.etree.ElementTree.fromstring(resp.text)
        sml_parameters = root.find("{http://www.opengis.net/sensorml/2.0}parameters")
        sml_parameter_list = sml_parameters.find(
            "{http://www.opengis.net/sensorml/2.0}ParameterList"
        )
        sml_parameter_entries = sml_parameter_list.findall(
            "{http://www.opengis.net/sensorml/2.0}parameter"
        )
        self.expect(sml_parameter_entries).to_have_length(1)
        sml_parameter = sml_parameter_entries[0]

        self.expect(sml_parameter.attrib.get("name")).to_equal("Fan_start_temperature")

        swe_quantity = sml_parameter.find("{http://www.opengis.net/swe/2.0}Quantity")
        self.expect(swe_quantity).not_.to_be_none()
        swe_uom = swe_quantity.find("{http://www.opengis.net/swe/2.0}uom")
        self.expect(swe_uom).not_.to_be_none()

        self.expect(swe_uom.attrib.get("code")).to_equal(parameter.unit_name)

    def test_get_public_platform_with_platform_parameter_value_change_actions(self):
        """Check that we give out the parameter change actions."""
        parameter = PlatformParameter(
            unit_name="°C",
            unit_uri="https://cv/units/1",
            label="Fan start temperature",
            description="Temperature on that the fan starts",
            platform=self.platform,
        )
        contact = Contact(
            given_name="first", family_name="contact", email="first.contact@localhost"
        )
        change_action = PlatformParameterValueChangeAction(
            platform_parameter=parameter,
            contact=contact,
            date=datetime.datetime(2023, 5, 3, 10, 00, 00, tzinfo=pytz.utc),
            value="42",
            description="The answer to everything - and the start temperature for the fan.",
        )
        db.session.add_all([parameter, contact, change_action])
        db.session.commit()

        with self.client:
            resp = self.client.get(f"{self.url}/{self.platform.id}/sensorml")

        self.expect(resp.status_code).to_equal(200)
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
        self.expect(sml_events).to_have_length(1)
        sml_change_event = sml_events[0]

        # Test the classification
        self.expect(
            sml_change_event.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}classification")
            .find("{http://www.opengis.net/sensorml/2.0}ClassifierList")
            .find("{http://www.opengis.net/sensorml/2.0}classifier")
            .find("{http://www.opengis.net/sensorml/2.0}Term")
            .attrib.get("definition")
        ).to_equal("ParameterChange")
        self.expect(
            sml_change_event.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}classification")
            .find("{http://www.opengis.net/sensorml/2.0}ClassifierList")
            .find("{http://www.opengis.net/sensorml/2.0}classifier")
            .find("{http://www.opengis.net/sensorml/2.0}Term")
            .find("{http://www.opengis.net/sensorml/2.0}label")
            .text,
        ).to_equal(
            f"Changed parameter for {parameter.label}",
        )
        self.expect(
            sml_change_event.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}classification")
            .find("{http://www.opengis.net/sensorml/2.0}ClassifierList")
            .find("{http://www.opengis.net/sensorml/2.0}classifier")
            .find("{http://www.opengis.net/sensorml/2.0}Term")
            .find("{http://www.opengis.net/sensorml/2.0}value")
            .text,
        ).to_equal(change_action.value)
        self.expect(
            sml_change_event.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}time")
            .find("{http://www.opengis.net/gml/3.2}TimeInstant")
            .find("{http://www.opengis.net/gml/3.2}timePosition")
            .text,
        ).to_equal(
            "2023-05-03T10:00:00+00:00",
        )
        sml_set_value = (
            sml_change_event.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}configuration")
            .find("{http://www.opengis.net/sensorml/2.0}Settings")
            .find("{http://www.opengis.net/sensorml/2.0}setValue")
        )
        self.expect(sml_set_value).not_.to_be_none()
        self.expect(sml_set_value.attrib.get("ref")).to_equal("Fan_start_temperature")
        self.expect(sml_set_value.text).to_equal(change_action.value)

    def test_get_public_platform_with_b2inst_record(self):
        """Check that we give out the website."""
        self.platform.b2inst_record_id = "123"
        current_app.config.update({"B2INST_URL": "https://b2inst-test.gwdg.de"})

        db.session.add(self.platform)
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.platform.id}/sensorml")

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
            "PIDINST",
        )
        self.assertEqual(
            sml_document_website.find(
                "{http://www.isotc211.org/2005/gmd}CI_OnlineResource"
            )
            .find("{http://www.isotc211.org/2005/gmd}linkage")
            .find("{http://www.isotc211.org/2005/gmd}URL")
            .text,
            f"https://b2inst-test.gwdg.de/records/{self.platform.b2inst_record_id}",
        )

    def test_get_public_platform_with_attachments(self):
        """Check that we give out the attachments."""
        attachment = PlatformAttachment(
            platform=self.platform, url="https://ufz.de", label="UFZ-Page"
        )

        db.session.add(attachment)
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.platform.id}/sensorml")

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
            f"Attachment_{attachment.id}_of_PhysicalSystem_platform_{self.platform.id}",
        )

    def test_get_public_platform_with_mount(self):
        """Check that we give out the platform mount."""
        configuration = Configuration(label="Test config")
        contact = Contact(given_name="Given", family_name="Fam", email="given@family")
        platform_mount = PlatformMountAction(
            platform=self.platform,
            configuration=configuration,
            begin_date=datetime.datetime(year=2022, month=12, day=24, tzinfo=pytz.utc),
            begin_contact=contact,
            end_date=datetime.datetime(year=2022, month=12, day=25, tzinfo=pytz.utc),
            begin_description="Mount of platform on test config",
        )

        db.session.add_all([configuration, platform_mount, contact])
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.platform.id}/sensorml")

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
            f"TimePeriodForPlatformMountAction_{platform_mount.id}_of_platform_{self.platform.id}",
        )
        self.assertEqual(
            sml_mount_event.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}time")
            .find("{http://www.opengis.net/gml/3.2}TimePeriod")
            .find("{http://www.opengis.net/gml/3.2}description")
            .text,
            platform_mount.begin_description,
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

    def test_get_public_platform_with_mount_without_end(self):
        """Check that we give out the platform mount without an end date."""
        configuration = Configuration(label="Test config")
        contact = Contact(given_name="Given", family_name="Fam", email="given@family")
        platform_mount = PlatformMountAction(
            platform=self.platform,
            configuration=configuration,
            begin_date=datetime.datetime(year=2022, month=12, day=24, tzinfo=pytz.utc),
            begin_contact=contact,
            begin_description="Mount of platform on test config",
        )

        db.session.add_all([configuration, platform_mount, contact])
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.platform.id}/sensorml")

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

        gml_end = (
            sml_mount_event.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}time")
            .find("{http://www.opengis.net/gml/3.2}TimePeriod")
            .find("{http://www.opengis.net/gml/3.2}end")
        )
        self.expect(len).of(
            gml_end.findall("{http://www.opengis.net/gml/3.2}TimeInstant")
        ).to_equal(0)
        self.expect(gml_end.attrib["nilReason"]).to_equal("inapplicable")

    def test_get_public_platform_with_mount_without_description(self):
        """Check that we give out the platform mount without a description."""
        configuration = Configuration(label="Test config")
        contact = Contact(given_name="Given", family_name="Fam", email="given@family")
        platform_mount = PlatformMountAction(
            platform=self.platform,
            configuration=configuration,
            begin_date=datetime.datetime(year=2022, month=12, day=24, tzinfo=pytz.utc),
            begin_contact=contact,
        )

        db.session.add_all([configuration, platform_mount, contact])
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.platform.id}/sensorml")

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

    def test_get_public_platform_with_mount_without_configuration_label(self):
        """Check that we give out the platform mount without a configuration label."""
        configuration = Configuration()
        contact = Contact(given_name="Given", family_name="Fam", email="given@family")
        platform_mount = PlatformMountAction(
            platform=self.platform,
            configuration=configuration,
            begin_date=datetime.datetime(year=2022, month=12, day=24, tzinfo=pytz.utc),
            begin_contact=contact,
        )

        db.session.add_all([configuration, platform_mount, contact])
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.platform.id}/sensorml")

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

    def test_get_public_platform_with_generic_action(self):
        """Check that we give out the generic action."""
        contact = Contact(given_name="Given", family_name="Fam", email="given@family")
        platform_maintenance_uri = current_app.config["CV_URL"] + "/actiontypes/5/"
        platform_action = GenericPlatformAction(
            platform=self.platform,
            begin_date=datetime.datetime(year=2022, month=12, day=24, tzinfo=pytz.utc),
            end_date=datetime.datetime(year=2022, month=12, day=25, tzinfo=pytz.utc),
            contact=contact,
            description="Some desc",
            action_type_name="Platform Maintenance",
            action_type_uri=platform_maintenance_uri,
        )

        db.session.add_all([contact, platform_action])
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.platform.id}/sensorml")

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
            platform_action.action_type_uri,
        )
        self.assertEqual(
            sml_action_event.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}classification")
            .find("{http://www.opengis.net/sensorml/2.0}ClassifierList")
            .find("{http://www.opengis.net/sensorml/2.0}classifier")
            .find("{http://www.opengis.net/sensorml/2.0}Term")
            .find("{http://www.opengis.net/sensorml/2.0}label")
            .text,
            platform_action.action_type_name,
        )
        self.assertEqual(
            sml_action_event.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}classification")
            .find("{http://www.opengis.net/sensorml/2.0}ClassifierList")
            .find("{http://www.opengis.net/sensorml/2.0}classifier")
            .find("{http://www.opengis.net/sensorml/2.0}Term")
            .find("{http://www.opengis.net/sensorml/2.0}value")
            .text,
            platform_action.action_type_name,
        )
        self.assertEqual(
            sml_action_event.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}time")
            .find("{http://www.opengis.net/gml/3.2}TimePeriod")
            .attrib.get("{http://www.opengis.net/gml/3.2}id"),
            f"TimePeriodForPlatformMaintenance_{platform_action.id}_"
            + f"of_platform_{self.platform.id}",
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
            platform_action.description,
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

    def test_get_public_platform_with_generic_action_without_end_date(self):
        """Check that we give out the generic action without an end date."""
        contact = Contact(given_name="Given", family_name="Fam", email="given@family")
        platform_maintenance_uri = current_app.config["CV_URL"] + "/actiontypes/5/"
        platform_action = GenericPlatformAction(
            platform=self.platform,
            begin_date=datetime.datetime(year=2022, month=12, day=24, tzinfo=pytz.utc),
            contact=contact,
            description="Some desc",
            action_type_name="Platform Maintenance",
            action_type_uri=platform_maintenance_uri,
        )

        db.session.add_all([contact, platform_action])
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.platform.id}/sensorml")

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

        gml_end = (
            sml_action_event.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}time")
            .find("{http://www.opengis.net/gml/3.2}TimePeriod")
            .find("{http://www.opengis.net/gml/3.2}end")
        )

        self.expect(len).of(
            gml_end.findall("{http://www.opengis.net/gml/3.2}TimeInstant")
        ).to_equal(0)
        self.expect(gml_end.attrib["nilReason"]).to_equal("inapplicable")

    def test_get_public_platform_with_generic_action_without_description(self):
        """Check that we give out the generic action without description."""
        contact = Contact(given_name="Given", family_name="Fam", email="given@family")
        platform_maintenance_uri = current_app.config["CV_URL"] + "/actiontypes/5/"
        platform_action = GenericPlatformAction(
            platform=self.platform,
            begin_date=datetime.datetime(year=2022, month=12, day=24, tzinfo=pytz.utc),
            contact=contact,
            action_type_name="Platform Maintenance",
            action_type_uri=platform_maintenance_uri,
        )

        db.session.add_all([contact, platform_action])
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.platform.id}/sensorml")

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

    def test_get_public_platform_with_generic_action_without_action_type_uri(self):
        """Check that we give out the generic action without action type uri."""
        contact = Contact(given_name="Given", family_name="Fam", email="given@family")
        platform_action = GenericPlatformAction(
            platform=self.platform,
            begin_date=datetime.datetime(year=2022, month=12, day=24, tzinfo=pytz.utc),
            contact=contact,
            action_type_name="Platform Maintenance",
        )

        db.session.add_all([contact, platform_action])
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.platform.id}/sensorml")

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

    def test_get_public_platform_with_software_update_action(self):
        """Check that we give out the software update action."""
        contact = Contact(given_name="Given", family_name="Fam", email="given@family")
        firmware_uri = current_app.config["CV_URL"] + "/softwaretypes/1/"
        update_action = PlatformSoftwareUpdateAction(
            platform=self.platform,
            update_date=datetime.datetime(year=2022, month=12, day=24, tzinfo=pytz.utc),
            contact=contact,
            description="Some desc",
            software_type_name="Firmware",
            software_type_uri=firmware_uri,
        )

        db.session.add_all([contact, update_action])
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.platform.id}/sensorml")

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
            f"TimeInstantForFirmwareUpdate_{update_action.id}_of_platform_{self.platform.id}",
        )
        self.assertEqual(
            sml_update_event.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}time")
            .find("{http://www.opengis.net/gml/3.2}TimeInstant")
            .find("{http://www.opengis.net/gml/3.2}timePosition")
            .text,
            "2022-12-24T00:00:00+00:00",
        )

    def test_get_public_platform_with_software_update_action_without_software_type_uri(
        self,
    ):
        """Check that we give out the software update action without software type uri."""
        contact = Contact(given_name="Given", family_name="Fam", email="given@family")
        update_action = PlatformSoftwareUpdateAction(
            platform=self.platform,
            update_date=datetime.datetime(year=2022, month=12, day=24, tzinfo=pytz.utc),
            contact=contact,
            description="Some desc",
            software_type_name="Firmware",
        )

        db.session.add_all([contact, update_action])
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.platform.id}/sensorml")

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

    def test_keywords(self):
        """Check that we give out keywords."""
        self.platform.keywords = ["some", "fancy keyword"]
        db.session.add(self.platform)
        db.session.commit()

        with self.client:
            resp = self.client.get(f"{self.url}/{self.platform.id}/sensorml")

        self.assertEqual(resp.status_code, 200)
        xml_text = resp.text
        self.schema.validate(xml_text)
        root = xml.etree.ElementTree.fromstring(resp.text)

        sml_keywords = root.find("{http://www.opengis.net/sensorml/2.0}keywords")
        sml_keyword_list = sml_keywords.find(
            "{http://www.opengis.net/sensorml/2.0}KeywordList"
        )
        sml_keyword_entries = sml_keyword_list.findall(
            "{http://www.opengis.net/sensorml/2.0}keyword"
        )
        self.assertEqual(len(sml_keyword_entries), 2)

        self.assertEqual(sml_keyword_entries[0].text, "some")
        self.assertEqual(sml_keyword_entries[1].text, "fancy keyword")

    def test_export_control(self):
        """Check that we give out export contorl information."""
        self.platform.manufacturer_name = "TRUEBENER"
        self.platform.model = "SMT 100"

        manufacturer_model = ManufacturerModel(
            manufacturer_name=self.platform.manufacturer_name, model=self.platform.model
        )
        export_control = ExportControl(
            manufacturer_model=manufacturer_model,
            dual_use=True,
            export_control_classification_number="1234",
            customs_tariff_number="5678",
        )
        visible_attachment = ExportControlAttachment(
            manufacturer_model=manufacturer_model,
            label="website",
            url="https://www.gfz-potsdam.de",
            is_export_control_only=False,
        )
        invisble_attachment = ExportControlAttachment(
            manufacturer_model=manufacturer_model,
            label="internal",
            url="https://www.gfz-potsdam.de/special",
            is_export_control_only=True,
        )
        db.session.add_all(
            [
                self.platform,
                manufacturer_model,
                export_control,
                visible_attachment,
                invisble_attachment,
            ]
        )
        db.session.commit()

        with self.client:
            resp = self.client.get(f"{self.url}/{self.platform.id}/sensorml")

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
        self.assertEqual(len(sml_identifiers), 5)

        sml_identifier1 = sml_identifiers[0]
        sml_term1 = sml_identifier1.find("{http://www.opengis.net/sensorml/2.0}Term")
        sml_term_definition1 = sml_term1.attrib.get("definition")
        self.assertEqual(
            sml_term_definition1, "http://sensorml.com/ont/swe/property/ShortName"
        )
        sml_term_label1 = sml_term1.find(
            "{http://www.opengis.net/sensorml/2.0}label"
        ).text
        self.assertEqual(sml_term_label1, "Short Name")
        sml_term_value1 = sml_term1.find(
            "{http://www.opengis.net/sensorml/2.0}value"
        ).text
        self.assertEqual(sml_term_value1, self.platform.short_name)

        sml_identifier2 = sml_identifiers[1]
        sml_term2 = sml_identifier2.find("{http://www.opengis.net/sensorml/2.0}Term")
        sml_term_label2 = sml_term2.find(
            "{http://www.opengis.net/sensorml/2.0}label"
        ).text
        self.assertEqual(sml_term_label2, "Model Number")
        sml_term_value2 = sml_term2.find(
            "{http://www.opengis.net/sensorml/2.0}value"
        ).text
        self.assertEqual(sml_term_value2, self.platform.model)

        sml_identifier3 = sml_identifiers[2]
        sml_term3 = sml_identifier3.find("{http://www.opengis.net/sensorml/2.0}Term")
        sml_term_label3 = sml_term3.find(
            "{http://www.opengis.net/sensorml/2.0}label"
        ).text
        self.assertEqual(sml_term_label3, "Manufacturer")
        sml_term_value3 = sml_term3.find(
            "{http://www.opengis.net/sensorml/2.0}value"
        ).text
        self.assertEqual(sml_term_value3, self.platform.manufacturer_name)

        sml_identifier4 = sml_identifiers[3]
        sml_term4 = sml_identifier4.find("{http://www.opengis.net/sensorml/2.0}Term")
        sml_term_label4 = sml_term4.find(
            "{http://www.opengis.net/sensorml/2.0}label"
        ).text
        self.assertEqual(sml_term_label4, "Export Control Classification Number")
        sml_term_value4 = sml_term4.find(
            "{http://www.opengis.net/sensorml/2.0}value"
        ).text
        self.assertEqual(
            sml_term_value4, export_control.export_control_classification_number
        )

        sml_identifier5 = sml_identifiers[4]
        sml_term5 = sml_identifier5.find("{http://www.opengis.net/sensorml/2.0}Term")
        sml_term_label5 = sml_term5.find(
            "{http://www.opengis.net/sensorml/2.0}label"
        ).text
        self.assertEqual(sml_term_label5, "Customs Tariff Number")
        sml_term_value5 = sml_term5.find(
            "{http://www.opengis.net/sensorml/2.0}value"
        ).text
        self.assertEqual(sml_term_value5, export_control.customs_tariff_number)

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
            visible_attachment.url,
        )
        self.assertEqual(
            sml_document_website.find(
                "{http://www.isotc211.org/2005/gmd}CI_OnlineResource"
            )
            .find("{http://www.isotc211.org/2005/gmd}name")
            .find("{http://www.isotc211.org/2005/gco}CharacterString")
            .text,
            visible_attachment.label,
        )

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
        sml_classifier_dual_use = sml_classifiers[0]

        self.assertEqual(
            sml_classifier_dual_use.find("{http://www.opengis.net/sensorml/2.0}Term")
            .find("{http://www.opengis.net/sensorml/2.0}label")
            .text,
            "dual use",
        )
        self.assertEqual(
            sml_classifier_dual_use.find("{http://www.opengis.net/sensorml/2.0}Term")
            .find("{http://www.opengis.net/sensorml/2.0}value")
            .text,
            "yes",
        )
