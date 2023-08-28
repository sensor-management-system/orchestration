# SPDX-FileCopyrightText: 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Mapper for the b2inst interaction."""

import itertools

from sqlalchemy import and_

from ...api.models import (
    ConfigurationContactRole,
    Contact,
    DeviceContactRole,
    DeviceMountAction,
    PlatformContactRole,
    PlatformMountAction,
)
from ...api.models.base_model import db
from . import schemas


class B2InstDeviceMapper:
    """Mapper to handle device data."""

    def to_draft_post(
        self, device, community, open_access, base_landing_page, schema_version
    ):
        """Map to a b2inst post to create a draft."""
        landing_page = f"{base_landing_page}/devices/{device.id}"
        return schemas.B2InstDraftPost(
            community=community,
            open_access=open_access,
            name=self._device_name(device),
            Name=self._device_name(device),
            Description=device.description,
            Owner=self._device_owners(device),
            InstrumentTypes=self._device_instrument_types(device),
            LandingPage=landing_page,
            Manufacturers=self._device_manufacturers(device),
            Models=self._device_models(device),
            MeasuredVariables=self._device_measured_variables(device),
            Dates=[],
            AlternateIdentifiers=self._device_alternate_identifiers(
                device, landing_page
            ),
            schemaVersion=schema_version,
        )

    def _device_name(self, device):
        parts = [device.short_name]
        for x in [device.manufacturer_name, device.model, device.serial_number]:
            if x:
                parts.append(x)
        return " - ".join(parts)

    def _device_owners(self, device):
        owners = []
        for contact_role in (
            db.session.query(DeviceContactRole)
            .join(Contact)
            .filter(
                and_(
                    DeviceContactRole.device_id == device.id,
                    DeviceContactRole.role_name == "Owner",
                    Contact.active.is_(True),
                )
            )
        ):
            contact = contact_role.contact
            name = f"{contact.given_name} {contact.family_name}"
            owner_identifier = None
            owner_identifier_type = None
            if contact.orcid:
                owner_identifier = f"https://orcid.org/{contact.orcid}"
                owner_identifier_type = "URL"
            owners.append(
                schemas.B2InstOwner(
                    ownerName=name,
                    ownerContact=contact.email,
                    ownerIdentifier=owner_identifier,
                    ownerIdentifierType=owner_identifier_type,
                )
            )
        return owners

    def _device_instrument_types(self, device):
        instrument_types = []
        if device.device_type_name:
            instrument_type_identifier = None
            instrument_type_identifier_type = None
            if device.device_type_uri:
                instrument_type_identifier = device.device_type_uri
                instrument_type_identifier_type = "URL"
            instrument_types.append(
                schemas.B2InstInstrumentType(
                    instrumentTypeName=device.device_type_name,
                    instrumentTypeIdentifier=instrument_type_identifier,
                    instrumentTypeIdentifierType=instrument_type_identifier_type,
                )
            )
        return instrument_types

    def _device_manufacturers(self, device):
        manufacturers = []
        if device.manufacturer_name:
            manufacturer_identifier = None
            manufacturer_identifier_type = None
            if device.manufacturer_uri:
                manufacturer_identifier = device.manufacturer_uri
                manufacturer_identifier_type = "URL"
            manufacturers.append(
                schemas.B2InstManufacturer(
                    manufacturerName=device.manufacturer_name,
                    manufacturerIdentifier=manufacturer_identifier,
                    manufacturerIdentifierType=manufacturer_identifier_type,
                )
            )
        return manufacturers

    def _device_models(self, device):
        models = []
        if device.model:
            models.append(schemas.B2InstModel(modelName=device.model))
        return models

    def _device_alternate_identifiers(self, device, landing_page):
        result = []
        if device.serial_number:
            result.append(
                schemas.B2InstAlternateIdentifier(
                    AlternateIdentifier=device.serial_number,
                    alternateIdentifierType="SerialNumber",
                    alternateIdentifierName=None,
                )
            )
        if device.inventory_number:
            result.append(
                schemas.B2InstAlternateIdentifier(
                    AlternateIdentifier=device.inventory_number,
                    alternateIdentifierType="InventoryNumber",
                    alternateIdentifierName=None,
                )
            )
        # You may ask why to include that while we still ahve the landing page
        # as an extra element.
        # The point is a small problem in b2inst, that doesn't allow us to patch
        # the alternateIdentifiers if we don't include them in the first place.
        # So if we put the landing page here (which we always have) then we don't
        # run into trouble when patching the entry later (when we have serial number
        # or inventory number).
        result.append(
            schemas.B2InstAlternateIdentifier(
                AlternateIdentifier=landing_page,
                alternateIdentifierType="Other",
                alternateIdentifierName="URL",
            )
        )
        return result

    def _device_measured_variables(self, device):
        variables = []
        for dp in device.device_properties:
            if dp.property_name:
                variables.append(dp.property_name)
        return variables


