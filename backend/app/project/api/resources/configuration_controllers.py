# SPDX-FileCopyrightText: 2022 - 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Controller resources for the configuration mounting actions."""

import dateutil.parser
from flask import request
from flask_rest_jsonapi import ResourceList
from sqlalchemy import and_, or_

from ..helpers.configuration_helpers import build_tree
from ..helpers.errors import (
    BadRequestError,
    ForbiddenError,
    MethodNotAllowed,
    NotFoundError,
)
from ..models import (
    Configuration,
    Device,
    DeviceMountAction,
    Platform,
    PlatformMountAction,
)
from ..models.base_model import db
from ..permissions.rules import can_see
from ..schemas.device_schema import DeviceSchema
from ..schemas.mount_actions_schema import (
    DeviceMountActionSchema,
    PlatformMountActionSchema,
)
from ..schemas.platform_schema import PlatformSchema


class ControllerConfigurationMountingActionTimepoints(ResourceList):
    """Controller that returns a list of timepoints for the mounting actions."""

    def get(self, *args, **kwargs):
        """Return the hierarchy for a timepoint."""
        if "configuration_id" not in kwargs.keys():
            raise NotFoundError("No id.")
        configuration_id = kwargs["configuration_id"]
        configuration = (
            db.session.query(Configuration).filter_by(id=configuration_id).one_or_none()
        )
        if not configuration:
            raise NotFoundError("No configuration with the given id.")
        if not can_see(configuration):
            raise ForbiddenError("Authentication required.")

        device_schema = DeviceSchema()
        platform_schema = PlatformSchema()

        device_mounts = db.session.query(DeviceMountAction).filter(
            DeviceMountAction.configuration_id == configuration_id,
        )
        platform_mounts = db.session.query(PlatformMountAction).filter(
            PlatformMountAction.configuration_id == configuration_id,
        )
        dates_with_labels = []
        for device_mount in device_mounts:
            dates_with_labels.append(
                {
                    "timepoint": device_mount.begin_date,
                    "type": "device_mount",
                    "attributes": device_schema.dump(device_mount.device)["data"][
                        "attributes"
                    ],
                }
            )
            if device_mount.end_date:
                dates_with_labels.append(
                    {
                        "timepoint": device_mount.end_date,
                        "type": "device_unmount",
                        "attributes": device_schema.dump(device_mount.device)["data"][
                            "attributes"
                        ],
                    }
                )
        for platform_mount in platform_mounts:
            dates_with_labels.append(
                {
                    "timepoint": platform_mount.begin_date,
                    "type": "platform_mount",
                    "attributes": platform_schema.dump(platform_mount.platform)["data"][
                        "attributes"
                    ],
                }
            )
            if platform_mount.end_date:
                dates_with_labels.append(
                    {
                        "timepoint": platform_mount.end_date,
                        "type": "platform_unmount",
                        "attributes": platform_schema.dump(platform_mount.platform)[
                            "data"
                        ]["attributes"],
                    }
                )

        dates_with_labels.sort(key=lambda x: x["timepoint"])
        return dates_with_labels

    def label_device(self, device):
        """Return a label for the device."""
        return device.short_name

    def label_platform(self, platform):
        """Return a label for the platform."""
        return platform.short_name

    def post(self):
        """Don't allow the post request."""
        raise MethodNotAllowed("endpoint is readonly")


class ControllerConfigurationMountingActions(ResourceList):
    """Controller that returns a hierarchy for a current timepoint."""

    # class wide variables
    device_mount_action_schema = DeviceMountActionSchema()
    device_schema = DeviceSchema()
    platform_mount_action_schema = PlatformMountActionSchema()
    platform_schema = PlatformSchema()

    def get(self, *args, **kwargs):
        """Return the hierarchy for a timepoint."""
        if "configuration_id" not in kwargs.keys():
            raise NotFoundError("No id.")
        configuration_id = kwargs["configuration_id"]
        configuration = (
            db.session.query(Configuration).filter_by(id=configuration_id).one_or_none()
        )
        if not configuration:
            raise NotFoundError("No configuration with the given id.")
        if not can_see(configuration):
            raise ForbiddenError("Authentication required.")

        if "timepoint" not in request.args.keys():
            raise BadRequestError("timepoint parameter required")
        timepoint_str = request.args["timepoint"]
        try:
            timepoint = dateutil.parser.parse(timepoint_str)
        except dateutil.parser.ParserError:
            raise BadRequestError("timepoint must be ISO 8601")

        active_device_mounts = (
            db.session.query(DeviceMountAction)
            .join(DeviceMountAction.device)
            .filter(
                and_(
                    DeviceMountAction.configuration_id == configuration_id,
                    DeviceMountAction.begin_date <= timepoint,
                    or_(
                        # an is None check doesn't work for this filter.
                        DeviceMountAction.end_date == None,  # noqa: E711
                        DeviceMountAction.end_date >= timepoint,
                    ),
                )
            )
            .order_by(Device.short_name)
        )
        active_platform_mounts = (
            db.session.query(PlatformMountAction)
            .join(PlatformMountAction.platform)
            .filter(
                and_(
                    PlatformMountAction.configuration_id == configuration_id,
                    PlatformMountAction.begin_date <= timepoint,
                    or_(
                        # an is None check doesn't work for this filter.
                        PlatformMountAction.end_date == None,  # noqa: E711
                        PlatformMountAction.end_date >= timepoint,
                    ),
                )
            )
            .order_by(Platform.short_name)
        )

        # It should not be possible to mount the very same platform
        # for the very same time. So we can use the platform_id as
        # key to put the children in.
        def platform_to_payload(platform_mount):
            """Set the fields we want to print out for a platform mount."""
            return {
                "action": self.platform_mount_action_schema.dump(platform_mount),
                "entity": self.platform_schema.dump(platform_mount.platform),
            }

        def device_to_payload(device_mount):
            """Set the fields we want to print out for a device mount."""
            return {
                "action": self.device_mount_action_schema.dump(device_mount),
                "entity": self.device_schema.dump(device_mount.device),
            }

        top_level_mounts = build_tree(
            platform_mounts=active_platform_mounts,
            device_mounts=active_device_mounts,
            f_platform_mount=platform_to_payload,
            f_device_mount=device_to_payload,
        )
        return top_level_mounts

    def post(self):
        """Don't allow the post request."""
        raise MethodNotAllowed("endpoint is readonly")
