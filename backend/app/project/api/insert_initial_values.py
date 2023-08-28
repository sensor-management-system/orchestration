# SPDX-FileCopyrightText: 2020 - 2022
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

from ..models.contact import Contact
from ..models.customfield import CustomField
from ..models.device import Device
from ..models.device_attachment import DeviceAttachment
from ..models.device_property import DeviceProperty
from ..models.platform import Platform
from ..models.platform_attachment import PlatformAttachment


def add_device():
    """""Ensure Add device model """
    device = Device(
        id=1,
        short_name="Device short name",
        long_name="Device long name",
        serial_number="0000001",
        model="test model",
        inventory_number="0000001",
        persistent_identifier="0000001",
        description="My first test device",
    )
    return device


def add_platform():
    """""Add platform model """
    platform = Platform(
        id=1,
        short_name="test short name",
        long_name="test long name",
        description="My first test platform",
    )
    return platform


def add_contact():
    """""Add contact model """
    contact = Contact(
        id=1, given_name="Max", family_name="Mustermann", email="test@test.test"
    )
    return contact


def add_customfield(device):
    """""Add customfield model """
    customfield = CustomField(
        id=1, key="test key", device_id=device.id, value="test value"
    )
    return customfield


def add_device_attachment(device):
    """""Add a device attachment model """
    device_attachment = DeviceAttachment(
        id=1, label="test label", device_id=device.id, url="http://test.test"
    )
    return device_attachment


def add_device_properties(device):
    """""Add device properties model """
    properties = DeviceProperty(id=1, device_id=device.id)
    return properties


def add_platform_attachment(platform):
    """""Add platform attachment model """
    attachment = PlatformAttachment(
        id=1,
        platform_id=platform.id,
        label="test platform label",
        url="http://www.google.de",
    )
    return attachment
