# Custom Field for the Sensor Management System software developed within the
# Helmholtz DataHub Initiative by GFZ and UFZ.
#
# Copyright (C) 2020
# - Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
# - Helmholtz Centre Potsdam - GFZ German Research Centre for
#   Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# Parts of this program were developed within the context of the
# following publicly funded projects or measures:
# - Helmholtz Earth and Environment DataHub
#   (https://www.helmholtz.de/en/research/earth_and_environment/initiatives/#h51095)
#
# Licensed under the HEESIL, Version 1.0 or - as soon they will be
# approved by the "Community" - subsequent versions of the HEESIL
# (the "Licence").
#
# You may not use this work except in compliance with the Licence.
#
# You may obtain a copy of the Licence at:
# https://gitext.gfz-potsdam.de/software/heesil
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the Licence is distributed on an "AS IS" basis,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied. See the Licence for the specific language governing
# permissions and limitations under the Licence.

from marshmallow_jsonapi import fields

from project.api.models.configuration import ConfigurationsTuple
from project.api.models.configuration_device import ConfigurationDevice
from project.api.models.configuration_platform import ConfigurationPlatform


class ConfigurationHierarchyField(fields.Field):
    """
    Create a custom-formatted field for a hierarchy Schema
    by create a subclass of marshmallow.fields.Field and
    implement its _serialize and _deserialize methods.
    Field that serializes to a dictionary(tree) and deserializes
    to a list of trees.
    for more information how it work visit:
    https://marshmallow.readthedocs.io/en/stable/custom_fields.html#custom-fields
    """

    def _serialize(self, value, *args, **kwargs):
        # build the tree out of the attributes

        configuration_platform = value.configurations_platform
        configuration_device = value.configurations_device

        # adopted from here: https://stackoverflow.com/a/35049729
        platform_nodes = {}

        for platform_configuration in configuration_platform:
            platform_id = platform_configuration.platform_id
            platform_nodes[platform_id] = {
                "id": platform_id,
                "type": "platform",
                "offset_x": platform_configuration.offset_x,
                "offset_y": platform_configuration.offset_y,
                "offset_z": platform_configuration.offset_z,
            }

        tree = []
        for platform_configuration in configuration_platform:
            platform_id = platform_configuration.platform_id
            parent_id = platform_configuration.parent_platform_id

            platform_node = platform_nodes[platform_id]

            if parent_id is None:
                tree.append(platform_node)
            else:
                parent = platform_nodes[parent_id]
                if "children" not in parent.keys():
                    parent["children"] = []
                children = parent["children"]
                children.append(platform_node)

        device_nodes = {}
        for device_configuration in configuration_device:
            device_id = device_configuration.device_id
            device_nodes[device_id] = {
                "id": device_id,
                "type": "device",
                "offset_x": device_configuration.offset_x,
                "offset_y": device_configuration.offset_y,
                "offset_z": device_configuration.offset_z,
                "calibration_date": device_configuration.calibration_date,
            }

        for device_configuration in configuration_device:
            device_id = device_configuration.device_id
            parent_id = device_configuration.parent_platform_id

            device_node = device_nodes[device_id]

            if parent_id is None:
                tree.append(device_node)
            else:
                parent = platform_nodes[parent_id]
                if "children" not in parent.keys():
                    parent["children"] = []
                children = parent["children"]
                children.append(device_node)

        return tree

    def _deserialize(self, value, *args, **kwargs):

        # value is like this
        # [
        #    {
        #        "id": 1,
        #        "type": "platform",
        #        "children": [
        #            {
        #                "id": 2,
        #                "type": "platform",
        #                "children": [
        #                    {
        #                        "id": 1,
        #                        "type": "device",
        #                    },
        #                    {
        #                        "id": 2,
        #                        "type": "device",
        #                    },
        #                    {
        #                        "id": 3,
        #                        "type": "device"
        #                    }
        #                ]
        #            }
        #        ]
        #    },
        #    {
        #        "id": 3,
        #        "type": "platform"
        #    }
        # ]

        def yield_platforms(value, parent=None):
            for entry in value:
                platform_id = entry.get("id", None)
                if entry.get("type", None) == "platform":
                    yield ConfigurationPlatform(
                        platform_id=platform_id,
                        parent_platform_id=parent,
                        offset_x=entry.get("offset_x"),
                        offset_y=entry.get("offset_y"),
                        offset_z=entry.get("offset_z"),
                    )
                children = entry.get("children", [])
                yield from yield_platforms(children, parent=platform_id)

        def yield_devices(value, parent=None):
            for entry in value:
                device_id = entry.get("id", None)
                if entry.get("type", None) == "device":
                    yield ConfigurationDevice(
                        device_id=device_id,
                        parent_platform_id=parent,
                        offset_x=entry.get("offset_x"),
                        offset_y=entry.get("offset_y"),
                        offset_z=entry.get("offset_z"),
                        calibration_date=entry.get("calibration_date"),
                    )
                children = entry.get("children", [])
                yield from yield_devices(children, parent=device_id)

        configurations_platform = list(yield_platforms(value))
        configurations_device = list(yield_devices(value))

        return ConfigurationsTuple(
            configurations_platform=configurations_platform,
            configurations_device=configurations_device,
        )
