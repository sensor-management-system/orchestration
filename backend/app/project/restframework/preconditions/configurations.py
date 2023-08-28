# SPDX-FileCopyrightText: 2022
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Precondition classes for configurations."""

from ...api.helpers.errors import ConflictError
from ...api.models import (
    ConfigurationDynamicLocationBeginAction,
    ConfigurationStaticLocationBeginAction,
    DeviceMountAction,
    PlatformMountAction,
)
from ...api.models.base_model import db
from ...api.models.mixin import utc_now
from .base import Precondition


class AllDeviceMountsForConfigurationAreFinishedInThePast(Precondition):
    """
    Checks the device mount actions of a configuration.

    This checks that all the device mounts have end dates & that
    they all are in the past.
    """

    def __init__(self):
        """Init the object."""

        def object_rule(object):
            """Return a conflict error if there is a problem on device mounts."""
            device_mounts = db.session.query(DeviceMountAction).filter_by(
                configuration_id=object.id
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


class AllPlatformMountsForConfigurationAreFinishedInThePast(Precondition):
    """
    Check the platform mounts for a configuration.

    Makes sure that the platform mounts all have ends & that they
    are in the past.
    """

    def __init__(self):
        """Init the object."""

        def object_rule(object):
            """Return a conflict error if needed on checking the platform mounts."""
            platform_mounts = db.session.query(PlatformMountAction).filter_by(
                configuration_id=object.id
            )
            now = self._get_current_date_time()

            for platform_mount in platform_mounts:
                if not platform_mount.end_date:
                    return self._to_conflict_no_end_date(platform_mount)
                if platform_mount.end_date > now:
                    return self._to_conflict_end_date_not_in_the_past(platform_mount)
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
    def _to_conflict_no_end_date(platform_mount):
        """Create a conflict error from the platform mount action without end date."""
        return ConflictError(
            f"Platform mount action {platform_mount.id} has no end date"
        )

    @staticmethod
    def _to_conflict_end_date_not_in_the_past(platform_mount):
        """Create a conflict error from a platform mount action that is still active now."""
        return ConflictError(
            f"Platform mount action {platform_mount.id} not in the past"
        )


class AllStaticLocationsForConfigurationAreFinishedInThePast(Precondition):
    """
    Check the static location actions of a configuration.

    Makes sure that all the static locations have an end date &
    that they all are in the past.
    """

    def __init__(self):
        """Init the object."""

        def object_rule(object):
            """Reutrn a conflict object on checking the static location actions."""
            static_locations = db.session.query(
                ConfigurationStaticLocationBeginAction
            ).filter_by(configuration_id=object.id)
            now = self._get_current_date_time()

            for location in static_locations:
                if not location.end_date:
                    return self._to_conflict_no_end_date(location)
                if location.end_date > now:
                    return self._to_conflict_end_date_not_in_the_past(location)
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
    def _to_conflict_no_end_date(location):
        """Create a conflict error from the location action without end date."""
        return ConflictError(f"Static location action {location.id} has no end date")

    @staticmethod
    def _to_conflict_end_date_not_in_the_past(location):
        """Create a conflict error from a location action that is still active now."""
        return ConflictError(f"Static location action {location.id} not in the past")


class AllDynamicLocationsForConfigurationAreFinishedInThePast(Precondition):
    """
    Precondition to check that all the dynamic location of a configuration.

    This checks if all locations have an end & that all the actions are
    in the past.
    """

    def __init__(self):
        """Init the object."""

        def object_rule(object):
            """Return a conflict error if a dynamic location doesn't end."""
            dynamic_locations = db.session.query(
                ConfigurationDynamicLocationBeginAction
            ).filter_by(configuration_id=object.id)
            now = self._get_current_date_time()

            for location in dynamic_locations:
                if not location.end_date:
                    return self._to_conflict_no_end_date(location)
                if location.end_date > now:
                    return self._to_conflict_end_date_not_in_the_past(location)
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
    def _to_conflict_no_end_date(location):
        """Create a conflict error from the location action without end date."""
        return ConflictError(f"Dynamic location action {location.id} has no end date")

    @staticmethod
    def _to_conflict_end_date_not_in_the_past(location):
        """Create a conflict error from a location action that is still active now."""
        return ConflictError(f"Dynamic location action {location.id} not in the past")


class SiteOfConfigurationIsNotArchived(Precondition):
    """Precondition to check that the site of a configuration is not archived."""

    def __init__(self):
        """Init the object."""

        def object_rule(object):
            """Return a conflict error if a dynamic location doesn't end."""
            site = object.site
            if site and site.archived:
                return ConflictError("Site of configuration is archved.")

        super().__init__(object_rule)
