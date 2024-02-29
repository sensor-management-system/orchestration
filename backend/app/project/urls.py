# SPDX-FileCopyrightText: 2020 - 2023
# - Martin Abbrent <martin.abbrent@ufz.de>
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Wilhelm Becker <wilhelm.becker@gfz-potsdam.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
# - Luca Johannes Nendel <luca-johannes.nendel@ufz.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0


"""Routing for the urls & the endpoints."""

from flask_rest_jsonapi import Api

from project.api.resources import *

from .api.resources.permission_group_resources import PermissionGroups

api = Api()

api.route(Ping, "test_connection", "/ping")
api.route(PermissionGroups, "permission_group_list", "/permission-groups")

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

# Platform Parameter
api.route(
    PlatformParameterDetail,
    "platform_parameter_detail",
    "/platform-parameters/<int:id>",
)
api.route(
    PlatformParameterList,
    "platform_parameter_list",
    "/platform-parameters",
    "/platforms/<int:platform_id>/platform-parameters",
)
# Platform Parameter Value Change Action
api.route(
    PlatformParameterValueChangeActionDetail,
    "platform_parameter_value_change_action_detail",
    "/platform-parameter-value-change-actions/<int:id>",
)
api.route(
    PlatformParameterValueChangeActionList,
    "platform_parameter_value_change_action_list",
    "/platform-parameter-value-change-actions",
    "/platforms/<int:platform_id>/platform-parameter-value-change-actions"
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
# Platform Images
api.route(
    PlatformImageList,
    "platform_image_list",
    "/platform-images",
    "/platforms/<int:platform_id>/platform-images",
)
api.route(
    PlatformImageDetail,
    "platform_image_detail",
    "/platform-images/<int:id>"
)
# configuration Attachment
api.route(
    ConfigurationAttachmentList,
    "configuration_attachment_list",
    "/configuration-attachments",
    "/configurations/<int:configuration_id>/configuration-attachments",
)
api.route(
    ConfigurationAttachmentDetail,
    "configuration_attachment_detail",
    "/configuration-attachments/<int:id>",
)
# Configuration Images
api.route(
    ConfigurationImageList,
    "configuration_image_list",
    "/configuration-images",
    "/configurations/<int:configuration_id>/configuration-images",
)
api.route(
    ConfigurationImageDetail,
    "configuration_image_detail",
    "/configuration-images/<int:id>"
)
# site Attachment
api.route(
    SiteAttachmentList,
    "site_attachment_list",
    "/site-attachments",
    "/sites/<int:site_id>/site-attachments",
)
api.route(
    SiteAttachmentDetail,
    "site_attachment_detail",
    "/site-attachments/<int:id>",
)
# Site Images
api.route(
    SiteImageList,
    "site_image_list",
    "/site-images",
    "/sites/<int:site_id>/site-images",
)
api.route(
    SiteImageDetail,
    "site_image_detail",
    "/site-images/<int:id>"
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
# Device Parameter
api.route(
    DeviceParameterDetail,
    "device_parameter_detail",
    "/device-parameters/<int:id>",
)
api.route(
    DeviceParameterList,
    "device_parameter_list",
    "/device-parameters",
    "/devices/<int:device_id>/device-parameters",
)
# Device Parameter Value Change Action
api.route(
    DeviceParameterValueChangeActionDetail,
    "device_parameter_value_change_action_detail",
    "/device-parameter-value-change-actions/<int:id>",
)
api.route(
    DeviceParameterValueChangeActionList,
    "device_parameter_value_change_action_list",
    "/device-parameter-value-change-actions",
    "/devices/<int:device_id>/device-parameter-value-change-actions"
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
# Device Images
api.route(
    DeviceImageList,
    "device_image_list",
    "/device-images",
    "/devices/<int:device_id>/device-images",
)
api.route(
    DeviceImageDetail,
    "device_image_detail",
    "/device-images/<int:id>"
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

# Contact
api.route(
    ContactList,
    "contact_list",
    "/contacts",
    "/devices/<int:device_id>/contacts",
    "/platforms/<int:platform_id>/contacts",
    "/configurations/<int:configuration_id>/contacts",
)
api.route(
    ContactDetail,
    "contact_detail",
    "/contacts/<int:id>",
)
api.route(
    ControllerConfigurationMountingActions,
    "controller_configuration_mounting_actions",
    "/controller/configurations/<int:configuration_id>/mounting-actions",
)
api.route(
    ControllerConfigurationMountingActionTimepoints,
    "controller_configuration_mounting_action_timepoints",
    "/controller/configurations/<int:configuration_id>/mounting-action-timepoints",
)
api.route(
    ControllerConfigurationParameterValues,
    "controller_configuration_parameter_values",
    "/controller/configurations/<int:configuration_id>/parameter-values"
)
api.route(
    ControllerDeviceParameterValues,
    "controller_device_parameter_values",
    "/controller/devices/<int:device_id>/parameter-values"
)
api.route(
    ControllerPlatformParameterValues,
    "controller_platform_parameter_values",
    "/controller/platforms/<int:platform_id>/parameter-values"
)
api.route(
    DeviceAvailabilities,
    "device_availabilities",
    "/controller/device-availabilities",
)
api.route(
    PlatformAvailabilities,
    "platform_availabilities",
    "/controller/platform-availabilities",
)
# User Info
api.route(
    UserInfo,
    "user_info",
    "/user-info",
)
# Users
api.route(
    UserList,
    "user_list",
    "/users",
    "/contacts/<int:id>/users",
)
api.route(UserDetail, "user_detail", "/users/<int:id>")
# User modifications
api.route(AcceptTermsOfUse, "accept_terms_of_use", "/accept-terms-of-use")
api.route(RevokeApikey, "revoke_apikey", "/revoke-apikey")

# Configuration
api.route(
    ConfigurationList,
    "configuration_list",
    "/configurations",
    "/sites/<int:site_id>/configurations",
)
api.route(
    ConfigurationDetail,
    "configuration_detail",
    "/configurations/<int:id>",
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

# ConfigurationStaticLocationBeginAction

api.route(
    ConfigurationStaticLocationBeginActionList,
    "configuration_static_location_begin_action_list",
    "/static-location-actions",
    "/configurations/<int:configuration_id>/static-location-actions",
    "/sites/<int:site_id>/static-location-actions",
)
api.route(
    ConfigurationStaticLocationBeginActionDetail,
    "configuration_static_location_begin_action_detail",
    "/static-location-actions/<int:id>",
)
# ConfigurationDynamicLocationBeginAction

api.route(
    ConfigurationDynamicLocationBeginActionList,
    "configuration_dynamic_location_begin_action_list",
    "/dynamic-location-actions",
    "/configurations/<int:configuration_id>/dynamic-location-actions",
    "/device-properties/<int:x_property_id>/dynamic-location-actions-x",
    "/device-properties/<int:y_property_id>/dynamic-location-actions-y",
    "/device-properties/<int:z_property_id>/dynamic-location-actions-z",
)
api.route(
    ConfigurationDynamicLocationBeginActionDetail,
    "configuration_dynamic_location_begin_action_detail",
    "/dynamic-location-actions/<int:id>",
)

# DeviceRoles
api.route(
    DeviceRoleList,
    "device_contact_role_list",
    "/device-contact-roles",
    "/devices/<int:device_id>/device-contact-roles",
)
api.route(
    DeviceRoleDetail, "device_contact_role_detail", "/device-contact-roles/<int:id>"
)

# PlatformRoles
api.route(
    PlatformRoleList,
    "platform_contact_role_list",
    "/platform-contact-roles",
    "/platforms/<int:platform_id>/platform-contact-roles",
)
api.route(
    PlatformRoleDetail,
    "platform_contact_role_detail",
    "/platform-contact-roles/<int:id>",
)

# ConfigurationRoles
api.route(
    ConfigurationRoleList,
    "configuration_contact_role_list",
    "/configuration-contact-roles",
    "/configurations/<int:configuration_id>/configuration-contact-roles",
)
api.route(
    ConfigurationRoleDetail,
    "configuration_contact_role_detail",
    "/configuration-contact-roles/<int:id>",
)
# SiteRoles
api.route(
    SiteRoleList,
    "site_contact_role_list",
    "/site-contact-roles",
    "/sites/<int:site_id>/site-contact-roles",
)
api.route(
    SiteRoleDetail,
    "site_contact_role_detail",
    "/site-contact-roles/<int:id>",
)

api.route(
    ControllerConfigurationLocationActionTimepoints,
    "controller_configuration_location_action_timepoints",
    "/controller/configurations/<int:configuration_id>/location-action-timepoints",
)
# Configuration CustomField
api.route(
    ConfigurationCustomFieldList,
    "configuration_customfield_list",
    "/configuration-customfields",
    "/configurations/<int:configuration_id>/configuration-customfields",
)
api.route(
    ConfigurationCustomFieldDetail,
    "configuration_customfield_detail",
    "/configuration-customfields/<int:id>",
)
# Configuration Parameter
api.route(
    ConfigurationParameterDetail,
    "configuration_parameter_detail",
    "/configuration-parameters/<int:id>",
)
api.route(
    ConfigurationParameterList,
    "configuration_parameter_list",
    "/configuration-parameters",
    "/configurations/<int:configuration_id>/configuration-parameters",
)
# Configuration Parameter Value Change Action
api.route(
    ConfigurationParameterValueChangeActionDetail,
    "configuration_parameter_value_change_action_detail",
    "/configuration-parameter-value-change-actions/<int:id>",
)
api.route(
    ConfigurationParameterValueChangeActionList,
    "configuration_parameter_value_change_action_list",
    "/configuration-parameter-value-change-actions",
    "/configurations/<int:configuration_id>/configuration-parameter-value-change-actions"
)
# Sites
api.route(SiteList, "site_list", "/sites", "/sites/<int:outer_site_id>/inner-sites")
api.route(SiteDetail, "site_detail", "/sites/<int:id>")

# Usage statistics
api.route(UsageStatistics, "usage_statistics", "/usage-statistics")
# PIDs
api.route(PidList, "pid_list", "/pids")
api.route(PidDetail, "pid_detail", "/pids/<pid>")
# Datastream links
api.route(
    DatastreamLinkList,
    "datastream_link_list",
    "/datastream-links",
    "/configurations/<int:configuration_id>/datastream-links",
)
api.route(DatastreamLinkDetail, "datastream_link_detail", "/datastream-links/<int:id>")
# TSM Endpoints
api.route(
    TsmEndpointList,
    "tsm_endpoint_list",
    "/tsm-endpoints",
)
api.route(TsmEndpointDetail, "tsm_endpoint_detail", "/tsm-endpoints/<int:id>")
