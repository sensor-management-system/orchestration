# SPDX-FileCopyrightText: 2022 - 2023
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""JSON API resource classes of our app."""

from .configuration_attachment_resources import (  # noqa: F401
    ConfigurationAttachmentDetail,
    ConfigurationAttachmentList,
)
from .configuration_controllers import (  # noqa: F401
    ControllerConfigurationMountingActions,
    ControllerConfigurationMountingActionTimepoints,
)
from .configuration_dynamic_location_begin_actions_resources import (  # noqa: F401
    ConfigurationDynamicLocationBeginActionDetail,
    ConfigurationDynamicLocationBeginActionList,
)
from .configuration_location_action_controller import (  # noqa: F401
    ControllerConfigurationLocationActionTimepoints,
)
from .configuration_resources import (  # noqa: F401
    ConfigurationDetail,
    ConfigurationList,
)
from .configuration_role_resources import (  # noqa: F401
    ConfigurationRoleDetail,
    ConfigurationRoleList,
)
from .configuration_parameter_resources import (  # noqa: F401
    ConfigurationParameterDetail,
    ConfigurationParameterList,
)
from .configuration_parameter_value_change_action_resources import (  # noqa: F401
    ConfigurationParameterValueChangeActionDetail,
    ConfigurationParameterValueChangeActionList,
)
from .configuration_parameter_value_controller import (  # noqa: F401
    ControllerConfigurationParameterValues
)
from .configuration_static_location_begin_actions_resources import (  # noqa: F401
    ConfigurationStaticLocationBeginActionDetail,
    ConfigurationStaticLocationBeginActionList,
)
from .configuration_customfield_resources import (  # noqa: F401
    ConfigurationCustomFieldDetail,
    ConfigurationCustomFieldList,
)
from .contact_resources import ContactDetail, ContactList  # noqa: F401
from .customfield_resources import CustomFieldDetail, CustomFieldList  # noqa: F401
from .datastream_link_resources import (  # noqa: F401
    DatastreamLinkDetail,
    DatastreamLinkList,
)
from .device_attachment_resources import (  # noqa: F401
    DeviceAttachmentDetail,
    DeviceAttachmentList,
)  # noqa: F401
from .device_calibration_action_attachment_resources import (  # noqa: F401
    DeviceCalibrationAttachmentDetail,
    DeviceCalibrationAttachmentList,
)
from .device_calibration_action_resources import (  # noqa: F401
    DeviceCalibrationActionDetail,
    DeviceCalibrationActionList,
)
from .device_mount_action_resources import (  # noqa: F401
    DeviceMountActionDetail,
    DeviceMountActionList,
)
from .device_parameter_resources import (  # noqa: F401
    DeviceParameterDetail,
    DeviceParameterList,
)
from .device_parameter_value_controller import (  # noqa: F401
    ControllerDeviceParameterValues
)
from .device_parameter_value_change_action_resources import (  # noqa: F401
    DeviceParameterValueChangeActionDetail,
    DeviceParameterValueChangeActionList,
)
from .device_property_calibration_resources import (  # noqa: F401
    DevicePropertyCalibrationDetail,
    DevicePropertyCalibrationList,
)
from .device_property_resources import (  # noqa: F401
    DevicePropertyDetail,
    DevicePropertyList,
)
from .device_resources import DeviceDetail, DeviceList  # noqa: F401
from .device_role_resources import DeviceRoleDetail, DeviceRoleList  # noqa: F401
from .device_software_update_action_attachment_resources import (  # noqa: F401
    DeviceSoftwareUpdateActionAttachmentDetail,
    DeviceSoftwareUpdateActionAttachmentList,
)
from .device_software_update_action_resource import (  # noqa: F401
    DeviceSoftwareUpdateActionDetail,
    DeviceSoftwareUpdateActionList,
)
from .generic_configuration_action_attachment_resources import (  # noqa: F401
    GenericConfigurationActionAttachmentDetail,
    GenericConfigurationActionAttachmentList,
)
from .generic_configuration_action_resources import (  # noqa: F401
    GenericConfigurationActionDetail,
    GenericConfigurationActionList,
)
from .generic_device_action_attachment_resources import (  # noqa: F401
    GenericDeviceActionAttachmentDetail,
    GenericDeviceActionAttachmentList,
)
from .generic_device_action_resources import (  # noqa: F401
    GenericDeviceActionDetail,
    GenericDeviceActionList,
)
from .generic_platform_action_attachment_resources import (  # noqa: F401
    GenericPlatformActionAttachmentDetail,
    GenericPlatformActionAttachmentList,
)
from .generic_platform_action_resources import (  # noqa: F401
    GenericPlatformActionDetail,
    GenericPlatformActionList,
)
from .mounting_availabilities import (  # noqa: F401
    DeviceAvailabilities,
    PlatformAvailabilities,
)
from .pid_resources import PidList, PidDetail  # noqa: F401
from .ping import Ping  # noqa: F401
from .platform_attachment_resources import (  # noqa: F401
    PlatformAttachmentDetail,
    PlatformAttachmentList,
)
from .platform_mount_action_resources import (  # noqa: F401
    PlatformMountActionDetail,
    PlatformMountActionList,
)
from .platform_parameter_resources import (  # noqa: F401
    PlatformParameterDetail,
    PlatformParameterList,
)
from .platform_parameter_value_controller import (  # noqa: F401
    ControllerPlatformParameterValues
)
from .platform_parameter_value_change_action_resources import (  # noqa: F401
    PlatformParameterValueChangeActionDetail,
    PlatformParameterValueChangeActionList,
)
from .platform_resources import PlatformDetail, PlatformList  # noqa: F401
from .platform_role_resources import PlatformRoleDetail, PlatformRoleList  # noqa: F401
from .platform_software_update_action_attachment_resources import (  # noqa: F401
    PlatformSoftwareUpdateActionAttachmentDetail,
    PlatformSoftwareUpdateActionAttachmentList,
)
from .platform_software_update_action_resource import (  # noqa: F401
    PlatformSoftwareUpdateActionDetail,
    PlatformSoftwareUpdateActionList,
)
from .site_resources import (  # noqa: F401
    SiteDetail,
    SiteList,
)
from .site_attachment_resources import (  # noqa: F401
    SiteAttachmentDetail,
    SiteAttachmentList,
)
from .site_role_resources import (  # noqa: F401
    SiteRoleDetail,
    SiteRoleList,
)
from .tsm_endpoint_resources import (  # noqa: F401
    TsmEndpointDetail,
    TsmEndpointList,
)
from .usage_statistics import UsageStatistics  # noqa: F401
from .user_info import UserInfo  # noqa: F401
from .user_modification import AcceptTermsOfUse, RevokeApikey  # noqa: F401
from .user_resources import UserDetail, UserList  # noqa: F401
