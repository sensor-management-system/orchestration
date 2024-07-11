# SPDX-FileCopyrightText: 2023-2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Test cases for the b2inst mappers."""

import datetime
from unittest import TestCase

import pytz

from project.api.models import (
    Configuration,
    ConfigurationContactRole,
    Contact,
    Device,
    DeviceContactRole,
    DeviceMountAction,
    DeviceProperty,
    Platform,
    PlatformContactRole,
    PlatformMountAction,
)
from project.api.models.base_model import db
from project.extensions.b2inst import mappers, schemas
from project.tests.base import BaseTestCase


class TestB2InstDeviceMapper(BaseTestCase):
    """Test class for the B2InstDeviceMapper class."""

    landing_page = "https://sms.helmholtz.cloud/"

    def test_to_draft_post_minimal(self):
        """Ensure we can map a minimal set of data to b2inst."""
        device = Device(short_name="", description="")
        db.session.add(device)
        db.session.commit()

        mapper = mappers.B2InstDeviceMapper()
        result = mapper.to_draft_post(
            device,
            community="A",
            open_access=True,
            base_landing_page=self.landing_page,
            schema_version="1.0.0",
        )

        # Some of the information need to be present in the
        # pidinst schema - and so for the b2inst too.
        # The pidinst docs for that are here:
        # https://docs.pidinst.org/en/latest/white-paper/metadata-schema-recommendations.html#dealing-with-unknown-information
        # For a missing name it makes sense to handle it as "Untitled" - so the :unas value makes most sense.
        # For a missing owner or manufacturer, maybe we should use :unav - as there might be an owner
        # or a manufacturer, but we have no information about it.
        expected = schemas.B2InstDraftPost(
            community="A",
            open_access=True,
            Name=":unas",
            Description="",
            Owner=[
                schemas.B2InstOwner(
                    ownerName=":unav",
                    ownerContact=None,
                    ownerIdentifier=None,
                    ownerIdentifierType=None,
                )
            ],
            InstrumentType=[],
            LandingPage=f"{self.landing_page}/devices/{device.id}",
            Manufacturer=[
                schemas.B2InstManufacturer(
                    manufacturerName=":unav",
                    manufacturerIdentifier=None,
                    manufacturerIdentifierType=None,
                )
            ],
            Model=None,
            MeasuredVariable=[],
            Date=[],
            AlternateIdentifier=[
                schemas.B2InstAlternateIdentifier(
                    alternateIdentifier=f"{self.landing_page}/devices/{device.id}",
                    alternateIdentifierType="Other",
                    alternateIdentifierName="URL",
                )
            ],
            SchemaVersion="1.0.0",
        )

        self.assertEqual(result, expected)

    def test_to_draft_post_large(self):
        """Ensure we can map a larger set of data to b2inst."""
        device = Device(
            short_name="SMT100",
            description="The SMT 100",
            manufacturer_name="TRUEBENER GmbH",
            manufacturer_uri="https://cv/api/v1/manufacturers/1/",
            device_type_name="Soil moisture sensor",
            device_type_uri="https://cv/api/v1/equipmenttypes/1/",
            model="SMT 100",
            serial_number="123",
            inventory_number="345",
        )
        contact1 = Contact(
            given_name="A",
            family_name="B",
            email="ab@localhost",
            orcid="1234-5678-9012-3456",
            organization="LocalHost",
        )
        contact2 = Contact(
            given_name="C",
            family_name="B",
            email="cb@localhost",
            orcid="9234-5678-9012-3456",
            organization="LocalHost",
        )
        device_contact_role1 = DeviceContactRole(
            device=device,
            contact=contact1,
            role_name="Owner",
            role_uri="https://cv/api/v1/roles/1/",
        )
        device_contact_role2 = DeviceContactRole(
            device=device,
            contact=contact2,
            role_name="Owner",
            role_uri="https://cv/api/v1/roles/1/",
        )
        device_property = DeviceProperty(
            device=device,
            property_name="Soil moisture",
        )
        db.session.add_all(
            [
                device,
                contact1,
                contact2,
                device_contact_role1,
                device_contact_role2,
                device_property,
            ]
        )
        db.session.commit()

        mapper = mappers.B2InstDeviceMapper()
        result = mapper.to_draft_post(
            device,
            community="A",
            open_access=True,
            base_landing_page=self.landing_page,
            schema_version="1.0.0",
        )

        expected = schemas.B2InstDraftPost(
            community="A",
            open_access=True,
            Name="SMT100 - TRUEBENER GmbH - SMT 100 - 123",
            Description="The SMT 100",
            Owner=[
                schemas.B2InstOwner(
                    ownerName="LocalHost",
                    ownerContact=None,
                    ownerIdentifier=None,
                    ownerIdentifierType=None,
                )
            ],
            InstrumentType=[
                schemas.B2InstInstrumentType(
                    instrumentTypeName="Soil moisture sensor",
                    instrumentTypeIdentifier="https://cv/api/v1/equipmenttypes/1/",
                    instrumentTypeIdentifierType="URL",
                )
            ],
            LandingPage=f"{self.landing_page}/devices/{device.id}",
            Manufacturer=[
                schemas.B2InstManufacturer(
                    manufacturerName="TRUEBENER GmbH",
                    manufacturerIdentifier="https://cv/api/v1/manufacturers/1/",
                    manufacturerIdentifierType="URL",
                )
            ],
            Model=schemas.B2InstModel(modelName="SMT 100"),
            MeasuredVariable=["Soil moisture"],
            Date=[],
            AlternateIdentifier=[
                schemas.B2InstAlternateIdentifier(
                    alternateIdentifier="123",
                    alternateIdentifierType="SerialNumber",
                    alternateIdentifierName=None,
                ),
                schemas.B2InstAlternateIdentifier(
                    alternateIdentifier="345",
                    alternateIdentifierType="InventoryNumber",
                    alternateIdentifierName=None,
                ),
                schemas.B2InstAlternateIdentifier(
                    alternateIdentifier=f"{self.landing_page}/devices/{device.id}",
                    alternateIdentifierType="Other",
                    alternateIdentifierName="URL",
                ),
            ],
            SchemaVersion="1.0.0",
        )

        self.assertEqual(result, expected)

    def test_to_draft_less_identifiers(self):
        """Ensure we can map a set of data without many identifiers to b2inst."""
        device = Device(
            short_name="SMT100",
            description="The SMT 100",
            manufacturer_name="TRUEBENER GmbH",
            device_type_name="Soil moisture sensor",
            model="SMT 100",
        )
        contact = Contact(
            given_name="A",
            family_name="B",
            email="ab@localhost",
            organization="LocalHost",
        )
        device_contact_role = DeviceContactRole(
            device=device,
            contact=contact,
            role_name="Owner",
            role_uri="https://cv/api/v1/roles/1/",
        )
        device_property = DeviceProperty(
            device=device,
            property_name="Soil moisture",
        )
        db.session.add_all([device, contact, device_contact_role, device_property])
        db.session.commit()

        mapper = mappers.B2InstDeviceMapper()
        result = mapper.to_draft_post(
            device,
            community="A",
            open_access=True,
            base_landing_page=self.landing_page,
            schema_version="1.0.0",
        )

        expected = schemas.B2InstDraftPost(
            community="A",
            open_access=True,
            Name="SMT100 - TRUEBENER GmbH - SMT 100",
            Description="The SMT 100",
            Owner=[
                schemas.B2InstOwner(
                    ownerName="LocalHost",
                    ownerContact=None,
                    ownerIdentifier=None,
                    ownerIdentifierType=None,
                )
            ],
            InstrumentType=[
                schemas.B2InstInstrumentType(
                    instrumentTypeName="Soil moisture sensor",
                    instrumentTypeIdentifier=None,
                    instrumentTypeIdentifierType=None,
                )
            ],
            LandingPage=f"{self.landing_page}/devices/{device.id}",
            Manufacturer=[
                schemas.B2InstManufacturer(
                    manufacturerName="TRUEBENER GmbH",
                    manufacturerIdentifier=None,
                    manufacturerIdentifierType=None,
                )
            ],
            Model=schemas.B2InstModel(modelName="SMT 100"),
            MeasuredVariable=["Soil moisture"],
            Date=[],
            AlternateIdentifier=[
                schemas.B2InstAlternateIdentifier(
                    alternateIdentifier=f"{self.landing_page}/devices/{device.id}",
                    alternateIdentifierType="Other",
                    alternateIdentifierName="URL",
                ),
            ],
            SchemaVersion="1.0.0",
        )

        self.assertEqual(result, expected)

    def test_to_draft_different_contact_role(self):
        """Ensure we list only contacts as owners that have this role."""
        device = Device(
            short_name="SMT100",
            description="The SMT 100",
            manufacturer_name="TRUEBENER GmbH",
            device_type_name="Soil moisture sensor",
            model="SMT 100",
        )
        contact = Contact(
            given_name="A",
            family_name="B",
            email="ab@localhost",
            organization="LocalHost",
        )
        device_contact_role = DeviceContactRole(
            device=device,
            contact=contact,
            role_name="PI",
            role_uri="https://cv/api/v1/roles/2/",
        )
        device_property = DeviceProperty(
            device=device,
            property_name="Soil moisture",
        )
        db.session.add_all([device, contact, device_contact_role, device_property])
        db.session.commit()

        mapper = mappers.B2InstDeviceMapper()
        result = mapper.to_draft_post(
            device,
            community="A",
            open_access=True,
            base_landing_page=self.landing_page,
            schema_version="1.0.0",
        )

        expected = schemas.B2InstDraftPost(
            community="A",
            open_access=True,
            Name="SMT100 - TRUEBENER GmbH - SMT 100",
            Description="The SMT 100",
            Owner=[
                schemas.B2InstOwner(
                    ownerName=":unav",
                    ownerContact=None,
                    ownerIdentifier=None,
                    ownerIdentifierType=None,
                )
            ],
            InstrumentType=[
                schemas.B2InstInstrumentType(
                    instrumentTypeName="Soil moisture sensor",
                    instrumentTypeIdentifier=None,
                    instrumentTypeIdentifierType=None,
                )
            ],
            LandingPage=f"{self.landing_page}/devices/{device.id}",
            Manufacturer=[
                schemas.B2InstManufacturer(
                    manufacturerName="TRUEBENER GmbH",
                    manufacturerIdentifier=None,
                    manufacturerIdentifierType=None,
                )
            ],
            Model=schemas.B2InstModel(modelName="SMT 100"),
            MeasuredVariable=["Soil moisture"],
            Date=[],
            AlternateIdentifier=[
                schemas.B2InstAlternateIdentifier(
                    alternateIdentifier=f"{self.landing_page}/devices/{device.id}",
                    alternateIdentifierType="Other",
                    alternateIdentifierName="URL",
                ),
            ],
            SchemaVersion="1.0.0",
        )

        self.assertEqual(result, expected)

    def test_to_draft_inactive_contact(self):
        """Ensure we list only active contacts."""
        device = Device(
            short_name="SMT100",
            description="The SMT 100",
            manufacturer_name="TRUEBENER GmbH",
            device_type_name="Soil moisture sensor",
            model="SMT 100",
        )
        contact = Contact(
            given_name="A",
            family_name="B",
            email="ab@localhost",
            active=False,
            organization="LocalHost",
        )
        device_contact_role = DeviceContactRole(
            device=device,
            contact=contact,
            role_name="Owner",
            role_uri="https://cv/api/v1/roles/1/",
        )
        device_property = DeviceProperty(
            device=device,
            property_name="Soil moisture",
        )
        db.session.add_all([device, contact, device_contact_role, device_property])
        db.session.commit()

        mapper = mappers.B2InstDeviceMapper()
        result = mapper.to_draft_post(
            device,
            community="A",
            open_access=True,
            base_landing_page=self.landing_page,
            schema_version="1.0.0",
        )

        expected = schemas.B2InstDraftPost(
            community="A",
            open_access=True,
            Name="SMT100 - TRUEBENER GmbH - SMT 100",
            Description="The SMT 100",
            Owner=[
                schemas.B2InstOwner(
                    ownerName=":unav",
                    ownerContact=None,
                    ownerIdentifier=None,
                    ownerIdentifierType=None,
                )
            ],
            InstrumentType=[
                schemas.B2InstInstrumentType(
                    instrumentTypeName="Soil moisture sensor",
                    instrumentTypeIdentifier=None,
                    instrumentTypeIdentifierType=None,
                )
            ],
            LandingPage=f"{self.landing_page}/devices/{device.id}",
            Manufacturer=[
                schemas.B2InstManufacturer(
                    manufacturerName="TRUEBENER GmbH",
                    manufacturerIdentifier=None,
                    manufacturerIdentifierType=None,
                )
            ],
            Model=schemas.B2InstModel(modelName="SMT 100"),
            MeasuredVariable=["Soil moisture"],
            Date=[],
            AlternateIdentifier=[
                schemas.B2InstAlternateIdentifier(
                    alternateIdentifier=f"{self.landing_page}/devices/{device.id}",
                    alternateIdentifierType="Other",
                    alternateIdentifierName="URL",
                ),
            ],
            SchemaVersion="1.0.0",
        )

        self.assertEqual(result, expected)


