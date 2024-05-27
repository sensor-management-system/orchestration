# SPDX-FileCopyrightText: 2022 - 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Resources for the mounting availabilities."""

import dateutil.parser
from flask import g, request
from flask_rest_jsonapi import ResourceList
from marshmallow import Schema, fields
from sqlalchemy import and_

from ..helpers.date_time_range import DateTimeRange
from ..helpers.errors import BadRequestError, MethodNotAllowed, UnauthorizedError
from ..models import Device, DeviceMountAction, Platform, PlatformMountAction
from ..models.base_model import db


class AvailableObjectSchema(Schema):
    """Schema for an availability information."""

    class Meta:
        """Meta class for the schema."""

        ordered = True

    id = fields.Str()
    available = fields.Boolean()
    mount = fields.Str()
    configuration = fields.Str()
    begin_date = fields.DateTime()
    end_date = fields.DateTime()


class DeviceAvailabilities(ResourceList):
    """Returns True if devices are available for mouting in a certain time range."""

    def get(self, *args, **kwargs):
        """Return a list with availability information of devices for a time range."""
        if not g.user:
            raise UnauthorizedError("Authentication required.")
        if "ids" not in request.args.keys():
            raise BadRequestError("Parameter ids not provided.")
        # First we take the ids as we get them.
        # However, we also have to make sure that we don't show information about
        # private devices here. (Private devices are only visible for its owner,
        # and we can't mount them on configurations.)
        device_ids = [int(v) for v in request.args["ids"].split(",") if v != ""]
        devices = db.session.query(Device).filter(
            and_(Device.is_private.is_(False), Device.id.in_(device_ids))
        )
        device_ids = [x.id for x in devices]

        device_mounts = db.session.query(DeviceMountAction).filter(
            DeviceMountAction.device_id.in_(device_ids)
        )

        from_time_point, to_time_point = extract_time_range_from_request()

        payload = []
        device_ids_add_to_payload = []
        timerange = DateTimeRange(from_time_point, to_time_point)
        for device_mount in device_mounts:
            existing_range = DateTimeRange(
                device_mount.begin_date, device_mount.end_date
            )

            if timerange.overlaps_with(existing_range):

                element_payload = {
                    "id": device_mount.device.id,
                    "available": False,
                    "mount": device_mount.id,
                    "configuration": device_mount.configuration.id,
                    "begin_date": device_mount.begin_date,
                    "end_date": device_mount.end_date,
                }
                payload.append(element_payload)
                device_ids_add_to_payload.append(device_mount.device.id)

        add_an_element_if_id_not_in_list(device_ids, payload, device_ids_add_to_payload)

        schema = AvailableObjectSchema(
            many=True,
        )
        return schema.dump(payload)

    def post(self):
        """Don't allow the post request."""
        raise MethodNotAllowed("endpoint is readonly")


class PlatformAvailabilities(ResourceList):
    """Returns True if platforms are available for mounting in a certain time range."""

    def get(self, *args, **kwargs):
        """Return a list with availability information of platforms for a time range."""
        if not g.user:
            raise UnauthorizedError("Authentication required.")
        if "ids" not in request.args.keys():
            raise BadRequestError("Parameter ids not provided.")
        # First we take the ids as we get them.
        # However, we also have to make sure that we don't show information about
        # private platforms here. (Private platform are only visible for its owner,
        # and we can't mount them on configurations.)
        platform_ids = [int(v) for v in request.args["ids"].split(",") if v != ""]
        platforms = db.session.query(Platform).filter(
            and_(Platform.is_private.is_(False), Platform.id.in_(platform_ids))
        )
        platform_ids = [x.id for x in platforms]
        platform_mounts = db.session.query(PlatformMountAction).filter(
            PlatformMountAction.platform_id.in_(platform_ids)
        )

        from_time_point, to_time_point = extract_time_range_from_request()

        payload = []
        platform_ids_add_to_payload = []
        asked_timerange = DateTimeRange(from_time_point, to_time_point)
        for platform_mount in platform_mounts:
            existing_range = DateTimeRange(
                platform_mount.begin_date, platform_mount.end_date
            )

            if asked_timerange.overlaps_with(existing_range):

                element_payload = {
                    "id": platform_mount.platform.id,
                    "available": False,
                    "mount": platform_mount.id,
                    "configuration": platform_mount.configuration.id,
                    "begin_date": platform_mount.begin_date,
                    "end_date": platform_mount.end_date,
                }
                payload.append(element_payload)
                platform_ids_add_to_payload.append(platform_mount.platform.id)

        add_an_element_if_id_not_in_list(
            platform_ids, payload, platform_ids_add_to_payload
        )
        schema = AvailableObjectSchema(
            many=True,
        )
        return schema.dump(payload)

    def post(self):
        """Don't allow the post request."""
        raise MethodNotAllowed("endpoint is readonly")


def extract_time_range_from_request():
    """
    Extract from and to for datetime interval from request.

    Also parse them to datetime objects.

    :return two datetime object: from_time_point and to_time_point
    """
    if "from" not in request.args.keys():
        raise BadRequestError("time-point parameters (from and to) are required")
    from_time_point_str = request.args["from"]
    to_time_point_str = None
    if "to" in request.args.keys():
        to_time_point_str = request.args["to"]
    try:
        from_time_point = dateutil.parser.parse(from_time_point_str)
        if to_time_point_str:
            to_time_point = dateutil.parser.parse(to_time_point_str)
        else:
            to_time_point = None
    except dateutil.parser.ParserError:
        raise BadRequestError("time-point must be ISO 8601")
    return from_time_point, to_time_point


def add_an_element_if_id_not_in_list(ids, payload, platform_ids_add_to_payload):
    """
    Add an entry as available if it is listed as unavailable before.

    :param ids: a list of ids.
    :param payload: the result list.
    :param platform_ids_add_to_payload: list of unavailable element.
    """
    for id_ in ids:
        if id_ not in platform_ids_add_to_payload:
            element_payload = {"id": id_, "available": True}
            payload.append(element_payload)
