# SPDX-FileCopyrightText: 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Cleanup functions for different usecases for the sensorML entries."""

import re


def identifier(text, replacement="", start="id"):
    """
    Clean the text for an identifier.

    An identifier can only hold numbers, chars, minus and underscores.
    And it must start with a char.
    """
    # In the sensorML we often have situations in that there is only
    # the following pattern allowed:
    # <xs:pattern xmlns:xs="http://www.w3.org/2001/XMLSchema" value="[\i-[:]][\c-[:]]*" />
    #
    # It is not supported in python ifself, so we need to build it on our own.
    # Step zero: Make sure we work with a string here
    if text is None:
        text = ""
    if not isinstance(text, str):
        text = str(text)
    # Step one: Replace all entries that don't follow the pattern.
    # We want to replace all occurance of elements that are either
    # - the minus
    # - the underscore
    # - chars
    # - numbers
    #
    # We want to replace it with the replacement.
    # If 2 or more of them are there in one place, we want to replace
    # them with only one entry of the replacement.
    text = re.sub(r"[^-_a-zA-Z0-9]+", replacement, text)
    # Step two: Check if the entry starts with a char.
    if not re.match("^[a-zA-Z]", text):
        text = start + text
    return text
