from project.api.models.attachment import Attachment
from project.api.models.contact import Contact
from project.api.models.customfield import CustomField
from project.api.models.device import Device
from project.api.models.event import Event
from project.api.models.platform import Platform


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


def add_attachment():
    """""Add attachment model """
    attachment = Attachment(id=1, label='test label',
                            url="http://test.test")
    return attachment
