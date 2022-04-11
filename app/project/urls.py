from project.api.resourceManager import *

from .api.ping import Ping
from .frj_csv_export.api import Api


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
    "/platforms/<int:id>/relationships/updated-user",
)
api.route(
    PlatformRelationship,
    "platform_platform_attachments",
    "/platforms/<int:id>/relationships/platform-attachments",
)
api.route(
    PlatformRelationship,
    "platform_generic_platform_actions",
    "/platforms/<int:id>/relationships/generic-platform-actions",
)
api.route(
    PlatformRelationship,
    "platform_platform_mount_actions",
    "/platforms/<int:id>/relationships/platform-mount-actions",
)
api.route(
    PlatformRelationship,
    "platform_platform_unmount_actions",
    "/platforms/<int:id>/relationships/platform-unmount-actions",
)
api.route(
    PlatformRelationship,
    "platform_platform_software_update_actions",
    "/platforms/<int:id>/relationships/platform-software-update-actions",
)
api.route(
    PlatformRelationship,
    "platform_configuration_platform",
    "/platforms/<int:id>/relationships/configuration-platform",
)
api.route(
    PlatformRelationship,
    "platform_inner_configuration_platform",
    "/platforms/<int:id>/relationships/inner-configuration-platform",
)
api.route(
    PlatformRelationship,
    "platform_inner_configuration_device",
    "/platforms/<int:id>/relationships/inner-configuration-device",
)
api.route(
    PlatformRelationship,
    "platform_outer_platform_mount_actions",
    "/platforms/<int:id>/relationships/outer-platform-mount-actions",
)
api.route(
    PlatformRelationship,
    "platform_outer_device_mount_actions",
    "/platforms/<int:id>/relationships/outer-device-mount-actions",
)

