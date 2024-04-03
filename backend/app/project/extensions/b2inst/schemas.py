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
        }
        if self.ownerContact:
            result["ownerContact"] = self.ownerContact
        if self.ownerIdentifierType and self.ownerIdentifier:
            result["ownerIdentifier"] = {
                "ownerIdentifierType": self.ownerIdentifierType,
                "ownerIdentifierValue": self.ownerIdentifier,
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
            result["instrumentTypeIdentifier"] = {
                "instrumentTypeIdentifierType": self.instrumentTypeIdentifierType,
                "instrumentTypeIdentifierValue": self.instrumentTypeIdentifier,
            }
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
            result["manufacturerIdentifier"] = {
                "manufacturerIdentifierValue": self.manufacturerIdentifier,
                "manufacturerIdentifierType": self.manufacturerIdentifierType,
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

    alternateIdentifier: str
    alternateIdentifierType: str
    alternateIdentifierName: typing.Optional[str]

    def dict(self):
        """Transform to a python dictionary."""
        result = {
            "alternateIdentifierValue": self.alternateIdentifier,
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
    Name: str
    Description: str
    Owner: typing.List[B2InstOwner]
    InstrumentType: typing.List[B2InstInstrumentType]
    LandingPage: str
    Manufacturer: typing.List[B2InstManufacturer]
    Model: typing.Optional[B2InstModel]
    MeasuredVariable: typing.List[str]
    Date: typing.List[B2InstDate]
    AlternateIdentifier: typing.List[B2InstAlternateIdentifier]
    SchemaVersion: str

    def dict(self):
        """Transform to a python dictionary."""
        result = {
            "community": self.community,
            "open_access": self.open_access,
            "Name": self.Name,
            "Description": self.Description,
            "Owner": [o.dict() for o in self.Owner],
            "LandingPage": self.LandingPage,
            "Manufacturer": [m.dict() for m in self.Manufacturer],
            "Date": [d.dict() for d in self.Date],
            "AlternateIdentifier": [a.dict() for a in self.AlternateIdentifier],
            "SchemaVersion": self.SchemaVersion,
        }
        # The following entries should not be included in the payload
        # if they are not set.
        # This affects lists - which have the strange minItems:1 setting
        # in the json schema (which I does not understand at all),
        # and there is the model which is an optional field (0 or 1) and
        # can't be set to None (don't ask my why not).
        if self.InstrumentType:
            result["InstrumentType"] = [i.dict() for i in self.InstrumentType]
        if self.Model:
            result["Model"] = self.Model.dict()
        if self.MeasuredVariable:
            result["MeasuredVariable"] = self.MeasuredVariable
        return result
