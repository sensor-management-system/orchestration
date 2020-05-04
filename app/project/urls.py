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


def Create_endpoints(api):
    api.route(Ping, 'test_connection', '/ping')

    # Platform
    api.route(PlatformList, 'platform_list', '/platforms')
    api.route(PlatformDetail, 'platform_detail', '/platforms/<int:id>',
              '/devices/<int:device_id>/platform')
    api.route(PlatformRelationship, 'platform_devices',
              '/platforms/<int:id>/relationships/devices')

    # Device
    api.route(DeviceList, 'devices_list', '/devices',
              '/platforms/<int:id>/devices')
    api.route(DeviceDetail, 'devices_detail', '/devices/<int:id>')
    api.route(DeviceRelationship, 'device_platform',
              '/devices/<int:id>/relationships/platform')
    api.route(DeviceRelationship, 'device_contacts',
              '/devices/<int:id>/relationships/contacts')
    api.route(DeviceRelationship, 'device_events',
              '/devices/<int:id>/relationships/events')
    api.route(DeviceRelationship, 'device_properties',
              '/devices/<int:id>/relationships/properties')
    # Event
    api.route(EventList, 'events_list', '/events')
    api.route(EventDetail, 'events_detail', '/events/<int:id>')
    api.route(EventRelationship, 'events_device',
              '/events/<int:id>/relationships/device')
    # Contact
    api.route(ContactList, 'contacts_list', '/contacts')
    api.route(ContactDetail, 'contacts_detail', '/contacts/<int:id>')
    api.route(ContactRelationship, 'contacts_device',
              '/contacts/<int:id>/relationships/device')
    # Properties
    api.route(PropertiesList, 'properties_list', '/properties')
    api.route(PropertiesDetail, 'properties_detail', '/properties/<int:id>')
    api.route(PropertiesRelationship, 'properties_device',
              '/properties/<int:id>/relationships/device')
