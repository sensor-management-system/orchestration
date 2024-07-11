# SPDX-FileCopyrightText: 2020 - 2024
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""
File to collect all the models.

This allows both easier access to the models,
but it is also a need to work properly with alembic
(as this is configured to only look into this module
to check for db changes).
"""
from .activity_log import ActivityLog  # noqa: F401
from .calibration_actions import (  # noqa: F401
    DeviceCalibrationAction,
    DevicePropertyCalibration,
)
from .calibration_attachments import DeviceCalibrationAttachment  # noqa: F401
from .configuration import Configuration  # noqa: F401
from .configuration_attachment import ConfigurationAttachment  # noqa: F401
from .configuration_customfield import ConfigurationCustomField  # noqa: F401
from .configuration_image import ConfigurationImage  # noqa: F401
from .configuration_location_actions import (  # noqa: F401
    ConfigurationDynamicLocationBeginAction,
    ConfigurationStaticLocationBeginAction,
)
from .configuration_parameter import ConfigurationParameter  # noqa: F401
from .configuration_parameter_value_change_action import (  # noqa: F401
    ConfigurationParameterValueChangeAction,
)
from .contact import Contact  # noqa: F401
from .contact_role import (  # noqa: F401
    ConfigurationContactRole,
    DeviceContactRole,
    PlatformContactRole,
    SiteContactRole,
)
from .customfield import CustomField  # noqa: F401
from .datastream_link import DatastreamLink  # noqa: F401
from .device import Device  # noqa: F401
from .device_attachment import DeviceAttachment  # noqa: F401
from .device_image import DeviceImage  # noqa: F401
from .device_parameter import DeviceParameter  # noqa: F401
from .device_parameter_value_change_action import (  # noqa: F401
    DeviceParameterValueChangeAction,
)
from .device_property import DeviceProperty  # noqa: F401
from .export_control import ExportControl  # noqa: F401
from .export_control_attachment import ExportControlAttachment  # noqa: F401
from .generic_action_attachments import (  # noqa: F401
    GenericConfigurationActionAttachment,
    GenericDeviceActionAttachment,
    GenericPlatformActionAttachment,
)
from .generic_actions import (  # noqa: F401
    GenericConfigurationAction,
    GenericDeviceAction,
    GenericPlatformAction,
)
from .manufacturer_model import ManufacturerModel  # noqa: F401
from .mount_actions import DeviceMountAction, PlatformMountAction  # noqa: F401
from .platform import Platform  # noqa: F401
from .platform_attachment import PlatformAttachment  # noqa: F401
from .platform_image import PlatformImage  # noqa: F401
from .platform_parameter import PlatformParameter  # noqa: F401
from .platform_parameter_value_change_action import (  # noqa: F401
    PlatformParameterValueChangeAction,
)
from .site import Site  # noqa: F401
from .site_attachment import SiteAttachment  # noqa: F401
from .site_image import SiteImage  # noqa: F401
from .software_update_action_attachments import (  # noqa: F401
    DeviceSoftwareUpdateActionAttachment,
    PlatformSoftwareUpdateActionAttachment,
)
from .software_update_actions import (  # noqa: F401
    DeviceSoftwareUpdateAction,
    PlatformSoftwareUpdateAction,
)
from .tsm_endpoint import TsmEndpoint  # noqa: F401
from .user import User  # noqa: F401
