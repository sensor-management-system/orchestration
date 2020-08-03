from project.api.models.contact import Contact
from project.api.models.customfield import CustomField
from project.api.models.device import Device
from project.api.models.device_attachment import DeviceAttachment
from project.api.models.event import Event
from project.api.models.platform import Platform
from project.api.models.platform_attachment import PlatformAttachment
from project.api.models.device_property import DeviceProperty


def add_sensor():
    """""Ensure Add device model """
    sensor = Device(id=1, serial_number='0000001',
                    manufacturer="test manufacturer",
                    model="test model", inventory_number="0000001",
                    persistent_identifier="0000001", type="test type",
                    description='My first test sensor')
    return sensor


def add_platform():
    """""Add platform model """
    platform = Platform(id=1,
                        short_name='test short name', type="test type",
                        description='My first test platform')
    return platform


def add_event():
    """""Add event model """
    event = Event(id=1, description='My first test event')
    return event


def add_contact():
    """""Add contact model """
    contact = Contact(id=1, username='test username',
                      email="test@test.test")
    return contact


def add_customfield():
    """""Add customfield model """
    customfield = CustomField(id=1, key='test key',
                              value="test value")
    return customfield


def add_device_attachment():
    """""Add a device attachment model """
    device_attachment = DeviceAttachment(id=1, label='test label',
                                         url="http://test.test")
    return device_attachment


def add_device_properties():
    """""Add device properties model """
    properties = DeviceProperty(id=1)
    return properties


def add_platform_attachment():
    """""Add platform attachment model """
    attachmet = PlatformAttachment(id=1)
    return attachmet
