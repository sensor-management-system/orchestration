from project.api.ping import Ping
from project.api.resourceManager import (
    ConfigurationDetail,
    ConfigurationDeviceDetail,
    ConfigurationDeviceList,
    ConfigurationDeviceRelationship,
    ConfigurationList,
    ConfigurationPlatformDetail,
    ConfigurationPlatformList,
    ConfigurationPlatformRelationship,
    ConfigurationRelationship,
    ContactDetail,
    ContactList,
    ContactRelationship,
    CustomFieldDetail,
    CustomFieldList,
    CustomFieldRelationship,
    DeviceAttachmentDetail,
    DeviceAttachmentList,
    DeviceAttachmentRelationship,
    DeviceDetail,
    DeviceList,
    DevicePropertyDetail,
    DevicePropertyList,
    DevicePropertyRelationship,
    DeviceRelationship,
    EventDetail,
    EventList,
    EventRelationship,
    PlatformAttachmentDetail,
    PlatformAttachmentList,
    PlatformAttachmentRelationship,
    PlatformDetail,
    PlatformList,
    PlatformRelationship,
    UserDetail,
    UserList,
    UserRelationship,
)
from project.frj_csv_export.api import Api

api = Api()

api.route(Ping, "test_connection", "/ping")

# Platform
api.route(
    PlatformList,
    "platform_list",
    "/platforms",
    "/contacts/<int:contact_id>/platforms",
)
api.route(
    PlatformDetail,
    "platform_detail",
    "/platforms/<int:id>",
)
api.route(
    PlatformRelationship,
    "platform_contacts",
    "/platforms/<int:id>/relationships/contacts",
)
api.route(
    PlatformRelationship,
    "platform_created_user",
    "/platforms/<int:id>/relationships/createdUser",
)
api.route(
    PlatformRelationship,
    "platform_updated_user",
    "/platforms/<int:id>/relationships/updatedUser",
)
# Platform Attachment
api.route(
    PlatformAttachmentList,
    "platform_attachment_list",
    "/platform-attachments",
    "/platform/<int:platform_id>/platform-attachments",
)
api.route(
    PlatformAttachmentDetail,
    "platform_attachment_detail",
    "/platform-attachments/<int:id>",
)
api.route(
    PlatformAttachmentRelationship,
    "platform_attachment_platform",
    "/platform-attachments/<int:id>/relationships/platform",
)
# Events
api.route(EventList, "event_list", "/events")
api.route(
    EventDetail,
    "event_detail",
    "/events/<int:id>",
)
api.route(
    EventRelationship,
    "event_user",
    "/events/<int:id>/relationships/user",
)

# Device
api.route(
    DeviceList,
    "device_list",
    "/devices",
    "/contacts/<int:id>/devices",
)
api.route(
    DeviceDetail,
    "device_detail",
    "/devices/<int:id>",
)
api.route(
    DeviceRelationship,
    "device_contacts",
    "/devices/<int:id>/relationships/contacts",
)
api.route(
    DeviceRelationship,
    "device_events",
    "/devices/<int:id>/relationships/events",
)
api.route(
    DeviceRelationship,
    "device_created_user",
    "/devices/<int:id>/relationships/createdUser",
)
api.route(
    DeviceRelationship,
    "device_updated_user",
    "/devices/<int:id>/relationships/updatedUser",
)

# Device Property
api.route(
    DevicePropertyDetail,
    "device_property_detail",
    "/device-properties/<int:id>",
)

api.route(
    DevicePropertyList,
    "device_property_list",
    "/device-properties",
    "/devices/<int:device_id>/device-properties",
)

api.route(
    DevicePropertyRelationship,
    "device_property_device",
    "/device-properties/<int:id>/relationships/device",
)

# Device Attachment
api.route(
    DeviceAttachmentList,
    "device_attachment_list",
    "/device-attachments",
    "/devices/<int:device_id>/device-attachments",
)
api.route(
    DeviceAttachmentDetail,
    "device_attachment_detail",
    "/device-attachments/<int:id>",
)
api.route(
    DeviceAttachmentRelationship,
    "device_attachemnt_device",
    "/device-attachments/<int:id>/relationships/device",
)

# CustomField
api.route(
    CustomFieldList,
    "customfield_list",
    "/customfields",
    "/devices/<int:device_id>/customfields",
)
api.route(
    CustomFieldDetail,
    "customfield_detail",
    "/customfields/<int:id>",
)
api.route(
    CustomFieldRelationship,
    "customfield_device",
    "/customfields/int:id>/relationships/device",
)

# Contact
api.route(
    ContactList,
    "contact_list",
    "/contacts",
    "/devices/<int:device_id>/contacts",
    "/platforms/<int:platform_id>/contacts",
)
api.route(ContactDetail, "contact_detail", "/contacts/<int:id>")
api.route(
    ContactRelationship,
    "contact_devices",
    "/contacts/<int:id>/relationships/devices",
)
api.route(
    ContactRelationship,
    "contact_platforms",
    "/contacts/<int:id>/relationships/platforms",
)
api.route(
    ContactRelationship,
    "contact_configurations",
    "/contacts/<int:id>/relationships/configurations",
)
api.route(
    ContactRelationship,
    "contact_user",
    "/contacts/<int:id>/relationships/user",
)
# Users
api.route(
    UserList,
    "user_list",
    "/users",
    "/contacts/<int:id>/users",
)
api.route(UserDetail, "user_detail", "/users/<int:id>")
api.route(
    UserRelationship,
    "user_contact",
    "/users/<int:id>/relationships/contact",
)
api.route(
    UserRelationship,
    "user_events",
    "/users/<int:id>/relationships/events",
)

# Configuration
api.route(
    ConfigurationList,
    "configuration_list",
    "/configurations",
)
api.route(
    ConfigurationDetail,
    "configuration_detail",
    "/configurations/<int:id>",
)
api.route(
    ConfigurationRelationship,
    "configuration_contacts",
    "/configurations/<int:id>/relationships/contacts",
)
api.route(
    ConfigurationRelationship,
    "configuration_platforms",
    "/configurations/<int:id>/relationships/configurationPlatforms",
)
api.route(
    ConfigurationRelationship,
    "configuration_devices",
    "/configurations/<int:id>/relationships/configurationDevices",
)
api.route(
    ConfigurationRelationship,
    "configuration_src_longitude",
    "/configurations/<int:id>/relationships/src-longitude",
)
api.route(
    ConfigurationRelationship,
    "configuration_src_latitude",
    "/configurations/<int:id>/relationships/src-latitude",
)
api.route(
    ConfigurationRelationship,
    "configuration_src_elevation",
    "/configurations/<int:id>/relationships/src-elevation",
)
# ConfigurationPlatform
api.route(
    ConfigurationPlatformList,
    "configuration_platform_list",
    "/configuration-platforms",
)
api.route(
    ConfigurationPlatformDetail,
    "configuration_platform_detail",
    "/configuration-platforms/<int:id>",
)
api.route(
    ConfigurationPlatformRelationship,
    "configuration_platform",
    "/configuration-platforms/<int:id>/relationships/platform",
)
# ConfigurationDevice
api.route(
    ConfigurationDeviceList,
    "configuration_device_list",
    "/configuration-devices",
)
api.route(
    ConfigurationDeviceDetail,
    "configuration_device_detail",
    "/configuration-devices/<int:id>",
)
api.route(
    ConfigurationDeviceRelationship,
    "configuration_device",
    "/configuration-devices/<int:id>/relationships/device",
)
