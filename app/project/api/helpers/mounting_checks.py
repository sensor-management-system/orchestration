"""Check functions to ensure consistency for mounts."""

import abc
import datetime
import itertools

import dateutil.parser
from sqlalchemy import and_, or_

from ... import db
from ..models import (
    ConfigurationDynamicLocationBeginAction,
    DeviceMountAction,
    DeviceProperty,
    PlatformMountAction,
)
from .date_time_range import DateTimeRange
from .errors import BadRequestError, ConflictError, NotFoundError


class AbstractMountActionValidator(abc.ABC):
    """
    Abstract base class to validate requested changes for mount actions.

    The idea is to run more complex checks before we create/update/delete
    a mount action - to ensure that none of our rules are violated.
    """

    def validate_create(self, payload_dict):
        """
        Validate that we can create a mount action.

        Raises a ConflictError if it is not possible.

        Current checks:
        - device/platform not already in use for the date time range.
        - parent platform provided for the date time range (if parent platform needed)
        """
        object_id = self._extract_object_id_to_mount(payload_dict)
        expected_date_time_range = self._extract_begin_and_end_dates(payload_dict)
        configuration_id = self._extract_configuration_id(payload_dict)
        parent_platform_id = self._extract_parent_platform_id(payload_dict)
        # First we check if we have the an existing mount action for the
        # object that we want to mount.
        overlapping_mount = self._get_overlapping_mount(
            object_id, expected_date_time_range, ignore_id=None
        )
        if overlapping_mount:
            raise ConflictError(self._build_error_message_blocked(overlapping_mount))
        # Ok, we don't have an existing mount action that could cause problems.
        # However, we must also check for our parent platform.
        # And this must also be mounted on the very same configuration.
        if parent_platform_id is not None and not self._get_parent_platform_mount(
            parent_platform_id, configuration_id, expected_date_time_range
        ):
            raise ConflictError(
                self._build_error_message_no_platform_mount(expected_date_time_range)
            )

    def validate_update(self, payload_dict, existing_mount_id):
        """
        Validate that we can update the mount action.

        Raises a ConflictError if it is not possible.

        It combines the checks that we have in the create & in the delete
        steps (but it is more complex as it has to check what the old
        data are & what the are the new ones).

        So it also checks that we still have only one usage of the
        device/platform at the time, still have the parent platform,
        and that we don't lose the connection to other actions (submounts,
        or location actions that refer to the current mount).
        """
        existing_mount = self._query_existing_mount(existing_mount_id)
        if not existing_mount:
            raise NotFoundError(
                self._build_error_message_no_existing_mount(existing_mount_id)
            )
        updated_object_id = self._extract_updated_object_id(
            payload_dict, existing_mount
        )
        updated_configuration_id = self._extract_updated_configuration_id(
            payload_dict, existing_mount
        )
        updated_parent_platform_id = self._extract_updated_parent_platform_id(
            payload_dict, existing_mount
        )
        expected_date_time_range = self._extract_updated_begin_and_end_dates(
            payload_dict, existing_mount
        )

        # Check if we still can use the object in the mount (but ignore
        # overlaps with the existng entry that we want to update).
        overlapping_mount = self._get_overlapping_mount(
            updated_object_id, expected_date_time_range, ignore_id=existing_mount.id
        )
        if overlapping_mount:
            raise ConflictError(self._build_error_message_blocked(overlapping_mount))
        # Ok, our object is free to be used for the updated time slide.
        # Now we also check that we still have a parent platform mount.
        if (
            updated_parent_platform_id is not None
            and not self._get_parent_platform_mount(
                updated_parent_platform_id,
                updated_configuration_id,
                expected_date_time_range,
            )
        ):
            raise ConflictError(
                self._build_error_message_no_platform_mount(expected_date_time_range)
            )
        # Ok, we still have a valid parent platform mount.
        # Now the last task is to check for orphanized child mounts.
        if self._get_first_orphan(
            updated_object_id,
            existing_mount,
            expected_date_time_range,
            updated_configuration_id,
        ):
            raise ConflictError(self._build_error_message_orphan())

    def validate_delete(self, existing_mount_id):
        """
        Validate that we can delete the mount action.

        Raises a ConflictError if it is not possible.

        Current checks:
        - check that we don't have any other actions (mounts, dynamic locations) that
          still refer to the mount action that we want to delete (refering in the terms
          that we refer to the platform/device that is mounted with this action).
        """
        existing_mount = self._query_existing_mount(existing_mount_id)
        if not existing_mount:
            raise NotFoundError(
                self._build_error_message_no_existing_mount(existing_mount_id)
            )
        object_id = self._extract_updated_object_id(
            {"relationships": {}}, existing_mount
        )
        # Main point is that both are the very same. No real action
        # can be covered by those.
        start_and_end = datetime.datetime.now()
        fake_date_time_range = DateTimeRange(start_and_end, start_and_end)

        # The _get_first_orphan method checks if we would lose any action by putting
        # it into another configuration. By giving a configuration_id of None we
        # simulate the deletion, as there isn't any binding to the current configuration
        # anymore in that this action could still be needed (for submounts for example).
        fake_configuration_id = None
        if self._get_first_orphan(
            object_id, existing_mount, fake_date_time_range, fake_configuration_id
        ):
            raise ConflictError(self._build_error_message_orphan())

    def _get_parent_platform_mount(
        self, parent_platform_id, configuration_id, expected_date_time_range
    ):
        """Search for a platform mount action. May return None."""
        parent_platform_mounts = self._query_parent_platform_mounts(
            parent_platform_id, configuration_id
        )
        for mount_action in parent_platform_mounts:
            existing_date_time_range = DateTimeRange(
                mount_action.begin_date, mount_action.end_date
            )
            if existing_date_time_range.covers(expected_date_time_range):
                return mount_action
        return None

    def _get_overlapping_mount(
        self, object_id, expected_date_time_range, ignore_id=None
    ):
        """Search if we have already an mount action for the object. Return if found."""
        existing_mount_actions = self._query_existing_mount_actions(
            object_id, expected_date_time_range.begin_date
        )
        for mount_action in existing_mount_actions:
            # We can ignore the existing mount that we want to update.
            if mount_action.id != ignore_id:
                existing_date_time_range = DateTimeRange(
                    mount_action.begin_date, mount_action.end_date
                )
                if expected_date_time_range.overlaps_with(existing_date_time_range):
                    return mount_action
        return None

    def _extract_begin_and_end_dates(self, payload_dict):
        """
        Extract the begin and end dates from the payload dict.

        The begin date must be there for the creation while the
        end date is optional.
        """
        if "begin_date" not in payload_dict["attributes"].keys():
            raise BadRequestError("begin_date is required.")
        begin_date_as_string = payload_dict["attributes"]["begin_date"]
        end_date_as_string = payload_dict["attributes"].get("end_date")
        begin_date = self._parse_datetime(begin_date_as_string)
        end_date = None
        if end_date_as_string:
            end_date = self._parse_datetime(end_date_as_string)
        return DateTimeRange(begin_date, end_date)

    @staticmethod
    def _parse_datetime(date_as_string):
        """Parse the string representation of a datetime object to the actual object."""
        try:
            return dateutil.parser.parse(date_as_string).replace(tzinfo=None)
        except dateutil.parser.ParserError:
            raise BadRequestError(
                f"'{date_as_string}' is not valid according to ISO 8601"
            )

    @staticmethod
    def _extract_configuration_id(payload_dict):
        """Extract the configuration id from the payload."""
        return payload_dict["relationships"]["configuration"]["data"]["id"]

    @staticmethod
    def _extract_parent_platform_id(payload_dict):
        """Extract the parent platform id from the payload. May be None."""
        return (
            payload_dict["relationships"]
            .get("parent_platform", {})
            .get("data", {})
            .get("id", None)
        )

    @staticmethod
    def _extract_updated_configuration_id(payload_dict, existing_mount):
        """
        Extract the configuration id for the update validation case.

        It could be set in the payload or it should still be the one of
        the mount action.
        """
        if "relationships" in payload_dict.keys():
            if "configuration" in payload_dict["relationships"].keys():
                if "data" in payload_dict["relationships"]["configuration"].keys():
                    if (
                        "id"
                        in payload_dict["relationships"]["configuration"]["data"].keys()
                    ):
                        return payload_dict["relationships"]["configuration"]["data"][
                            "id"
                        ]
        return existing_mount.configuration_id

    @staticmethod
    def _extract_updated_parent_platform_id(payload_dict, existing_mount):
        """
        Extract the parent platform id for the update case.

        Again: This can be set in the payload or in the current object.
        """
        if "relationships" in payload_dict.keys():
            if "parent_platform" in payload_dict["relationships"].keys():
                if "data" in payload_dict["relationships"]["parent_platform"].keys():
                    if (
                        "id"
                        in payload_dict["relationships"]["parent_platform"][
                            "data"
                        ].keys()
                    ):
                        return payload_dict["relationships"]["parent_platform"]["data"][
                            "id"
                        ]
        return existing_mount.parent_platform_id

    def _extract_updated_begin_and_end_dates(self, payload_dict, existing_mount):
        """Extract the begin and end dates for the update case."""
        if "begin_date" in payload_dict["attributes"].keys():
            begin_date_as_string = payload_dict["attributes"]["begin_date"]
            begin_date = self._parse_datetime(begin_date_as_string)
        else:
            begin_date = existing_mount.begin_date
        if "end_date" in payload_dict["attributes"].keys():
            end_date_as_string = payload_dict["attributes"]["end_date"]
            if end_date_as_string is not None:
                end_date = self._parse_datetime(end_date_as_string)
            else:
                end_date = None
        else:
            end_date = existing_mount.end_date
        return DateTimeRange(begin_date, end_date)

    @staticmethod
    def _query_parent_platform_mounts(parent_platform_id, configuration_id):
        """Find mount action for the parent platform."""
        return db.session.query(PlatformMountAction).filter(
            and_(
                PlatformMountAction.platform_id == parent_platform_id,
                PlatformMountAction.configuration_id == configuration_id,
            ),
        )

    @staticmethod
    def _build_error_message_no_platform_mount(expected_date_time_range):
        """Create an error message if there is no parent platform mount for the whole time span."""
        parts = [
            "Parent platform is not mounted for the whole time",
            f"from {expected_date_time_range.begin_date}",
        ]
        if expected_date_time_range.end_date:
            parts.append(f"to {expected_date_time_range.end_date}")
        return " ".join(parts)

    # And here we have all the abstract method that need to be implemented by
    # the sub classes.
    @abc.abstractmethod
    def _get_first_orphan(
        self,
        object_id,
        existing_mount,
        expected_date_time_range,
        updated_configuration_id,
    ):
        """Return an object that would be orphanized with the suggested changes or None."""
        pass

    @abc.abstractmethod
    def _extract_object_id_to_mount(self, payload_dict):
        """Extract the id of the object that we want to change the mount for."""
        pass

    @abc.abstractmethod
    def _query_existing_mount(self, mount_id):
        """Return the existing mount if that one exists."""
        pass

    @abc.abstractmethod
    def _query_existing_mount_actions(self, object_id, begin_date):
        """Return the collection of existing mounts for the device/platform."""
        pass

    @abc.abstractmethod
    def _extract_updated_object_id(self, payload_dict, existing_mount):
        """Extract the device/platform after the update."""
        pass

    @abc.abstractmethod
    def _build_error_message_blocked(self, mount_action):
        """Return a string with an error message if the object is blocked (other use)."""
        pass

    @abc.abstractmethod
    def _build_error_message_no_existing_mount(self, existing_mount_id):
        """Return a string with an error message if we can't find the existing mount."""
        pass

    @abc.abstractmethod
    def _build_error_message_orphan(self):
        """Return a string with an error if we would get an orphanized object with the change."""
        pass


