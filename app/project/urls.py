from project.frj_csv_export.api import Api
from project.api.ping import Ping
from project.api.resourceManager import (
    ConfigurationDetail,
    ConfigurationList,
    ConfigurationRelationship,
    ContactDetail,
    ContactList,
    ContactRelationship,
    DeviceDetail,
    DeviceList,
    DevicePropertyDetail,
    DevicePropertyList,
    DevicePropertyRelationship,
    DeviceRelationship,
    EventDetail,
    EventList,
    EventRelationship,
    PlatformDetail,
    PlatformList,
    PlatformRelationship,
    UserDetail,
    UserList,
    UserRelationship,
    ConfigurationPlatformList,
    ConfigurationDeviceList,
    ConfigurationDeviceDetail,
    ConfigurationPlatformDetail,
    ConfigurationPlatformRelationship,
    ConfigurationDeviceRelationship,
)

from project.api.resourceManager.generic_device_action_resources import (
    GenericDeviceActionList,
    GenericDeviceActionDetail,
    GenericDeviceActionRelationship)

from project.api.resourceManager.generic_device_action_attachment_resources import \
    GenericDeviceActionAttachmentList, GenericDeviceActionAttachmentDetail, \
    GenericDeviceActionAttachmentRelationship

from project.api.resourceManager.generic_platform_action_resources import \
    GenericPlatformActionList, GenericPlatformActionRelationship, GenericPlatformActionDetail

from project.api.resourceManager.generic_platform_action_attachment_resources import \
    GenericPlatformActionAttachmentList, GenericPlatformActionAttachmentDetail, \
    GenericPlatformActionAttachmentRelationship

from project.api.resourceManager.generic_configuration_action_resources import \
    GenericConfigurationActionRelationship, GenericConfigurationActionList, \
    GenericConfigurationActionDetail

from project.api.resourceManager.generic_configuration_action_attachment_resources import \
    GenericConfigurationActionAttachmentList, GenericConfigurationActionAttachmentDetail, \
    GenericConfigurationActionAttachmentRelationship

from project.api.resourceManager.device_mount_action_resources import DeviceMountActionList, \
    DeviceMountActionDetail, DeviceMountActionRelationship

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
    "/platforms/<int:id>/relationships/created-user",
)
api.route(
    PlatformRelationship,
    "platform_updated_user",
    "/platforms/<int:id>/relationships/created-user",
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
    "/devices/<int:id>/relationships/created-user",
)
api.route(
    DeviceRelationship,
    "device_updated_user",
    "/devices/<int:id>/relationships/created-user",
)

# Device Property
api.route(
    DevicePropertyDetail,
    "device_property_detail",
    "/device-properties/<int:id>",
)

api.route(DevicePropertyList, "device_property_list", "/device-properties")

