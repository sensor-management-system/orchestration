# SPDX-FileCopyrightText: 2023 - 2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Tests to extract sensorML for sites."""

import pathlib
import pickle
import xml

from flask import current_app

from project import base_url
from project.api.helpers.dictutils import dict_from_kv_list
from project.api.models import (
    Configuration,
    Contact,
    Site,
    SiteAttachment,
    SiteContactRole,
    User,
)
from project.api.models.base_model import db
from project.api.serializer.fields.wkt_polygon_field import WktPolygonField
from project.tests.base import BaseTestCase


class TestSensorMLSite(BaseTestCase):
    """Test class for the sensor ML transformation for sites."""

    url = base_url + "/sites"

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

        self.site = Site(
            is_public=True,
            is_internal=False,
            label="dummy site",
        )
        db.session.add_all([self.site])
        db.session.commit()

    def test_get_non_existing(self):
        """Ensure we get an 404 if the site doesn't exist."""
        with self.client:
            resp = self.client.get(f"{self.url}/9999999999/sensorml")
        self.assertEqual(resp.status_code, 404)

    def test_get_internal_site_without_user(self):
        """Ensure we don't show sensorML for internal sites without a user."""
        self.site.is_internal = True
        self.site.is_public = False
        db.session.add_all([self.site])
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.site.id}/sensorml")
        self.assertEqual(resp.status_code, 401)

    def test_get_internal_site_with_user(self):
        """Ensure we show sensorML for internal sites with a user."""
        self.site.is_internal = True
        self.site.is_public = False
        contact = Contact(given_name="Given", family_name="Fam", email="given@family")
        user = User(subject=contact.email, contact=contact)
        db.session.add_all([self.site, contact, user])
        db.session.commit()

        with self.run_requests_as(user):
            with self.client:
                resp = self.client.get(f"{self.url}/{self.site.id}/sensorml")
        self.assertEqual(resp.status_code, 200)

    def test_get_public_site_no_contacts(self):
        """
        Test with a site without contacts.

        The public site should be visible for everyone.
        But a basic site doesn't has contacts yet (the backend
        api creates one, but in our test we don't have one).

        But we can test the id & the label.
        """
        with self.client:
            resp = self.client.get(f"{self.url}/{self.site.id}/sensorml")
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
        self.assertEqual(gml_id, f"site_{self.site.id}")

        self.assertEqual(
            root.find("{http://www.opengis.net/gml/3.2}name").text,
            self.site.label,
        )

    def test_get_public_site_with_description(self):
        """Check that we give out the description."""
        self.site.description = "Some long description"
        db.session.add(self.site)
        db.session.commit()

        with self.client:
            resp = self.client.get(f"{self.url}/{self.site.id}/sensorml")

        self.assertEqual(resp.status_code, 200)
        xml_text = resp.text
        self.schema.validate(xml_text)
        root = xml.etree.ElementTree.fromstring(resp.text)
        sml_description = root.find("{http://www.opengis.net/gml/3.2}description")
        self.assertEqual(sml_description.text, self.site.description)

    def test_get_public_site_contacts(self):
        """Test with a site with some contacts."""
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
        contact_role1 = SiteContactRole(
            contact=contact1,
            site=self.site,
            role_name=owner_name,
            role_uri=owner_uri,
        )
        contact_role2 = SiteContactRole(
            contact=contact2,
            site=self.site,
            role_name=pi_name,
            role_uri=pi_uri,
        )

        db.session.add_all([contact1, contact2, contact_role1, contact_role2])
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.site.id}/sensorml")
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

    def test_get_public_site_with_website(self):
        """Check that we give out the website."""
        self.site.website = "https://gfz-potsdam.de"

        db.session.add(self.site)
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.site.id}/sensorml")

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
            self.site.website,
        )

    def test_get_public_site_with_attachments(self):
        """Check that we give out the attachments."""
        attachment = SiteAttachment(
            site=self.site, url="https://ufz.de", label="UFZ-Page"
        )

        db.session.add(attachment)
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.site.id}/sensorml")

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
            f"Attachment_{attachment.id}_of_PhysicalSystem_site_{self.site.id}",
        )

    def test_get_public_site_with_site_type(self):
        """Check that we give out the site type."""
        self.site.site_type_name = "Forest"

        db.session.add(self.site)
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.site.id}/sensorml")

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
        sml_classifier_site_type = sml_classifiers[0]

        self.assertEqual(
            sml_classifier_site_type.find(
                "{http://www.opengis.net/sensorml/2.0}Term"
            ).attrib.get("definition"),
            "SiteType",
        )
        self.assertEqual(
            sml_classifier_site_type.find("{http://www.opengis.net/sensorml/2.0}Term")
            .find("{http://www.opengis.net/sensorml/2.0}label")
            .text,
            "site type",
        )
        self.assertEqual(
            sml_classifier_site_type.find("{http://www.opengis.net/sensorml/2.0}Term")
            .find("{http://www.opengis.net/sensorml/2.0}value")
            .text,
            self.site.site_type_name,
        )

    def test_get_public_site_with_site_usage(self):
        """Check that we give out the site usage."""
        self.site.site_usage_name = "Forest"

        db.session.add(self.site)
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.site.id}/sensorml")

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
        sml_classifier_site_usage = sml_classifiers[0]

        self.assertEqual(
            sml_classifier_site_usage.find(
                "{http://www.opengis.net/sensorml/2.0}Term"
            ).attrib.get("definition"),
            "SiteUsage",
        )
        self.assertEqual(
            sml_classifier_site_usage.find("{http://www.opengis.net/sensorml/2.0}Term")
            .find("{http://www.opengis.net/sensorml/2.0}label")
            .text,
            "site usage",
        )
        self.assertEqual(
            sml_classifier_site_usage.find("{http://www.opengis.net/sensorml/2.0}Term")
            .find("{http://www.opengis.net/sensorml/2.0}value")
            .text,
            self.site.site_usage_name,
        )

    def test_get_public_site_textual_location(self):
        """Ensure we put the textual location in the sensorML."""
        self.site.city = "Potsdam"
        self.site.zip_code = "14473"
        self.site.country = "Germany"
        self.site.street = "Telegrafenberg"
        # GFZ doesn't have a street number, but lets imagine that it would have it.
        self.site.street_number = "123"
        self.site.building = "A70"
        self.site.room = "319"

        db.session.add(self.site)
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.site.id}/sensorml")

        self.assertEqual(resp.status_code, 200)
        xml_text = resp.text
        self.schema.validate(xml_text)
        root = xml.etree.ElementTree.fromstring(resp.text)
        sml_position = root.find("{http://www.opengis.net/sensorml/2.0}position")
        sml_text = sml_position.find("{http://www.opengis.net/swe/2.0}Text")
        sml_extension = sml_text.find("{http://www.opengis.net/swe/2.0}extension")
        gmd_ci_address = sml_extension.find(
            "{http://www.isotc211.org/2005/gmd}CI_Address"
        )
        self.assertEqual(
            gmd_ci_address.find("{http://www.isotc211.org/2005/gmd}city")
            .find("{http://www.isotc211.org/2005/gco}CharacterString")
            .text,
            self.site.city,
        )
        self.assertEqual(
            gmd_ci_address.find("{http://www.isotc211.org/2005/gmd}postalCode")
            .find("{http://www.isotc211.org/2005/gco}CharacterString")
            .text,
            self.site.zip_code,
        )
        self.assertEqual(
            gmd_ci_address.find("{http://www.isotc211.org/2005/gmd}country")
            .find("{http://www.isotc211.org/2005/gco}CharacterString")
            .text,
            self.site.country,
        )
        self.assertEqual(
            gmd_ci_address.find("{http://www.isotc211.org/2005/gmd}deliveryPoint")
            .find("{http://www.isotc211.org/2005/gco}CharacterString")
            .text,
            "Telegrafenberg 123 - Building: A70 Room: 319",
        )

    def test_get_public_site_geometry_location(self):
        """Ensure we put the geometry location in the sensorML."""
        wkt = "POLYGON ((0 0, 0 15, 15 15, 15 0, 0 0))"
        self.site.geometry = WktPolygonField().deserialize(wkt)
        self.site.epsg_code = "4326"
        db.session.add(self.site)
        db.session.commit()

        with self.client:
            resp = self.client.get(f"{self.url}/{self.site.id}/sensorml")

        self.assertEqual(resp.status_code, 200)
        xml_text = resp.text
        self.schema.validate(xml_text)
        root = xml.etree.ElementTree.fromstring(resp.text)

        gml_location = root.find("{http://www.opengis.net/gml/3.2}location")
        gml_polygon = gml_location.find("{http://www.opengis.net/gml/3.2}Polygon")
        self.assertEqual(
            gml_polygon.attrib.get("srsName"),
            "http://www.opengis.net/def/crs/EPSG/0/4326",
        )
        self.assertEqual(
            gml_polygon.attrib.get("{http://www.opengis.net/gml/3.2}id"),
            f"site_{self.site.id}_geometry",
        )

        gml_exterior = gml_polygon.find("{http://www.opengis.net/gml/3.2}exterior")
        gml_linear_ring = gml_exterior.find(
            "{http://www.opengis.net/gml/3.2}LinearRing"
        )
        gml_pos_list = gml_linear_ring.findall("{http://www.opengis.net/gml/3.2}pos")
        self.assertEqual(gml_pos_list[0].text, "0.0 0.0")
        self.assertEqual(gml_pos_list[1].text, "15.0 0.0")
        self.assertEqual(gml_pos_list[2].text, "15.0 15.0")
        self.assertEqual(gml_pos_list[3].text, "0.0 15.0")
        self.assertEqual(gml_pos_list[4].text, "0.0 0.0")

    def test_get_public_site_textual_location_and_geometry(self):
        """Check that we can show both in the sensorML at the same time."""
        self.site.city = "Potsdam"
        self.site.zip_code = "14473"
        self.site.country = "Germany"
        self.site.street = "Telegrafenberg"
        # GFZ doesn't have a street number, but lets imagine that it would have it.
        self.site.building = "A70"
        self.site.room = "319"
        wkt = "POLYGON ((0 0, 0 15, 15 15, 15 0, 0 0))"
        self.site.geometry = WktPolygonField().deserialize(wkt)

        db.session.add(self.site)
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.site.id}/sensorml")

        self.assertEqual(resp.status_code, 200)
        xml_text = resp.text
        self.schema.validate(xml_text)
        root = xml.etree.ElementTree.fromstring(resp.text)
        sml_position = root.find("{http://www.opengis.net/sensorml/2.0}position")
        sml_text = sml_position.find("{http://www.opengis.net/swe/2.0}Text")
        sml_extension = sml_text.find("{http://www.opengis.net/swe/2.0}extension")
        gmd_ci_address = sml_extension.find(
            "{http://www.isotc211.org/2005/gmd}CI_Address"
        )
        self.assertEqual(
            gmd_ci_address.find("{http://www.isotc211.org/2005/gmd}city")
            .find("{http://www.isotc211.org/2005/gco}CharacterString")
            .text,
            self.site.city,
        )
        self.assertEqual(
            gmd_ci_address.find("{http://www.isotc211.org/2005/gmd}postalCode")
            .find("{http://www.isotc211.org/2005/gco}CharacterString")
            .text,
            self.site.zip_code,
        )
        self.assertEqual(
            gmd_ci_address.find("{http://www.isotc211.org/2005/gmd}country")
            .find("{http://www.isotc211.org/2005/gco}CharacterString")
            .text,
            self.site.country,
        )
        self.assertEqual(
            gmd_ci_address.find("{http://www.isotc211.org/2005/gmd}deliveryPoint")
            .find("{http://www.isotc211.org/2005/gco}CharacterString")
            .text,
            "Telegrafenberg - Building: A70 Room: 319",
        )

        gml_location = root.find("{http://www.opengis.net/gml/3.2}location")
        gml_polygon = gml_location.find("{http://www.opengis.net/gml/3.2}Polygon")
        gml_exterior = gml_polygon.find("{http://www.opengis.net/gml/3.2}exterior")
        gml_linear_ring = gml_exterior.find(
            "{http://www.opengis.net/gml/3.2}LinearRing"
        )
        gml_pos_list = gml_linear_ring.findall("{http://www.opengis.net/gml/3.2}pos")
        self.assertEqual(gml_pos_list[0].text, "0.0 0.0")
        self.assertEqual(gml_pos_list[1].text, "15.0 0.0")
        self.assertEqual(gml_pos_list[2].text, "15.0 15.0")
        self.assertEqual(gml_pos_list[3].text, "0.0 15.0")
        self.assertEqual(gml_pos_list[4].text, "0.0 0.0")

    def test_public_site_with_public_and_internal_configuration_without_user(self):
        """Ensure we put public configurations into the sensorML."""
        public_configuration = Configuration(
            label="public configuration1",
            site=self.site,
            is_public=True,
            is_internal=False,
        )
        internal_configuration = Configuration(
            label="internal configuration1",
            site=self.site,
            is_public=False,
            is_internal=True,
        )
        db.session.add_all([public_configuration, internal_configuration])
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.site.id}/sensorml")

        self.assertEqual(resp.status_code, 200)
        xml_text = resp.text
        self.schema.validate(xml_text)
        root = xml.etree.ElementTree.fromstring(resp.text)
        sml_components = root.find("{http://www.opengis.net/sensorml/2.0}components")
        sml_component_list = sml_components.find(
            "{http://www.opengis.net/sensorml/2.0}ComponentList"
        )
        sml_component_entries = sml_component_list.findall(
            "{http://www.opengis.net/sensorml/2.0}component"
        )

        self.assertEqual(len(sml_component_entries), 1)

        sml_physical_system_public_config = sml_component_entries[0].find(
            "{http://www.opengis.net/sensorml/2.0}PhysicalSystem"
        )
        gml_id_public_config = sml_physical_system_public_config.attrib.get(
            "{http://www.opengis.net/gml/3.2}id"
        )

        self.assertEqual(
            gml_id_public_config, f"configuration_{public_configuration.id}"
        )

    def test_public_site_with_public_and_internal_configuration_with_user(self):
        """Ensure we put internal configurations into the sensorML too."""
        public_configuration = Configuration(
            label="public configuration1",
            site=self.site,
            is_public=True,
            is_internal=False,
        )
        internal_configuration = Configuration(
            label="internal configuration1",
            site=self.site,
            is_public=False,
            is_internal=True,
        )
        contact = Contact(given_name="Given", family_name="Fam", email="given@family")
        user = User(subject=contact.email, contact=contact)
        db.session.add_all(
            [public_configuration, internal_configuration, contact, user]
        )
        db.session.commit()
        with self.run_requests_as(user):
            with self.client:
                resp = self.client.get(f"{self.url}/{self.site.id}/sensorml")

        self.assertEqual(resp.status_code, 200)
        xml_text = resp.text
        self.schema.validate(xml_text)
        root = xml.etree.ElementTree.fromstring(resp.text)
        sml_components = root.find("{http://www.opengis.net/sensorml/2.0}components")
        sml_component_list = sml_components.find(
            "{http://www.opengis.net/sensorml/2.0}ComponentList"
        )
        sml_component_entries = sml_component_list.findall(
            "{http://www.opengis.net/sensorml/2.0}component"
        )

        self.assertEqual(len(sml_component_entries), 2)

        sml_physical_system_public_config = sml_component_entries[0].find(
            "{http://www.opengis.net/sensorml/2.0}PhysicalSystem"
        )
        gml_id_public_config = sml_physical_system_public_config.attrib.get(
            "{http://www.opengis.net/gml/3.2}id"
        )

        self.assertEqual(
            gml_id_public_config, f"configuration_{public_configuration.id}"
        )

        sml_physical_system_internal_config = sml_component_entries[1].find(
            "{http://www.opengis.net/sensorml/2.0}PhysicalSystem"
        )
        gml_id_internal_config = sml_physical_system_internal_config.attrib.get(
            "{http://www.opengis.net/gml/3.2}id"
        )

        self.assertEqual(
            gml_id_internal_config, f"configuration_{internal_configuration.id}"
        )

    def test_keywords(self):
        """Check that we give out keywords."""
        self.site.keywords = ["some", "fancy keyword"]
        db.session.add(self.site)
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.site.id}/sensorml")

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

    def test_public_site_with_public_and_internal_inner_site_without_user(self):
        """Ensure we put public inner sites into the sensorML."""
        public_inner_site = Site(
            label="public inner site1",
            outer_site=self.site,
            is_public=True,
            is_internal=False,
        )
        internal_inner_site = Site(
            label="internal inner site2",
            outer_site=self.site,
            is_public=False,
            is_internal=True,
        )
        db.session.add_all([public_inner_site, internal_inner_site])
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.site.id}/sensorml")

        self.assertEqual(resp.status_code, 200)
        xml_text = resp.text
        self.schema.validate(xml_text)
        root = xml.etree.ElementTree.fromstring(resp.text)
        sml_components = root.find("{http://www.opengis.net/sensorml/2.0}components")
        sml_component_list = sml_components.find(
            "{http://www.opengis.net/sensorml/2.0}ComponentList"
        )
        sml_component_entries = sml_component_list.findall(
            "{http://www.opengis.net/sensorml/2.0}component"
        )

        self.assertEqual(len(sml_component_entries), 1)

        sml_physical_system_public_config = sml_component_entries[0].find(
            "{http://www.opengis.net/sensorml/2.0}PhysicalSystem"
        )
        gml_id_public_config = sml_physical_system_public_config.attrib.get(
            "{http://www.opengis.net/gml/3.2}id"
        )

        self.assertEqual(gml_id_public_config, f"site_{public_inner_site.id}")

    def test_public_site_with_public_and_internal_inner_site_with_user(self):
        """Ensure we put internal inner sites into the sensorML too."""
        public_inner_site = Site(
            label="public inner site1",
            outer_site=self.site,
            is_public=True,
            is_internal=False,
        )
        internal_inner_site = Site(
            label="internal inner site2",
            outer_site=self.site,
            is_public=False,
            is_internal=True,
        )
        contact = Contact(given_name="Given", family_name="Fam", email="given@family")
        user = User(subject=contact.email, contact=contact)
        db.session.add_all([public_inner_site, internal_inner_site, contact, user])
        db.session.commit()
        with self.run_requests_as(user):
            with self.client:
                resp = self.client.get(f"{self.url}/{self.site.id}/sensorml")

        self.assertEqual(resp.status_code, 200)
        xml_text = resp.text
        self.schema.validate(xml_text)
        root = xml.etree.ElementTree.fromstring(resp.text)
        sml_components = root.find("{http://www.opengis.net/sensorml/2.0}components")
        sml_component_list = sml_components.find(
            "{http://www.opengis.net/sensorml/2.0}ComponentList"
        )
        sml_component_entries = sml_component_list.findall(
            "{http://www.opengis.net/sensorml/2.0}component"
        )

        self.assertEqual(len(sml_component_entries), 2)

        sml_physical_system_public_config = sml_component_entries[0].find(
            "{http://www.opengis.net/sensorml/2.0}PhysicalSystem"
        )
        gml_id_public_config = sml_physical_system_public_config.attrib.get(
            "{http://www.opengis.net/gml/3.2}id"
        )

        self.assertEqual(gml_id_public_config, f"site_{public_inner_site.id}")

        sml_physical_system_internal_config = sml_component_entries[1].find(
            "{http://www.opengis.net/sensorml/2.0}PhysicalSystem"
        )
        gml_id_internal_config = sml_physical_system_internal_config.attrib.get(
            "{http://www.opengis.net/gml/3.2}id"
        )

        self.assertEqual(gml_id_internal_config, f"site_{internal_inner_site.id}")

    def test_ordering(self):
        """Ensure we use the right ordering for the elements."""
        wkt = "POLYGON ((0 0, 0 15, 15 15, 15 0, 0 0))"
        self.site.geometry = WktPolygonField().deserialize(wkt)
        self.site.epsg_code = "4326"
        self.site.site_type_name = "Forest"
        self.site.description = "example site"
        self.site.city = "Potsdam"
        self.site.zip_code = "14473"
        self.site.country = "Germany"
        self.site.street = "Telegrafenberg"
        # GFZ doesn't have a street number, but lets imagine that it would have it.
        self.site.street_number = "123"
        self.site.building = "A70"
        self.site.room = "319"

        owner_name = "Owner"
        owner_uri = current_app.config["CV_URL"] + "/contactroles/4/"
        contact1 = Contact(
            given_name="Given",
            family_name="Fam",
            email="given@family",
            website="https://given.fam/index.html",
            organization="Dummy organization",
        )
        contact_role1 = SiteContactRole(
            contact=contact1,
            site=self.site,
            role_name=owner_name,
            role_uri=owner_uri,
        )
        attachment = SiteAttachment(
            site=self.site, url="https://ufz.de", label="UFZ-Page"
        )

        db.session.add_all([self.site, contact1, contact_role1, attachment])
        db.session.commit()

        with self.client:
            resp = self.client.get(f"{self.url}/{self.site.id}/sensorml")

        self.assertEqual(resp.status_code, 200)
        xml_text = resp.text
        self.schema.validate(xml_text)