class B2InstPlatformMapper:
    """Mapper to handle platform data."""

    def to_draft_post(
        self, platform, community, open_access, base_landing_page, schema_version
    ):
        """Map to a b2inst post to create a draft."""
        landing_page = f"{base_landing_page}/platforms/{platform.id}"
        return schemas.B2InstDraftPost(
            community=community,
            open_access=open_access,
            name=self._platform_name(platform),
            Name=self._platform_name(platform),
            Description=platform.description,
            Owner=self._platform_owners(platform),
            InstrumentTypes=self._platform_instrument_types(platform),
            LandingPage=landing_page,
            Manufacturers=self._platform_manufacturers(platform),
            Models=self._platform_models(platform),
            AlternateIdentifiers=self._platform_alternate_identifiers(
                platform, landing_page
            ),
            MeasuredVariables=[],
            Dates=[],
            schemaVersion=schema_version,
        )

    def _platform_name(self, platform):
        parts = [platform.short_name]
        for x in [platform.manufacturer_name, platform.model, platform.serial_number]:
            if x:
                parts.append(x)
        return " - ".join(parts)

    def _platform_owners(self, platform):
        owners = []
        for contact_role in (
            db.session.query(PlatformContactRole)
            .join(Contact)
            .filter(
                and_(
                    PlatformContactRole.platform_id == platform.id,
                    PlatformContactRole.role_name == "Owner",
                    Contact.active.is_(True),
                )
            )
        ):
            contact = contact_role.contact
            name = f"{contact.given_name} {contact.family_name}"
            owner_identifier = None
            owner_identifier_type = None
            if contact.orcid:
                owner_identifier = f"https://orcid.org/{contact.orcid}"
                owner_identifier_type = "URL"
            owners.append(
                schemas.B2InstOwner(
                    ownerName=name,
                    ownerContact=contact.email,
                    ownerIdentifier=owner_identifier,
                    ownerIdentifierType=owner_identifier_type,
                )
            )
        return owners

    def _platform_instrument_types(self, platform):
        instrument_types = []
        if platform.platform_type_name:
            instrument_type_identifier = None
            instrument_type_identifier_type = None
            if platform.platform_type_uri:
                instrument_type_identifier = platform.platform_type_uri
                instrument_type_identifier_type = "URL"
            instrument_types.append(
                schemas.B2InstInstrumentType(
                    instrumentTypeName=platform.platform_type_name,
                    instrumentTypeIdentifier=instrument_type_identifier,
                    instrumentTypeIdentifierType=instrument_type_identifier_type,
                )
            )
        return instrument_types

    def _platform_manufacturers(self, platform):
        manufacturers = []
        if platform.manufacturer_name:
            manufacturer_identifier = None
            manufacturer_identifier_type = None
            if platform.manufacturer_uri:
                manufacturer_identifier = platform.manufacturer_uri
                manufacturer_identifier_type = "URL"
            manufacturers.append(
                schemas.B2InstManufacturer(
                    manufacturerName=platform.manufacturer_name,
                    manufacturerIdentifier=manufacturer_identifier,
                    manufacturerIdentifierType=manufacturer_identifier_type,
                )
            )
        return manufacturers

    def _platform_models(self, platform):
        models = []
        if platform.model:
            models.append(schemas.B2InstModel(modelName=platform.model))
        return models

    def _platform_alternate_identifiers(self, platform, landing_page):
        result = []
        if platform.serial_number:
            result.append(
                schemas.B2InstAlternateIdentifier(
                    AlternateIdentifier=platform.serial_number,
                    alternateIdentifierType="SerialNumber",
                    alternateIdentifierName=None,
                )
            )
        if platform.inventory_number:
            result.append(
                schemas.B2InstAlternateIdentifier(
                    AlternateIdentifier=platform.inventory_number,
                    alternateIdentifierType="InventoryNumber",
                    alternateIdentifierName=None,
                )
            )
        result.append(
            schemas.B2InstAlternateIdentifier(
                AlternateIdentifier=landing_page,
                alternateIdentifierType="Other",
                alternateIdentifierName="URL",
            )
        )
        return result