# Platform Attachment
api.route(
    PlatformAttachmentList,
    "platform_attachment_list",
    "/platform-attachments",
    "/platforms/<int:platform_id>/platform-attachments",
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
# configuration Attachment
api.route(
    ConfigurationAttachmentList,
    "configuration_attachment_list",
    "/configuration-attachments",
    "/configuration/<int:configuration_id>/configuration-attachments",
)
api.route(
    ConfigurationAttachmentDetail,
    "configuration_attachment_detail",
    "/configuration-attachments/<int:id>",
)
api.route(
    ConfigurationAttachmentRelationship,
    "configuration_attachment_configuration",
    "/configuration-attachments/<int:id>/relationships/configuration",
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
    "/devices/<int:id>/relationships/updated-user",
)
api.route(
    DeviceRelationship,
    "device_device_attachments",
    "/devices/<int:id>/relationships/device-attachments",
)
api.route(
    DeviceRelationship,
    "device_device_properties",
    "/devices/<int:id>/relationships/device-properties",
)
api.route(
    DeviceRelationship,
    "device_customfields",
    "/devices/<int:id>/relationships/customfields",
)
api.route(
    DeviceRelationship,
    "device_generic_device_actions",
    "/devices/<int:id>/relationships/generic-device-actions",
)
api.route(
    DeviceRelationship,
    "device_device_mount_actions",
    "/devices/<int:id>/relationships/device-mount-actions",
)
api.route(
    DeviceRelationship,
    "device_device_unmount_actions",
    "/devices/<int:id>/relationships/device-unmount-actions",
)

api.route(
    DeviceRelationship,
    "device_device_calibration_actions",
    "/devices/<int:id>/relationships/device-calibration-actions",
)
api.route(
    DeviceRelationship,
    "device_device_software_update_actions",
    "/devices/<int:id>/relationships/device-software-update-actions",
)
api.route(
    DeviceRelationship,
    "device_configuration_device",
    "/devices/<int:id>/relationships/configuration-device",
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
    "device_attachment_device",
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
    "/customfields/<int:id>/relationships/device",
)

# Contact
api.route(
    ContactList,
    "contact_list",
    "/contacts",
    "/devices/<int:device_id>/contacts",
    "/platforms/<int:platform_id>/contacts",
    "/configurations/<int:configuration_id>/contacts",
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
    "/configurations/<int:id>/relationships/updated-user",
)
api.route(
    PlatformRelationship,
    "configuration_generic_configuration_actions",
    "/configurations/<int:id>/relationships/generic-configuration-actions",
)
api.route(
    PlatformRelationship,
    "configuration_device_mount_actions",
    "/configurations/<int:id>/relationships/device-mount-actions",
)
api.route(
    PlatformRelationship,
    "configuration_device_unmount_actions",
    "/configurations/<int:id>/relationships/device-unmount-actions",
)
api.route(
    PlatformRelationship,
    "configuration_platform_mount_actions",
    "/configurations/<int:id>/relationships/platform-mount-actions",
)
api.route(
    PlatformRelationship,
    "configuration_platform_unmount_actions",
    "/configurations/<int:id>/relationships/platform-unmount-actions",
)
api.route(
    PlatformRelationship,
    "configuration_configuration_static_location_begin_actions",
    "/configurations/<int:id>/relationships/configuration-static-location-begin-actions",
)
api.route(
    PlatformRelationship,
    "configuration_configuration_static_location_end_actions",
    "/configurations/<int:id>/relationships/configuration-static-location-end-actions",
)
api.route(
    PlatformRelationship,
    "configuration_configuration_dynamic_location_begin_actions",
    "/configurations/<int:id>/relationships/configuration-dynamic-location-begin-actions",
)
api.route(
    PlatformRelationship,
    "configuration_configuration_dynamic_location_end_actions",
    "/configurations/<int:id>/relationships/configuration-dynamic-location-end-actions",
)
# GenericDeviceAction
api.route(
    GenericDeviceActionList,
    "generic_device_action_list",
    "/generic-device-actions",
    "/devices/<int:device_id>/generic-device-actions",
)
api.route(
    GenericDeviceActionDetail,
    "generic_device_action_detail",
    "/generic-device-actions/<int:id>",
)
api.route(
    GenericDeviceActionRelationship,
    "generic_device_action_device",
    "/generic-device-actions/<int:id>/relationships/device",
)
api.route(
    GenericDeviceActionRelationship,
    "generic_device_action_contact",
    "/generic-device-actions/<int:id>/relationships/contact",
)
api.route(
    GenericDeviceActionRelationship,
    "generic_device_action_attachment",
    "/generic-device-actions/<int:id>/relationships/attachment",
)
api.route(
    GenericDeviceActionRelationship,
    "generic_device_action_created_user",
    "/generic-device-actions/<int:id>/relationships/created-user",
)
api.route(
    GenericDeviceActionRelationship,
    "generic_device_action_updated_user",
    "/generic-device-actions/<int:id>/relationships/updated-user",
)
api.route(
    GenericDeviceActionRelationship,
    "generic_device_action_attachments",
    "/generic-device-actions/<int:id>/relationships/generic-device-action-attachments",
)
# GenericDeviceActionAttachment
api.route(
    GenericDeviceActionAttachmentList,
    "generic_device_action_attachment_list",
    "/generic-device-action-attachments",
)
api.route(
    GenericDeviceActionAttachmentDetail,
    "generic_device_action_attachment_detail",
    "/generic-device-action-attachments/<int:id>",
)
api.route(
    GenericDeviceActionAttachmentRelationship,
    "generic_device_action_attachment_action",
    "/generic-device-action-attachments/<int:id>/relationships/action",
)
api.route(
    GenericDeviceActionAttachmentRelationship,
    "generic_device_action_attachment_attachment",
    "/generic-device-action-attachments/<int:id>/relationships/attachment",
)
# GenericPlatformAction
api.route(
    GenericPlatformActionList,
    "generic_platform_action_list",
    "/generic-platform-actions",
    "/platforms/<int:platform_id>/generic-platform-actions",
)
api.route(
    GenericPlatformActionDetail,
    "generic_platform_action_detail",
    "/generic-platform-actions/<int:id>",
)
api.route(
    GenericPlatformActionRelationship,
    "generic_platform_action_platform",
    "/generic-platform-actions/<int:id>/relationships/platform",
)
api.route(
    GenericPlatformActionRelationship,
    "generic_platform_action_contact",
    "/generic-platform-actions/<int:id>/relationships/contact",
)
api.route(
    GenericPlatformActionRelationship,
    "generic_platform_action_attachment",
    "/generic-platform-actions/<int:id>/relationships/attachment",
)
api.route(
    GenericPlatformActionRelationship,
    "generic_platform_action_created_user",
    "/generic-platform-actions/<int:id>/relationships/created-user",
)
api.route(
    GenericPlatformActionRelationship,
    "generic_platform_action_updated_user",
    "/generic-platform-actions/<int:id>/relationships/updated-user",
)
api.route(
    GenericPlatformActionRelationship,
    "generic_platform_action_attachments",
    "/generic-platform-actions/<int:id>/relationships/generic-platform-action-attachments",
)
# GenericPlatformActionAttachment
api.route(
    GenericPlatformActionAttachmentList,
    "generic_platform_action_attachment_list",
    "/generic-platform-action-attachments",
)
api.route(
    GenericPlatformActionAttachmentDetail,
    "generic_platform_action_attachment_detail",
    "/generic-platform-action-attachments/<int:id>",
)
api.route(
    GenericPlatformActionAttachmentRelationship,
    "generic_platform_action_attachment_action",
    "/generic-platform-action-attachments/<int:id>/relationships/action",
)
api.route(
    GenericPlatformActionAttachmentRelationship,
    "generic_platform_action_attachment_attachment",
    "/generic-platform-action-attachments/<int:id>/relationships/attachment",
)

# GenericConfigurationAction
api.route(
    GenericConfigurationActionList,
    "generic_configuration_action_list",
    "/generic-configuration-actions",
    "/configurations/<int:configuration_id>/generic-configuration-actions",
)
api.route(
    GenericConfigurationActionDetail,
    "generic_configuration_action_detail",
    "/generic-configuration-actions/<int:id>",
)
api.route(
    GenericConfigurationActionRelationship,
    "generic_configuration_action_configuration",
    "/generic-configuration-actions/<int:id>/relationships/configuration",
)
api.route(
    GenericConfigurationActionRelationship,
    "generic_configuration_action_contact",
    "/generic-configuration-actions/<int:id>/relationships/contact",
)
api.route(
    GenericConfigurationActionRelationship,
    "generic_configuration_action_attachment",
    "/generic-configuration-actions/<int:id>/relationships/attachment",
)
api.route(
    GenericConfigurationActionRelationship,
    "generic_configuration_action_created_user",
    "/generic-configuration-actions/<int:id>/relationships/created-user",
)
api.route(
    GenericConfigurationActionRelationship,
    "generic_configuration_action_updated_user",
    "/generic-configuration-actions/<int:id>/relationships/updated-user",
)
api.route(
    GenericConfigurationActionRelationship,
    "generic_configuration_action_attachments",
    "/generic-configuration-actions/<int:id>/relationships/generic-configuration-action-attachments",
)
# GenericConfigurationActionAttachment
api.route(
    GenericConfigurationActionAttachmentList,
    "generic_configuration_action_attachment_list",
    "/generic-configuration-action-attachments",
)
api.route(
    GenericConfigurationActionAttachmentDetail,
    "generic_configuration_action_attachment_detail",
    "/generic-configuration-action-attachments/<int:id>",
)
api.route(
    GenericConfigurationActionAttachmentRelationship,
    "generic_configuration_action_attachment_action",
    "/generic-configuration-action-attachments/<int:id>/relationships/action",
)
api.route(
    GenericConfigurationActionAttachmentRelationship,
    "generic_configuration_action_attachment_attachment",
    "/generic-configuration-action-attachments/<int:id>/relationships/attachment",
)

# MountDeviceAction
api.route(
    DeviceMountActionList,
    "device_mount_action_list",
    "/device-mount-actions",
    "/configurations/<int:configuration_id>/device-mount-actions",
    "/devices/<int:device_id>/device-mount-actions",
    "/platforms/<int:parent_platform_id>/device-mount-actions",
)
api.route(
    DeviceMountActionDetail,
    "device_mount_action_detail",
    "/device-mount-actions/<int:id>",
)
api.route(
    DeviceMountActionRelationship,
    "device_mount_action_device",
    "/device-mount-actions/<int:id>/relationships/device",
)
api.route(
    DeviceMountActionRelationship,
    "device_mount_action_contact",
    "/device-mount-actions/<int:id>/relationships/contact",
)
api.route(
    DeviceMountActionRelationship,
    "device_mount_action_configuration",
    "/device-mount-actions/<int:id>/relationships/configuration",
)
api.route(
    DeviceMountActionRelationship,
    "device_mount_action_parent_platform",
    "/device-mount-actions/<int:id>/relationships/parent-platform",
)
api.route(
    DeviceMountActionRelationship,
    "device_mount_action_created_user",
    "/device-mount-actions/<int:id>/relationships/created-user",
)
api.route(
    DeviceMountActionRelationship,
    "device_mount_action_updated_user",
    "/device-mount-actions/<int:id>/relationships/updated-user",
)
# MountPlatformAction
api.route(
    PlatformMountActionList,
    "platform_mount_action_list",
    "/platform-mount-actions",
    "/configurations/<int:configuration_id>/platform-mount-actions",
    "/platforms/<int:platform_id>/platform-mount-actions",
    "/platforms/<int:parent_platform_id>/parent-platform-mount-actions",
)
api.route(
    PlatformMountActionDetail,
    "platform_mount_action_detail",
    "/platform-mount-actions/<int:id>",
)
api.route(
    PlatformMountActionRelationship,
    "platform_mount_action_platform",
    "/platform-mount-actions/<int:id>/relationships/platform",
)
api.route(
    PlatformMountActionRelationship,
    "platform_mount_action_contact",
    "/platform-mount-actions/<int:id>/relationships/contact",
)
api.route(
    PlatformMountActionRelationship,
    "platform_mount_action_configuration",
    "/platform-mount-actions/<int:id>/relationships/configuration",
)
api.route(
    PlatformMountActionRelationship,
    "platform_mount_action_parent_platform",
    "/platform-mount-actions/<int:id>/relationships/parent-platform",
)
api.route(
    PlatformMountActionRelationship,
    "platform_mount_action_created_user",
    "/platform-mount-actions/<int:id>/relationships/created-user",
)
api.route(
    PlatformMountActionRelationship,
    "platform_mount_action_updated_user",
    "/platform-mount-actions/<int:id>/relationships/updated-user",
)
# DeviceUnmountAction
api.route(
    DeviceUnmountActionList,
    "device_unmount_action_list",
    "/device-unmount-actions",
    "/configurations/<int:configuration_id>/device-unmount-actions",
    "/devices/<int:device_id>/device-unmount-actions",
)
api.route(
    DeviceUnmountActionDetail,
    "device_unmount_action_detail",
    "/device-unmount-actions/<int:id>",
)
api.route(
    DeviceUnmountActionRelationship,
    "device_unmount_action_device",
    "/device-unmount-actions/<int:id>/relationships/device",
)
api.route(
    DeviceUnmountActionRelationship,
    "device_unmount_action_contact",
    "/device-unmount-actions/<int:id>/relationships/contact",
)
api.route(
    DeviceUnmountActionRelationship,
    "device_unmount_action_configuration",
    "/device-unmount-actions/<int:id>/relationships/configuration",
)
api.route(
    DeviceUnmountActionRelationship,
    "device_unmount_action_parent_platform",
    "/device-unmount-actions/<int:id>/relationships/parent-platform",
)
api.route(
    DeviceUnmountActionRelationship,
    "device_unmount_action_created_user",
    "/device-unmount-actions/<int:id>/relationships/created-user",
)
api.route(
    DeviceUnmountActionRelationship,
    "device_unmount_action_updated_user",
    "/device-unmount-actions/<int:id>/relationships/updated-user",
)
# UnMountPlatformAction
api.route(
    PlatformUnmountActionList,
    "platform_unmount_action_list",
    "/platform-unmount-actions",
    "/configurations/<int:configuration_id>/platform-unmount-actions",
    "/platforms/<int:platform_id>/platform-unmount-actions",
)
api.route(
    PlatformUnmountActionDetail,
    "platform_unmount_action_detail",
    "/platform-unmount-actions/<int:id>",
)
api.route(
    PlatformUnmountActionRelationship,
    "platform_unmount_action_platform",
    "/platform-unmount-actions/<int:id>/relationships/platform",
)
api.route(
    PlatformUnmountActionRelationship,
    "platform_unmount_action_contact",
    "/platform-unmount-actions/<int:id>/relationships/contact",
)
api.route(
    PlatformUnmountActionRelationship,
    "platform_unmount_action_configuration",
    "/platform-unmount-actions/<int:id>/relationships/configuration",
)
api.route(
    PlatformUnmountActionRelationship,
    "platform_unmount_action_parent_platform",
    "/platform-unmount-actions/<int:id>/relationships/parent-platform",
)
api.route(
    PlatformUnmountActionRelationship,
    "platform_unmount_action_created_user",
    "/platform-unmount-actions/<int:id>/relationships/created-user",
)
api.route(
    PlatformUnmountActionRelationship,
    "platform_unmount_action_updated_user",
    "/{upa_url}s/<int:id>/relationships/updated-user",
)

# DeviceCalibrationAction
api.route(
    DeviceCalibrationActionList,
    "device_calibration_action_list",
    "/device-calibration-actions",
    "/devices/<int:device_id>/device-calibration-actions",
)
api.route(
    DeviceCalibrationActionDetail,
    "device_calibration_action_detail",
    "/device-calibration-actions/<int:id>",
)
api.route(
    DeviceCalibrationActionRelationship,
    "device_calibration_action_device",
    "/device-calibration-actions/<int:id>/relationships/device",
)
api.route(
    DeviceCalibrationActionRelationship,
    "device_calibration_action_contact",
    "/device-calibration-actions/<int:id>/relationships/contact",
)
api.route(
    DeviceCalibrationActionRelationship,
    "device_calibration_action_attachments",
    "/device-calibration-actions/<int:id>/relationships/device-calibration-attachments",
)
api.route(
    DeviceCalibrationActionRelationship,
    "device_calibration_device_property_calibrations",
    "/device-calibration-actions/<int:id>/relationships/device-property-calibrations",
)
# DeviceCalibrationAttachment
api.route(
    DeviceCalibrationAttachmentList,
    "device_calibration_attachment_list",
    "/device-calibration-attachments",
)
api.route(
    DeviceCalibrationAttachmentDetail,
    "device_calibration_attachment_detail",
    "/device-calibration-attachments/<int:id>",
)
api.route(
    DeviceCalibrationAttachmentRelationship,
    "device_calibration_attachment_action",
    "/device-calibration-attachments/<int:id>/relationships/action",
)
api.route(
    DeviceCalibrationAttachmentRelationship,
    "device_calibration_attachment_attachment",
    "/device-calibration-attachments/<int:id>/relationships/attachment",
)
# DeviceSoftwareUpdateAction
api.route(
    DeviceSoftwareUpdateActionList,
    "device_software_update_action_list",
    "/device-software-update-actions",
    "/devices/<int:device_id>/device-software-update-actions",
)
api.route(
    DeviceSoftwareUpdateActionDetail,
    "device_software_update_action_detail",
    "/device-software-update-actions/<int:id>",
)
api.route(
    DeviceSoftwareUpdateActionRelationship,
    "device_software_update_action_device",
    "/device-software-update-actions/<int:id>/relationships/device",
)
api.route(
    DeviceSoftwareUpdateActionRelationship,
    "device_software_update_action_contact",
    "/device-software-update-actions/<int:id>/relationships/contact",
)
api.route(
    DeviceSoftwareUpdateActionRelationship,
    "device_software_update_action_created_user",
    "/device-software-update-actions/<int:id>/relationships/created-user",
)
api.route(
    DeviceSoftwareUpdateActionRelationship,
    "device_software_update_action_updated_user",
    "/device-software-update-actions/<int:id>/relationships/updated-user",
)
api.route(
    DeviceSoftwareUpdateActionRelationship,
    "device_software_update_action_attachments",
    "/device-software-update-actions/<int:id>/relationships/device-software-update-action-attachments",
)

# DeviceSoftwareUpdateActionAttachment
api.route(
    DeviceSoftwareUpdateActionAttachmentList,
    "device_software_update_action_attachment_list",
    "/device-software-update-action-attachments",
)
api.route(
    DeviceSoftwareUpdateActionAttachmentDetail,
    "device_software_update_action_attachment_detail",
    "/device-software-update-action-attachments/<int:id>",
)
api.route(
    DeviceSoftwareUpdateActionAttachmentRelationship,
    "device_software_update_action_attachment_action",
    "/device-software-update-action-attachments/<int:id>/relationships/action",
)
api.route(
    DeviceSoftwareUpdateActionAttachmentRelationship,
    "device_software_update_action_attachment_attachment",
    "/device-software-update-action-attachments/<int:id>/relationships/attachment",
)
# PlatformSoftwareUpdateAction
api.route(
    PlatformSoftwareUpdateActionList,
    "platform_software_update_action_list",
    "/platform-software-update-actions",
    "/platforms/<int:platform_id>/platform-software-update-actions",
)
api.route(
    PlatformSoftwareUpdateActionDetail,
    "platform_software_update_action_detail",
    "/platform-software-update-actions/<int:id>",
)
api.route(
    PlatformSoftwareUpdateActionRelationship,
    "platform_software_update_action_platform",
    "/platform-software-update-actions/<int:id>/relationships/platform",
)
api.route(
    PlatformSoftwareUpdateActionRelationship,
    "platform_software_update_action_contact",
    "/platform-software-update-actions/<int:id>/relationships/contact",
)
api.route(
    PlatformSoftwareUpdateActionRelationship,
    "platform_software_update_action_created_user",
    "/platform-software-update-actions/<int:id>/relationships/created-user",
)
api.route(
    PlatformSoftwareUpdateActionRelationship,
    "platform_software_update_action_updated_user",
    "/platform-software-update-actions/<int:id>/relationships/updated-user",
)
api.route(
    PlatformSoftwareUpdateActionRelationship,
    "platform_software_update_action_attachments",
    "/platform-software-update-actions/<int:id>/relationships/platform-software-update-action-attachments",
)

# PlatformSoftwareUpdateActionAttachment
api.route(
    PlatformSoftwareUpdateActionAttachmentList,
    "platform_software_update_action_attachment_list",
    "/platform-software-update-action-attachments",
)
api.route(
    PlatformSoftwareUpdateActionAttachmentDetail,
    "platform_software_update_action_attachment_detail",
    "/platform-software-update-action-attachments/<int:id>",
)
api.route(
    PlatformSoftwareUpdateActionAttachmentRelationship,
    "platform_software_update_action_attachment_action",
    "/platform-software-update-action-attachments/<int:id>/relationships/action",
)
api.route(
    PlatformSoftwareUpdateActionAttachmentRelationship,
    "platform_software_update_action_attachment_attachment",
    "/platform-software-update-action-attachments/<int:id>/relationships/attachment",
)

# DevicePropertyCalibration

api.route(
    DevicePropertyCalibrationList,
    "device_property_calibration_list",
    "/device-property-calibrations",
    "/device-calibration-actions/<int:device_calibration_action_id>/device-property-calibrations",
    "/device-properties/<int:device_property_id>/device-property-calibrations",
    "/devices/<int:device_id>/device-property-calibrations",
)
api.route(
    DevicePropertyCalibrationDetail,
    "device_property_calibration_detail",
    "/device-property-calibrations/<int:id>",
)
api.route(
    DevicePropertyCalibrationRelationship,
    "device_property_calibration_calibration_action",
    "/device-property-calibrations/<int:id>/relationships/calibration-action",
)
api.route(
    DevicePropertyCalibrationRelationship,
    "device_property_calibration_device_property",
    "/device-property-calibrations/<int:id>/relationships/device-property",
)

# ConfigurationStaticLocationBeginAction

api.route(
    ConfigurationStaticLocationBeginActionList,
    "configuration_static_location_begin_action_list",
    "/static-location-begin-actions",
    "/configurations/<int:configuration_id>/static-location-begin-actions",
)
api.route(
    ConfigurationStaticLocationBeginActionDetail,
    "configuration_static_location_begin_action_detail",
    "/static-location-begin-actions/<int:id>",
)
api.route(
    ConfigurationStaticLocationBeginActionRelationship,
    "configuration_static_location_begin_action_contact",
    "/static-location-begin-actions/<int:id>/relationships/contact",
)
api.route(
    ConfigurationStaticLocationBeginActionRelationship,
    "configuration_static_location_begin_action_configuration",
    "/static-location-begin-actions/<int:id>/relationships/configuration",
)

# ConfigurationStaticLocationEndAction

api.route(
    ConfigurationStaticLocationEndActionList,
    "configuration_static_location_end_action_list",
    "/static-location-end-actions",
    "/configurations/<int:configuration_id>/static-location-end-actions",
)
api.route(
    ConfigurationStaticLocationEndActionDetail,
    "configuration_static_location_end_action_detail",
    "/static-location-end-actions/<int:id>",
)
api.route(
    ConfigurationStaticLocationEndActionRelationship,
    "configuration_static_location_end_action_contact",
    "/static-location-end-actions/<int:id>/relationships/contact",
)
api.route(
    ConfigurationStaticLocationEndActionRelationship,
    "configuration_static_location_end_action_configuration",
    "/static-location-end-actions/<int:id>/relationships/configuration",
)

# ConfigurationDynamicLocationBeginAction

api.route(
    ConfigurationDynamicLocationBeginActionList,
    "configuration_dynamic_location_begin_action_list",
    "/dynamic-location-begin-actions",
    "/configurations/<int:configuration_id>/dynamic-location-begin-action",
    "/device-properties/<int:x_property_id>/dynamic-location-begin-actions-x",
    "/device-properties/<int:y_property_id>/dynamic-location-begin-actions-y",
    "/device-properties/<int:z_property_id>/dynamic-location-begin-actions-z",
)
api.route(
    ConfigurationDynamicLocationBeginActionDetail,
    "configuration_dynamic_location_begin_action_detail",
    "/dynamic-location-begin-actions/<int:id>",
)
api.route(
    ConfigurationDynamicLocationBeginActionRelationship,
    "configuration_dynamic_location_begin_action_contact",
    "/dynamic-location-begin-actions/<int:id>/relationships/contact",
)
api.route(
    ConfigurationDynamicLocationBeginActionRelationship,
    "configuration_dynamic_location_begin_action_configuration",
    "/dynamic-location-begin-actions/<int:id>/relationships/configuration",
)
api.route(
    ConfigurationDynamicLocationBeginActionRelationship,
    "configuration_dynamic_location_begin_action_x_property",
    "/dynamic-location-begin-actions/<int:id>/relationships/x-property",
)
api.route(
    ConfigurationDynamicLocationBeginActionRelationship,
    "configuration_dynamic_location_begin_action_y_property",
    "/dynamic-location-begin-actions/<int:id>/relationships/y-property",
)
api.route(
    ConfigurationDynamicLocationBeginActionRelationship,
    "configuration_dynamic_location_begin_action_z_property",
    "/dynamic-location-begin-actions/<int:id>/relationships/z-property",
)

# ConfigurationDynamicLocationEndAction

api.route(
    ConfigurationDynamicLocationEndActionList,
    "configuration_dynamic_location_end_action_list",
    "/dynamic-location-end-actions",
    "/configurations/<int:configuration_id>/dynamic-location-end-actions",
)
api.route(
    ConfigurationDynamicLocationEndActionDetail,
    "configuration_dynamic_location_end_action_detail",
    "/dynamic-location-end-actions/<int:id>",
)
api.route(
    ConfigurationDynamicLocationEndActionRelationship,
    "configuration_dynamic_location_end_action_contact",
    "/dynamic-location-end-actions/<int:id>/relationships/contact",
)
api.route(
    ConfigurationDynamicLocationEndActionRelationship,
    "configuration_dynamic_location_end_action_configuration",
    "/dynamic-location-end-actions/<int:id>/relationships/configuration",
)