class TestB2InstPlatformMapper(BaseTestCase):
    """Test class for the B2InstPlatformMapper class."""

    landing_page = "https://sms.helmholtz.cloud/"

    def test_to_draft_post_minimal(self):
        """Ensure we can map a minimal set of data to b2inst."""
        platform = Platform(short_name="", description="")
        db.session.add(platform)
        db.session.commit()

        mapper = mappers.B2InstPlatformMapper()
        result = mapper.to_draft_post(
            platform,
            community="A",
            open_access=True,
            base_landing_page=self.landing_page,
            schema_version="1.0.0",
        )

        expected = schemas.B2InstDraftPost(
            community="A",
            open_access=True,
            Name=":unas",
            Description="",
            Owner=[
                schemas.B2InstOwner(
                    ownerName=":unav",
                    ownerContact=None,
                    ownerIdentifier=None,
                    ownerIdentifierType=None,
                )
            ],
            InstrumentType=[],
            LandingPage=f"{self.landing_page}/platforms/{platform.id}",
            Manufacturer=[
                schemas.B2InstManufacturer(
                    manufacturerName=":unav",
                    manufacturerIdentifier=None,
                    manufacturerIdentifierType=None,
                )
            ],
            Model=None,
            MeasuredVariable=[],
            Date=[],
            AlternateIdentifier=[
                schemas.B2InstAlternateIdentifier(
                    alternateIdentifier=f"{self.landing_page}/platforms/{platform.id}",
                    alternateIdentifierType="Other",
                    alternateIdentifierName="URL",
                )
            ],
            SchemaVersion="1.0.0",
        )

        self.assertEqual(result, expected)

    def test_to_draft_post_large(self):
        """Ensure we can map a larger set of data to b2inst."""
        platform = Platform(
            short_name="CR1000",
            description="The CR 1000",
            manufacturer_name="Campbell Scientific",
            manufacturer_uri="https://cv/api/v1/manufacturers/1/",
            platform_type_name="Logger",
            platform_type_uri="https://cv/api/v1/equipmenttypes/1/",
            model="CR 1000",
            serial_number="123",
            inventory_number="345",
        )
        contact1 = Contact(
            given_name="A",
            family_name="B",
            email="ab@localhost",
            orcid="1234-5678-9012-3456",
            organization="LocalHost",
        )
        contact2 = Contact(
            given_name="C",
            family_name="B",
            email="cb@localhost",
            orcid="9234-5678-9012-3456",
            organization="LocalHost",
        )
        platform_contact_role1 = PlatformContactRole(
            platform=platform,
            contact=contact1,
            role_name="Owner",
            role_uri="https://cv/api/v1/roles/1/",
        )
        platform_contact_role2 = PlatformContactRole(
            platform=platform,
            contact=contact2,
            role_name="Owner",
            role_uri="https://cv/api/v1/roles/1/",
        )
        db.session.add_all(
            [
                platform,
                contact1,
                contact2,
                platform_contact_role1,
                platform_contact_role2,
            ]
        )
        db.session.commit()

        mapper = mappers.B2InstPlatformMapper()
        result = mapper.to_draft_post(
            platform,
            community="A",
            open_access=True,
            base_landing_page=self.landing_page,
            schema_version="1.0.0",
        )

        expected = schemas.B2InstDraftPost(
            community="A",
            open_access=True,
            Name="CR1000 - Campbell Scientific - CR 1000 - 123",
            Description="The CR 1000",
            Owner=[
                schemas.B2InstOwner(
                    ownerName="LocalHost",
                    ownerContact=None,
                    ownerIdentifier=None,
                    ownerIdentifierType=None,
                )
            ],
            InstrumentType=[
                schemas.B2InstInstrumentType(
                    instrumentTypeName="Logger",
                    instrumentTypeIdentifier="https://cv/api/v1/equipmenttypes/1/",
                    instrumentTypeIdentifierType="URL",
                )
            ],
            LandingPage=f"{self.landing_page}/platforms/{platform.id}",
            Manufacturer=[
                schemas.B2InstManufacturer(
                    manufacturerName="Campbell Scientific",
                    manufacturerIdentifier="https://cv/api/v1/manufacturers/1/",
                    manufacturerIdentifierType="URL",
                )
            ],
            Model=schemas.B2InstModel(modelName="CR 1000"),
            MeasuredVariable=[],
            Date=[],
            AlternateIdentifier=[
                schemas.B2InstAlternateIdentifier(
                    alternateIdentifier="123",
                    alternateIdentifierType="SerialNumber",
                    alternateIdentifierName=None,
                ),
                schemas.B2InstAlternateIdentifier(
                    alternateIdentifier="345",
                    alternateIdentifierType="InventoryNumber",
                    alternateIdentifierName=None,
                ),
                schemas.B2InstAlternateIdentifier(
                    alternateIdentifier=f"{self.landing_page}/platforms/{platform.id}",
                    alternateIdentifierType="Other",
                    alternateIdentifierName="URL",
                ),
            ],
            SchemaVersion="1.0.0",
        )

        self.assertEqual(result, expected)

    def test_to_draft_less_identifiers(self):
        """Ensure we can map a set of data without many identifiers to b2inst."""
        platform = Platform(
            short_name="CR1000",
            description="The CR 1000",
            manufacturer_name="Campbell Scientific",
            platform_type_name="Logger",
            model="CR 1000",
        )
        contact = Contact(
            given_name="A",
            family_name="B",
            email="ab@localhost",
            organization="LocalHost",
        )
        platform_contact_role = PlatformContactRole(
            platform=platform,
            contact=contact,
            role_name="Owner",
            role_uri="https://cv/api/v1/roles/1/",
        )
        db.session.add_all([platform, contact, platform_contact_role])
        db.session.commit()

        mapper = mappers.B2InstPlatformMapper()
        result = mapper.to_draft_post(
            platform,
            community="A",
            open_access=True,
            base_landing_page=self.landing_page,
            schema_version="1.0.0",
        )

        expected = schemas.B2InstDraftPost(
            community="A",
            open_access=True,
            Name="CR1000 - Campbell Scientific - CR 1000",
            Description="The CR 1000",
            Owner=[
                schemas.B2InstOwner(
                    ownerName="LocalHost",
                    ownerContact=None,
                    ownerIdentifier=None,
                    ownerIdentifierType=None,
                )
            ],
            InstrumentType=[
                schemas.B2InstInstrumentType(
                    instrumentTypeName="Logger",
                    instrumentTypeIdentifier=None,
                    instrumentTypeIdentifierType=None,
                )
            ],
            LandingPage=f"{self.landing_page}/platforms/{platform.id}",
            Manufacturer=[
                schemas.B2InstManufacturer(
                    manufacturerName="Campbell Scientific",
                    manufacturerIdentifier=None,
                    manufacturerIdentifierType=None,
                )
            ],
            Model=schemas.B2InstModel(modelName="CR 1000"),
            MeasuredVariable=[],
            Date=[],
            AlternateIdentifier=[
                schemas.B2InstAlternateIdentifier(
                    alternateIdentifier=f"{self.landing_page}/platforms/{platform.id}",
                    alternateIdentifierType="Other",
                    alternateIdentifierName="URL",
                ),
            ],
            SchemaVersion="1.0.0",
        )

        self.assertEqual(result, expected)

    def test_to_draft_different_contact_role(self):
        """Ensure we list only contacts as owners that have this role."""
        platform = Platform(
            short_name="CR1000",
            description="The CR 1000",
            manufacturer_name="Campbell Scientific",
            platform_type_name="Logger",
            model="CR 1000",
        )
        contact = Contact(
            given_name="A",
            family_name="B",
            email="ab@localhost",
            organization="LocalHost",
        )
        platform_contact_role = PlatformContactRole(
            platform=platform,
            contact=contact,
            role_name="PI",
            role_uri="https://cv/api/v1/roles/2/",
        )
        db.session.add_all([platform, contact, platform_contact_role])
        db.session.commit()

        mapper = mappers.B2InstPlatformMapper()
        result = mapper.to_draft_post(
            platform,
            community="A",
            open_access=True,
            base_landing_page=self.landing_page,
            schema_version="1.0.0",
        )

        expected = schemas.B2InstDraftPost(
            community="A",
            open_access=True,
            Name="CR1000 - Campbell Scientific - CR 1000",
            Description="The CR 1000",
            Owner=[
                schemas.B2InstOwner(
                    ownerName=":unav",
                    ownerContact=None,
                    ownerIdentifier=None,
                    ownerIdentifierType=None,
                )
            ],
            InstrumentType=[
                schemas.B2InstInstrumentType(
                    instrumentTypeName="Logger",
                    instrumentTypeIdentifier=None,
                    instrumentTypeIdentifierType=None,
                )
            ],
            LandingPage=f"{self.landing_page}/platforms/{platform.id}",
            Manufacturer=[
                schemas.B2InstManufacturer(
                    manufacturerName="Campbell Scientific",
                    manufacturerIdentifier=None,
                    manufacturerIdentifierType=None,
                )
            ],
            Model=schemas.B2InstModel(modelName="CR 1000"),
            MeasuredVariable=[],
            Date=[],
            AlternateIdentifier=[
                schemas.B2InstAlternateIdentifier(
                    alternateIdentifier=f"{self.landing_page}/platforms/{platform.id}",
                    alternateIdentifierType="Other",
                    alternateIdentifierName="URL",
                ),
            ],
            SchemaVersion="1.0.0",
        )

        self.assertEqual(result, expected)

    def test_to_draft_inactive_contact(self):
        """Ensure we list only active contacts."""
        platform = Platform(
            short_name="CR1000",
            description="The CR 1000",
            manufacturer_name="Campbell Scientific",
            platform_type_name="Logger",
            model="CR 1000",
        )
        contact = Contact(
            given_name="A",
            family_name="B",
            email="ab@localhost",
            active=False,
            organization="LocalHost",
        )
        platform_contact_role = PlatformContactRole(
            platform=platform,
            contact=contact,
            role_name="Owner",
            role_uri="https://cv/api/v1/roles/1/",
        )
        db.session.add_all([platform, contact, platform_contact_role])
        db.session.commit()

        mapper = mappers.B2InstPlatformMapper()
        result = mapper.to_draft_post(
            platform,
            community="A",
            open_access=True,
            base_landing_page=self.landing_page,
            schema_version="1.0.0",
        )

        expected = schemas.B2InstDraftPost(
            community="A",
            open_access=True,
            Name="CR1000 - Campbell Scientific - CR 1000",
            Description="The CR 1000",
            Owner=[
                schemas.B2InstOwner(
                    ownerName=":unav",
                    ownerContact=None,
                    ownerIdentifier=None,
                    ownerIdentifierType=None,
                )
            ],
            InstrumentType=[
                schemas.B2InstInstrumentType(
                    instrumentTypeName="Logger",
                    instrumentTypeIdentifier=None,
                    instrumentTypeIdentifierType=None,
                )
            ],
            LandingPage=f"{self.landing_page}/platforms/{platform.id}",
            Manufacturer=[
                schemas.B2InstManufacturer(
                    manufacturerName="Campbell Scientific",
                    manufacturerIdentifier=None,
                    manufacturerIdentifierType=None,
                )
            ],
            Model=schemas.B2InstModel(modelName="CR 1000"),
            MeasuredVariable=[],
            Date=[],
            AlternateIdentifier=[
                schemas.B2InstAlternateIdentifier(
                    alternateIdentifier=f"{self.landing_page}/platforms/{platform.id}",
                    alternateIdentifierType="Other",
                    alternateIdentifierName="URL",
                ),
            ],
            SchemaVersion="1.0.0",
        )

        self.assertEqual(result, expected)


