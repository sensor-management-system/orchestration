# SPDX-FileCopyrightText: 2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Openapi specification for the involved devices in datastream links."""


from ...api.helpers.openapi import MarshmallowJsonApiToOpenApiMapper
from ...api.schemas.involved_device_for_datastream_link_schema import (
    InvolvedDeviceForDatastreamLinkSchema,
)

schema_mapper = MarshmallowJsonApiToOpenApiMapper(InvolvedDeviceForDatastreamLinkSchema)

paths = {
    "/involved-devices-for-datastream-links": {
        "get": {
            "tags": ["Datastream links"],
            "parameters": [
                {"$ref": "#/components/parameters/include"},
                {"$ref": "#/components/parameters/page_number"},
                {"$ref": "#/components/parameters/page_size"},
                {"$ref": "#/components/parameters/sort"},
                *schema_mapper.filters(),
            ],
            "responses": {
                "200": {
                    "description": "List of involved devices in datastream links",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_list(),
                    },
                }
            },
            "description": "Retrieve a list of involved devices for datastream links",
            "operationId": "RetrievecollectionofInvolvedDevicesForDatastreamLinkObjects",
        },
        "post": {
            "tags": ["Datastream links"],
            "requestBody": {
                "content": {
                    "application/vnd.api+json": schema_mapper.post(),
                },
                "required": True,
            },
            "responses": {
                "201": {
                    "description": "Payload of the created relationship of a device for a datastream link",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                },
            },
            "operationId": "CreateInvolvedDeviceForDatastreamLink",
        },
    },
    "/involved-devices-for-datastream-links/{involved_device_for_datastream_link_id}": {
        "get": {
            "tags": ["Datastream links"],
            "parameters": [
                {"$ref": "#/components/parameters/include"},
                {
                    "$ref": "#/components/parameters/involved_device_for_datastream_link_id"
                },
            ],
            "responses": {
                "200": {
                    "description": "Instance of an involved device for datastream link",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                },
                "404": {"$ref": "#/components/responses/jsonapi_error_404"},
            },
            "description": "Retrieve a single involved device for a datastream link",
            "operationId": "RetrieveInvolvedDeviceForDatastreamLinkInstance",
        },
        "patch": {
            "tags": ["Datastream links"],
            "parameters": [
                {
                    "$ref": "#/components/parameters/involved_device_for_datastream_link_id"
                },
            ],
            "requestBody": {
                "content": {
                    "application/vnd.api+json": schema_mapper.patch(),
                },
                "description": "InvolvedDeviceForDatastream attributes",
                "required": True,
            },
            "responses": {
                "200": {
                    "description": "Payload of the updated involved device for datastream link",
                    "content": {
                        "application/vnd.api+json": schema_mapper.get_one(),
                    },
                },
                "404": {"$ref": "#/components/responses/jsonapi_error_404"},
            },
            "description": "Update InvolvedDeviceForDatastreamLink attributes",
            "operationId": "UpdateInvolvedDeviceForDatastreamLink",
        },
        "delete": {
            "tags": ["Datastream links"],
            "parameters": [
                {
                    "$ref": "#/components/parameters/involved_device_for_datastream_link_id"
                },
            ],
            "responses": {
                "200": {"$ref": "#/components/responses/object_deleted"},
                "404": {"$ref": "#/components/responses/jsonapi_error_404"},
            },
            "operationId": "DeleteInvolvedDeviceForDatastreamLink",
        },
    },
}

components = {
    "parameters": {
        "involved_device_for_datastream_link_id": {
            "name": "involved_device_for_datastream_link_id",
            "in": "path",
            "required": True,
            "schema": {"type": "string"},
        }
    },
}