class B2InstConfigurationMapper:
    """
    Mapper to handle configuration data.

    Integrates data from mounted devices & platforms.
    """

    def __init__(self):
        """Init the mapper with sub mappers."""
        self._device_mapper = B2InstDeviceMapper()
        self._platform_mapper = B2InstPlatformMapper()

    def to_draft_post(
        self, configuration, community, open_access, base_landing_page, schema_version
    ):
        """Map to a b2inst post to create a draft."""
        device_data = []
        platform_data = []

        for device_mount in db.session.query(DeviceMountAction).filter(
            DeviceMountAction.configuration_id == configuration.id
        ):
            device = device_mount.device
            device_data.append(
                self._device_mapper.to_draft_post(
                    device,
                    community=community,
                    open_access=open_access,
                    base_landing_page=base_landing_page,
                    schema_version=schema_version,
                )
            )
        for platform_mount in db.session.query(PlatformMountAction).filter(
            PlatformMountAction.configuration_id == configuration.id
        ):
            platform = platform_mount.platform
            platform_data.append(
                self._platform_mapper.to_draft_post(
                    platform,
                    community=community,
                    open_access=open_access,
                    base_landing_page=base_landing_page,
                    schema_version=schema_version,
                )
            )

        instrument_types = set()
        manufacturers = set()
        measured_variables = set()
        models = set()
        measured_variables = set()
        for data in itertools.chain(device_data, platform_data):
            for instrument_type in data.InstrumentTypes:
                instrument_types.add(instrument_type)
            for manufacturer in data.Manufacturers:
                manufacturers.add(manufacturer)
            for model in data.Models:
                models.add(model)
            for measured_variable in data.MeasuredVariables:
                measured_variables.add(measured_variable)

        dates = []
        if configuration.start_date:
            dates.append(
                schemas.B2InstDate(
                    Date=configuration.start_date, dateType="Commissioned"
                )
            )
        if configuration.end_date:
            dates.append(
                schemas.B2InstDate(
                    Date=configuration.end_date, dateType="DeCommissioned"
                )
            )

        landing_page = f"{base_landing_page}/configurations/{configuration.id}"
        return schemas.B2InstDraftPost(
            community=community,
            open_access=open_access,
            name=configuration.label,
            Name=configuration.label,
            Description=configuration.description,
            Owner=self._configuration_owners(configuration),
            InstrumentTypes=sorted(
                instrument_types, key=lambda x: x.instrumentTypeName
            ),
            LandingPage=landing_page,
            Manufacturers=sorted(manufacturers, key=lambda x: x.manufacturerName),
            Models=sorted(models, key=lambda x: x.modelName),
            # We don't reuse the alternate identifiers of the platforms & devices here.
            AlternateIdentifiers=[
                schemas.B2InstAlternateIdentifier(
                    AlternateIdentifier=landing_page,
                    alternateIdentifierType="Other",
                    alternateIdentifierName="URL",
                )
            ],
            MeasuredVariables=sorted(measured_variables),
            Dates=dates,
            schemaVersion=schema_version,
        )

    def _configuration_owners(self, configuration):
        owners = []
        for contact_role in (
            db.session.query(ConfigurationContactRole)
            .join(Contact)
            .filter(
                and_(
                    ConfigurationContactRole.configuration_id == configuration.id,
                    ConfigurationContactRole.role_name == "Owner",
                    Contact.active.is_(True),
                )
            )
        ):
            contact = contact_role.contact
            name = f"{contact.given_name} {contact.family_name}"
            owner_identifier = None
            owner_identifier_type = None
            if contact.orcid:
                owner_identifier = f"https://orcid.org/{contact.orcid}"
                owner_identifier_type = "URL"
            owners.append(
                schemas.B2InstOwner(
                    ownerName=name,
                    ownerContact=contact.email,
                    ownerIdentifier=owner_identifier,
                    ownerIdentifierType=owner_identifier_type,
                )
            )
        return owners


class B2InstDraftMapper:
    """Mapper to work with b2inst draft post data."""

    def to_json_patch(self, draft):
        """Transform to a json patch request setting all the field that may changed."""
        return [
            {
                "op": "replace",
                "path": "/name",
                "value": draft.name,
            },
            {
                "op": "replace",
                "path": "/Name",
                "value": draft.Name,
            },
            {
                "op": "replace",
                "path": "/Description",
                "value": draft.Description,
            },
            {
                "op": "replace",
                "path": "/Owner",
                "value": [o.dict() for o in draft.Owner],
            },
            {
                "op": "replace",
                "path": "/InstrumentTypes",
                "value": [i.dict() for i in draft.InstrumentTypes],
            },
            {
                "op": "replace",
                "path": "/LandingPage",
                "value": draft.LandingPage,
            },
            {
                "op": "replace",
                "path": "/Manufacturers",
                "value": [m.dict() for m in draft.Manufacturers],
            },
            {
                "op": "replace",
                "path": "/Models",
                "value": [m.dict() for m in draft.Models],
            },
            {
                "op": "replace",
                "path": "/MeasuredVariables",
                "value": draft.MeasuredVariables,
            },
            {
                "op": "replace",
                "path": "/Dates",
                "value": [d.dict() for d in draft.Dates],
            },
            {
                "op": "replace",
                "path": "/AlternateIdentifiers",
                "value": [a.dict() for a in draft.AlternateIdentifiers],
            },
        ]