class TestB2InstConfigurationMapper(BaseTestCase):
    """Test class for the B2InstConfigurationMapper class."""

    landing_page = "https://sms.helmholtz.cloud/"

    def test_to_draft_post_minimal(self):
        """Ensure we can map a minimal set of data to b2inst."""
        configuration = Configuration(label="", description="")
        db.session.add(configuration)
        db.session.commit()

        mapper = mappers.B2InstConfigurationMapper()
        result = mapper.to_draft_post(
            configuration,
            community="A",
            open_access=True,
            base_landing_page=self.landing_page,
            schema_version="1.0.0",
        )

        expected = schemas.B2InstDraftPost(
            community="A",
            open_access=True,
            Name=":unas",
            Description="",
            Owner=[
                schemas.B2InstOwner(
                    ownerName=":unav",
                    ownerContact=None,
                    ownerIdentifier=None,
                    ownerIdentifierType=None,
                )
            ],
            InstrumentType=[],
            LandingPage=f"{self.landing_page}/configurations/{configuration.id}",
            Manufacturer=[
                schemas.B2InstManufacturer(
                    manufacturerName=":unav",
                    manufacturerIdentifier=None,
                    manufacturerIdentifierType=None,
                )
            ],
            Model=None,
            MeasuredVariable=[],
            Date=[],
            AlternateIdentifier=[
                schemas.B2InstAlternateIdentifier(
                    alternateIdentifier=f"{self.landing_page}/configurations/{configuration.id}",
                    alternateIdentifierType="Other",
                    alternateIdentifierName="URL",
                )
            ],
            SchemaVersion="1.0.0",
        )

        self.assertEqual(result, expected)

    def test_to_draft_post_large(self):
        """Ensure we can map a larger set of data to b2inst."""
        configuration = Configuration(
            label="Example configuration",
            description="example description",
            start_date=datetime.datetime(2022, 1, 1, 0, 0, 0, tzinfo=pytz.utc),
            end_date=datetime.datetime(2024, 1, 1, 0, 0, 0, tzinfo=pytz.utc),
        )
        contact1 = Contact(
            given_name="A",
            family_name="B",
            email="ab@localhost",
            orcid="1234-5678-9012-3456",
            organization="LocalHost",
        )
        contact2 = Contact(
            given_name="Z",
            family_name="B",
            email="zb@localhost",
            orcid="9234-5678-9012-3456",
            organization="LocalHost",
        )
        configuration_contact_role1 = ConfigurationContactRole(
            configuration=configuration,
            contact=contact1,
            role_name="Owner",
            role_uri="https://cv/api/v1/roles/1/",
        )
        configuration_contact_role2 = ConfigurationContactRole(
            configuration=configuration,
            contact=contact2,
            role_name="Owner",
            role_uri="https://cv/api/v1/roles/1/",
        )
        device = Device(
            short_name="Test device",
            device_type_name="Soil moisture sensor",
            device_type_uri="https://cv/api/v1/equipmenttypes/1/",
            manufacturer_name="TRUEBENER GmbH",
            manufacturer_uri="https://cv/api/v1/manufacturers/1/",
            model="SMT 100",
        )
        device_contact = Contact(
            given_name="C",
            family_name="B",
            email="cb@localhost",
            orcid="1234-5678-9012-5555",
            organization="LocalHost",
        )
        device_contact_role = DeviceContactRole(
            device=device,
            contact=device_contact,
            role_name="Owner",
            role_uri="https://cv/api/v1/roles/1/",
        )
        device_mount_action = DeviceMountAction(
            device=device,
            configuration=configuration,
            begin_contact=device_contact,
            begin_date=datetime.datetime(2023, 1, 1, 0, 0, 0, tzinfo=pytz.utc),
        )
        device_property = DeviceProperty(
            device=device,
            property_name="Soil moisture",
        )
        platform = Platform(
            short_name="CR1000",
            description="The CR 1000",
            manufacturer_name="Campbell Scientific",
            manufacturer_uri="https://cv/api/v1/manufacturers/2/",
            platform_type_name="Logger",
            platform_type_uri="https://cv/api/v1/equipmenttypes/2/",
            model="CR 1000",
            serial_number="123",
            inventory_number="345",
        )
        platform_contact_role = PlatformContactRole(
            platform=platform,
            contact=device_contact,
            role_name="Owner",
            role_uri="https://cv/api/v1/roles/1/",
        )
        platform_mount_action = PlatformMountAction(
            platform=platform,
            configuration=configuration,
            begin_contact=device_contact,
            begin_date=datetime.datetime(2023, 1, 1, 0, 0, 0, tzinfo=pytz.utc),
        )
        db.session.add_all(
            [
                configuration,
                configuration_contact_role1,
                configuration_contact_role2,
                contact1,
                contact2,
                device,
                device_contact,
                device_contact_role,
                device_mount_action,
                device_property,
                platform,
                platform_contact_role,
                platform_mount_action,
            ]
        )
        db.session.commit()

        mapper = mappers.B2InstConfigurationMapper()
        result = mapper.to_draft_post(
            configuration,
            community="A",
            open_access=True,
            base_landing_page=self.landing_page,
            schema_version="1.0.0",
        )

        expected = schemas.B2InstDraftPost(
            community="A",
            open_access=True,
            Name="Example configuration",
            Description="example description",
            Owner=[
                schemas.B2InstOwner(
                    ownerName="LocalHost",
                    ownerContact=None,
                    ownerIdentifier=None,
                    ownerIdentifierType=None,
                )
            ],
            InstrumentType=[
                schemas.B2InstInstrumentType(
                    instrumentTypeName="Logger",
                    instrumentTypeIdentifier="https://cv/api/v1/equipmenttypes/2/",
                    instrumentTypeIdentifierType="URL",
                ),
                schemas.B2InstInstrumentType(
                    instrumentTypeName="Soil moisture sensor",
                    instrumentTypeIdentifier="https://cv/api/v1/equipmenttypes/1/",
                    instrumentTypeIdentifierType="URL",
                ),
            ],
            LandingPage=f"{self.landing_page}/configurations/{configuration.id}",
            Manufacturer=[
                schemas.B2InstManufacturer(
                    manufacturerName="Campbell Scientific",
                    manufacturerIdentifier="https://cv/api/v1/manufacturers/2/",
                    manufacturerIdentifierType="URL",
                ),
                schemas.B2InstManufacturer(
                    manufacturerName="TRUEBENER GmbH",
                    manufacturerIdentifier="https://cv/api/v1/manufacturers/1/",
                    manufacturerIdentifierType="URL",
                ),
            ],
            Model=None,
            MeasuredVariable=["Soil moisture"],
            Date=[
                schemas.B2InstDate(
                    Date=configuration.start_date,
                    dateType="Commissioned",
                ),
                schemas.B2InstDate(
                    Date=configuration.end_date,
                    dateType="DeCommissioned",
                ),
            ],
            AlternateIdentifier=[
                schemas.B2InstAlternateIdentifier(
                    alternateIdentifier=f"{self.landing_page}/configurations/{configuration.id}",
                    alternateIdentifierType="Other",
                    alternateIdentifierName="URL",
                )
            ],
            SchemaVersion="1.0.0",
        )

        self.assertEqual(result, expected)

    def test_to_draft_different_contact_role(self):
        """Ensure we list only contacts as owners that have this role."""
        configuration = Configuration(label="", description="")
        contact = Contact(
            given_name="A",
            family_name="B",
            email="ab@localhost",
            orcid="1234-5678-9012-3456",
            organization="LocalHost",
        )
        configuration_contact_role = ConfigurationContactRole(
            configuration=configuration,
            contact=contact,
            role_name="PI",
            role_uri="https://cv/api/v1/roles/3/",
        )
        db.session.add_all(
            [
                configuration,
                contact,
                configuration_contact_role,
            ]
        )
        mapper = mappers.B2InstConfigurationMapper()
        result = mapper.to_draft_post(
            configuration,
            community="A",
            open_access=True,
            base_landing_page=self.landing_page,
            schema_version="1.0.0",
        )

        expected = schemas.B2InstDraftPost(
            community="A",
            open_access=True,
            Name=":unas",
            Description="",
            Owner=[
                schemas.B2InstOwner(
                    ownerName=":unav",
                    ownerContact=None,
                    ownerIdentifier=None,
                    ownerIdentifierType=None,
                )
            ],
            InstrumentType=[],
            LandingPage=f"{self.landing_page}/configurations/{configuration.id}",
            Manufacturer=[
                schemas.B2InstManufacturer(
                    manufacturerName=":unav",
                    manufacturerIdentifier=None,
                    manufacturerIdentifierType=None,
                )
            ],
            Model=None,
            MeasuredVariable=[],
            Date=[],
            AlternateIdentifier=[
                schemas.B2InstAlternateIdentifier(
                    alternateIdentifier=f"{self.landing_page}/configurations/{configuration.id}",
                    alternateIdentifierType="Other",
                    alternateIdentifierName="URL",
                )
            ],
            SchemaVersion="1.0.0",
        )

        self.assertEqual(result, expected)

    def test_to_draft_inactive_contact(self):
        """Ensure we list only active contacts."""
        configuration = Configuration(label="", description="")
        contact = Contact(
            given_name="A",
            family_name="B",
            email="ab@localhost",
            orcid="1234-5678-9012-3456",
            active=False,
            organization="LocalHost",
        )
        configuration_contact_role = ConfigurationContactRole(
            configuration=configuration,
            contact=contact,
            role_name="Owner",
            role_uri="https://cv/api/v1/roles/1/",
        )
        db.session.add_all(
            [
                configuration,
                contact,
                configuration_contact_role,
            ]
        )
        mapper = mappers.B2InstConfigurationMapper()
        result = mapper.to_draft_post(
            configuration,
            community="A",
            open_access=True,
            base_landing_page=self.landing_page,
            schema_version="1.0.0",
        )

        expected = schemas.B2InstDraftPost(
            community="A",
            open_access=True,
            Name=":unas",
            Description="",
            Owner=[
                schemas.B2InstOwner(
                    ownerName=":unav",
                    ownerContact=None,
                    ownerIdentifier=None,
                    ownerIdentifierType=None,
                )
            ],
            InstrumentType=[],
            LandingPage=f"{self.landing_page}/configurations/{configuration.id}",
            Manufacturer=[
                schemas.B2InstManufacturer(
                    manufacturerName=":unav",
                    manufacturerIdentifier=None,
                    manufacturerIdentifierType=None,
                )
            ],
            Model=None,
            MeasuredVariable=[],
            Date=[],
            AlternateIdentifier=[
                schemas.B2InstAlternateIdentifier(
                    alternateIdentifier=f"{self.landing_page}/configurations/{configuration.id}",
                    alternateIdentifierType="Other",
                    alternateIdentifierName="URL",
                )
            ],
            SchemaVersion="1.0.0",
        )

        self.assertEqual(result, expected)


