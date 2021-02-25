from .configuration_detail import ConfigurationDetail
from .configuration_list import ConfigurationList
from .configuration_relationship import ConfigurationRelationship
from .contact_detail import ContactDetail
from .contact_list import ContactList
from .contact_relationship import ContactRelationship
from .device_detail import DeviceDetail
from .device_list import DeviceList
from .device_property_detail import DevicePropertyDetail
from .device_property_list import DevicePropertyList
from .device_property_relationship import DevicePropertyRelationship
from .device_relationship import DeviceRelationship
from .event_detail import EventDetail
from .event_list import EventList
from .event_relationship import EventRelationship
from .platform_detail import PlatformDetail
from .platform_list import PlatformList
from .platform_relationship import PlatformRelationship
from .user_detail import UserDetail
from .user_list import UserList
from .user_relationship import UserRelationship
from .configuration_device_list import ConfigurationDeviceList
from .configuration_device_detail import ConfigurationDeviceDetail
from .configuration_platform_list import ConfigurationPlatformList
from .configuration_platform_detail import ConfigurationPlatformDetail
from .configuration_device_relationship import ConfigurationDeviceRelationship
from .configuration_platform_relationship import ConfigurationPlatformRelationship
# This data model import is temporal and done just to force alembic migration to make the tables
from project.api.models.mount_actions import (DeviceMountAction,  # noqa: F401
                                                  PlatformMountAction)
from project.api.models.unmount_actions import (DeviceUnmountAction,  # noqa: F401
                                                    PlatformUnmountAction)
from project.api.models.generic_actions import (GenericDeviceAction,  # noqa: F401
                                                    GenericConfigurationAction,
                                                    GenericPlatformAction)
from project.api.models.configuration_attachment import ConfigurationAttachment  # noqa: F401
from project.api.models.generic_action_attachments import (  # noqa: F401
    GenericDeviceActionAttachment,
    GenericConfigurationActionAttachment,
    GenericPlatformActionAttachment)
from project.api.models.calibration_actions import (DeviceCalibrationAction,  # noqa: F401
                                                        DevicePropertyCalibration)
from project.api.models.software_update_action_attachments import (  # noqa: F401
    PlatformSoftwareUpdateActionAttachment,
    DeviceSoftwareUpdateActionAttachment)
from project.api.models.software_update_actions import (  # noqa: F401
    DeviceSoftwareUpdateAction,
    PlatformSoftwareUpdateAction)
from project.api.models.configuration_location_actions import (  # noqa: F401
    ConfigurationStaticLocationEndAction, ConfigurationDynamicLocationBeginAction,
    ConfigurationStaticLocationBeginAction, ConfigurationDynamicLocationEndAction)
from project.api.models.calibration_attachments import DeviceCalibrationAttachment  # noqa: F401
