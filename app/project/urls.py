from project.api.ping import Ping
from project.api.resourceManager.deviceDetail import DeviceDetail
from project.api.resourceManager.deviceList import DeviceList
from project.api.resourceManager.deviceRelationship import DeviceRelationship
from project.api.resourceManager.eventDetail import EventDetail
from project.api.resourceManager.eventList import EventList
from project.api.resourceManager.eventRelationship import EventRelationship
from project.api.resourceManager.platformDetail import PlatformDetail
from project.api.resourceManager.platformList import PlatformList
from project.api.resourceManager.platformRelationship import PlatformRelationship
from project.api.resourceManager.contactList import ContactList
from project.api.resourceManager.contactDetail import ContactDetail
from project.api.resourceManager.contactRelationship import ContactRelationship
from project.api.resourceManager.propertiesList import PropertiesList
from project.api.resourceManager.propertiesDetail import PropertiesDetail
from project.api.resourceManager.propertiesRelationship import PropertiesRelationship

base_url = '/sis/v1'


def Create_endpoints(api):
    api.route(Ping, 'test_connection', base_url + '/ping')

    # Platform
    api.route(PlatformList, 'platform_list', base_url + '/platforms')
    api.route(PlatformDetail, 'platform_detail', base_url + '/platforms/<int:id>',
              base_url + '/devices/<int:device_id>/platform')
    api.route(PlatformRelationship, 'platform_devices',
              base_url + '/platforms/<int:id>/relationships/devices')

    # Device
    api.route(DeviceList, 'devices_list', base_url + '/devices',
              base_url + '/platforms/<int:id>/devices')
    api.route(DeviceDetail, 'devices_detail', base_url + '/devices/<int:id>')
    api.route(DeviceRelationship, 'device_platform',
              base_url + '/devices/<int:id>/relationships/platform')
    api.route(DeviceRelationship, 'device_contacts',
              base_url + '/devices/<int:id>/relationships/contacts')
    api.route(DeviceRelationship, 'device_events',
              base_url + '/devices/<int:id>/relationships/events')
    api.route(DeviceRelationship, 'device_properties',
              base_url + '/devices/<int:id>/relationships/properties')
    # Event
    api.route(EventList, 'events_list', base_url + '/events')
    api.route(EventDetail, 'events_detail', base_url + '/events/<int:id>')
    api.route(EventRelationship, 'events_device',
              base_url + '/events/<int:id>/relationships/device')
    # Contact
    api.route(ContactList, 'contacts_list', base_url + '/contacts')
    api.route(ContactDetail, 'contacts_detail', base_url + '/contacts/<int:id>')
    api.route(ContactRelationship, 'contacts_device',
              base_url + '/contacts/<int:id>/relationships/device')
    # Properties
    api.route(PropertiesList, 'properties_list', base_url + '/properties')
    api.route(PropertiesDetail, 'properties_detail', base_url + '/properties/<int:id>')
    api.route(PropertiesRelationship, 'properties_device',
              base_url + '/properties/<int:id>/relationships/device')
