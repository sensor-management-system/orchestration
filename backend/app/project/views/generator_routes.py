# SPDX-FileCopyrightText: 2026
# - Nils Brinckmann <nils.brinckmann@gfz.de>
# - GFZ - Helmholtz Centre for Geosciences (GFZ, https://www.gfz.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Views to generate something."""

import random
import string

from flask import Blueprint, g, request

from ..api.models import Device, Organization, Platform
from ..api.models.base_model import db
from ..config import env

generator_routes = Blueprint(
    "generator_routes", __name__, url_prefix=env("URL_PREFIX", "/rdm/svm-api/v1")
)


@generator_routes.route("/controller/generators/serial-number", methods=["GET"])
def generate_serial_number():
    """Generate a artificial serial number.

    Used for the cases where devices don't have a serial number at all
    or where it is not acessible.
    """
    # The idea is to have a similar system to the car plates (Nummerschild) as in Germany.
    # We start with a prefix that shows some location (or institute in our case).
    # Then we have one or two chars.
    # And then 1 till 4 numbers.
    # Something like
    # GFZ-AB-1234
    # In order to keep the space large, I would extend middle part to 4 chars
    # For the car plates it is the way that the first part is some kind of a
    # registred namespace.
    # So we can do the same thing here & introduce a lookup table for the organization.
    fallback_organization_part = "SMS"
    organization_part = fallback_organization_part

    query_organization_part = request.args.get("organization_part", None)
    if query_organization_part is not None:
        organization_part = query_organization_part[:4]
    elif g.user:
        organization_name = g.user.contact.organization
        if organization_name:
            organization = (
                db.session.query(Organization).filter_by(name=organization_name).first()
            )
            if organization and organization.abbreviation:
                organization_part = organization.abbreviation

    r = random.Random()
    seed = request.args.get("seed", None)
    if seed is not None:
        r.seed(seed)

    new_serial_number = None
    while new_serial_number is None:
        chars = generate_char_part(r, 2, 4)
        numbers = generate_number_part(r, 2, 4)

        new_serial_number_candidate = "-".join([organization_part, chars, numbers])

        existing_device_with_this_serial_number = (
            db.session.query(Device)
            .filter_by(serial_number=new_serial_number_candidate)
            .first()
        )
        if existing_device_with_this_serial_number:
            # Next iteration
            continue
        existing_platform_with_this_serial_number = (
            db.session.query(Platform)
            .filter_by(serial_number=new_serial_number_candidate)
            .first()
        )
        if existing_platform_with_this_serial_number:
            continue

        # Avoid some recognizable but unfortunate names.
        # Geofon does something similar in order to avoid earthquake ids
        # like gfz2026dead
        # Some of the block words are from https://github.com/Hesham-Elbadawi/list-of-banned-words
        # for en and de
        char_part_skip_set = {
            "AFFE",
            "ANAL",
            "ANUS",
            "ASS",
            "BEER",
            "BIER",
            "BOOB",
            "BUTT",
            "CLIT",
            "COCK",
            "CRAP",
            "CUM",
            "CUNT",
            "DAMN",
            "DEAD",
            "DEPP",
            "DICK",
            "DOOF",
            "DUMB",
            "DUMM",
            "FART",
            "FICK",
            "FUCK",
            "HEIL",
            "HH",
            "HURE",
            "JERK",
            "KACK",
            "LUST",
            "MILF",
            "NAZI",
            "NUDE",
            "ORGY",
            "PORN",
            "RAGE",
            "RAPE",
            "SEX",
            "SHIT",
            "SLUT",
            "SS",
            "SUCK",
            "TIT",
            "TITS",
            "WANK",
        }
        if chars in char_part_skip_set:
            continue

        new_serial_number = new_serial_number_candidate

    result = {"data": new_serial_number}
    return result


def generate_char_part(r, min_nchars, max_nchars):
    """Generate a character part for the serial number.

    The result should be something like:
    - AA
    - BBBB
    - EFGH
    - ...
    """
    nchars = r.randint(min_nchars, max_nchars)
    chars = "".join(r.choices(string.ascii_uppercase, k=nchars))
    return chars


def generate_number_part(r, min_nnumbers, max_nnumbers):
    """Generate a number part for the serial number.

    The result should be something like this:
    - 12
    - 345
    - 6789
    """
    nnumbers = r.randint(2, 4)
    numbers = "".join(
        [*r.choices(string.digits[1:]), *r.choices(string.digits, k=nnumbers - 1)]
    )
    return numbers
