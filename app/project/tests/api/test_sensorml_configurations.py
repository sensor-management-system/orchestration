# SPDX-FileCopyrightText: 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Tests to extract sensorML for configurations."""

import datetime
import pathlib
import pickle
import xml

import pytz
from flask import current_app, url_for

from project import base_url
from project.api.models import (
    Configuration,
    ConfigurationAttachment,
    ConfigurationContactRole,
    ConfigurationDynamicLocationBeginAction,
    ConfigurationParameter,
    ConfigurationParameterValueChangeAction,
    ConfigurationStaticLocationBeginAction,
    Contact,
    Device,
    DeviceMountAction,
    DeviceProperty,
    GenericConfigurationAction,
    Platform,
    PlatformMountAction,
    User,
)
from project.api.models.base_model import db
from project.tests.base import BaseTestCase


class TestSensorMLConfiguration(BaseTestCase):
    """Test class for the sensor ML transformation for configurations."""

    url = base_url + "/configurations"

    def setUp(self):
        """Set up data for the tests."""
        super().setUp()
        path_this_file = pathlib.Path(__file__)
        path_pickle_schema = (
            path_this_file.parent / "helpers" / "sensorml_schema_validator.pickle"
        )

        with path_pickle_schema.open("rb") as infile:
            self.schema = pickle.load(infile)

        self.configuration = Configuration(
            is_public=True,
            is_internal=False,
            label="dummy config",
        )
        db.session.add_all([self.configuration])
        db.session.commit()

    def test_get_non_existing(self):
        """Ensure we get an 404 if the configuration doesn't exist."""
        with self.client:
            resp = self.client.get(f"{self.url}/9999999999/sensorml")
        self.assertEqual(resp.status_code, 404)

    def test_get_internal_config_without_user(self):
        """Ensure we don't show sensorML for internal configurations without a user."""
        self.configuration.is_internal = True
        self.configuration.is_public = False
        db.session.add_all([self.configuration])
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.configuration.id}/sensorml")
        self.assertEqual(resp.status_code, 401)

    def test_get_internal_config_with_user(self):
        """Ensure we don't show sensorML for internal configurations without a user."""
        self.configuration.is_internal = True
        self.configuration.is_public = False
        contact = Contact(given_name="Given", family_name="Fam", email="given@family")
        user = User(subject=contact.email, contact=contact)
        db.session.add_all([self.configuration, contact, user])
        db.session.commit()

        with self.run_requests_as(user):
            with self.client:
                resp = self.client.get(f"{self.url}/{self.configuration.id}/sensorml")
        self.assertEqual(resp.status_code, 200)

    def test_get_public_config_no_contacts_no_events(self):
        """
        Test with a configuration without contacts nor events.

        The public configuration should be visible for everyone.
        But a basic configuration doesn't has contacts yet (the backend
        api creates one, but in our test we don't have one), nor
        events.

        But we can test the id & the label.
        """
        with self.client:
            resp = self.client.get(f"{self.url}/{self.configuration.id}/sensorml")
        self.assertEqual(resp.status_code, 200)
        xml_text = resp.text
        self.schema.validate(xml_text)
        root = xml.etree.ElementTree.fromstring(resp.text)

        gml_id = root.attrib.get("{http://www.opengis.net/gml/3.2}id")
        self.assertEqual(gml_id, f"configuration_{self.configuration.id}")

        self.assertEqual(
            root.find("{http://www.opengis.net/gml/3.2}name").text,
            self.configuration.label,
        )

    def test_get_public_config_with_start_and_enddate(self):
        """Test with a configuration with start & end dates."""
        self.configuration.start_date = datetime.datetime(
            2022, 12, 24, 0, 0, 0, tzinfo=pytz.utc
        )
        self.configuration.end_date = datetime.datetime(
            2022, 12, 25, 12, 0, 0, tzinfo=pytz.utc
        )

        db.session.add(self.configuration)
        db.session.commit()

        with self.client:
            resp = self.client.get(f"{self.url}/{self.configuration.id}/sensorml")
        self.assertEqual(resp.status_code, 200)
        xml_text = resp.text
        self.schema.validate(xml_text)
        root = xml.etree.ElementTree.fromstring(resp.text)

        gml_id = root.attrib.get("{http://www.opengis.net/gml/3.2}id")
        self.assertEqual(gml_id, f"configuration_{self.configuration.id}")

        self.assertEqual(
            root.find("{http://www.opengis.net/sensorml/2.0}validTime")
            .find("{http://www.opengis.net/gml/3.2}TimePeriod")
            .attrib.get("{http://www.opengis.net/gml/3.2}id"),
            f"ValidTime_configuration_{self.configuration.id}",
        )

        self.assertEqual(
            root.find("{http://www.opengis.net/sensorml/2.0}validTime")
            .find("{http://www.opengis.net/gml/3.2}TimePeriod")
            .find("{http://www.opengis.net/gml/3.2}begin")
            .find("{http://www.opengis.net/gml/3.2}TimeInstant")
            .find("{http://www.opengis.net/gml/3.2}timePosition")
            .text,
            "2022-12-24T00:00:00+00:00",
        )
        self.assertEqual(
            root.find("{http://www.opengis.net/sensorml/2.0}validTime")
            .find("{http://www.opengis.net/gml/3.2}TimePeriod")
            .find("{http://www.opengis.net/gml/3.2}end")
            .find("{http://www.opengis.net/gml/3.2}TimeInstant")
            .find("{http://www.opengis.net/gml/3.2}timePosition")
            .text,
            "2022-12-25T12:00:00+00:00",
        )

    def test_get_public_config_without_enddate(self):
        """Test with a configuration without end date."""
        self.configuration.start_date = datetime.datetime(
            2022, 12, 24, 0, 0, 0, tzinfo=pytz.utc
        )

        db.session.add(self.configuration)
        db.session.commit()

        with self.client:
            resp = self.client.get(f"{self.url}/{self.configuration.id}/sensorml")
        self.assertEqual(resp.status_code, 200)
        xml_text = resp.text
        self.schema.validate(xml_text)
        root = xml.etree.ElementTree.fromstring(resp.text)

        gml_id = root.attrib.get("{http://www.opengis.net/gml/3.2}id")
        self.assertEqual(gml_id, f"configuration_{self.configuration.id}")

        self.assertEqual(
            root.find("{http://www.opengis.net/sensorml/2.0}validTime")
            .find("{http://www.opengis.net/gml/3.2}TimePeriod")
            .attrib.get("{http://www.opengis.net/gml/3.2}id"),
            f"ValidTime_configuration_{self.configuration.id}",
        )

        self.assertEqual(
            root.find("{http://www.opengis.net/sensorml/2.0}validTime")
            .find("{http://www.opengis.net/gml/3.2}TimePeriod")
            .find("{http://www.opengis.net/gml/3.2}begin")
            .find("{http://www.opengis.net/gml/3.2}TimeInstant")
            .find("{http://www.opengis.net/gml/3.2}timePosition")
            .text,
            "2022-12-24T00:00:00+00:00",
        )
        self.assertEqual(
            len(
                root.find("{http://www.opengis.net/sensorml/2.0}validTime")
                .find("{http://www.opengis.net/gml/3.2}TimePeriod")
                .find("{http://www.opengis.net/gml/3.2}end")
                .findall("{http://www.opengis.net/gml/3.2}TimeInstant")
            ),
            0,
        )

    def test_get_public_configuration_with_description(self):
        """Check that we give out the description."""
        self.configuration.description = "Some long description"
        db.session.add(self.configuration)
        db.session.commit()

        with self.client:
            resp = self.client.get(f"{self.url}/{self.configuration.id}/sensorml")

        self.assertEqual(resp.status_code, 200)
        xml_text = resp.text
        self.schema.validate(xml_text)
        root = xml.etree.ElementTree.fromstring(resp.text)
        sml_description = root.find("{http://www.opengis.net/gml/3.2}description")
        self.assertEqual(sml_description.text, self.configuration.description)

    def test_get_public_configuration_with_pid(self):
        """Check that we give out the pid."""
        self.configuration.persistent_identifier = "12345/test.abc.1234-4567"

        db.session.add(self.configuration)
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.configuration.id}/sensorml")

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
        self.assertEqual(len(sml_identifiers), 1)
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
            self.configuration.persistent_identifier,
        )

    def test_get_public_configuration_with_project(self):
        """Check that we give out the configurations project."""
        self.configuration.project = "Moses"

        db.session.add(self.configuration)
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.configuration.id}/sensorml")

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
            "http://xmlns.com/foaf/0.1/#term_Project",
        )
        self.assertEqual(
            sml_classifier_device_type.find("{http://www.opengis.net/sensorml/2.0}Term")
            .find("{http://www.opengis.net/sensorml/2.0}label")
            .text,
            "Project",
        )
        self.assertEqual(
            sml_classifier_device_type.find("{http://www.opengis.net/sensorml/2.0}Term")
            .find("{http://www.opengis.net/sensorml/2.0}value")
            .text,
            self.configuration.project,
        )

    def test_get_public_configuration_with_b2inst_record(self):
        """Check that we give out the website."""
        self.configuration.b2inst_record_id = "123"
        current_app.config.update({"B2INST_URL": "https://b2inst-test.gwdg.de"})

        db.session.add(self.configuration)
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.configuration.id}/sensorml")

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
            f"https://b2inst-test.gwdg.de/records/{self.configuration.b2inst_record_id}",
        )

    def test_get_public_configuration_contacts(self):
        """Test with a configuration with some contacts."""
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
        contact_role1 = ConfigurationContactRole(
            contact=contact1,
            configuration=self.configuration,
            role_name=owner_name,
            role_uri=owner_uri,
        )
        contact_role2 = ConfigurationContactRole(
            contact=contact2,
            configuration=self.configuration,
            role_name=pi_name,
            role_uri=pi_uri,
        )

        db.session.add_all([contact1, contact2, contact_role1, contact_role2])
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.configuration.id}/sensorml")
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

    def test_get_public_configuration_with_configuration_parameters(self):
        """Check that we give out the configuration parameters."""
        parameter = ConfigurationParameter(
            unit_name="°C",
            unit_uri="https://cv/units/1",
            label="Fan start temperature",
            description="Temperature on that the fan starts",
            configuration=self.configuration,
        )
        db.session.add(parameter)
        db.session.commit()

        with self.client:
            resp = self.client.get(f"{self.url}/{self.configuration.id}/sensorml")

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

    def test_get_public_configuration_with_configuration_parameter_value_change_actions(
        self,
    ):
        """Check that we give out the parameter change actions."""
        parameter = ConfigurationParameter(
            unit_name="°C",
            unit_uri="https://cv/units/1",
            label="Fan start temperature",
            description="Temperature on that the fan starts",
            configuration=self.configuration,
        )
        contact = Contact(
            given_name="first", family_name="contact", email="first.contact@localhost"
        )
        change_action = ConfigurationParameterValueChangeAction(
            configuration_parameter=parameter,
            contact=contact,
            date=datetime.datetime(2023, 5, 3, 10, 00, 00, tzinfo=pytz.utc),
            value="42",
            description="The answer to everything - and the start temperature for the fan.",
        )
        db.session.add_all([parameter, contact, change_action])
        db.session.commit()

        with self.client:
            resp = self.client.get(f"{self.url}/{self.configuration.id}/sensorml")

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

    def test_get_public_configuration_with_attachments(self):
        """Check that we give out the attachments."""
        attachment = ConfigurationAttachment(
            configuration=self.configuration, url="https://ufz.de", label="UFZ-Page"
        )

        db.session.add(attachment)
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.configuration.id}/sensorml")

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
            f"Attachment_{attachment.id}_of_PhysicalSystem_configuration_{self.configuration.id}",
        )

    def test_get_public_configuration_with_generic_action(self):
        """Check that we give out the generic action."""
        contact = Contact(given_name="Given", family_name="Fam", email="given@family")
        configuration_maintenance_uri = current_app.config["CV_URL"] + "/actiontypes/5/"
        configuration_action = GenericConfigurationAction(
            configuration=self.configuration,
            begin_date=datetime.datetime(year=2022, month=12, day=24, tzinfo=pytz.utc),
            end_date=datetime.datetime(year=2022, month=12, day=25, tzinfo=pytz.utc),
            contact=contact,
            description="Some desc",
            action_type_name="Configuration Maintenance",
            action_type_uri=configuration_maintenance_uri,
        )

        db.session.add_all([contact, configuration_action])
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.configuration.id}/sensorml")

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
            configuration_action.action_type_uri,
        )
        self.assertEqual(
            sml_action_event.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}classification")
            .find("{http://www.opengis.net/sensorml/2.0}ClassifierList")
            .find("{http://www.opengis.net/sensorml/2.0}classifier")
            .find("{http://www.opengis.net/sensorml/2.0}Term")
            .find("{http://www.opengis.net/sensorml/2.0}label")
            .text,
            configuration_action.action_type_name,
        )
        self.assertEqual(
            sml_action_event.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}classification")
            .find("{http://www.opengis.net/sensorml/2.0}ClassifierList")
            .find("{http://www.opengis.net/sensorml/2.0}classifier")
            .find("{http://www.opengis.net/sensorml/2.0}Term")
            .find("{http://www.opengis.net/sensorml/2.0}value")
            .text,
            configuration_action.action_type_name,
        )
        self.assertEqual(
            sml_action_event.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}time")
            .find("{http://www.opengis.net/gml/3.2}TimePeriod")
            .attrib.get("{http://www.opengis.net/gml/3.2}id"),
            f"TimePeriodForConfigurationMaintenance_{configuration_action.id}_of_configuration_{self.configuration.id}",
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
            configuration_action.description,
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

    def test_get_public_configuration_with_generic_action_without_end_date(self):
        """Check that we give out the generic action without an end date."""
        contact = Contact(given_name="Given", family_name="Fam", email="given@family")
        configuration_maintenance_uri = current_app.config["CV_URL"] + "/actiontypes/5/"
        configuration_action = GenericConfigurationAction(
            configuration=self.configuration,
            begin_date=datetime.datetime(year=2022, month=12, day=24, tzinfo=pytz.utc),
            contact=contact,
            description="Some desc",
            action_type_name="Configuration Maintenance",
            action_type_uri=configuration_maintenance_uri,
        )

        db.session.add_all([contact, configuration_action])
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.configuration.id}/sensorml")

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

    def test_get_public_configuration_with_generic_action_without_description(self):
        """Check that we give out the generic action without description."""
        contact = Contact(given_name="Given", family_name="Fam", email="given@family")
        configuration_maintenance_uri = current_app.config["CV_URL"] + "/actiontypes/5/"
        configuration_action = GenericConfigurationAction(
            configuration=self.configuration,
            begin_date=datetime.datetime(year=2022, month=12, day=24, tzinfo=pytz.utc),
            contact=contact,
            action_type_name="Configuration Maintenance",
            action_type_uri=configuration_maintenance_uri,
        )

        db.session.add_all([contact, configuration_action])
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.configuration.id}/sensorml")

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

    def test_get_public_configuration_with_generic_action_without_action_type_uri(self):
        """Check that we give out the generic action without action type uri."""
        contact = Contact(given_name="Given", family_name="Fam", email="given@family")
        configuration_action = GenericConfigurationAction(
            configuration=self.configuration,
            begin_date=datetime.datetime(year=2022, month=12, day=24, tzinfo=pytz.utc),
            contact=contact,
            action_type_name="Configuration Maintenance",
        )

        db.session.add_all([contact, configuration_action])
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.configuration.id}/sensorml")

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

    def test_get_public_configuration_with_static_location(self):
        """Check that we give out the static location."""
        contact = Contact(given_name="Given", family_name="Fam", email="given@family")
        static_location_action = ConfigurationStaticLocationBeginAction(
            configuration=self.configuration,
            begin_date=datetime.datetime(year=2022, month=12, day=24, tzinfo=pytz.utc),
            end_date=datetime.datetime(year=2022, month=12, day=25, tzinfo=pytz.utc),
            begin_contact=contact,
            begin_description="Some desc",
            x=1,
            y=2,
            z=1.5,
        )

        db.session.add_all([contact, static_location_action])
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.configuration.id}/sensorml")

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

        sml_location_event = sml_events[0]

        self.assertEqual(
            sml_location_event.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}classification")
            .find("{http://www.opengis.net/sensorml/2.0}ClassifierList")
            .find("{http://www.opengis.net/sensorml/2.0}classifier")
            .find("{http://www.opengis.net/sensorml/2.0}Term")
            .attrib.get("definition"),
            "StaticLocationAction",
        )
        self.assertEqual(
            sml_location_event.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}classification")
            .find("{http://www.opengis.net/sensorml/2.0}ClassifierList")
            .find("{http://www.opengis.net/sensorml/2.0}classifier")
            .find("{http://www.opengis.net/sensorml/2.0}Term")
            .find("{http://www.opengis.net/sensorml/2.0}label")
            .text,
            "StaticLocationAction",
        )
        self.assertEqual(
            sml_location_event.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}classification")
            .find("{http://www.opengis.net/sensorml/2.0}ClassifierList")
            .find("{http://www.opengis.net/sensorml/2.0}classifier")
            .find("{http://www.opengis.net/sensorml/2.0}Term")
            .find("{http://www.opengis.net/sensorml/2.0}value")
            .text,
            "StaticLocationAction",
        )
        self.assertEqual(
            sml_location_event.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}time")
            .find("{http://www.opengis.net/gml/3.2}TimePeriod")
            .attrib.get("{http://www.opengis.net/gml/3.2}id"),
            f"TimePeriodForStaticLocationAction_{static_location_action.id}_of_configuration_{self.configuration.id}",
        )
        self.assertEqual(
            sml_location_event.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}time")
            .find("{http://www.opengis.net/gml/3.2}TimePeriod")
            .find("{http://www.opengis.net/gml/3.2}begin")
            .find("{http://www.opengis.net/gml/3.2}TimeInstant")
            .find("{http://www.opengis.net/gml/3.2}timePosition")
            .text,
            "2022-12-24T00:00:00+00:00",
        )
        self.assertEqual(
            sml_location_event.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}time")
            .find("{http://www.opengis.net/gml/3.2}TimePeriod")
            .find("{http://www.opengis.net/gml/3.2}end")
            .find("{http://www.opengis.net/gml/3.2}TimeInstant")
            .find("{http://www.opengis.net/gml/3.2}timePosition")
            .text,
            "2022-12-25T00:00:00+00:00",
        )

        self.assertEqual(
            sml_location_event.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}time")
            .find("{http://www.opengis.net/gml/3.2}TimePeriod")
            .find("{http://www.opengis.net/gml/3.2}description")
            .text,
            static_location_action.begin_description,
        )

    def test_get_public_configuration_with_static_location_with_label(self):
        """Check that we give out the static location with a label."""
        contact = Contact(given_name="Given", family_name="Fam", email="given@family")
        static_location_action = ConfigurationStaticLocationBeginAction(
            configuration=self.configuration,
            begin_date=datetime.datetime(year=2022, month=12, day=24, tzinfo=pytz.utc),
            end_date=datetime.datetime(year=2022, month=12, day=25, tzinfo=pytz.utc),
            begin_contact=contact,
            begin_description="Some desc",
            label="Somewhere",
            x=1,
            y=2,
            z=1.5,
        )

        db.session.add_all([contact, static_location_action])
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.configuration.id}/sensorml")

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

        sml_location_event = sml_events[0]

        self.assertEqual(
            sml_location_event.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}classification")
            .find("{http://www.opengis.net/sensorml/2.0}ClassifierList")
            .find("{http://www.opengis.net/sensorml/2.0}classifier")
            .find("{http://www.opengis.net/sensorml/2.0}Term")
            .find("{http://www.opengis.net/sensorml/2.0}value")
            .text,
            static_location_action.label,
        )

    def test_get_public_configuration_with_static_location_without_end(self):
        """Check that we give out the static location without end date."""
        contact = Contact(given_name="Given", family_name="Fam", email="given@family")
        static_location_action = ConfigurationStaticLocationBeginAction(
            configuration=self.configuration,
            begin_date=datetime.datetime(year=2022, month=12, day=24, tzinfo=pytz.utc),
            begin_contact=contact,
            begin_description="Some desc",
            x=1,
            y=2,
            z=1.5,
        )

        db.session.add_all([contact, static_location_action])
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.configuration.id}/sensorml")

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

        sml_location_event = sml_events[0]

        self.assertEqual(
            len(
                sml_location_event.find("{http://www.opengis.net/sensorml/2.0}Event")
                .find("{http://www.opengis.net/sensorml/2.0}time")
                .find("{http://www.opengis.net/gml/3.2}TimePeriod")
                .find("{http://www.opengis.net/gml/3.2}end")
                .findall("{http://www.opengis.net/gml/3.2}TimeInstant")
            ),
            0,
        )

    def test_get_public_configuration_with_static_location_without_description(self):
        """Check that we give out the static location."""
        contact = Contact(given_name="Given", family_name="Fam", email="given@family")
        static_location_action = ConfigurationStaticLocationBeginAction(
            configuration=self.configuration,
            begin_date=datetime.datetime(year=2022, month=12, day=24, tzinfo=pytz.utc),
            begin_contact=contact,
            x=1,
            y=2,
            z=1.5,
        )

        db.session.add_all([contact, static_location_action])
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.configuration.id}/sensorml")

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

        sml_location_event = sml_events[0]

        self.assertIsNone(
            sml_location_event.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}time")
            .find("{http://www.opengis.net/gml/3.2}TimePeriod")
            .find("{http://www.opengis.net/gml/3.2}description")
            .text,
        )

    def test_get_public_configuration_with_dynamic_location(self):
        """Check that we give out the dynamic location."""
        contact = Contact(given_name="Given", family_name="Fam", email="given@family")
        dynamic_location_action = ConfigurationDynamicLocationBeginAction(
            configuration=self.configuration,
            begin_date=datetime.datetime(year=2022, month=12, day=24, tzinfo=pytz.utc),
            end_date=datetime.datetime(year=2022, month=12, day=25, tzinfo=pytz.utc),
            begin_contact=contact,
            begin_description="Some desc",
        )

        db.session.add_all([contact, dynamic_location_action])
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.configuration.id}/sensorml")

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

        sml_location_event = sml_events[0]

        self.assertEqual(
            sml_location_event.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}classification")
            .find("{http://www.opengis.net/sensorml/2.0}ClassifierList")
            .find("{http://www.opengis.net/sensorml/2.0}classifier")
            .find("{http://www.opengis.net/sensorml/2.0}Term")
            .attrib.get("definition"),
            "DynamicLocationAction",
        )
        self.assertEqual(
            sml_location_event.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}classification")
            .find("{http://www.opengis.net/sensorml/2.0}ClassifierList")
            .find("{http://www.opengis.net/sensorml/2.0}classifier")
            .find("{http://www.opengis.net/sensorml/2.0}Term")
            .find("{http://www.opengis.net/sensorml/2.0}label")
            .text,
            "DynamicLocationAction",
        )
        self.assertEqual(
            sml_location_event.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}classification")
            .find("{http://www.opengis.net/sensorml/2.0}ClassifierList")
            .find("{http://www.opengis.net/sensorml/2.0}classifier")
            .find("{http://www.opengis.net/sensorml/2.0}Term")
            .find("{http://www.opengis.net/sensorml/2.0}value")
            .text,
            "DynamicLocationAction",
        )
        self.assertEqual(
            sml_location_event.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}time")
            .find("{http://www.opengis.net/gml/3.2}TimePeriod")
            .attrib.get("{http://www.opengis.net/gml/3.2}id"),
            f"TimePeriodForDynamicLocationAction_{dynamic_location_action.id}_of_configuration_{self.configuration.id}",
        )
        self.assertEqual(
            sml_location_event.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}time")
            .find("{http://www.opengis.net/gml/3.2}TimePeriod")
            .find("{http://www.opengis.net/gml/3.2}begin")
            .find("{http://www.opengis.net/gml/3.2}TimeInstant")
            .find("{http://www.opengis.net/gml/3.2}timePosition")
            .text,
            "2022-12-24T00:00:00+00:00",
        )
        self.assertEqual(
            sml_location_event.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}time")
            .find("{http://www.opengis.net/gml/3.2}TimePeriod")
            .find("{http://www.opengis.net/gml/3.2}end")
            .find("{http://www.opengis.net/gml/3.2}TimeInstant")
            .find("{http://www.opengis.net/gml/3.2}timePosition")
            .text,
            "2022-12-25T00:00:00+00:00",
        )

        self.assertEqual(
            sml_location_event.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}time")
            .find("{http://www.opengis.net/gml/3.2}TimePeriod")
            .find("{http://www.opengis.net/gml/3.2}description")
            .text,
            dynamic_location_action.begin_description,
        )

    def test_get_public_configuration_with_dynamic_location_with_label(self):
        """Check that we give out the dynamic location with a label."""
        contact = Contact(given_name="Given", family_name="Fam", email="given@family")
        dynamic_location_action = ConfigurationDynamicLocationBeginAction(
            configuration=self.configuration,
            begin_date=datetime.datetime(year=2022, month=12, day=24, tzinfo=pytz.utc),
            end_date=datetime.datetime(year=2022, month=12, day=25, tzinfo=pytz.utc),
            begin_contact=contact,
            begin_description="Some desc",
            label="Somewhere",
        )

        db.session.add_all([contact, dynamic_location_action])
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.configuration.id}/sensorml")

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

        sml_location_event = sml_events[0]

        self.assertEqual(
            sml_location_event.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}classification")
            .find("{http://www.opengis.net/sensorml/2.0}ClassifierList")
            .find("{http://www.opengis.net/sensorml/2.0}classifier")
            .find("{http://www.opengis.net/sensorml/2.0}Term")
            .find("{http://www.opengis.net/sensorml/2.0}value")
            .text,
            dynamic_location_action.label,
        )

    def test_get_public_configuration_with_dynamic_location_without_end(self):
        """Check that we give out the dynamic location without end date."""
        contact = Contact(given_name="Given", family_name="Fam", email="given@family")
        dynamic_location_action = ConfigurationDynamicLocationBeginAction(
            configuration=self.configuration,
            begin_date=datetime.datetime(year=2022, month=12, day=24, tzinfo=pytz.utc),
            begin_contact=contact,
            begin_description="Some desc",
        )

        db.session.add_all([contact, dynamic_location_action])
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.configuration.id}/sensorml")

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

        sml_location_event = sml_events[0]

        self.assertEqual(
            len(
                sml_location_event.find("{http://www.opengis.net/sensorml/2.0}Event")
                .find("{http://www.opengis.net/sensorml/2.0}time")
                .find("{http://www.opengis.net/gml/3.2}TimePeriod")
                .find("{http://www.opengis.net/gml/3.2}end")
                .findall("{http://www.opengis.net/gml/3.2}TimeInstant")
            ),
            0,
        )

    def test_get_public_configuration_with_dynamic_location_without_description(self):
        """Check that we give out the dynamic location."""
        contact = Contact(given_name="Given", family_name="Fam", email="given@family")
        dynamic_location_action = ConfigurationDynamicLocationBeginAction(
            configuration=self.configuration,
            begin_date=datetime.datetime(year=2022, month=12, day=24, tzinfo=pytz.utc),
            begin_contact=contact,
        )

        db.session.add_all([contact, dynamic_location_action])
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.configuration.id}/sensorml")

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

        sml_location_event = sml_events[0]

        self.assertIsNone(
            sml_location_event.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}time")
            .find("{http://www.opengis.net/gml/3.2}TimePeriod")
            .find("{http://www.opengis.net/gml/3.2}description")
            .text,
        )

    def test_get_public_configuration_with_platform_mount(self):
        """Check that we give out the platform mount."""
        contact = Contact(given_name="Given", family_name="Fam", email="given@family")
        platform = Platform(short_name="test platform", is_public=True)
        platform_mount_action = PlatformMountAction(
            configuration=self.configuration,
            platform=platform,
            begin_date=datetime.datetime(year=2022, month=12, day=24, tzinfo=pytz.utc),
            end_date=datetime.datetime(year=2022, month=12, day=25, tzinfo=pytz.utc),
            begin_contact=contact,
            begin_description="Some desc",
        )

        db.session.add_all([contact, platform, platform_mount_action])
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.configuration.id}/sensorml")

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

        self.assertEqual(
            sml_mount_event.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}classification")
            .find("{http://www.opengis.net/sensorml/2.0}ClassifierList")
            .find("{http://www.opengis.net/sensorml/2.0}classifier")
            .find("{http://www.opengis.net/sensorml/2.0}Term")
            .attrib.get("definition"),
            "PlatformMountAction",
        )
        self.assertEqual(
            sml_mount_event.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}classification")
            .find("{http://www.opengis.net/sensorml/2.0}ClassifierList")
            .find("{http://www.opengis.net/sensorml/2.0}classifier")
            .find("{http://www.opengis.net/sensorml/2.0}Term")
            .find("{http://www.opengis.net/sensorml/2.0}label")
            .text,
            "PlatformMountAction",
        )
        self.assertEqual(
            sml_mount_event.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}classification")
            .find("{http://www.opengis.net/sensorml/2.0}ClassifierList")
            .find("{http://www.opengis.net/sensorml/2.0}classifier")
            .find("{http://www.opengis.net/sensorml/2.0}Term")
            .find("{http://www.opengis.net/sensorml/2.0}value")
            .text,
            "PlatformMountAction",
        )
        self.assertEqual(
            sml_mount_event.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}time")
            .find("{http://www.opengis.net/gml/3.2}TimePeriod")
            .attrib.get("{http://www.opengis.net/gml/3.2}id"),
            f"TimePeriodForPlatformMountAction_{platform_mount_action.id}_of_configuration_{self.configuration.id}",
        )

        self.assertEqual(
            sml_mount_event.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}time")
            .find("{http://www.opengis.net/gml/3.2}TimePeriod")
            .find("{http://www.opengis.net/gml/3.2}description")
            .text,
            platform_mount_action.begin_description,
        )

        sml_components = root.find("{http://www.opengis.net/sensorml/2.0}components")
        sml_component_list = sml_components.find(
            "{http://www.opengis.net/sensorml/2.0}ComponentList"
        )
        sml_component_entries = sml_component_list.findall(
            "{http://www.opengis.net/sensorml/2.0}component"
        )

        self.assertEqual(len(sml_component_entries), 1)

        url_to_platform_sensorml = url_for(
            "sensorml.platform_to_sensor_ml", platform_id=platform.id, _external=True
        )

        self.assertTrue(url_to_platform_sensorml.startswith("http"))

        self.assertEqual(
            sml_component_entries[0].attrib.get(
                "{http://www.w3.org/1999/xlink}href",
            ),
            url_to_platform_sensorml,
        )

        sml_physical_system = sml_component_entries[0].find(
            "{http://www.opengis.net/sensorml/2.0}PhysicalSystem"
        )

        gml_id = sml_physical_system.attrib.get("{http://www.opengis.net/gml/3.2}id")
        self.assertEqual(gml_id, f"platform_{platform.id}")

        sml_identification = sml_physical_system.find(
            "{http://www.opengis.net/sensorml/2.0}identification"
        )
        sml_identifier_list = sml_identification.find(
            "{http://www.opengis.net/sensorml/2.0}IdentifierList"
        )
        sml_identifiers = sml_identifier_list.findall(
            "{http://www.opengis.net/sensorml/2.0}identifier"
        )
        self.assertEqual(len(sml_identifiers), 1)
        sml_identifier_short_name = sml_identifiers[0]

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
            platform.short_name,
        )
        sml_history_pl = sml_physical_system.find(
            "{http://www.opengis.net/sensorml/2.0}history"
        )
        sml_event_list_pl = sml_history_pl.find(
            "{http://www.opengis.net/sensorml/2.0}EventList"
        )
        sml_events_pl = sml_event_list_pl.findall(
            "{http://www.opengis.net/sensorml/2.0}event"
        )
        self.assertEqual(len(sml_events_pl), 1)

        sml_mount_event_pl = sml_events_pl[0]

        self.assertEqual(
            sml_mount_event_pl.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}classification")
            .find("{http://www.opengis.net/sensorml/2.0}ClassifierList")
            .find("{http://www.opengis.net/sensorml/2.0}classifier")
            .find("{http://www.opengis.net/sensorml/2.0}Term")
            .attrib.get("definition"),
            "Mount",
        )
        self.assertEqual(
            sml_mount_event_pl.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}classification")
            .find("{http://www.opengis.net/sensorml/2.0}ClassifierList")
            .find("{http://www.opengis.net/sensorml/2.0}classifier")
            .find("{http://www.opengis.net/sensorml/2.0}Term")
            .find("{http://www.opengis.net/sensorml/2.0}label")
            .text,
            f"Mounted to {self.configuration.label}",
        )
        self.assertEqual(
            sml_mount_event_pl.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}classification")
            .find("{http://www.opengis.net/sensorml/2.0}ClassifierList")
            .find("{http://www.opengis.net/sensorml/2.0}classifier")
            .find("{http://www.opengis.net/sensorml/2.0}Term")
            .find("{http://www.opengis.net/sensorml/2.0}value")
            .text,
            "Mount",
        )
        self.assertEqual(
            sml_mount_event_pl.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}time")
            .find("{http://www.opengis.net/gml/3.2}TimePeriod")
            .attrib.get("{http://www.opengis.net/gml/3.2}id"),
            f"TimePeriodForPlatformMountAction_{platform_mount_action.id}_of_platform_{platform.id}",
        )
        self.assertEqual(
            sml_mount_event_pl.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}time")
            .find("{http://www.opengis.net/gml/3.2}TimePeriod")
            .find("{http://www.opengis.net/gml/3.2}description")
            .text,
            platform_mount_action.begin_description,
        )
        self.assertEqual(
            sml_mount_event_pl.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}time")
            .find("{http://www.opengis.net/gml/3.2}TimePeriod")
            .find("{http://www.opengis.net/gml/3.2}begin")
            .find("{http://www.opengis.net/gml/3.2}TimeInstant")
            .find("{http://www.opengis.net/gml/3.2}timePosition")
            .text,
            "2022-12-24T00:00:00+00:00",
        )
        self.assertEqual(
            sml_mount_event_pl.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}time")
            .find("{http://www.opengis.net/gml/3.2}TimePeriod")
            .find("{http://www.opengis.net/gml/3.2}end")
            .find("{http://www.opengis.net/gml/3.2}TimeInstant")
            .find("{http://www.opengis.net/gml/3.2}timePosition")
            .text,
            "2022-12-25T00:00:00+00:00",
        )

    def test_get_public_configuration_with_platform_mount_without_end_date(self):
        """Check that we give out the platform mount without end date."""
        contact = Contact(given_name="Given", family_name="Fam", email="given@family")
        platform = Platform(short_name="test platform", is_public=True)
        platform_mount_action = PlatformMountAction(
            configuration=self.configuration,
            platform=platform,
            begin_date=datetime.datetime(year=2022, month=12, day=24, tzinfo=pytz.utc),
            begin_contact=contact,
        )

        db.session.add_all([contact, platform, platform_mount_action])
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.configuration.id}/sensorml")

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

        self.assertIsNone(
            sml_mount_event.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}time")
            .find("{http://www.opengis.net/gml/3.2}TimePeriod")
            .find("{http://www.opengis.net/gml/3.2}description")
            .text,
        )

        sml_components = root.find("{http://www.opengis.net/sensorml/2.0}components")
        sml_component_list = sml_components.find(
            "{http://www.opengis.net/sensorml/2.0}ComponentList"
        )
        sml_component_entries = sml_component_list.findall(
            "{http://www.opengis.net/sensorml/2.0}component"
        )

        self.assertEqual(len(sml_component_entries), 1)

        sml_physical_system = sml_component_entries[0].find(
            "{http://www.opengis.net/sensorml/2.0}PhysicalSystem"
        )

        sml_history_pl = sml_physical_system.find(
            "{http://www.opengis.net/sensorml/2.0}history"
        )
        sml_event_list_pl = sml_history_pl.find(
            "{http://www.opengis.net/sensorml/2.0}EventList"
        )
        sml_events_pl = sml_event_list_pl.findall(
            "{http://www.opengis.net/sensorml/2.0}event"
        )
        self.assertEqual(len(sml_events_pl), 1)

        sml_mount_event_pl = sml_events_pl[0]

        self.assertIsNone(
            sml_mount_event_pl.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}time")
            .find("{http://www.opengis.net/gml/3.2}TimePeriod")
            .find("{http://www.opengis.net/gml/3.2}description")
            .text,
        )
        self.assertEqual(
            len(
                sml_mount_event_pl.find("{http://www.opengis.net/sensorml/2.0}Event")
                .find("{http://www.opengis.net/sensorml/2.0}time")
                .find("{http://www.opengis.net/gml/3.2}TimePeriod")
                .find("{http://www.opengis.net/gml/3.2}end")
                .findall("{http://www.opengis.net/gml/3.2}TimeInstant")
            ),
            0,
        )

    def test_get_public_configuration_with_device_mount(self):
        """Check that we give out the device mount."""
        contact = Contact(given_name="Given", family_name="Fam", email="given@family")
        device = Device(short_name="test device", is_public=True)
        device_mount_action = DeviceMountAction(
            configuration=self.configuration,
            device=device,
            begin_date=datetime.datetime(year=2022, month=12, day=24, tzinfo=pytz.utc),
            end_date=datetime.datetime(year=2022, month=12, day=25, tzinfo=pytz.utc),
            begin_contact=contact,
            begin_description="Some desc",
        )

        db.session.add_all([contact, device, device_mount_action])
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.configuration.id}/sensorml")

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

        self.assertEqual(
            sml_mount_event.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}classification")
            .find("{http://www.opengis.net/sensorml/2.0}ClassifierList")
            .find("{http://www.opengis.net/sensorml/2.0}classifier")
            .find("{http://www.opengis.net/sensorml/2.0}Term")
            .attrib.get("definition"),
            "DeviceMountAction",
        )
        self.assertEqual(
            sml_mount_event.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}classification")
            .find("{http://www.opengis.net/sensorml/2.0}ClassifierList")
            .find("{http://www.opengis.net/sensorml/2.0}classifier")
            .find("{http://www.opengis.net/sensorml/2.0}Term")
            .find("{http://www.opengis.net/sensorml/2.0}label")
            .text,
            "DeviceMountAction",
        )
        self.assertEqual(
            sml_mount_event.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}classification")
            .find("{http://www.opengis.net/sensorml/2.0}ClassifierList")
            .find("{http://www.opengis.net/sensorml/2.0}classifier")
            .find("{http://www.opengis.net/sensorml/2.0}Term")
            .find("{http://www.opengis.net/sensorml/2.0}value")
            .text,
            "DeviceMountAction",
        )
        self.assertEqual(
            sml_mount_event.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}time")
            .find("{http://www.opengis.net/gml/3.2}TimePeriod")
            .attrib.get("{http://www.opengis.net/gml/3.2}id"),
            f"TimePeriodForDeviceMountAction_{device_mount_action.id}_of_configuration_{self.configuration.id}",
        )

        self.assertEqual(
            sml_mount_event.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}time")
            .find("{http://www.opengis.net/gml/3.2}TimePeriod")
            .find("{http://www.opengis.net/gml/3.2}description")
            .text,
            device_mount_action.begin_description,
        )

        sml_components = root.find("{http://www.opengis.net/sensorml/2.0}components")
        sml_component_list = sml_components.find(
            "{http://www.opengis.net/sensorml/2.0}ComponentList"
        )
        sml_component_entries = sml_component_list.findall(
            "{http://www.opengis.net/sensorml/2.0}component"
        )

        self.assertEqual(len(sml_component_entries), 1)

        url_to_device_sensorml = url_for(
            "sensorml.device_to_sensor_ml", device_id=device.id, _external=True
        )
        self.assertTrue(url_to_device_sensorml.startswith("http"))

        self.assertEqual(
            sml_component_entries[0].attrib.get(
                "{http://www.w3.org/1999/xlink}href",
            ),
            url_to_device_sensorml,
        )

        sml_physical_system = sml_component_entries[0].find(
            "{http://www.opengis.net/sensorml/2.0}PhysicalSystem"
        )

        gml_id = sml_physical_system.attrib.get("{http://www.opengis.net/gml/3.2}id")
        self.assertEqual(gml_id, f"device_{device.id}")

        sml_identification = sml_physical_system.find(
            "{http://www.opengis.net/sensorml/2.0}identification"
        )
        sml_identifier_list = sml_identification.find(
            "{http://www.opengis.net/sensorml/2.0}IdentifierList"
        )
        sml_identifiers = sml_identifier_list.findall(
            "{http://www.opengis.net/sensorml/2.0}identifier"
        )
        self.assertEqual(len(sml_identifiers), 1)
        sml_identifier_short_name = sml_identifiers[0]

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
            device.short_name,
        )
        sml_history_pl = sml_physical_system.find(
            "{http://www.opengis.net/sensorml/2.0}history"
        )
        sml_event_list_pl = sml_history_pl.find(
            "{http://www.opengis.net/sensorml/2.0}EventList"
        )
        sml_events_pl = sml_event_list_pl.findall(
            "{http://www.opengis.net/sensorml/2.0}event"
        )
        self.assertEqual(len(sml_events_pl), 1)

        sml_mount_event_pl = sml_events_pl[0]

        self.assertEqual(
            sml_mount_event_pl.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}classification")
            .find("{http://www.opengis.net/sensorml/2.0}ClassifierList")
            .find("{http://www.opengis.net/sensorml/2.0}classifier")
            .find("{http://www.opengis.net/sensorml/2.0}Term")
            .attrib.get("definition"),
            "Mount",
        )
        self.assertEqual(
            sml_mount_event_pl.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}classification")
            .find("{http://www.opengis.net/sensorml/2.0}ClassifierList")
            .find("{http://www.opengis.net/sensorml/2.0}classifier")
            .find("{http://www.opengis.net/sensorml/2.0}Term")
            .find("{http://www.opengis.net/sensorml/2.0}label")
            .text,
            f"Mounted to {self.configuration.label}",
        )
        self.assertEqual(
            sml_mount_event_pl.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}classification")
            .find("{http://www.opengis.net/sensorml/2.0}ClassifierList")
            .find("{http://www.opengis.net/sensorml/2.0}classifier")
            .find("{http://www.opengis.net/sensorml/2.0}Term")
            .find("{http://www.opengis.net/sensorml/2.0}value")
            .text,
            "Mount",
        )
        self.assertEqual(
            sml_mount_event_pl.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}time")
            .find("{http://www.opengis.net/gml/3.2}TimePeriod")
            .attrib.get("{http://www.opengis.net/gml/3.2}id"),
            f"TimePeriodForDeviceMountAction_{device_mount_action.id}_of_device_{device.id}",
        )
        self.assertEqual(
            sml_mount_event_pl.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}time")
            .find("{http://www.opengis.net/gml/3.2}TimePeriod")
            .find("{http://www.opengis.net/gml/3.2}description")
            .text,
            device_mount_action.begin_description,
        )
        self.assertEqual(
            sml_mount_event_pl.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}time")
            .find("{http://www.opengis.net/gml/3.2}TimePeriod")
            .find("{http://www.opengis.net/gml/3.2}begin")
            .find("{http://www.opengis.net/gml/3.2}TimeInstant")
            .find("{http://www.opengis.net/gml/3.2}timePosition")
            .text,
            "2022-12-24T00:00:00+00:00",
        )
        self.assertEqual(
            sml_mount_event_pl.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}time")
            .find("{http://www.opengis.net/gml/3.2}TimePeriod")
            .find("{http://www.opengis.net/gml/3.2}end")
            .find("{http://www.opengis.net/gml/3.2}TimeInstant")
            .find("{http://www.opengis.net/gml/3.2}timePosition")
            .text,
            "2022-12-25T00:00:00+00:00",
        )

    def test_get_public_configuration_with_device_mount_without_end_date(self):
        """Check that we give out the device mount without end date."""
        contact = Contact(given_name="Given", family_name="Fam", email="given@family")
        device = Device(short_name="test device", is_public=True)
        device_mount_action = DeviceMountAction(
            configuration=self.configuration,
            device=device,
            begin_date=datetime.datetime(year=2022, month=12, day=24, tzinfo=pytz.utc),
            begin_contact=contact,
        )

        db.session.add_all([contact, device, device_mount_action])
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.configuration.id}/sensorml")

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

        self.assertIsNone(
            sml_mount_event.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}time")
            .find("{http://www.opengis.net/gml/3.2}TimePeriod")
            .find("{http://www.opengis.net/gml/3.2}description")
            .text,
        )

        sml_components = root.find("{http://www.opengis.net/sensorml/2.0}components")
        sml_component_list = sml_components.find(
            "{http://www.opengis.net/sensorml/2.0}ComponentList"
        )
        sml_component_entries = sml_component_list.findall(
            "{http://www.opengis.net/sensorml/2.0}component"
        )

        self.assertEqual(len(sml_component_entries), 1)

        sml_physical_system = sml_component_entries[0].find(
            "{http://www.opengis.net/sensorml/2.0}PhysicalSystem"
        )

        sml_history_dv = sml_physical_system.find(
            "{http://www.opengis.net/sensorml/2.0}history"
        )
        sml_event_list_dv = sml_history_dv.find(
            "{http://www.opengis.net/sensorml/2.0}EventList"
        )
        sml_events_dv = sml_event_list_dv.findall(
            "{http://www.opengis.net/sensorml/2.0}event"
        )
        self.assertEqual(len(sml_events_dv), 1)

        sml_mount_event_dv = sml_events_dv[0]

        self.assertIsNone(
            sml_mount_event_dv.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}time")
            .find("{http://www.opengis.net/gml/3.2}TimePeriod")
            .find("{http://www.opengis.net/gml/3.2}description")
            .text,
        )
        self.assertEqual(
            len(
                sml_mount_event_dv.find("{http://www.opengis.net/sensorml/2.0}Event")
                .find("{http://www.opengis.net/sensorml/2.0}time")
                .find("{http://www.opengis.net/gml/3.2}TimePeriod")
                .find("{http://www.opengis.net/gml/3.2}end")
                .findall("{http://www.opengis.net/gml/3.2}TimeInstant")
            ),
            0,
        )

    def test_get_public_configuration_with_device_mount_with_empty_device_property(
        self,
    ):
        """Check that we give out the device mount with an empty device property."""
        contact = Contact(given_name="Given", family_name="Fam", email="given@family")
        device = Device(short_name="test device", is_public=True)
        device_mount_action = DeviceMountAction(
            configuration=self.configuration,
            device=device,
            begin_date=datetime.datetime(year=2022, month=12, day=24, tzinfo=pytz.utc),
            end_date=datetime.datetime(year=2022, month=12, day=25, tzinfo=pytz.utc),
            begin_contact=contact,
            begin_description="Some desc",
        )
        device_property = DeviceProperty(
            device=device,
            property_name="",
        )

        db.session.add(device_property)
        db.session.commit()

        db.session.add_all([contact, device, device_mount_action, device_property])
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.configuration.id}/sensorml")

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

        sml_physical_system = sml_component_entries[0].find(
            "{http://www.opengis.net/sensorml/2.0}PhysicalSystem"
        )
        sml_output = sml_physical_system.find(
            "{http://www.opengis.net/sensorml/2.0}outputs"
        )
        self.assertIsNone(sml_output)

    def test_get_public_configuration_with_platform_and_device_mount(self):
        """Check that we give out the platform & device mounts."""
        contact = Contact(given_name="Given", family_name="Fam", email="given@family")
        device = Device(short_name="test device", is_public=True)
        platform = Platform(short_name="test platform", is_public=True)
        platform_mount_action = PlatformMountAction(
            configuration=self.configuration,
            platform=platform,
            begin_date=datetime.datetime(year=2022, month=12, day=23, tzinfo=pytz.utc),
            end_date=datetime.datetime(year=2022, month=12, day=26, tzinfo=pytz.utc),
            begin_contact=contact,
            begin_description="Some platform desc",
        )
        device_mount_action = DeviceMountAction(
            configuration=self.configuration,
            parent_platform=platform,
            device=device,
            begin_date=datetime.datetime(year=2022, month=12, day=24, tzinfo=pytz.utc),
            end_date=datetime.datetime(year=2022, month=12, day=25, tzinfo=pytz.utc),
            begin_contact=contact,
            begin_description="Some device desc",
        )

        db.session.add_all(
            [contact, platform, device, platform_mount_action, device_mount_action]
        )
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.configuration.id}/sensorml")

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
        self.assertEqual(len(sml_events), 2)

        sml_mount_event_device = sml_events[0]
        sml_mount_event_platform = sml_events[1]

        self.assertEqual(
            sml_mount_event_platform.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}time")
            .find("{http://www.opengis.net/gml/3.2}TimePeriod")
            .find("{http://www.opengis.net/gml/3.2}begin")
            .find("{http://www.opengis.net/gml/3.2}TimeInstant")
            .find("{http://www.opengis.net/gml/3.2}timePosition")
            .text,
            "2022-12-23T00:00:00+00:00",
        )
        self.assertEqual(
            sml_mount_event_platform.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}time")
            .find("{http://www.opengis.net/gml/3.2}TimePeriod")
            .find("{http://www.opengis.net/gml/3.2}end")
            .find("{http://www.opengis.net/gml/3.2}TimeInstant")
            .find("{http://www.opengis.net/gml/3.2}timePosition")
            .text,
            "2022-12-26T00:00:00+00:00",
        )

        self.assertEqual(
            sml_mount_event_platform.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}classification")
            .find("{http://www.opengis.net/sensorml/2.0}ClassifierList")
            .find("{http://www.opengis.net/sensorml/2.0}classifier")
            .find("{http://www.opengis.net/sensorml/2.0}Term")
            .attrib.get("definition"),
            "PlatformMountAction",
        )
        self.assertEqual(
            sml_mount_event_platform.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}classification")
            .find("{http://www.opengis.net/sensorml/2.0}ClassifierList")
            .find("{http://www.opengis.net/sensorml/2.0}classifier")
            .find("{http://www.opengis.net/sensorml/2.0}Term")
            .find("{http://www.opengis.net/sensorml/2.0}label")
            .text,
            "PlatformMountAction",
        )
        self.assertEqual(
            sml_mount_event_platform.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}classification")
            .find("{http://www.opengis.net/sensorml/2.0}ClassifierList")
            .find("{http://www.opengis.net/sensorml/2.0}classifier")
            .find("{http://www.opengis.net/sensorml/2.0}Term")
            .find("{http://www.opengis.net/sensorml/2.0}value")
            .text,
            "PlatformMountAction",
        )
        self.assertEqual(
            sml_mount_event_platform.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}time")
            .find("{http://www.opengis.net/gml/3.2}TimePeriod")
            .attrib.get("{http://www.opengis.net/gml/3.2}id"),
            f"TimePeriodForPlatformMountAction_{platform_mount_action.id}_of_configuration_{self.configuration.id}",
        )

        self.assertEqual(
            sml_mount_event_platform.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}time")
            .find("{http://www.opengis.net/gml/3.2}TimePeriod")
            .find("{http://www.opengis.net/gml/3.2}description")
            .text,
            platform_mount_action.begin_description,
        )

        self.assertEqual(
            sml_mount_event_device.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}time")
            .find("{http://www.opengis.net/gml/3.2}TimePeriod")
            .find("{http://www.opengis.net/gml/3.2}begin")
            .find("{http://www.opengis.net/gml/3.2}TimeInstant")
            .find("{http://www.opengis.net/gml/3.2}timePosition")
            .text,
            "2022-12-24T00:00:00+00:00",
        )
        self.assertEqual(
            sml_mount_event_device.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}time")
            .find("{http://www.opengis.net/gml/3.2}TimePeriod")
            .find("{http://www.opengis.net/gml/3.2}end")
            .find("{http://www.opengis.net/gml/3.2}TimeInstant")
            .find("{http://www.opengis.net/gml/3.2}timePosition")
            .text,
            "2022-12-25T00:00:00+00:00",
        )

        self.assertEqual(
            sml_mount_event_device.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}classification")
            .find("{http://www.opengis.net/sensorml/2.0}ClassifierList")
            .find("{http://www.opengis.net/sensorml/2.0}classifier")
            .find("{http://www.opengis.net/sensorml/2.0}Term")
            .attrib.get("definition"),
            "DeviceMountAction",
        )
        self.assertEqual(
            sml_mount_event_device.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}classification")
            .find("{http://www.opengis.net/sensorml/2.0}ClassifierList")
            .find("{http://www.opengis.net/sensorml/2.0}classifier")
            .find("{http://www.opengis.net/sensorml/2.0}Term")
            .find("{http://www.opengis.net/sensorml/2.0}label")
            .text,
            "DeviceMountAction",
        )
        self.assertEqual(
            sml_mount_event_device.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}classification")
            .find("{http://www.opengis.net/sensorml/2.0}ClassifierList")
            .find("{http://www.opengis.net/sensorml/2.0}classifier")
            .find("{http://www.opengis.net/sensorml/2.0}Term")
            .find("{http://www.opengis.net/sensorml/2.0}value")
            .text,
            "DeviceMountAction",
        )
        self.assertEqual(
            sml_mount_event_device.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}time")
            .find("{http://www.opengis.net/gml/3.2}TimePeriod")
            .attrib.get("{http://www.opengis.net/gml/3.2}id"),
            f"TimePeriodForDeviceMountAction_{platform_mount_action.id}_of_configuration_{self.configuration.id}",
        )

        self.assertEqual(
            sml_mount_event_device.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}time")
            .find("{http://www.opengis.net/gml/3.2}TimePeriod")
            .find("{http://www.opengis.net/gml/3.2}description")
            .text,
            device_mount_action.begin_description,
        )

        sml_components = root.find("{http://www.opengis.net/sensorml/2.0}components")
        sml_component_list = sml_components.find(
            "{http://www.opengis.net/sensorml/2.0}ComponentList"
        )
        sml_component_entries = sml_component_list.findall(
            "{http://www.opengis.net/sensorml/2.0}component"
        )

        # It is nested, so we have here only the platform first.
        # Then we have the device included there.
        self.assertEqual(len(sml_component_entries), 1)

        sml_physical_system = sml_component_entries[0].find(
            "{http://www.opengis.net/sensorml/2.0}PhysicalSystem"
        )

        gml_id = sml_physical_system.attrib.get("{http://www.opengis.net/gml/3.2}id")
        self.assertEqual(gml_id, f"platform_{platform.id}")

        sml_identification = sml_physical_system.find(
            "{http://www.opengis.net/sensorml/2.0}identification"
        )
        sml_identifier_list = sml_identification.find(
            "{http://www.opengis.net/sensorml/2.0}IdentifierList"
        )
        sml_identifiers = sml_identifier_list.findall(
            "{http://www.opengis.net/sensorml/2.0}identifier"
        )
        self.assertEqual(len(sml_identifiers), 1)
        sml_identifier_short_name = sml_identifiers[0]

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
            platform.short_name,
        )
        sml_history_pl = sml_physical_system.find(
            "{http://www.opengis.net/sensorml/2.0}history"
        )
        sml_event_list_pl = sml_history_pl.find(
            "{http://www.opengis.net/sensorml/2.0}EventList"
        )
        sml_events_pl = sml_event_list_pl.findall(
            "{http://www.opengis.net/sensorml/2.0}event"
        )
        self.assertEqual(len(sml_events_pl), 1)

        sml_mount_event_pl = sml_events_pl[0]

        self.assertEqual(
            sml_mount_event_pl.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}classification")
            .find("{http://www.opengis.net/sensorml/2.0}ClassifierList")
            .find("{http://www.opengis.net/sensorml/2.0}classifier")
            .find("{http://www.opengis.net/sensorml/2.0}Term")
            .attrib.get("definition"),
            "Mount",
        )
        self.assertEqual(
            sml_mount_event_pl.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}classification")
            .find("{http://www.opengis.net/sensorml/2.0}ClassifierList")
            .find("{http://www.opengis.net/sensorml/2.0}classifier")
            .find("{http://www.opengis.net/sensorml/2.0}Term")
            .find("{http://www.opengis.net/sensorml/2.0}label")
            .text,
            f"Mounted to {self.configuration.label}",
        )
        self.assertEqual(
            sml_mount_event_pl.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}classification")
            .find("{http://www.opengis.net/sensorml/2.0}ClassifierList")
            .find("{http://www.opengis.net/sensorml/2.0}classifier")
            .find("{http://www.opengis.net/sensorml/2.0}Term")
            .find("{http://www.opengis.net/sensorml/2.0}value")
            .text,
            "Mount",
        )
        self.assertEqual(
            sml_mount_event_pl.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}time")
            .find("{http://www.opengis.net/gml/3.2}TimePeriod")
            .attrib.get("{http://www.opengis.net/gml/3.2}id"),
            f"TimePeriodForPlatformMountAction_{platform_mount_action.id}_of_platform_{platform.id}",
        )
        self.assertEqual(
            sml_mount_event_pl.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}time")
            .find("{http://www.opengis.net/gml/3.2}TimePeriod")
            .find("{http://www.opengis.net/gml/3.2}description")
            .text,
            platform_mount_action.begin_description,
        )
        self.assertEqual(
            sml_mount_event_pl.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}time")
            .find("{http://www.opengis.net/gml/3.2}TimePeriod")
            .find("{http://www.opengis.net/gml/3.2}begin")
            .find("{http://www.opengis.net/gml/3.2}TimeInstant")
            .find("{http://www.opengis.net/gml/3.2}timePosition")
            .text,
            "2022-12-23T00:00:00+00:00",
        )
        self.assertEqual(
            sml_mount_event_pl.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}time")
            .find("{http://www.opengis.net/gml/3.2}TimePeriod")
            .find("{http://www.opengis.net/gml/3.2}end")
            .find("{http://www.opengis.net/gml/3.2}TimeInstant")
            .find("{http://www.opengis.net/gml/3.2}timePosition")
            .text,
            "2022-12-26T00:00:00+00:00",
        )

        # And test for the device data that is nested.
        sml_components = sml_physical_system.find(
            "{http://www.opengis.net/sensorml/2.0}components"
        )
        sml_component_list = sml_components.find(
            "{http://www.opengis.net/sensorml/2.0}ComponentList"
        )
        sml_component_entries = sml_component_list.findall(
            "{http://www.opengis.net/sensorml/2.0}component"
        )

        self.assertEqual(len(sml_component_entries), 1)

        sml_physical_system = sml_component_entries[0].find(
            "{http://www.opengis.net/sensorml/2.0}PhysicalSystem"
        )

        gml_id = sml_physical_system.attrib.get("{http://www.opengis.net/gml/3.2}id")
        self.assertEqual(gml_id, f"device_{device.id}")

        sml_identification = sml_physical_system.find(
            "{http://www.opengis.net/sensorml/2.0}identification"
        )
        sml_identifier_list = sml_identification.find(
            "{http://www.opengis.net/sensorml/2.0}IdentifierList"
        )
        sml_identifiers = sml_identifier_list.findall(
            "{http://www.opengis.net/sensorml/2.0}identifier"
        )
        self.assertEqual(len(sml_identifiers), 1)
        sml_identifier_short_name = sml_identifiers[0]

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
            device.short_name,
        )
        sml_history_dv = sml_physical_system.find(
            "{http://www.opengis.net/sensorml/2.0}history"
        )
        sml_event_list_dv = sml_history_dv.find(
            "{http://www.opengis.net/sensorml/2.0}EventList"
        )
        sml_events_dv = sml_event_list_dv.findall(
            "{http://www.opengis.net/sensorml/2.0}event"
        )
        self.assertEqual(len(sml_events_dv), 1)

        sml_mount_event_dv = sml_events_dv[0]

        self.assertEqual(
            sml_mount_event_dv.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}classification")
            .find("{http://www.opengis.net/sensorml/2.0}ClassifierList")
            .find("{http://www.opengis.net/sensorml/2.0}classifier")
            .find("{http://www.opengis.net/sensorml/2.0}Term")
            .attrib.get("definition"),
            "Mount",
        )
        self.assertEqual(
            sml_mount_event_dv.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}classification")
            .find("{http://www.opengis.net/sensorml/2.0}ClassifierList")
            .find("{http://www.opengis.net/sensorml/2.0}classifier")
            .find("{http://www.opengis.net/sensorml/2.0}Term")
            .find("{http://www.opengis.net/sensorml/2.0}label")
            .text,
            f"Mounted to {self.configuration.label}",
        )
        self.assertEqual(
            sml_mount_event_dv.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}classification")
            .find("{http://www.opengis.net/sensorml/2.0}ClassifierList")
            .find("{http://www.opengis.net/sensorml/2.0}classifier")
            .find("{http://www.opengis.net/sensorml/2.0}Term")
            .find("{http://www.opengis.net/sensorml/2.0}value")
            .text,
            "Mount",
        )
        self.assertEqual(
            sml_mount_event_dv.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}time")
            .find("{http://www.opengis.net/gml/3.2}TimePeriod")
            .attrib.get("{http://www.opengis.net/gml/3.2}id"),
            f"TimePeriodForDeviceMountAction_{device_mount_action.id}_of_device_{device.id}",
        )
        self.assertEqual(
            sml_mount_event_dv.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}time")
            .find("{http://www.opengis.net/gml/3.2}TimePeriod")
            .find("{http://www.opengis.net/gml/3.2}description")
            .text,
            device_mount_action.begin_description,
        )
        self.assertEqual(
            sml_mount_event_dv.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}time")
            .find("{http://www.opengis.net/gml/3.2}TimePeriod")
            .find("{http://www.opengis.net/gml/3.2}begin")
            .find("{http://www.opengis.net/gml/3.2}TimeInstant")
            .find("{http://www.opengis.net/gml/3.2}timePosition")
            .text,
            "2022-12-24T00:00:00+00:00",
        )
        self.assertEqual(
            sml_mount_event_dv.find("{http://www.opengis.net/sensorml/2.0}Event")
            .find("{http://www.opengis.net/sensorml/2.0}time")
            .find("{http://www.opengis.net/gml/3.2}TimePeriod")
            .find("{http://www.opengis.net/gml/3.2}end")
            .find("{http://www.opengis.net/gml/3.2}TimeInstant")
            .find("{http://www.opengis.net/gml/3.2}timePosition")
            .text,
            "2022-12-25T00:00:00+00:00",
        )

    def test_multiple_device_mount_on_same_platform(self):
        """Ensure that the device is only listed once below the platform."""
        contact = Contact(given_name="Given", family_name="Fam", email="given@family")
        device = Device(short_name="test device", is_public=True)
        platform = Platform(short_name="test platform", is_public=True)
        platform_mount_action = PlatformMountAction(
            configuration=self.configuration,
            platform=platform,
            begin_date=datetime.datetime(year=2022, month=12, day=23, tzinfo=pytz.utc),
            end_date=datetime.datetime(year=2023, month=12, day=26, tzinfo=pytz.utc),
            begin_contact=contact,
            begin_description="Some platform desc",
        )
        device_mount_action1 = DeviceMountAction(
            configuration=self.configuration,
            parent_platform=platform,
            device=device,
            begin_date=datetime.datetime(year=2022, month=12, day=24, tzinfo=pytz.utc),
            end_date=datetime.datetime(year=2022, month=12, day=25, tzinfo=pytz.utc),
            begin_contact=contact,
            begin_description="Some device desc",
        )
        device_mount_action2 = DeviceMountAction(
            configuration=self.configuration,
            parent_platform=platform,
            device=device,
            begin_date=datetime.datetime(year=2023, month=12, day=24, tzinfo=pytz.utc),
            end_date=datetime.datetime(year=2023, month=12, day=25, tzinfo=pytz.utc),
            begin_contact=contact,
            begin_description="Some extended device mount desc",
        )

        db.session.add_all(
            [
                contact,
                platform,
                device,
                platform_mount_action,
                device_mount_action1,
                device_mount_action2,
            ]
        )
        db.session.commit()

        with self.client:
            resp = self.client.get(f"{self.url}/{self.configuration.id}/sensorml")

        self.assertEqual(resp.status_code, 200)
        xml_text = resp.text
        self.schema.validate(xml_text)
        root = xml.etree.ElementTree.fromstring(resp.text)

        # The first components entry is that of the configuration.
        # Here we have one entry (the platform).
        sml_components = root.find("{http://www.opengis.net/sensorml/2.0}components")
        sml_component_list = sml_components.find(
            "{http://www.opengis.net/sensorml/2.0}ComponentList"
        )
        sml_component_entries = sml_component_list.findall(
            "{http://www.opengis.net/sensorml/2.0}component"
        )
        self.assertEqual(len(sml_component_entries), 1)

        sml_physical_system = sml_component_entries[0].find(
            "{http://www.opengis.net/sensorml/2.0}PhysicalSystem"
        )
        gml_id = sml_physical_system.attrib.get("{http://www.opengis.net/gml/3.2}id")

        self.assertEqual(gml_id, f"platform_{platform.id}")

        sml_components_pl = sml_physical_system.find(
            "{http://www.opengis.net/sensorml/2.0}components"
        )
        sml_component_list_pl = sml_components_pl.find(
            "{http://www.opengis.net/sensorml/2.0}ComponentList"
        )
        sml_component_entries_pl = sml_component_list_pl.findall(
            "{http://www.opengis.net/sensorml/2.0}component"
        )

        self.assertEqual(len(sml_component_entries_pl), 1)

        sml_physical_system_dv = sml_component_entries_pl[0].find(
            "{http://www.opengis.net/sensorml/2.0}PhysicalSystem"
        )
        gml_id_dv = sml_physical_system_dv.attrib.get(
            "{http://www.opengis.net/gml/3.2}id"
        )

        self.assertEqual(gml_id_dv, f"device_{device.id}")

    def test_multiple_device_mount_on_base(self):
        """Ensure that the device is only listed once below the configuration."""
        contact = Contact(given_name="Given", family_name="Fam", email="given@family")
        device = Device(short_name="test device", is_public=True)
        device_mount_action1 = DeviceMountAction(
            configuration=self.configuration,
            device=device,
            begin_date=datetime.datetime(year=2022, month=12, day=24, tzinfo=pytz.utc),
            end_date=datetime.datetime(year=2022, month=12, day=25, tzinfo=pytz.utc),
            begin_contact=contact,
            begin_description="Some device desc",
        )
        device_mount_action2 = DeviceMountAction(
            configuration=self.configuration,
            device=device,
            begin_date=datetime.datetime(year=2023, month=12, day=24, tzinfo=pytz.utc),
            end_date=datetime.datetime(year=2023, month=12, day=25, tzinfo=pytz.utc),
            begin_contact=contact,
            begin_description="Some extended device mount desc",
        )

        db.session.add_all(
            [
                contact,
                device,
                device_mount_action1,
                device_mount_action2,
            ]
        )
        db.session.commit()

        with self.client:
            resp = self.client.get(f"{self.url}/{self.configuration.id}/sensorml")

        self.assertEqual(resp.status_code, 200)
        xml_text = resp.text
        self.schema.validate(xml_text)
        root = xml.etree.ElementTree.fromstring(resp.text)

        # There is only one components entry (the device itself).
        sml_components = root.find("{http://www.opengis.net/sensorml/2.0}components")
        sml_component_list = sml_components.find(
            "{http://www.opengis.net/sensorml/2.0}ComponentList"
        )
        sml_component_entries = sml_component_list.findall(
            "{http://www.opengis.net/sensorml/2.0}component"
        )
        self.assertEqual(len(sml_component_entries), 1)

        sml_physical_system = sml_component_entries[0].find(
            "{http://www.opengis.net/sensorml/2.0}PhysicalSystem"
        )
        gml_id = sml_physical_system.attrib.get("{http://www.opengis.net/gml/3.2}id")

        self.assertEqual(gml_id, f"device_{device.id}")

    def test_multiple_platform_mount_on_base(self):
        """Ensure that the platform is only listed once below the configuration."""
        contact = Contact(given_name="Given", family_name="Fam", email="given@family")
        platform = Platform(short_name="test platform", is_public=True)
        platform_mount_action1 = PlatformMountAction(
            configuration=self.configuration,
            platform=platform,
            begin_date=datetime.datetime(year=2022, month=12, day=24, tzinfo=pytz.utc),
            end_date=datetime.datetime(year=2022, month=12, day=25, tzinfo=pytz.utc),
            begin_contact=contact,
            begin_description="Some platform desc",
        )
        platform_mount_action2 = PlatformMountAction(
            configuration=self.configuration,
            platform=platform,
            begin_date=datetime.datetime(year=2023, month=12, day=24, tzinfo=pytz.utc),
            end_date=datetime.datetime(year=2023, month=12, day=25, tzinfo=pytz.utc),
            begin_contact=contact,
            begin_description="Some extended platform mount desc",
        )

        db.session.add_all(
            [
                contact,
                platform,
                platform_mount_action1,
                platform_mount_action2,
            ]
        )
        db.session.commit()

        with self.client:
            resp = self.client.get(f"{self.url}/{self.configuration.id}/sensorml")

        self.assertEqual(resp.status_code, 200)
        xml_text = resp.text
        self.schema.validate(xml_text)
        root = xml.etree.ElementTree.fromstring(resp.text)

        # There is only one components entry (the platform itself).
        sml_components = root.find("{http://www.opengis.net/sensorml/2.0}components")
        sml_component_list = sml_components.find(
            "{http://www.opengis.net/sensorml/2.0}ComponentList"
        )
        sml_component_entries = sml_component_list.findall(
            "{http://www.opengis.net/sensorml/2.0}component"
        )
        self.assertEqual(len(sml_component_entries), 1)

        sml_physical_system = sml_component_entries[0].find(
            "{http://www.opengis.net/sensorml/2.0}PhysicalSystem"
        )
        gml_id = sml_physical_system.attrib.get("{http://www.opengis.net/gml/3.2}id")

        self.assertEqual(gml_id, f"platform_{platform.id}")

    def test_multiple_mounts_for_platform_under_platform(self):
        """Ensure we put the subplatform only once under a platform."""
        contact = Contact(given_name="Given", family_name="Fam", email="given@family")
        platform1 = Platform(short_name="first platform", is_public=True)
        platform2 = Platform(short_name="second platform", is_public=True)
        platform_mount_action1 = PlatformMountAction(
            configuration=self.configuration,
            platform=platform1,
            begin_date=datetime.datetime(year=2022, month=12, day=24, tzinfo=pytz.utc),
            end_date=datetime.datetime(year=2023, month=12, day=25, tzinfo=pytz.utc),
            begin_contact=contact,
            begin_description="Some first platform desc",
        )
        platform_mount_action2 = PlatformMountAction(
            configuration=self.configuration,
            platform=platform2,
            parent_platform=platform1,
            begin_date=datetime.datetime(year=2022, month=12, day=24, tzinfo=pytz.utc),
            end_date=datetime.datetime(year=2022, month=12, day=25, tzinfo=pytz.utc),
            begin_contact=contact,
            begin_description="Some second platform desc",
        )
        platform_mount_action3 = PlatformMountAction(
            configuration=self.configuration,
            platform=platform2,
            parent_platform=platform1,
            begin_date=datetime.datetime(year=2023, month=12, day=24, tzinfo=pytz.utc),
            end_date=datetime.datetime(year=2023, month=12, day=25, tzinfo=pytz.utc),
            begin_contact=contact,
            begin_description="Some other second platform mount desc",
        )

        db.session.add_all(
            [
                contact,
                platform1,
                platform2,
                platform_mount_action1,
                platform_mount_action2,
                platform_mount_action3,
            ]
        )
        db.session.commit()

        with self.client:
            resp = self.client.get(f"{self.url}/{self.configuration.id}/sensorml")

        self.assertEqual(resp.status_code, 200)
        xml_text = resp.text
        self.schema.validate(xml_text)
        root = xml.etree.ElementTree.fromstring(resp.text)

        # The first components entry is that of the configuration.
        # Here we have one entry (the platform1).
        sml_components = root.find("{http://www.opengis.net/sensorml/2.0}components")
        sml_component_list = sml_components.find(
            "{http://www.opengis.net/sensorml/2.0}ComponentList"
        )
        sml_component_entries = sml_component_list.findall(
            "{http://www.opengis.net/sensorml/2.0}component"
        )
        self.assertEqual(len(sml_component_entries), 1)

        sml_physical_system = sml_component_entries[0].find(
            "{http://www.opengis.net/sensorml/2.0}PhysicalSystem"
        )
        gml_id = sml_physical_system.attrib.get("{http://www.opengis.net/gml/3.2}id")

        self.assertEqual(gml_id, f"platform_{platform1.id}")

        sml_components_pl = sml_physical_system.find(
            "{http://www.opengis.net/sensorml/2.0}components"
        )
        sml_component_list_pl = sml_components_pl.find(
            "{http://www.opengis.net/sensorml/2.0}ComponentList"
        )
        sml_component_entries_pl = sml_component_list_pl.findall(
            "{http://www.opengis.net/sensorml/2.0}component"
        )

        self.assertEqual(len(sml_component_entries_pl), 1)

        sml_physical_system_pl2 = sml_component_entries_pl[0].find(
            "{http://www.opengis.net/sensorml/2.0}PhysicalSystem"
        )
        gml_id_pl2 = sml_physical_system_pl2.attrib.get(
            "{http://www.opengis.net/gml/3.2}id"
        )

        self.assertEqual(gml_id_pl2, f"platform_{platform2.id}")

    def test_device_mounted_on_different_platforms(self):
        """Ensure that we insert the device as component for both platforms."""
        contact = Contact(given_name="Given", family_name="Fam", email="given@family")
        device = Device(short_name="test device", is_public=True)
        platform1 = Platform(short_name="test platform 1", is_public=True)
        platform2 = Platform(short_name="test platform 2", is_public=True)
        platform_mount_action1 = PlatformMountAction(
            configuration=self.configuration,
            platform=platform1,
            begin_date=datetime.datetime(year=2022, month=12, day=23, tzinfo=pytz.utc),
            end_date=datetime.datetime(year=2022, month=12, day=26, tzinfo=pytz.utc),
            begin_contact=contact,
            begin_description="Some platform desc",
        )
        platform_mount_action2 = PlatformMountAction(
            configuration=self.configuration,
            platform=platform2,
            begin_date=datetime.datetime(year=2023, month=12, day=23, tzinfo=pytz.utc),
            end_date=datetime.datetime(year=2023, month=12, day=26, tzinfo=pytz.utc),
            begin_contact=contact,
            begin_description="Some platform desc",
        )
        device_mount_action1 = DeviceMountAction(
            configuration=self.configuration,
            parent_platform=platform1,
            device=device,
            begin_date=datetime.datetime(year=2022, month=12, day=24, tzinfo=pytz.utc),
            end_date=datetime.datetime(year=2022, month=12, day=25, tzinfo=pytz.utc),
            begin_contact=contact,
            begin_description="Some device desc",
        )
        device_mount_action2 = DeviceMountAction(
            configuration=self.configuration,
            parent_platform=platform2,
            device=device,
            begin_date=datetime.datetime(year=2023, month=12, day=24, tzinfo=pytz.utc),
            end_date=datetime.datetime(year=2023, month=12, day=25, tzinfo=pytz.utc),
            begin_contact=contact,
            begin_description="Some device desc",
        )
        db.session.add_all(
            [
                contact,
                platform1,
                platform2,
                device,
                platform_mount_action1,
                platform_mount_action2,
                device_mount_action1,
                device_mount_action2,
            ]
        )
        db.session.commit()
        with self.client:
            resp = self.client.get(f"{self.url}/{self.configuration.id}/sensorml")

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
        # We have two different platforms here.
        self.assertEqual(len(sml_component_entries), 2)

        first_platform = sml_component_entries[0].find(
            "{http://www.opengis.net/sensorml/2.0}PhysicalSystem"
        )
        second_platform = sml_component_entries[1].find(
            "{http://www.opengis.net/sensorml/2.0}PhysicalSystem"
        )

        self.assertEqual(
            first_platform.attrib.get("{http://www.opengis.net/gml/3.2}id"),
            f"platform_{platform1.id}",
        )

        self.assertEqual(
            len(
                first_platform.find("{http://www.opengis.net/sensorml/2.0}components")
                .find("{http://www.opengis.net/sensorml/2.0}ComponentList")
                .findall("{http://www.opengis.net/sensorml/2.0}component")
            ),
            1,
        )
        self.assertEqual(
            first_platform.find("{http://www.opengis.net/sensorml/2.0}components")
            .find("{http://www.opengis.net/sensorml/2.0}ComponentList")
            .find("{http://www.opengis.net/sensorml/2.0}component")
            .find("{http://www.opengis.net/sensorml/2.0}PhysicalSystem")
            .attrib.get("{http://www.opengis.net/gml/3.2}id"),
            f"device_{device.id}",
        )

        self.assertEqual(
            second_platform.attrib.get("{http://www.opengis.net/gml/3.2}id"),
            f"platform_{platform2.id}",
        )
        self.assertEqual(
            len(
                second_platform.find("{http://www.opengis.net/sensorml/2.0}components")
                .find("{http://www.opengis.net/sensorml/2.0}ComponentList")
                .findall("{http://www.opengis.net/sensorml/2.0}component")
            ),
            1,
        )
        self.assertEqual(
            second_platform.find("{http://www.opengis.net/sensorml/2.0}components")
            .find("{http://www.opengis.net/sensorml/2.0}ComponentList")
            .find("{http://www.opengis.net/sensorml/2.0}component")
            .find("{http://www.opengis.net/sensorml/2.0}PhysicalSystem")
            .attrib.get("{http://www.opengis.net/gml/3.2}id"),
            # We have a different gml id here, but rest is the same.
            f"device_{device.id}_dup_1",
        )
