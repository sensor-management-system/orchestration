# SPDX-FileCopyrightText: 2020 - 2023
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""
File to collect all the models.

This allows both easier access to the models,
but it is also a need to work properly with alembic
(as this is configured to only look into this module
to check for db changes).
"""
from .calibration_actions import (  # noqa: F401
    DeviceCalibrationAction,
    DevicePropertyCalibration,
)
from .calibration_attachments import DeviceCalibrationAttachment  # noqa: F401
from .configuration import Configuration  # noqa: F401
from .configuration_attachment import ConfigurationAttachment  # noqa: F401
from .configuration_location_actions import (  # noqa: F401
    ConfigurationDynamicLocationBeginAction,
    ConfigurationStaticLocationBeginAction,
)
from .contact import Contact  # noqa: F401
from .contact_role import (  # noqa: F401
    ConfigurationContactRole,
    DeviceContactRole,
    PlatformContactRole,
    SiteContactRole,
)
from .configuration_customfield import ConfigurationCustomField  # noqa: F401
from .customfield import CustomField  # noqa: F401
from .datastream_link import DatastreamLink  # noqa: F401
from .device import Device  # noqa: F401
from .device_attachment import DeviceAttachment  # noqa: F401
from .device_property import DeviceProperty  # noqa: F401
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
from .mount_actions import DeviceMountAction, PlatformMountAction  # noqa: F401
from .platform import Platform  # noqa: F401
from .platform_attachment import PlatformAttachment  # noqa: F401
from .site import Site  # noqa: F401
from .software_update_action_attachments import (  # noqa: F401
    DeviceSoftwareUpdateActionAttachment,
    PlatformSoftwareUpdateActionAttachment,
)
from .software_update_actions import (  # noqa: F401
    DeviceSoftwareUpdateAction,
    PlatformSoftwareUpdateAction,
)
from .user import User  # noqa: F401