class TestB2InstDraftMapper(TestCase):
    """Test class for the B2InstDraftMapper."""

    def test_to_json_patch(self):
        """Ensure we can convert it to a json patch structure."""
        draft = schemas.B2InstDraftPost(
            community="A",
            open_access=True,
            Name="Example configuration",
            Description="example description",
            Owner=[
                schemas.B2InstOwner(
                    ownerName="A B",
                    ownerContact="ab@localhost",
                    ownerIdentifier="https://orcid.org/1234-5678-9012-3456",
                    ownerIdentifierType="URN",
                )
            ],
            InstrumentType=[
                schemas.B2InstInstrumentType(
                    instrumentTypeName="Logger",
                    instrumentTypeIdentifier="https://cv/api/v1/equipmenttypes/2/",
                    instrumentTypeIdentifierType="URL",
                ),
                schemas.B2InstInstrumentType(
                    instrumentTypeName="Soil moisture sensor",
                    instrumentTypeIdentifier="https://cv/api/v1/equipmenttypes/1/",
                    instrumentTypeIdentifierType="URL",
                ),
            ],
            LandingPage="https://localhost/configurations/123",
            Manufacturer=[
                schemas.B2InstManufacturer(
                    manufacturerName="Campbell Scientific",
                    manufacturerIdentifier="https://cv/api/v1/manufacturers/2/",
                    manufacturerIdentifierType="URL",
                ),
                schemas.B2InstManufacturer(
                    manufacturerName="TRUEBENER GmbH",
                    manufacturerIdentifier="https://cv/api/v1/manufacturers/1/",
                    manufacturerIdentifierType="URL",
                ),
            ],
            Model=schemas.B2InstModel(modelName="CR 1000"),
            MeasuredVariable=["Soil moisture"],
            Date=[
                schemas.B2InstDate(
                    Date=datetime.datetime(2022, 1, 1, 0, 0, 0, tzinfo=pytz.utc),
                    dateType="Commissioned",
                ),
                schemas.B2InstDate(
                    Date=datetime.datetime(2024, 1, 1, 0, 0, 0, tzinfo=pytz.utc),
                    dateType="DeCommissioned",
                ),
            ],
            AlternateIdentifier=[
                schemas.B2InstAlternateIdentifier(
                    alternateIdentifier="https://localhost/configurations/123",
                    alternateIdentifierType="Other",
                    alternateIdentifierName="URL",
                )
            ],
            SchemaVersion="1.0.0",
        )
        expected = [
            {"op": "replace", "path": "/Name", "value": "Example configuration"},
            {
                "op": "replace",
                "path": "/Description",
                "value": "example description",
            },
            {
                "op": "replace",
                "path": "/Owner",
                "value": [
                    {
                        "ownerName": "A B",
                        "ownerContact": "ab@localhost",
                        "ownerIdentifier": {
                            "ownerIdentifierValue": "https://orcid.org/1234-5678-9012-3456",
                            "ownerIdentifierType": "URN",
                        },
                    }
                ],
            },
            {
                "op": "replace",
                "path": "/LandingPage",
                "value": "https://localhost/configurations/123",
            },
            {
                "op": "replace",
                "path": "/Manufacturer",
                "value": [
                    {
                        "manufacturerName": "Campbell Scientific",
                        "manufacturerIdentifier": {
                            "manufacturerIdentifierValue": "https://cv/api/v1/manufacturers/2/",
                            "manufacturerIdentifierType": "URL",
                        },
                    },
                    {
                        "manufacturerName": "TRUEBENER GmbH",
                        "manufacturerIdentifier": {
                            "manufacturerIdentifierValue": "https://cv/api/v1/manufacturers/1/",
                            "manufacturerIdentifierType": "URL",
                        },
                    },
                ],
            },
            {
                "op": "replace",
                "path": "/Date",
                "value": [
                    {
                        "Date": "2022-01-01T00:00:00+00:00",
                        "dateType": "Commissioned",
                    },
                    {
                        "Date": "2024-01-01T00:00:00+00:00",
                        "dateType": "DeCommissioned",
                    },
                ],
            },
            {
                "op": "replace",
                "path": "/AlternateIdentifier",
                "value": [
                    {
                        "alternateIdentifierValue": "https://localhost/configurations/123",
                        "alternateIdentifierType": "Other",
                        "alternateIdentifierName": "URL",
                    }
                ],
            },
            {
                "op": "replace",
                "path": "/InstrumentType",
                "value": [
                    {
                        "instrumentTypeName": "Logger",
                        "instrumentTypeIdentifier": {
                            "instrumentTypeIdentifierValue": "https://cv/api/v1/equipmenttypes/2/",
                            "instrumentTypeIdentifierType": "URL",
                        },
                    },
                    {
                        "instrumentTypeName": "Soil moisture sensor",
                        "instrumentTypeIdentifier": {
                            "instrumentTypeIdentifierValue": "https://cv/api/v1/equipmenttypes/1/",
                            "instrumentTypeIdentifierType": "URL",
                        },
                    },
                ],
            },
            {
                "op": "replace",
                "path": "/Model",
                "value": {
                    "modelName": "CR 1000",
                },
            },
            {
                "op": "replace",
                "path": "/MeasuredVariable",
                "value": ["Soil moisture"],
            },
        ]

        mapper = mappers.B2InstDraftMapper()
        existing = {
            "MeasuredVariable": ["ab"],
            "Model": "xzy",
            "InstrumentType": [{"instrumentTypeName": "xxx"}],
        }
        result = mapper.to_json_patch(draft, existing)

        self.assertEqual(expected, result)

    def test_to_json_patch_adding(self):
        """Ensure we can add entries with the json patch structure."""
        draft = schemas.B2InstDraftPost(
            community="A",
            open_access=True,
            Name="Example configuration",
            Description="example description",
            Owner=[
                schemas.B2InstOwner(
                    ownerName="A B",
                    ownerContact="ab@localhost",
                    ownerIdentifier="https://orcid.org/1234-5678-9012-3456",
                    ownerIdentifierType="URN",
                )
            ],
            InstrumentType=[
                schemas.B2InstInstrumentType(
                    instrumentTypeName="Logger",
                    instrumentTypeIdentifier="https://cv/api/v1/equipmenttypes/2/",
                    instrumentTypeIdentifierType="URL",
                ),
                schemas.B2InstInstrumentType(
                    instrumentTypeName="Soil moisture sensor",
                    instrumentTypeIdentifier="https://cv/api/v1/equipmenttypes/1/",
                    instrumentTypeIdentifierType="URL",
                ),
            ],
            LandingPage="https://localhost/configurations/123",
            Manufacturer=[
                schemas.B2InstManufacturer(
                    manufacturerName="Campbell Scientific",
                    manufacturerIdentifier="https://cv/api/v1/manufacturers/2/",
                    manufacturerIdentifierType="URL",
                ),
                schemas.B2InstManufacturer(
                    manufacturerName="TRUEBENER GmbH",
                    manufacturerIdentifier="https://cv/api/v1/manufacturers/1/",
                    manufacturerIdentifierType="URL",
                ),
            ],
            Model=schemas.B2InstModel(modelName="CR 1000"),
            MeasuredVariable=["Soil moisture"],
            Date=[
                schemas.B2InstDate(
                    Date=datetime.datetime(2022, 1, 1, 0, 0, 0, tzinfo=pytz.utc),
                    dateType="Commissioned",
                ),
                schemas.B2InstDate(
                    Date=datetime.datetime(2024, 1, 1, 0, 0, 0, tzinfo=pytz.utc),
                    dateType="DeCommissioned",
                ),
            ],
            AlternateIdentifier=[
                schemas.B2InstAlternateIdentifier(
                    alternateIdentifier="https://localhost/configurations/123",
                    alternateIdentifierType="Other",
                    alternateIdentifierName="URL",
                )
            ],
            SchemaVersion="1.0.0",
        )
        expected = [
            {"op": "replace", "path": "/Name", "value": "Example configuration"},
            {
                "op": "replace",
                "path": "/Description",
                "value": "example description",
            },
            {
                "op": "replace",
                "path": "/Owner",
                "value": [
                    {
                        "ownerName": "A B",
                        "ownerContact": "ab@localhost",
                        "ownerIdentifier": {
                            "ownerIdentifierValue": "https://orcid.org/1234-5678-9012-3456",
                            "ownerIdentifierType": "URN",
                        },
                    }
                ],
            },
            {
                "op": "replace",
                "path": "/LandingPage",
                "value": "https://localhost/configurations/123",
            },
            {
                "op": "replace",
                "path": "/Manufacturer",
                "value": [
                    {
                        "manufacturerName": "Campbell Scientific",
                        "manufacturerIdentifier": {
                            "manufacturerIdentifierValue": "https://cv/api/v1/manufacturers/2/",
                            "manufacturerIdentifierType": "URL",
                        },
                    },
                    {
                        "manufacturerName": "TRUEBENER GmbH",
                        "manufacturerIdentifier": {
                            "manufacturerIdentifierValue": "https://cv/api/v1/manufacturers/1/",
                            "manufacturerIdentifierType": "URL",
                        },
                    },
                ],
            },
            {
                "op": "replace",
                "path": "/Date",
                "value": [
                    {
                        "Date": "2022-01-01T00:00:00+00:00",
                        "dateType": "Commissioned",
                    },
                    {
                        "Date": "2024-01-01T00:00:00+00:00",
                        "dateType": "DeCommissioned",
                    },
                ],
            },
            {
                "op": "replace",
                "path": "/AlternateIdentifier",
                "value": [
                    {
                        "alternateIdentifierValue": "https://localhost/configurations/123",
                        "alternateIdentifierType": "Other",
                        "alternateIdentifierName": "URL",
                    }
                ],
            },
            {
                "op": "add",
                "path": "/InstrumentType",
                "value": [
                    {
                        "instrumentTypeName": "Logger",
                        "instrumentTypeIdentifier": {
                            "instrumentTypeIdentifierValue": "https://cv/api/v1/equipmenttypes/2/",
                            "instrumentTypeIdentifierType": "URL",
                        },
                    },
                    {
                        "instrumentTypeName": "Soil moisture sensor",
                        "instrumentTypeIdentifier": {
                            "instrumentTypeIdentifierValue": "https://cv/api/v1/equipmenttypes/1/",
                            "instrumentTypeIdentifierType": "URL",
                        },
                    },
                ],
            },
            {
                "op": "add",
                "path": "/Model",
                "value": {
                    "modelName": "CR 1000",
                },
            },
            {
                "op": "add",
                "path": "/MeasuredVariable",
                "value": ["Soil moisture"],
            },
        ]

        mapper = mappers.B2InstDraftMapper()
        existing = {}
        result = mapper.to_json_patch(draft, existing)

        self.assertEqual(expected, result)

    def test_to_json_patch_removing(self):
        """Ensure we can remove entries with the json patch structure."""
        draft = schemas.B2InstDraftPost(
            community="A",
            open_access=True,
            Name="Example configuration",
            Description="example description",
            Owner=[
                schemas.B2InstOwner(
                    ownerName="A B",
                    ownerContact="ab@localhost",
                    ownerIdentifier="https://orcid.org/1234-5678-9012-3456",
                    ownerIdentifierType="URN",
                )
            ],
            InstrumentType=[],
            LandingPage="https://localhost/configurations/123",
            Manufacturer=[
                schemas.B2InstManufacturer(
                    manufacturerName="Campbell Scientific",
                    manufacturerIdentifier="https://cv/api/v1/manufacturers/2/",
                    manufacturerIdentifierType="URL",
                ),
                schemas.B2InstManufacturer(
                    manufacturerName="TRUEBENER GmbH",
                    manufacturerIdentifier="https://cv/api/v1/manufacturers/1/",
                    manufacturerIdentifierType="URL",
                ),
            ],
            Model=None,
            MeasuredVariable=[],
            Date=[
                schemas.B2InstDate(
                    Date=datetime.datetime(2022, 1, 1, 0, 0, 0, tzinfo=pytz.utc),
                    dateType="Commissioned",
                ),
                schemas.B2InstDate(
                    Date=datetime.datetime(2024, 1, 1, 0, 0, 0, tzinfo=pytz.utc),
                    dateType="DeCommissioned",
                ),
            ],
            AlternateIdentifier=[
                schemas.B2InstAlternateIdentifier(
                    alternateIdentifier="https://localhost/configurations/123",
                    alternateIdentifierType="Other",
                    alternateIdentifierName="URL",
                )
            ],
            SchemaVersion="1.0.0",
        )
        expected = [
            {"op": "replace", "path": "/Name", "value": "Example configuration"},
            {
                "op": "replace",
                "path": "/Description",
                "value": "example description",
            },
            {
                "op": "replace",
                "path": "/Owner",
                "value": [
                    {
                        "ownerName": "A B",
                        "ownerContact": "ab@localhost",
                        "ownerIdentifier": {
                            "ownerIdentifierValue": "https://orcid.org/1234-5678-9012-3456",
                            "ownerIdentifierType": "URN",
                        },
                    }
                ],
            },
            {
                "op": "replace",
                "path": "/LandingPage",
                "value": "https://localhost/configurations/123",
            },
            {
                "op": "replace",
                "path": "/Manufacturer",
                "value": [
                    {
                        "manufacturerName": "Campbell Scientific",
                        "manufacturerIdentifier": {
                            "manufacturerIdentifierValue": "https://cv/api/v1/manufacturers/2/",
                            "manufacturerIdentifierType": "URL",
                        },
                    },
                    {
                        "manufacturerName": "TRUEBENER GmbH",
                        "manufacturerIdentifier": {
                            "manufacturerIdentifierValue": "https://cv/api/v1/manufacturers/1/",
                            "manufacturerIdentifierType": "URL",
                        },
                    },
                ],
            },
            {
                "op": "replace",
                "path": "/Date",
                "value": [
                    {
                        "Date": "2022-01-01T00:00:00+00:00",
                        "dateType": "Commissioned",
                    },
                    {
                        "Date": "2024-01-01T00:00:00+00:00",
                        "dateType": "DeCommissioned",
                    },
                ],
            },
            {
                "op": "replace",
                "path": "/AlternateIdentifier",
                "value": [
                    {
                        "alternateIdentifierValue": "https://localhost/configurations/123",
                        "alternateIdentifierType": "Other",
                        "alternateIdentifierName": "URL",
                    }
                ],
            },
            {
                "op": "remove",
                "path": "/InstrumentType",
            },
            {
                "op": "remove",
                "path": "/Model",
            },
            {
                "op": "remove",
                "path": "/MeasuredVariable",
            },
        ]

        mapper = mappers.B2InstDraftMapper()
        existing = {
            "MeasuredVariable": ["ab"],
            "Model": "xzy",
            "InstrumentType": [{"instrumentTypeName": "xxx"}],
        }
        result = mapper.to_json_patch(draft, existing)

        self.assertEqual(expected, result)
