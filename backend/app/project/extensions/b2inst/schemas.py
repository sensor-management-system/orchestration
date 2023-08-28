# SPDX-FileCopyrightText: 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Schema classes to handle b2inst data."""

import dataclasses
import datetime
import typing


@dataclasses.dataclass(eq=True, frozen=True)
class B2InstOwner:
    """Owner schema for b2inst."""

    ownerName: str
    ownerContact: typing.Optional[str]
    ownerIdentifier: typing.Optional[str]
    ownerIdentifierType: typing.Optional[str]

    def dict(self):
        """Transform to a python dictionary."""
        result = {
            "ownerName": self.ownerName,
            "ownerContact": self.ownerContact,
        }
        if self.ownerIdentifierType and self.ownerIdentifier:
            # Yes it is currently named with the underscore.
            # And we can only add those to the payload if
            # we have at least the identifierType.
            result["owner_identifier"] = {
                "ownerIdentifierType": self.ownerIdentifierType,
                "ownerIdentifier": self.ownerIdentifier,
            }
        return result


@dataclasses.dataclass(eq=True, frozen=True)
class B2InstInstrumentType:
    """Instrument type schema for b2inst."""

    instrumentTypeName: str
    instrumentTypeIdentifier: typing.Optional[str]
    instrumentTypeIdentifierType: typing.Optional[str]

    def dict(self):
        """Transform to a python dictionary."""
        result = {
            "instrumentTypeName": self.instrumentTypeName,
        }
        if self.instrumentTypeIdentifier and self.instrumentTypeIdentifierType:
            # If you are here & ask why we have extra types for manufacturer identifiers
            # and owner identifiers, but we don't do that for the instrument types
            # (and just put them in the schema for the InstrumentType itself),
            # then you may have an imagination about the "fun" to check how
            # b2inst works & to write this code.
            result["instrumentTypeIdentifier"] = self.instrumentTypeIdentifier
            result["instrumentTypeIdentifierType"] = self.instrumentTypeIdentifierType
        return result


@dataclasses.dataclass(eq=True, frozen=True)
class B2InstManufacturer:
    """Manufacturer schema for b2inst."""

    manufacturerName: str
    manufacturerIdentifier: typing.Optional[str]
    manufacturerIdentifierType: typing.Optional[str]

    def dict(self):
        """Transform to a python dictionary."""
        result = {
            "manufacturerName": self.manufacturerName,
        }
        if self.manufacturerIdentifier and self.manufacturerIdentifierType:
            # If you are like me, you would ask:
            #
            # > Why the hell is it 'modelIdentifier' for the manufacturer??
            # > What is wrong with you?
            # > As if the inconsistent naming with snake_case was not bad
            # > enough already, now also this?
            #
            # but unfortunally it is the way the schema on the b2inst is
            # specified.
            # I hope you don't feel as much pain as I did when writing it here.
            result["manufacturer_Identifier"] = {
                "modelIdentifier": self.manufacturerIdentifier,
                "modelIdentifierType": self.manufacturerIdentifierType,
            }
        return result


@dataclasses.dataclass(eq=True, frozen=True)
class B2InstModel:
    """Model schema for b2inst."""

    modelName: str

    def dict(self):
        """Transform to a python dictionary."""
        return {
            # There are also other fields possible for b2inst, but none
            # that we could fill from the sms (identifier, identifier type for the
            # model is not part of the sms data model).
            "modelName": self.modelName,
        }


@dataclasses.dataclass(eq=True, frozen=True)
class B2InstAlternateIdentifier:
    """Alternate identifier schema for b2inst."""

    AlternateIdentifier: str
    alternateIdentifierType: str
    alternateIdentifierName: typing.Optional[str]

    def dict(self):
        """Transform to a python dictionary."""
        result = {
            "AlternateIdentifier": self.AlternateIdentifier,
            "alternateIdentifierType": self.alternateIdentifierType,
        }
        if self.alternateIdentifierName:
            result["alternateIdentifierName"] = self.alternateIdentifierName
        return result


@dataclasses.dataclass(eq=True, frozen=True)
class B2InstDate:
    """Date schema for b2inst."""

    Date: datetime.datetime
    dateType: str

    def dict(self):
        """Transform to a python dictionary."""
        return {
            # They speak about dates, but they expect a datetime in iso 8601
            # format. A date object (without time) would not be sufficient
            # for b2inst.
            "Date": self.Date.isoformat(),
            # dateType is either Commissioned or DeCommissioned
            "dateType": self.dateType,
        }


@dataclasses.dataclass
class B2InstDraftPost:
    """Schema for a b2inst post request to create a draft."""

    community: str
    open_access: bool
    name: str
    Name: str
    Description: str
    Owner: typing.List[B2InstOwner]
    InstrumentTypes: typing.List[B2InstInstrumentType]
    LandingPage: str
    Manufacturers: typing.List[B2InstManufacturer]
    Models: typing.List[B2InstModel]
    MeasuredVariables: typing.List[str]
    Dates: typing.List[B2InstDate]
    AlternateIdentifiers: typing.List[B2InstAlternateIdentifier]
    schemaVersion: str

    def dict(self):
        """Transform to a python dictionary."""
        return {
            "community": self.community,
            "open_access": self.open_access,
            "name": self.name,
            "Name": self.Name,
            "Description": self.Description,
            "Owner": [o.dict() for o in self.Owner],
            "InstrumentTypes": [i.dict() for i in self.InstrumentTypes],
            "LandingPage": self.LandingPage,
            "Manufacturers": [m.dict() for m in self.Manufacturers],
            "Models": [m.dict() for m in self.Models],
            "MeasuredVariables": self.MeasuredVariables,
            "Dates": [d.dict() for d in self.Dates],
            "AlternateIdentifiers": [a.dict() for a in self.AlternateIdentifiers],
            "schemaVersion": self.schemaVersion,
        }
