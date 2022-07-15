"""PID resources.."""
from flask import g, request
from flask_rest_jsonapi import ResourceDetail
from sqlalchemy import and_

from .base_resource import add_pid
from ..helpers.errors import (
    BadRequestError,
    UnauthorizedError,
)
from ..models import (
    Device,
    Platform,
    DeviceContactRole,
    PlatformContactRole,
)
from ... import db
from ...extensions.instances import pid
from ...frj_csv_export.resource import ResourceList


class PidList(ResourceList):
    def get(self, *args, **kwargs):
        """List Pids, or search PIDS for a term in url.

        :example for list:
        http://vm04.pid.gwdg.de:8081/handles/21.T11998/
        0-TEST
        00-001M-0000-002E-A349-6
        00-1735-0000-0001-11C9-7
        00-1735-0000-0001-11CB-3
        00-1735-0000-0001-3066-D
        00-1735-0000-0001-306B-3
        00-1735-0000-0001-307F-8
        00-1735-0000-0001-3080-2
        00-1735-0000-0001-3081-F
        00-1735-0000-0001-3082-D
        00-1735-0000-0001-3083-B
        00-1735-0000-0001-3084-9
        00-1735-0000-0001-3085-7
        00-1735-0000-0001-3086-5
        00-1735-0000-0001-3087-3
        00-1735-0000-0001-3088-1

        :example for search:
        http://vm04.pid.gwdg.de:8081/handles/21.T11998/?URL=*localhost.localdomain*
        Response.txt ->
        0000-001C-2FAE-B-SMS
        0000-001C-2FAF-A
        01455944-00FF-11ED-BBC5-0242AC150006
        F884FA14-0110-11ED-8398-0242AC150006
        SMS-0000-001C-2FB1-6-TEST
        SMS-0000-001C-2FB2-5-TEST
        SMS-0000-001C-2FB3-4-TEST
        SMS-0000-001C-2FB4-3-TEST
        SMS-0000-001C-2FB5-2-TEST
        SMS-0000-001C-2FE7-A-STAGE-TEST

        """
        """List Pids, or search PIDS for a term in url."""
        if not g.user:
            raise UnauthorizedError("Authentication required.")
        limit = request.args["limit"] if "limit" in request.args.keys() else None
        page = request.args["page"] if "page" in request.args.keys() else None
        if "term" in request.args:
            term = request.args["term"]
            response = pid.search_after_a_pid(term, limit)
        else:
            response = pid.list_pids(limit, page)
        return response

    def post(self, *args, **kwargs):
        """Create a new PID"""
        if not g.user:
            raise UnauthorizedError("Authentication required.")
        if "url" not in request.args.keys():
            raise BadRequestError("No url.")
        url = request.args["url"]
        persistent_identifier = pid.create_a_new_pid(url)
        response = {"pid": persistent_identifier}
        return response


class PidDetail(ResourceDetail):
    def get(self, *args, **kwargs):
        """GEt PID information."""
        if not g.user:
            raise UnauthorizedError("Authentication required.")
        if "pid" not in kwargs.keys():
            raise BadRequestError("No pid.")
        source_object_pid = kwargs["pid"]
        response = pid.get_a_pid(source_object_pid)
        return response

    def patch(self, *args, **kwargs):
        """Update PID."""
        if not g.user:
            raise UnauthorizedError("Authentication required.")
        if "pid" not in kwargs.keys() or "url" not in request.args.keys():
            raise BadRequestError("No pid or url.")
        source_object_pid = kwargs["pid"]
        updated_url = request.args["url"]
        return pid.update_existing_pid(source_object_pid, updated_url)

    def delete(self, *args, **kwargs):
        """Delete a PID."""
        if not g.user:
            raise UnauthorizedError("Authentication required.")
        if "pid" not in kwargs.keys():
            raise BadRequestError("No pid.")
        source_object_pid = kwargs["pid"]
        return pid.delete(source_object_pid)