class DeviceMountActionValidator(AbstractMountActionValidator):
    """Validator subclass for the device mount actions."""

    def _get_first_orphan(
        self,
        object_id,
        existing_mount,
        expected_date_time_range,
        updated_configuration_id,
    ):
        existing_date_time_range = DateTimeRange(
            existing_mount.begin_date, existing_mount.end_date
        )
        device_property_ids = [
            x.id
            for x in db.session.query(DeviceProperty).filter(
                DeviceProperty.device_id == existing_mount.device_id
            )
        ]
        dynamic_location_actions = (
            db.session.query(ConfigurationDynamicLocationBeginAction)
            .filter(
                and_(
                    ConfigurationDynamicLocationBeginAction.configuration_id
                    == existing_mount.configuration_id,
                    or_(
                        ConfigurationDynamicLocationBeginAction.x_property_id.in_(
                            device_property_ids
                        ),
                        ConfigurationDynamicLocationBeginAction.y_property_id.in_(
                            device_property_ids
                        ),
                        ConfigurationDynamicLocationBeginAction.z_property_id.in_(
                            device_property_ids
                        ),
                    ),
                )
            )
            .order_by(ConfigurationDynamicLocationBeginAction.begin_date)
            .all()
        )

        for dynamic_location_action in dynamic_location_actions:
            end_date = dynamic_location_action.end_date
            check_date_time_range = DateTimeRange(dynamic_location_action.begin_date, end_date)
            if existing_date_time_range.overlaps_with(check_date_time_range):
                if (
                    dynamic_location_action.configuration_id != updated_configuration_id
                    or object_id != existing_mount.device_id
                    or not expected_date_time_range.covers(check_date_time_range)
                ):

                    return dynamic_location_action

        return None

    @staticmethod
    def _extract_object_id_to_mount(payload_dict):
        return payload_dict["relationships"]["device"]["data"]["id"]

    def _query_existing_mount(self, mount_id):
        return (
            db.session.query(DeviceMountAction)
            .filter(
                DeviceMountAction.id == mount_id,
            )
            .first()
        )

    @staticmethod
    def _query_existing_mount_actions(object_id, begin_date):
        return db.session.query(DeviceMountAction).filter(
            and_(
                DeviceMountAction.device_id == object_id,
                or_(
                    DeviceMountAction.end_date.is_(None),
                    DeviceMountAction.end_date > begin_date,
                ),
            )
        )

    @staticmethod
    def _extract_updated_object_id(payload_dict, existing_mount):
        if "relationships" in payload_dict.keys():
            if "device" in payload_dict["relationships"].keys():
                if "data" in payload_dict["relationships"]["device"].keys():
                    if "id" in payload_dict["relationships"]["device"]["data"].keys():
                        return payload_dict["relationships"]["device"]["data"]["id"]
        return existing_mount.device_id

    @staticmethod
    def _build_error_message_blocked(mount_action):
        parts = [
            f"Device is blocked due to usage in {mount_action.configuration.label}",
            f"from {mount_action.begin_date}",
        ]
        if mount_action.end_date is not None:
            parts.append(f"to {mount_action.end_date}")
        return " ".join(parts) + "."

    @staticmethod
    def _build_error_message_no_existing_mount(existing_mount_id):
        return f"There is no DeviceMountAction with id={existing_mount_id}"

    @staticmethod
    def _build_error_message_orphan():
        return (
            "There is still a ConfigurationDynamicLocationBeginAction "
            + "that is not covered by the updated data."
        )


