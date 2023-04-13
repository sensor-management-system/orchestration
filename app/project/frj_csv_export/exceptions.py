# SPDX-FileCopyrightText: 2020
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

# -*- coding: utf-8 -*-

"""Collection of useful http error for the Api
Modifications: Adopted form Custom content negotiation #171 ( miLibris /
flask-rest-jsonapi )"""
from flask_rest_jsonapi import JsonApiException


class InvalidContentType(JsonApiException):
    """When the request uses a content type the API doesn't understand"""

    title = "Bad request"
    status = "415"


class InvalidAcceptType(JsonApiException):
    """When the request expects a content type that the API doesn't support"""

    title = "Bad request"
    status = "406"