def make_instrument_data_from_instance(instrument_instance: dict) -> (list, object):
    """
    prepare the data toi be sent to the pid handler.
    The data is a list of dict, which has two attributes:
         - type: required: The data type defines the syntax and semantics of the data in its data field.
         - parsed_data: required: The syntax and semantics of parsed data are identified by the field.

    :param instrument_instance: a dictionary, which has the type of entity and its id.
    :return: a list of instrument data to be added as Metadata tp a PID.
    """
    if instrument_instance["type"] == "device":
        instrument = (
            db.session.query(Device).filter_by(id=instrument_instance["id"]).first()
        )
        # role = (
        #     db.session.query(DeviceContactRole)
        #     .filter(
        #         and_(
        #             DeviceContactRole.device_id == instrument_instance["id"],
        #             DeviceContactRole.role_name == "Owner",
        #         )
        #     )
        #     .first()
        # )
    elif instrument_instance["type"] == "platform":
        instrument = (
            db.session.query(Platform).filter_by(id=instrument_instance["id"]).first()
        )
        # role = (
        #     db.session.query(PlatformContactRole)
        #     .filter_by(platform_id=instrument_instance["id"], role_name="Owner")
        #     .first()
        # )
    else:
        raise BadRequestError("Type Not Implemented.")
    try:
        instrument_data = [
            {"type": "URL", "parsed_data": instrument_instance["source_uri"]},
            # {"type": "LandingPage", "parsed_data": instrument_instance["source_uri"]},
            # {"type": "Identifier", "parsed_data": str(instrument.id)},
            # {"type": "IdentifierType", "parsed_data": instrument.identifier_type},
            # {"type": "SchemaVersion", "parsed_data": instrument.schema_version},
            # {"type": "Name", "parsed_data": instrument.short_name},
            # {"type": "Owner", "parsed_data": role.contact.email},
            # {
            #     "type": "OwnerName",
            #     "parsed_data": f"{role.contact.given_name} {role.contact.family_name}",
            # },
            # {"type": "Manufacturer", "parsed_data": instrument.manufacturer_uri},
            # {
            #     "type": "Description",
            #     "parsed_data": instrument.description if hasattr(instrument, 'description') else None
            # },
            # {"type": "ManufacturerName", "parsed_data": instrument.manufacturer_name},
            # {"type": "Model", "parsed_data": instrument.model if hasattr(instrument, 'model') else None},
            # {"type": "Modelname", "parsed_data": instrument.modelname if hasattr(instrument, 'modelname') else None},
            # {
            #     "type": "AlternateIdentifier",
            #     "parsed_data": instrument.alternateidentifier if hasattr(instrument,'alternateidentifier') else None
            # },
            # {
            #     "type": "InstrumentType",
            #     "parsed_data": instrument.instrumenttype if hasattr(instrument, 'instrumenttype') else None
            # },
            # {
            #     "type": "InstrumentTypeName",
            #     "parsed_data": instrument.instrumenttypename if hasattr(instrument, 'instrumenttypename') else None
            # },
            # {
            #     "type": "MeasuredVariable",
            #     "parsed_data": instrument.measuredvariable if hasattr(instrument, "measuredvariable") else None
            # }
        ]
    except AttributeError as e:
        raise BadRequestError(repr(e))
    return instrument_data, instrument


def make_instrument_data_from_request(instrument_data: dict) -> list:
    """
    prepare the data to be sent to the pid handler.
    The data is a list of dict, which has two attributes:
         - type: required: The data type defines the syntax and semantics of the data in its data field.
         - parsed_data: required: The syntax and semantics of parsed data are identified by the field.

    :param instrument_data: a dictionary, which has the type of entity and its id.
    :return: a list of instrument data to be added as Metadata tp a PID.
    """
    try:
        instrument_data = [
            {"type": "URL", "parsed_data": instrument_data["source_object_url"]},
            # {
            #     "type": "LandingPage",
            #     "parsed_data": instrument_data["source_object_url"],
            # },
            # {"type": "Identifier", "parsed_data": str(instrument_data["id"])},
            # {
            #     "type": "IdentifierType",
            #     "parsed_data": instrument_data["identifier_type"],
            # },
            # {
            #     "type": "SchemaVersion",
            #     "parsed_data": instrument_data["schema_version"],
            # },
            # {"type": "Name", "parsed_data": instrument_data["short_name"]},
            # {"type": "Owner", "parsed_data": instrument_data["contact_email"]},
            # {
            #     "type": "OwnerName",
            #     "parsed_data": f"{instrument_data['given_name']} {instrument_data['family_name']}",
            # },
            # {
            #     "type": "Manufacturer",
            #     "parsed_data": instrument_data["manufacturer_uri"],
            # },
            # {
            #     "type": "Description",
            #     "parsed_data": instrument_data["description"] if hasattr(instrument_data, 'description') else None
            # },
            # {
            #     "type": "ManufacturerName",
            #     "parsed_data": instrument_data["manufacturer_name"],
            # },
            # {"type": "Model", "parsed_data": instrument_data["model"] if hasattr(instrument_data, 'model') else None},
            # {
            #     "type": "Modelname",
            #     "parsed_data": instrument_data["modelname"] if hasattr(instrument_data, 'modelname') else None
            # },
            # {
            #     "type": "AlternateIdentifier",
            #     "parsed_data":
            #       instrument_data["alternateidentifier"] if hasattr(instrument_data, 'alternateidentifier')
            #     else None
            # },
            # {
            #     "type": "InstrumentType",
            #     "parsed_data": instrument_data["instrumenttype"] if hasattr(instrument_data, 'instrumenttype')
            #     else None
            # },
            # {
            #     "type": "InstrumentTypeName",
            #     "parsed_data": instrument_data["instrumenttypename"] if hasattr(instrument_data, 'instrumenttypename')
            #     else None
            # },
            # {
            #     "type": "MeasuredVariable",
            #     "parsed_data": instrument_data["measuredvariable"] if hasattr(instrument_data, "measuredvariable")
            #     else None
            # }
        ]
    except KeyError as e:
        raise BadRequestError(repr(e))
    return instrument_data
        return pid.delete_a_pid(source_object_pid)
