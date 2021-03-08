import stringcase

from project.api.ping import Ping
from project.api.resourceManager import *
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
    "/platforms/<int:id>/relationships/created-user",
)
api.route(
    PlatformRelationship,
    "platform_updated_user",
    "/platforms/<int:id>/relationships/updated-user",
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
    "/devices/<int:id>/relationships/updated-user",
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
    "/configurations/<int:id>/relationships/updated-user",
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
gda = stringcase.snakecase("genericDeviceAction")
gda_url = stringcase.spinalcase(gda)
api.route(GenericDeviceActionList, f"{gda}_list", f"/{gda_url}s")
api.route(GenericDeviceActionDetail, f"{gda}_detail", f"/{gda_url}s/<int:id>")
api.route(
    GenericDeviceActionRelationship,
    f"{gda}_device",
    f"/{gda_url}s/<int:id>/relationships/device",
)
api.route(
    GenericDeviceActionRelationship,
    f"{gda}_contact",
    f"/{gda_url}s/<int:id>/relationships/contact",
)
api.route(
    GenericDeviceActionRelationship,
    f"{gda}s_attachment",
    f"/{gda_url}s/<int:id>/relationships/attachment",
)
api.route(
    GenericDeviceActionRelationship,
    f"{gda}_created_user",
    f"/{gda_url}s/<int:id>/relationships/created-user",
)
api.route(
    GenericDeviceActionRelationship,
    f"{gda}_updated_user",
    f"/{gda_url}s/<int:id>/relationships/updated-user",
)
# GenericDeviceActionAttachment
gda_a = stringcase.snakecase("genericDeviceActionAttachment")
gda_a_url = stringcase.spinalcase(gda_a)
api.route(GenericDeviceActionAttachmentList, f"{gda_a}_list", f"/{gda_a_url}s")
api.route(
    GenericDeviceActionAttachmentDetail, f"{gda_a}_detail", f"/{gda_a_url}s/<int:id>"
)
api.route(
    GenericDeviceActionAttachmentRelationship,
    f"{gda_a}_action",
    f"/{gda_a_url}s/<int:id>/relationships/action",
)
api.route(
    GenericDeviceActionAttachmentRelationship,
    f"{gda_a}_attachment",
    f"/{gda_a_url}s/<int:id>/relationships/attachment",
)
# GenericPlatformAction
gpa = stringcase.snakecase("genericPlatformAction")
gpa_url = stringcase.spinalcase(gpa)
api.route(GenericPlatformActionList, f"{gpa}_list", f"/{gpa_url}s")
api.route(GenericPlatformActionDetail, f"{gpa}_detail", f"/{gpa_url}s/<int:id>")
api.route(
    GenericPlatformActionRelationship,
    f"{gpa}_platform",
    f"/{gpa_url}s/<int:id>/relationships/platform",
)
api.route(
    GenericPlatformActionRelationship,
    f"{gpa}_contact",
    f"/{gpa_url}s/<int:id>/relationships/contact",
)
api.route(
    GenericPlatformActionRelationship,
    f"{gpa}s_attachment",
    f"/{gpa_url}s/<int:id>/relationships/attachment",
)
api.route(
    GenericPlatformActionRelationship,
    f"{gpa}_created_user",
    f"/{gpa_url}s/<int:id>/relationships/created-user",
)
api.route(
    GenericPlatformActionRelationship,
    f"{gpa}_updated_user",
    f"/{gpa_url}s/<int:id>/relationships/updated-user",
)
# GenericPlatformActionAttachment
gpa_a = stringcase.snakecase("genericPlatformActionAttachment")
gpa_a_url = stringcase.spinalcase(gpa_a)
api.route(GenericPlatformActionAttachmentList, f"{gpa_a}_list", f"/{gpa_a_url}s")
api.route(
    GenericPlatformActionAttachmentDetail, f"{gpa_a}_detail", f"/{gpa_a_url}s/<int:id>"
)
api.route(
    GenericPlatformActionAttachmentRelationship,
    f"{gpa_a}_action",
    f"/{gpa_a_url}s/<int:id>/relationships/action",
)
api.route(
    GenericPlatformActionAttachmentRelationship,
    f"{gpa_a}_attachment",
    f"/{gpa_a_url}s/<int:id>/relationships/attachment",
)

# GenericConfigurationAction
gca = stringcase.snakecase("genericConfigurationAction")
gca_url = stringcase.spinalcase(gca)
api.route(GenericConfigurationActionList, f"{gca}_list", f"/{gca_url}s")
api.route(GenericConfigurationActionDetail, f"{gca}_detail", f"/{gca_url}s/<int:id>")
api.route(
    GenericConfigurationActionRelationship,
    f"{gca}_configuration",
    f"/{gca_url}s/<int:id>/relationships/configuration",
)
api.route(
    GenericConfigurationActionRelationship,
    f"{gca}_contact",
    f"/{gca_url}s/<int:id>/relationships/contact",
)
api.route(
    GenericConfigurationActionRelationship,
    f"{gca}s",
    f"/{gca_url}s/<int:id>/relationships/attachment",
)
api.route(
    GenericConfigurationActionRelationship,
    f"{gca}_created_user",
    f"/{gca_url}s/<int:id>/relationships/created-user",
)
api.route(
    GenericConfigurationActionRelationship,
    f"{gca}_updated_user",
    f"/{gca_url}s/<int:id>/relationships/updated-user",
)
# GenericConfigurationActionAttachment
gca_a = stringcase.snakecase("genericConfigurationActionAttachment")
gca_a_url = stringcase.spinalcase(gca_a)
api.route(GenericConfigurationActionAttachmentList, f"{gca_a}_list", f"/{gca_a_url}s")
api.route(
    GenericConfigurationActionAttachmentDetail,
    f"{gca_a}_detail",
    f"/{gca_a_url}s/<int:id>",
)
api.route(
    GenericConfigurationActionAttachmentRelationship,
    f"{gca_a}_action",
    f"/{gca_a_url}s/<int:id>/relationships/action",
)
api.route(
    GenericConfigurationActionAttachmentRelationship,
    f"{gca_a}_attachment",
    f"/{gca_a_url}s/<int:id>/relationships/attachment",
)

# MountDeviceAction
mda = stringcase.snakecase("DeviceMountAction")
mda_url = stringcase.spinalcase(mda)
api.route(DeviceMountActionList, f"{mda}_list", f"/{mda_url}s")
api.route(DeviceMountActionDetail, f"{mda}_detail", f"/{mda_url}s/<int:id>")
api.route(
    DeviceMountActionRelationship,
    f"{mda}_device",
    f"/{mda_url}s/<int:id>/relationships/device",
)
api.route(
    DeviceMountActionRelationship,
    f"{mda}_contact",
    f"/{mda_url}s/<int:id>/relationships/contact",
)
api.route(
    DeviceMountActionRelationship,
    f"{mda}_configuration",
    f"/{mda_url}s/<int:id>/relationships/configuration",
)
api.route(
    DeviceMountActionRelationship,
    f"{mda}_parent_platform",
    f"/{mda_url}s/<int:id>/relationships/parent-platform",
)
api.route(
    DeviceMountActionRelationship,
    f"{mda}_created_user",
    f"/{mda_url}s/<int:id>/relationships/created-user",
)
api.route(
    DeviceMountActionRelationship,
    f"{mda}_updated_user",
    f"/{mda_url}s/<int:id>/relationships/updated-user",
)
# MountPlatformAction
mpa = stringcase.snakecase("PlatformMountAction")
mpa_url = stringcase.spinalcase(mpa)
api.route(PlatformMountActionList, f"{mpa}_list", f"/{mpa_url}s")
api.route(PlatformMountActionDetail, f"{mpa}_detail", f"/{mpa_url}s/<int:id>")
api.route(
    PlatformMountActionRelationship,
    f"{mpa}_platform",
    f"/{mpa_url}s/<int:id>/relationships/device",
)
api.route(
    PlatformMountActionRelationship,
    f"{mpa}_contact",
    f"/{mpa_url}s/<int:id>/relationships/contact",
)
api.route(
    PlatformMountActionRelationship,
    f"{mpa}_configuration",
    f"/{mpa_url}s/<int:id>/relationships/configuration",
)
api.route(
    PlatformMountActionRelationship,
    f"{mpa}_parent_platform",
    f"/{mpa_url}s/<int:id>/relationships/parent-platform",
)
api.route(
    PlatformMountActionRelationship,
    f"{mpa}_created_user",
    f"/{mpa_url}s/<int:id>/relationships/created-user",
)
api.route(
    PlatformMountActionRelationship,
    f"{mpa}_updated_user",
    f"/{mpa_url}s/<int:id>/relationships/updated-user",
)
# UnMountDeviceAction
uda = stringcase.snakecase("deviceUnmountAction")
uda_url = stringcase.spinalcase(uda)
api.route(DeviceUnmountActionList, f"{uda}_list", f"/{uda_url}s")
api.route(DeviceUnmountActionDetail, f"{uda}_detail", f"/{uda_url}s/<int:id>")
api.route(
    DeviceUnmountActionRelationship,
    f"{uda}_device",
    f"/{uda_url}s/<int:id>/relationships/device",
)
api.route(
    DeviceUnmountActionRelationship,
    f"{uda}_contact",
    f"/{uda_url}s/<int:id>/relationships/contact",
)
api.route(
    DeviceUnmountActionRelationship,
    f"{uda}_configuration",
    f"/{uda_url}s/<int:id>/relationships/configuration",
)
api.route(
    DeviceUnmountActionRelationship,
    f"{uda}_parent_platform",
    f"/{uda_url}s/<int:id>/relationships/parent-platform",
)
# UnMountPlatformAction
upa = stringcase.snakecase("platformUnmountAction")
upa_url = stringcase.spinalcase(upa)
api.route(PlatformUnmountActionList, f"{upa}_list", f"/{upa_url}s")
api.route(PlatformUnmountActionDetail, f"{upa}_detail", f"/{upa_url}s/<int:id>")
api.route(
    PlatformUnmountActionRelationship,
    f"{upa}_platform",
    f"/{upa_url}s/<int:id>/relationships/device",
)
api.route(
    PlatformUnmountActionRelationship,
    f"{upa}_contact",
    f"/{upa_url}s/<int:id>/relationships/contact",
)
api.route(
    PlatformUnmountActionRelationship,
    f"{upa}_configuration",
    f"/{upa_url}s/<int:id>/relationships/configuration",
)
api.route(
    PlatformUnmountActionRelationship,
    f"{upa}_parent_platform",
    f"/{upa_url}s/<int:id>/relationships/parent-platform",
)

# device_calibration_action
dca = stringcase.snakecase("deviceCalibrationAction")
dca_url = stringcase.spinalcase(dca)
api.route(DeviceCalibrationActionList, f"{dca}_list", f"/{dca_url}s")
api.route(DeviceCalibrationActionDetail, f"{dca}_detail", f"/{dca_url}s/<int:id>")
api.route(
    DeviceCalibrationActionRelationship,
    f"{dca}_device",
    f"/{dca_url}s/<int:id>/relationships/device",
)
api.route(
    DeviceCalibrationActionRelationship,
    f"{dca}_contact",
    f"/{dca_url}s/<int:id>/relationships/contact",
)
# DeviceCalibrationAttachment
dca_a = stringcase.snakecase("deviceCalibrationAttachment")
dca_a_url = stringcase.spinalcase(dca_a)
api.route(DeviceCalibrationAttachmentList, f"{dca_a}_list", f"/{dca_a_url}s")
api.route(
    DeviceCalibrationAttachmentDetail, f"{dca_a}_detail", f"/{dca_a_url}s/<int:id>"
)
api.route(
    DeviceCalibrationAttachmentRelationship,
    f"{dca_a}_action",
    f"/{dca_a_url}s/<int:id>/relationships/action",
)
api.route(
    DeviceCalibrationAttachmentRelationship,
    f"{dca_a}_attachment",
    f"/{dca_a_url}s/<int:id>/relationships/attachment",
)
# DeviceSoftwareUpdateAction
dsu = stringcase.snakecase("deviceSoftwareUpdateAction")
dsu_url = stringcase.spinalcase(dsu)
api.route(DeviceSoftwareUpdateActionList, f"{dsu}_list", f"/{dsu_url}s")
api.route(DeviceSoftwareUpdateActionDetail, f"{dsu}_detail", f"/{dsu_url}s/<int:id>")
api.route(
    DeviceSoftwareUpdateActionRelationship,
    f"{dsu}_device",
    f"/{dsu_url}s/<int:id>/relationships/device",
)
api.route(
    DeviceSoftwareUpdateActionRelationship,
    f"{dsu}_contact",
    f"/{dsu_url}s/<int:id>/relationships/contact",
)
api.route(
    DeviceSoftwareUpdateActionRelationship,
    f"{dsu}_created_user",
    f"/{dsu_url}s/<int:id>/relationships/created-user",
)
api.route(
    DeviceSoftwareUpdateActionRelationship,
    f"{dsu}_updated_user",
    f"/{dsu_url}s/<int:id>/relationships/updated-user",
)

# DeviceSoftwareUpdateActionAttachment
dsu_a = stringcase.snakecase("deviceSoftwareUpdateActionAttachment")
dsu_a_url = stringcase.spinalcase(dsu_a)
api.route(DeviceSoftwareUpdateActionAttachmentList, f"{dsu_a}_list", f"/{dsu_a_url}s")
api.route(
    DeviceSoftwareUpdateActionAttachmentDetail,
    f"{dsu_a}_detail",
    f"/{dsu_a_url}s/<int:id>",
)
api.route(
    DeviceSoftwareUpdateActionAttachmentRelationship,
    f"{dsu_a}_action",
    f"/{dsu_a_url}s/<int:id>/relationships/action",
)
api.route(
    DeviceSoftwareUpdateActionAttachmentRelationship,
    f"{dsu_a}_attachment",
    f"/{dsu_a_url}s/<int:id>/relationships/attachment",
)
# PlatformSoftwareUpdateAction
psu = stringcase.snakecase("platformSoftwareUpdateAction")
psu_url = stringcase.spinalcase(psu)
api.route(PlatformSoftwareUpdateActionList, f"{psu}_list", f"/{psu_url}s")
api.route(
    PlatformSoftwareUpdateActionDetail,
    f"{psu}_detail",
    f"/{psu_url}s/<int:id>",
)
api.route(
    PlatformSoftwareUpdateActionRelationship,
    f"{psu}_platform",
    f"/{psu_url}s/<int:id>/relationships/platform",
)
api.route(
    PlatformSoftwareUpdateActionRelationship,
    f"{psu}_contact",
    f"/{psu_url}s/<int:id>/relationships/contact",
)
api.route(
    PlatformSoftwareUpdateActionRelationship,
    f"{psu}_created_user",
    f"/{psu_url}s/<int:id>/relationships/created-user",
)
api.route(
    PlatformSoftwareUpdateActionRelationship,
    f"{psu}_updated_user",
    f"/{psu_url}s/<int:id>/relationships/updated-user",
)

# PlatformSoftwareUpdateActionAttachment
psu_a = stringcase.snakecase("platformSoftwareUpdateActionAttachment")
psu_a_url = stringcase.spinalcase(psu_a)
api.route(PlatformSoftwareUpdateActionAttachmentList, f"{psu_a}_list", f"/{psu_a_url}s")
api.route(
    PlatformSoftwareUpdateActionAttachmentDetail,
    f"{psu_a}_detail",
    f"/{psu_a_url}s/<int:id>",
)
api.route(
    PlatformSoftwareUpdateActionAttachmentRelationship,
    f"{psu_a}_action",
    f"/{psu_a_url}s/<int:id>/relationships/action",
)
api.route(
    PlatformSoftwareUpdateActionAttachmentRelationship,
    f"{psu_a}_attachment",
    f"/{psu_a_url}s/<int:id>/relationships/attachment",
)

# DevicePropertyCalibration
dpa = stringcase.snakecase("devicePropertyCalibration")
dpa_url = stringcase.spinalcase(dpa)
api.route(DevicePropertyCalibrationList, f"{dpa}_list", f"/{dpa_url}s")
api.route(
    DevicePropertyCalibrationDetail,
    f"{dpa}_detail",
    f"/{dpa_url}s/<int:id>",
)
api.route(
    DevicePropertyCalibrationRelationship,
    f"{dpa}_calibration_action",
    f"/{dpa_url}s/<int:id>/relationships/calibration_action",
)
api.route(
    DevicePropertyCalibrationRelationship,
    f"{dpa}_device",
    f"/{dpa_url}s/<int:id>/relationships/device",
)
