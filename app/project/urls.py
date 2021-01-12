from flask_rest_jsonapi import Api
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
)

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
    "/configurations/<int:id>/relationships/configuration-platforms",
)
api.route(
    ConfigurationRelationship,
    "configuration_devices",
    "/configurations/<int:id>/relationships/configuration-devices",
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
