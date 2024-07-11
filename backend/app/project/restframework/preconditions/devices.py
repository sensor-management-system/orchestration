# SPDX-FileCopyrightText: 2022 - 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Preconditions for devices."""
from ...api.helpers.errors import ConflictError
from ...api.models import DeviceMountAction
from ...api.models.base_model import db
from ...api.models.mixin import utc_now
from .base import Precondition


class AllMountsOfDeviceAreFinishedInThePast(Precondition):
    """Precondition that there are no open & active device mounts."""

    def __init__(self):
        """Init the object."""

        def object_rule(object):
            """Return a ConflictError if there is an open/future mount action."""

            device_mounts = db.session.query(DeviceMountAction).filter_by(
                device_id=object.id
            )
            now = self._get_current_date_time()

            for device_mount in device_mounts:
                if not device_mount.end_date:
                    return self._to_conflict_no_end_date(device_mount)
                if device_mount.end_date > now:
                    return self._to_conflict_end_date_not_in_the_past(device_mount)
            return None

        super().__init__(object_rule)

    @staticmethod
    def _get_current_date_time():
        """
        Get the current date time.

        Is especially here to mock the extraction of the current date.
        """
        return utc_now()

    @staticmethod
    def _to_conflict_no_end_date(device_mount):
        """Create a conflict error from the device mount action without end date."""
        return ConflictError(f"Device mount action {device_mount.id} has no end date")

    @staticmethod
    def _to_conflict_end_date_not_in_the_past(device_mount):
        """Create a conflict error from a device mount action that is still active now."""
        return ConflictError(f"Device mount action {device_mount.id} not in the past")


class AllUsagesAsParentDeviceInDeviceMountsFinishedInThePast(Precondition):
    """Precondition - no open & active device mounts with the device as parent."""

    def __init__(self):
        """Init the object."""

        def object_rule(object):
            """Return a ConflictError if there is an open/future mount action."""
            device_mounts = db.session.query(DeviceMountAction).filter_by(
                parent_device_id=object.id
            )
            now = self._get_current_date_time()

            for mount in device_mounts:
                if not mount.end_date:
                    return self._to_conflict_no_end_date(mount)
                if mount.end_date > now:
                    return self._to_conflict_end_date_not_in_the_past(mount)
            return None

        super().__init__(object_rule)

    @staticmethod
    def _get_current_date_time():
        """
        Get the current date time.

        Is especially here to mock the extraction of the current date.
        """
        return utc_now()

    @staticmethod
    def _to_conflict_no_end_date(mount):
        """Create a conflict error from the device mount action without end date."""
        return ConflictError(f"Device mount action {mount.id} has no end date")

    @staticmethod
    def _to_conflict_end_date_not_in_the_past(mount):
        """Create a conflict error from a device mount action that is still active now."""
        return ConflictError(f"Device mount action {mount.id} not in the past")
