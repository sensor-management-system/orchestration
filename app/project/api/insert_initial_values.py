from project.api.models.contact import Contact
from project.api.models.customfield import CustomField
from project.api.models.device import Device
from project.api.models.device_attachment import DeviceAttachment
from project.api.models.event import Event
from project.api.models.platform import Platform
from project.api.models.platform_attachment import PlatformAttachment
from project.api.models.device_property import DeviceProperty


def add_device():
    """""Ensure Add device model """
    sensor = Device(
        id=1,
        short_name='Device short name',
        long_name='Device long name',
        serial_number='0000001',
        model="test model", 
        inventory_number="0000001",
        persistent_identifier="0000001",
        description='My first test sensor'
    )
    return sensor


def add_platform():
    """""Add platform model """
    platform = Platform(id=1,
                        short_name='test short name',
                        long_name='test long name',
                        description='My first test platform')
    return platform


def add_event(device):
    """""Add event model """
    event = Event(id=1, description='My first test event', device_id=device.id)
    return event


def add_contact():
    """""Add contact model """
    contact = Contact(id=1, given_name='Max', family_name='Mustermann',
                      email="test@test.test")
    return contact


def add_customfield(device):
    """""Add customfield model """
    customfield = CustomField(id=1, key='test key',
                              device_id=device.id,
                              value="test value")
    return customfield


def add_device_attachment(device):
    """""Add a device attachment model """
    device_attachment = DeviceAttachment(id=1, label='test label',
                                         device_id=device.id,
                                         url="http://test.test")
    return device_attachment


def add_device_properties(device):
    """""Add device properties model """
    properties = DeviceProperty(id=1, device_id=device.id)
    return properties


def add_platform_attachment(platform):
    """""Add platform attachment model """
    attachment PlatformAttachment(
        id=1,
        platform_id=platform.id,
        label="test platform label",
        url="http://www.google.de"
    )
    return attachment