api.route(
    DevicePropertyRelationship,
    "device_property_device",
    "/device-properties/<int:id>/relationships/device",
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
api.route(
    PlatformRelationship,
    "configuration_created_user",
    "/configurations/<int:id>/relationships/created-user",
)
api.route(
    PlatformRelationship,
    "configuration_updated_user",
    "/configurations/<int:id>/relationships/created-user",
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
# GenericDeviceAction
api.route(GenericDeviceActionList, "generic_device_action_list", "/generic-device-actions")
api.route(
    GenericDeviceActionDetail,
    "generic_device_action_detail",
    "/generic-device-actions/<int:id>"
)
api.route(GenericDeviceActionRelationship, "generic_device_action_device",
          "/generic-device-actions/<int:id>/relationships/device")
api.route(GenericDeviceActionRelationship, "generic_device_action_contact",
          "/generic-device-actions/<int:id>/relationhips/contact")
api.route(GenericDeviceActionRelationship, "generic_device_action_attachments",
          "/generic-device-actions/<int:id>/relationships/attachments")
# GenericDeviceActionAttachment
api.route(GenericDeviceActionAttachmentList, "generic_device_action_attachment_list",
          "/generic-device-action-attachments")
api.route(GenericDeviceActionAttachmentDetail, "generic_device_action_attachment_detail",
          "/generic-device-action-attachments/<int:id>")
api.route(GenericDeviceActionAttachmentRelationship, "generic_device_action_attachment_action",
          "/generic-device-action-attachments/<int:id>/relationships/action")
api.route(GenericDeviceActionAttachmentRelationship, "generic_device_action_attachment_attachments",
          "/generic-device-action-attachments/<int:id>/relationships/attachments")
# GenericPlatformAction
api.route(GenericPlatformActionList, "generic_platform_action_list", "/generic-platform-actions")
api.route(
    GenericPlatformActionDetail,
    "generic_platform_action_detail",
    "/generic-platform-actions/<int:id>"
)
api.route(GenericPlatformActionRelationship, "generic_platform_action_platform",
          "/generic-platform-actions/<int:id>/relationships/platform")
api.route(GenericPlatformActionRelationship, "generic_platform_action_contact",
          "/generic-platform-actions/<int:id>/relationhips/contact")
api.route(GenericPlatformActionRelationship, "generic_platform_action_attachments",
          "/generic-platform-actions/<int:id>/relationships/attachments")
# GenericPlatformActionAttachment
api.route(GenericPlatformActionAttachmentList, "generic_platform_action_attachment_list",
          "/generic-platform-action-attachments")
api.route(GenericPlatformActionAttachmentDetail, "generic_platform_action_attachment_detail",
          "/generic-platform-action-attachments/<int:id>")
api.route(GenericPlatformActionAttachmentRelationship, "generic_platform_action_attachment_action",
          "/generic-platform-action-attachments/<int:id>/relationships/action")
api.route(GenericPlatformActionAttachmentRelationship,
          "generic_platform_action_attachment_attachments",
          "/generic-platform-action-attachments/<int:id>/relationships/attachments")
# GenericConfigurationAction
api.route(GenericConfigurationActionList, "generic_configuration_action_list",
          "/generic-configuration-actions")
api.route(
    GenericConfigurationActionDetail,
    "generic_configuration_action_detail",
    "/generic-configuration-actions/<int:id>"
)
api.route(GenericConfigurationActionRelationship, "generic_configuration_action_configuration",
          "/generic-configuration-actions/<int:id>/relationships/configuration")
api.route(GenericConfigurationActionRelationship, "generic_configuration_action_contact",
          "/generic-configuration-actions/<int:id>/relationhips/contact")
api.route(GenericConfigurationActionRelationship, "generic_configuration_action_attachments",
          "/generic-configuration-actions/<int:id>/relationships/attachments")
# GenericConfigurationActionAttachment
api.route(GenericConfigurationActionAttachmentList, "generic_configuration_action_attachment_list",
          "/generic-configuration-action-attachments")
api.route(GenericConfigurationActionAttachmentDetail,
          "generic_configuration_action_attachment_detail",
          "/generic-configuration-action-attachments/<int:id>")
api.route(GenericConfigurationActionAttachmentRelationship,
          "generic_configuration_action_attachment_action",
          "/generic-configuration-action-attachments/<int:id>/relationships/action")
api.route(GenericConfigurationActionAttachmentRelationship,
          "generic_configuration_action_attachment_attachments",
          "/generic-configuration-action-attachments/<int:id>/relationships/attachments")
# MountDeviceAction
api.route(DeviceMountActionList, "mount_device_action_list", "/mount-device-actions")
api.route(
    DeviceMountActionDetail,
    "device_mount_action_detail",
    "/mount-device-actions/<int:id>"
)
api.route(DeviceMountActionRelationship, "mount_device_action_device",
          "/mount-device-actions/<int:id>/relationships/device")
api.route(DeviceMountActionRelationship, "mount_device_action_contact",
          "/mount-device-actions/<int:id>/relationships/contact")
api.route(DeviceMountActionRelationship, "mount_device_action_configuration",
          "/mount-device-actions/<int:id>/relationships/configuration")
api.route(DeviceMountActionRelationship, "mount_device_action_parent_platform",
          "/mount-device-actions/<int:id>/relationships/parent-platform")