class PlatformMountActionValidator(AbstractMountActionValidator):
    """Validator subclass for the platform mount actions."""

    def _get_first_orphan(
        self,
        object_id,
        existing_mount,
        expected_date_time_range,
        updated_configuration_id,
    ):

        child_platform_mount_actions = db.session.query(PlatformMountAction).filter(
            and_(
                PlatformMountAction.parent_platform_id == existing_mount.platform_id,
                PlatformMountAction.configuration_id == existing_mount.configuration_id,
            )
        )
        child_device_mount_actions = db.session.query(DeviceMountAction).filter(
            and_(
                DeviceMountAction.parent_platform_id == existing_mount.platform_id,
                DeviceMountAction.configuration_id == existing_mount.configuration_id,
            )
        )
        old_date_time_range = DateTimeRange(
            existing_mount.begin_date, existing_mount.end_date
        )
        for mount_action in itertools.chain(
            child_platform_mount_actions, child_device_mount_actions
        ):
            existing_date_time_range = DateTimeRange(
                mount_action.begin_date, mount_action.end_date
            )
            if old_date_time_range.covers(existing_date_time_range):
                if (
                    # Did we changed the platform of our current mount?
                    # In that case the child mounts would point to the
                    # wrong parent_platform_id
                    mount_action.parent_platform_id != object_id
                    # Or did we changed the configuration?
                    # If so, we will have all entries with that
                    # parent_platform_id be orphanized
                    or mount_action.configuration_id != updated_configuration_id
                    # Or is just the time range of the child mount
                    # no longer covered?
                    or not expected_date_time_range.covers(existing_date_time_range)
                ):
                    return mount_action
        return None

    @staticmethod
    def _extract_object_id_to_mount(payload_dict):
        return payload_dict["relationships"]["platform"]["data"]["id"]

    @staticmethod
    def _extract_updated_object_id(payload_dict, existing_mount):
        if "relationships" in payload_dict.keys():
            if "platform" in payload_dict["relationships"].keys():
                if "data" in payload_dict["relationships"]["platform"].keys():
                    if "id" in payload_dict["relationships"]["platform"]["data"].keys():
                        return payload_dict["relationships"]["platform"]["data"]["id"]
        return existing_mount.platform_id

    def _query_existing_mount(self, mount_id):
        return (
            db.session.query(PlatformMountAction)
            .filter(
                PlatformMountAction.id == mount_id,
            )
            .first()
        )

    def _query_existing_mount_actions(self, object_id, begin_date):
        return db.session.query(PlatformMountAction).filter(
            and_(
                PlatformMountAction.platform_id == object_id,
                or_(
                    PlatformMountAction.end_date.is_(None),
                    PlatformMountAction.end_date > begin_date,
                ),
            )
        )

    def _build_error_message_blocked(self, mount_action):
        parts = [
            f"Platform is blocked due to usage in {mount_action.configuration.label}",
            f"from {mount_action.begin_date}",
        ]
        if mount_action.end_date is not None:
            parts.append(f"to {mount_action.end_date}")
        return " ".join(parts) + "."

    def _build_error_message_no_existing_mount(self, existing_mount_id):
        return f"There is no PlatformMountAction with id={existing_mount_id}"

    def _build_error_message_orphan(self):
        return "There is still a child mount that is not covered by the updated data."
