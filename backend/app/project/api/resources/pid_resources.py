# SPDX-FileCopyrightText: 2022 - 2023
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Florian Gransee <florian.gransee@ufz.de>
# - Luca Johannes Nendel <Luca-Johannes.Nendel@ufz.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""PID resources."""
import datetime

from flask import g, request
from flask_rest_jsonapi import ResourceDetail, ResourceList

from ... import db
from ...extensions.instances import pidinst
from ..helpers.errors import (
    BadRequestError,
    ConflictError,
    ForbiddenError,
    MethodNotAllowed,
    NotFoundError,
    UnauthorizedError,
)
from ..models import Configuration, Device, Platform, Site
from ..permissions.rules import can_edit


class PidList(ResourceList):
    """List resource for pid handling."""

    def get(self, *args, **kwargs):
        """Don't allow get requests."""
        raise MethodNotAllowed("Get is not allowed.")

    def post(self, *args, **kwargs):
        """
        Create a new PID with instrument data or with instrument instance.

        Example: of the Instrument instance:

        {
            "instrument_instance":{
                "type":"device",
                "id": "1",
            }
        }
        """
        if not g.user:
            raise UnauthorizedError("Authentication required.")
        if "instrument_instance" in request.get_json():
            instrument_instance = request.get_json()["instrument_instance"]
            instrument = get_instrument(instrument_instance)
        else:
            raise BadRequestError("No instrument_instance.")

        if not instrument:
            raise NotFoundError("Instrument not found.")

        if not can_edit(instrument):
            raise ForbiddenError("No permissions to edit the instrument.")

        if instrument.persistent_identifier:
            raise ConflictError("Instrument has already a persistent identifier.")
        if getattr(instrument, "is_private", False):
            raise ConflictError("PIDs can't be generated for private instruments.")

        persistent_identifier = pidinst.create_pid(instrument)

        instrument.persistent_identifier = persistent_identifier
        instrument.update_description = "create;persistent identifier"
        instrument.updated_at = datetime.datetime.utcnow()
        instrument.updated_by = g.user

        db.session.add(instrument)
        db.session.commit()

        response = {"pid": persistent_identifier}
        return response


class PidDetail(ResourceDetail):
    """Detail resource for PID handling."""

    def get(self, *args, **kwargs):
        """Don't allow get requests."""
        raise MethodNotAllowed("Get is not allowed.")

    def patch(self, *args, **kwargs):
        """Don't allow manual change of the pid data."""
        raise MethodNotAllowed("Patch is not allowed.")

    def delete(self, *args, **kwargs):
        """Don't allow to manual delete the pid data."""
        raise MethodNotAllowed("Delete is not allowed.")


def get_instrument(instrument_instance: dict):
    """
    Load the instrument for the pid from the database.

    :param instrument_instance: a dictionary, which has the type of entity and its id.
    :return: the model instance.
    """
    if instrument_instance.get("type") == "device":
        instrument = (
            db.session.query(Device).filter_by(id=instrument_instance.get("id")).first()
        )
        return instrument
    elif instrument_instance.get("type") == "platform":
        instrument = (
            db.session.query(Platform)
            .filter_by(id=instrument_instance.get("id"))
            .first()
        )
        return instrument
    elif instrument_instance.get("type") == "configuration":
        instrument = (
            db.session.query(Configuration)
            .filter_by(id=instrument_instance.get("id"))
            .first()
        )
        return instrument
    elif instrument_instance.get("type") == "site":
        instrument = (
            db.session.query(Site).filter_by(id=instrument_instance.get("id")).first()
        )
        return instrument
    else:
        raise BadRequestError("Type not implemented.")
