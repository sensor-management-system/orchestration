from project.api.ping import Ping
from project.api.resourceManager.contact_detail import ContactDetail
from project.api.resourceManager.contact_list import ContactList
from project.api.resourceManager.contact_relationship import ContactRelationship
from project.api.resourceManager.device_detail import DeviceDetail
from project.api.resourceManager.device_list import DeviceList
from project.api.resourceManager.device_relationship import DeviceRelationship
from project.api.resourceManager.event_detail import EventDetail
from project.api.resourceManager.event_list import EventList
from project.api.resourceManager.event_relationship import EventRelationship
from project.api.resourceManager.platform_detail import PlatformDetail
from project.api.resourceManager.platform_list import PlatformList
from project.api.resourceManager.platform_relationship import PlatformRelationship
from project.api.resourceManager.user_detail import UserDetail
from project.api.resourceManager.user_list import UserList
from project.api.resourceManager.user_relationship import UserRelationship

base_url = "/rdm/svm-api/v1"


def create_endpoints(api):
    """"
    The routing system
    """
    api.route(Ping, "test_connection", base_url + "/ping")

    # Platform
    api.route(
        PlatformList,
        "platform_list",
        base_url + "/platforms",
        base_url + "/contacts/<int:contact_id>/platforms",
    )
    api.route(
        PlatformDetail, "platform_detail", base_url + "/platforms/<int:id>",
    )
    api.route(
        PlatformRelationship,
        "platform_contacts",
        base_url + "/platforms/<int:id>/relationships/contacts",
    )
    api.route(
        PlatformRelationship,
        "platform_created_user",
        base_url + "/platforms/<int:id>/relationships/createdUser",
    )
    api.route(
        PlatformRelationship,
        "platform_updated_user",
        base_url + "/platforms/<int:id>/relationships/updatedUser",
    )
    # Events
    api.route(EventList, "event_list", base_url + "/events")
    api.route(
        EventDetail, "event_detail", base_url + "/events/<int:id>",
    )
    api.route(
        EventRelationship,
        "event_user",
        base_url + "/events/<int:id>/relationships/user",
    )

    # Device
    api.route(
        DeviceList,
        "device_list",
        base_url + "/devices",
        base_url + "/contacts/<int:id>/devices",
    )
    api.route(
        DeviceDetail, "device_detail", base_url + "/devices/<int:id>",
    )
    api.route(
        DeviceRelationship,
        "device_contacts",
        base_url + "/devices/<int:id>/relationships/contacts",
    )
    api.route(
        DeviceRelationship,
        "device_events",
        base_url + "/devices/<int:id>/relationships/events",
    )
    api.route(
        DeviceRelationship,
        "device_created_user",
        base_url + "/devices/<int:id>/relationships/createdUser",
    )
    api.route(
        DeviceRelationship,
        "device_updated_user",
        base_url + "/devices/<int:id>/relationships/updatedUser",
    )
    # Contact
    api.route(
        ContactList,
        "contact_list",
        base_url + "/contacts",
        base_url + "/devices/<int:device_id>/contacts",
        base_url + "/platforms/<int:platform_id>/contacts",
    )
    api.route(ContactDetail, "contact_detail", base_url + "/contacts/<int:id>")
    api.route(
        ContactRelationship,
        "contact_devices",
        base_url + "/contacts/<int:id>/relationships/devices",
    )
    api.route(
        ContactRelationship,
        "contact_platforms",
        base_url + "/contacts/<int:id>/relationships/platforms",
    )
    api.route(
        ContactRelationship,
        "contact_user",
        base_url + "/contacts/<int:id>/relationships/user",
    )
    # Users
    api.route(
        UserList,
        "user_list",
        base_url + "/users",
        base_url + "/contacts/<int:id>/users",
    )
    api.route(UserDetail, "user_detail", base_url + "/users/<int:id>")
    api.route(
        UserRelationship,
        "user_contact",
        base_url + "/users/<int:id>/relationships/contact",
    )
    api.route(
        UserRelationship,
        "user_events",
        base_url + "/users/<int:id>/relationships/events",
    )
