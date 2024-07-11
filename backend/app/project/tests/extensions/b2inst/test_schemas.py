# SPDX-FileCopyrightText: 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Test cases for the b2inst schemas."""

import datetime
from unittest import TestCase

import pytz

from project.extensions.b2inst import schemas


class TestB2InstOwner(TestCase):
    """Test class for the B2InstOwner class."""

    def test_dict_just_name_and_contact(self):
        """Test the dict method with just the name & contact."""
        owner = schemas.B2InstOwner(
            ownerName="Homer S.",
            ownerContact="homerj@nuclear.us",
            ownerIdentifier=None,
            ownerIdentifierType=None,
        )

        result = owner.dict()

        expected = {
            "ownerName": "Homer S.",
            "ownerContact": "homerj@nuclear.us",
        }
        self.assertEqual(result, expected)

    def test_dict_with_identifier(self):
        """Test the dict method including the identifier."""
        owner = schemas.B2InstOwner(
            ownerName="Homer S.",
            ownerContact="homerj@nuclear.us",
            ownerIdentifier="https://orcid.org/1234-5678-9012",
            ownerIdentifierType="URN",
        )

        result = owner.dict()

        expected = {
            "ownerName": "Homer S.",
            "ownerContact": "homerj@nuclear.us",
            "ownerIdentifier": {
                "ownerIdentifierValue": "https://orcid.org/1234-5678-9012",
                "ownerIdentifierType": "URN",
            },
        }
        self.assertEqual(result, expected)

    def test_dict_with_only_the_name(self):
        """Test the dict method even without the contact."""
        owner = schemas.B2InstOwner(
            ownerName=":unav",
            ownerContact=None,
            ownerIdentifier=None,
            ownerIdentifierType=None,
        )

        result = owner.dict()

        expected = {
            "ownerName": ":unav",
        }
        self.assertEqual(result, expected)


class TestB2InstInstrumentType(TestCase):
    """Test class for the B2InstInstrumentType class."""

    def test_dict_just_instrument_type_name(self):
        """Test the dict method with just the type name."""
        instrument_type = schemas.B2InstInstrumentType(
            instrumentTypeName="sensor",
            instrumentTypeIdentifier=None,
            instrumentTypeIdentifierType=None,
        )

        result = instrument_type.dict()

        expected = {"instrumentTypeName": "sensor"}
        self.assertEqual(result, expected)

    def test_dict_with_identifier(self):
        """Test the dict method including the identifier."""
        instrument_type = schemas.B2InstInstrumentType(
            instrumentTypeName="sensor",
            instrumentTypeIdentifier="https://sensors.org/1",
            instrumentTypeIdentifierType="URL",
        )
        result = instrument_type.dict()

        expected = {
            "instrumentTypeName": "sensor",
            "instrumentTypeIdentifier": {
                "instrumentTypeIdentifierValue": "https://sensors.org/1",
                "instrumentTypeIdentifierType": "URL",
            },
        }
        self.assertEqual(result, expected)


class TestB2InstManufacturer(TestCase):
    """Test class for the B2InstManufacturer class."""

    def test_dict_just_manufacturer_name(self):
        """Test the dict method with just the name."""
        manufacturer = schemas.B2InstManufacturer(
            manufacturerName="Sensors GmbH",
            manufacturerIdentifier=None,
            manufacturerIdentifierType=None,
        )

        result = manufacturer.dict()

        expected = {"manufacturerName": "Sensors GmbH"}
        self.assertEqual(result, expected)

    def test_dict_with_identifier(self):
        """Test the dict method including the identifier."""
        manufacturer = schemas.B2InstManufacturer(
            manufacturerName="Sensors GmbH",
            manufacturerIdentifier="https://sensorsgmbh.de/",
            manufacturerIdentifierType="URL",
        )
        result = manufacturer.dict()

        expected = {
            "manufacturerName": "Sensors GmbH",
            "manufacturerIdentifier": {
                "manufacturerIdentifierValue": "https://sensorsgmbh.de/",
                "manufacturerIdentifierType": "URL",
            },
        }
        self.assertEqual(result, expected)


class TestB2InstModel(TestCase):
    """Test class for the B2InstModel class."""

    def test_dict(self):
        """Test the dict method."""
        model = schemas.B2InstModel(modelName="0815")

        result = model.dict()

        expected = {
            "modelName": "0815",
        }
        self.assertEqual(result, expected)


class TestB2InstAlternateIdentifier(TestCase):
    """Test class for the B2InstAlternateIdentifier class."""

    def test_dict_serialnumber(self):
        """Test the dict with a serial number identifier."""
        identifier = schemas.B2InstAlternateIdentifier(
            alternateIdentifier="123",
            alternateIdentifierType="SerialNumber",
            alternateIdentifierName=None,
        )

        result = identifier.dict()

        expected = {
            "alternateIdentifierValue": "123",
            "alternateIdentifierType": "SerialNumber",
        }
        self.assertEqual(result, expected)

    def test_dict_other(self):
        """Test the dict with another identifier type."""
        identifier = schemas.B2InstAlternateIdentifier(
            alternateIdentifier="123",
            alternateIdentifierType="Other",
            alternateIdentifierName="DB id",
        )

        result = identifier.dict()

        expected = {
            "alternateIdentifierValue": "123",
            "alternateIdentifierType": "Other",
            "alternateIdentifierName": "DB id",
        }
        self.assertEqual(result, expected)


