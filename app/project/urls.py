from project.api.ping import Ping
from project.api.resourceManager.attachment_detail import AttachmentDetail
from project.api.resourceManager.attachment_list import AttachmentList
from project.api.resourceManager.attachment_relationship \
    import AttachmentRelationship
from project.api.resourceManager.contact_detail import ContactDetail
from project.api.resourceManager.contact_list import ContactList
from project.api.resourceManager.contact_relationship \
    import ContactRelationship
from project.api.resourceManager.device_detail import DeviceDetail
from project.api.resourceManager.device_list import DeviceList
from project.api.resourceManager.device_relationship import DeviceRelationship
from project.api.resourceManager.event_detail import EventDetail
from project.api.resourceManager.event_list import EventList
from project.api.resourceManager.event_relationship import EventRelationship
from project.api.resourceManager.platform_detail import PlatformDetail
from project.api.resourceManager.platform_list import PlatformList
from project.api.resourceManager.platform_relationship \
    import PlatformRelationship
from project.api.resourceManager.properties_detail import PropertiesDetail
from project.api.resourceManager.properties_list import PropertiesList
from project.api.resourceManager.properties_relationship \
    import PropertiesRelationship
from project.api.resourceManager.user_detail import UserDetail
from project.api.resourceManager.user_list import UserList
from project.api.resourceManager.user_relationship \
    import UserRelationship

base_url = '/rdm/svm-api/v1'


def Create_endpoints(api):
    """"
    The routing system
    """
    api.route(Ping, 'test_connection', base_url + '/ping')

    # Platform
    api.route(PlatformList, 'platform_list', base_url + '/platforms')
    api.route(PlatformDetail, 'platform_detail',
              base_url + '/platforms/<int:id>',
              base_url + '/contacts/<int:contact_id>/platforms')
    api.route(PlatformRelationship, 'platforms_contacts',
              base_url + '/platforms/<int:id>/relationships/contacts')

    # Device
    api.route(DeviceList, 'devices_list', base_url + '/devices',
              base_url + '/contacts/<int:id>/devices')
    api.route(DeviceDetail, 'devices_detail', base_url + '/devices/<int:id>',
              base_url + '/events/<int:event_id>/device',
              base_url + '/contact/<int:contact_id>/device',
              base_url + '/attachments/<int:attachment_id>/device',
              base_url + '/properties/<int:properties_id>/device')
    api.route(DeviceRelationship, 'devices_contacts',
              base_url + '/devices/<int:id>/relationships/contacts')
    api.route(DeviceRelationship, 'device_events',
              base_url + '/devices/<int:id>/relationships/events')
    api.route(DeviceRelationship, 'device_properties',
              base_url + '/devices/<int:id>/relationships/properties')
    api.route(DeviceRelationship, 'device_attachments',
              base_url + '/devices/<int:id>/relationships/attachments')
    api.route(DeviceRelationship, 'device_customfields',
              base_url + '/devices/<int:id>/relationships/customfields')
    # Event
    api.route(EventList, 'events_list', base_url + '/events',
              base_url + '/devices/<int:id>/events')
    api.route(EventDetail, 'events_detail', base_url + '/events/<int:id>')
    api.route(EventRelationship, 'events_device',
              base_url + '/events/<int:id>/relationships/device')
    api.route(EventRelationship, 'events_user',
              base_url + '/events/<int:id>/relationships/user')
    # Contact
    api.route(ContactList, 'contacts_list', base_url + '/contacts',
              base_url + '/devices/<int:device_id>/contacts',
              base_url + '/platforms/<int:platform_id>/contacts')
    api.route(ContactDetail, 'contacts_detail',
              base_url + '/contacts/<int:id>')
    api.route(ContactRelationship, 'contacts_devices',
              base_url + '/contacts/<int:id>/relationships/devices')
    api.route(ContactRelationship, 'contacts_platforms',
              base_url + '/contacts/<int:id>/relationships/platforms')
    api.route(ContactRelationship, 'contact_user',
              base_url + '/contacts/<int:id>/relationships/user')
    # Properties
    api.route(PropertiesList, 'properties_list', base_url + '/properties',
              base_url + '/devices/<int:device_id>/properties')
    api.route(PropertiesDetail, 'properties_detail',
              base_url + '/properties/<int:id>')
    api.route(PropertiesRelationship, 'properties_device',
              base_url + '/properties/<int:device_id>/relationships/device')
    # Attachment
    api.route(AttachmentList, 'attachments_list', base_url + '/attachments',
              base_url + '/devices/<int:device_id>/attachments')
    api.route(AttachmentDetail, 'attachments_detail',
              base_url + '/attachments/<int:id>')
    api.route(AttachmentRelationship, 'attachments_device',
              base_url + '/attachments/<int:id>/relationships/device')
    # Users
    api.route(UserList, 'users_list', base_url + '/users',
              base_url + '/contacts/<int:id>/users')
    api.route(UserDetail, 'users_detail', base_url + '/users/<int:id>')
    api.route(UserRelationship, 'user_contact',
              base_url + '/users/<int:id>/relationships/contact')
    api.route(UserRelationship, 'user_events',
              base_url + '/users/<int:id>/relationships/events')