class TestB2InstDate(TestCase):
    """Test class for the B2InstDate class."""

    def test_dict(self):
        """Test the dict method."""
        date = schemas.B2InstDate(
            Date=datetime.datetime(2022, 1, 1, 0, 0, 0, tzinfo=pytz.utc),
            dateType="Commissioned",
        )

        result = date.dict()

        expected = {"Date": "2022-01-01T00:00:00+00:00", "dateType": "Commissioned"}
        self.assertEqual(result, expected)


class TestB2InstDraftPost(TestCase):
    """Test class for the B2InstDraftPost class."""

    def test_dict(self):
        """Test the dict method."""
        draft_post = schemas.B2InstDraftPost(
            community="0000-0001",
            open_access=True,
            Name="Name2",
            Description="Some text",
            Owner=[
                schemas.B2InstOwner(
                    ownerName="Homer S.",
                    ownerContact="homerj@nuclear.us",
                    ownerIdentifier=None,
                    ownerIdentifierType=None,
                )
            ],
            InstrumentType=[
                schemas.B2InstInstrumentType(
                    instrumentTypeName="sensor",
                    instrumentTypeIdentifier=None,
                    instrumentTypeIdentifierType=None,
                )
            ],
            LandingPage="https://somewhere.in/the/web",
            Manufacturer=[
                schemas.B2InstManufacturer(
                    manufacturerName="Sensors GmbH",
                    manufacturerIdentifier=None,
                    manufacturerIdentifierType=None,
                )
            ],
            Model=schemas.B2InstModel(modelName="0815"),
            MeasuredVariable=["temperature", "voltage"],
            Date=[
                schemas.B2InstDate(
                    Date=datetime.datetime(2022, 1, 1, 0, 0, 0, tzinfo=pytz.utc),
                    dateType="Commissioned",
                )
            ],
            AlternateIdentifier=[
                schemas.B2InstAlternateIdentifier(
                    alternateIdentifier="123",
                    alternateIdentifierType="SerialNumber",
                    alternateIdentifierName=None,
                )
            ],
            SchemaVersion="1.0.1",
        )

        result = draft_post.dict()

        expected = {
            "community": "0000-0001",
            "open_access": True,
            "Name": "Name2",
            "Description": "Some text",
            "Owner": [
                {
                    "ownerName": "Homer S.",
                    "ownerContact": "homerj@nuclear.us",
                }
            ],
            "InstrumentType": [{"instrumentTypeName": "sensor"}],
            "LandingPage": "https://somewhere.in/the/web",
            "Manufacturer": [{"manufacturerName": "Sensors GmbH"}],
            "Model": {
                "modelName": "0815",
            },
            "MeasuredVariable": ["temperature", "voltage"],
            "Date": [{"Date": "2022-01-01T00:00:00+00:00", "dateType": "Commissioned"}],
            "AlternateIdentifier": [
                {
                    "alternateIdentifierValue": "123",
                    "alternateIdentifierType": "SerialNumber",
                }
            ],
            "SchemaVersion": "1.0.1",
        }

        self.assertEqual(result, expected)

    def test_dict_without_optinal_fields(self):
        """Test the dict method but this time without some of the fields that are seen as optional in b2inst."""
        draft_post = schemas.B2InstDraftPost(
            community="0000-0001",
            open_access=True,
            Name="Name2",
            Description="Some text",
            Owner=[
                schemas.B2InstOwner(
                    ownerName="Homer S.",
                    ownerContact="homerj@nuclear.us",
                    ownerIdentifier=None,
                    ownerIdentifierType=None,
                )
            ],
            InstrumentType=[],
            LandingPage="https://somewhere.in/the/web",
            Manufacturer=[
                schemas.B2InstManufacturer(
                    manufacturerName="Sensors GmbH",
                    manufacturerIdentifier=None,
                    manufacturerIdentifierType=None,
                )
            ],
            Model=None,
            MeasuredVariable=[],
            Date=[
                schemas.B2InstDate(
                    Date=datetime.datetime(2022, 1, 1, 0, 0, 0, tzinfo=pytz.utc),
                    dateType="Commissioned",
                )
            ],
            AlternateIdentifier=[
                schemas.B2InstAlternateIdentifier(
                    alternateIdentifier="123",
                    alternateIdentifierType="SerialNumber",
                    alternateIdentifierName=None,
                )
            ],
            SchemaVersion="1.0.1",
        )

        result = draft_post.dict()

        expected = {
            "community": "0000-0001",
            "open_access": True,
            "Name": "Name2",
            "Description": "Some text",
            "Owner": [
                {
                    "ownerName": "Homer S.",
                    "ownerContact": "homerj@nuclear.us",
                }
            ],
            "LandingPage": "https://somewhere.in/the/web",
            "Manufacturer": [{"manufacturerName": "Sensors GmbH"}],
            "Date": [{"Date": "2022-01-01T00:00:00+00:00", "dateType": "Commissioned"}],
            "AlternateIdentifier": [
                {
                    "alternateIdentifierValue": "123",
                    "alternateIdentifierType": "SerialNumber",
                }
            ],
            "SchemaVersion": "1.0.1",
        }

        self.assertEqual(result, expected)
