"""Helper classes ot check location actions."""
import abc

import dateutil.parser
from sqlalchemy import and_

from ..models import (
    ConfigurationDynamicLocationBeginAction,
    ConfigurationStaticLocationBeginAction,
    DeviceMountAction,
    DeviceProperty,
)
from ..models.base_model import db
from .date_time_range import DateTimeRange
from .errors import BadRequestError, ConflictError, NotFoundError


class AbstractLocationActionValidator(abc.ABC):
    """Abstract base class to validate requested changes for location actions."""

    def validate_create(self, payload_dict):
        """
        Validate that we can create a location action.

        Basically we have two cases to check here:
        - Is there an location action that covers (parts of) the new location action?
          So would adding the new location make it unclear where the configuation is, as
          we would have two locations at the same time?
        - Are all the device properties that we need to read the coordinates from
          also available for the whole time of the configuration?
        """
        configuration_id = self._extract_configuration_id(payload_dict)
        expected_date_time_range = self._extract_begin_and_end_dates(payload_dict)
        # First check that don't have an existing location action
        # for the very same time.
        overlapping_location = self._get_overlapping_location(
            configuration_id, expected_date_time_range, ignore_id=None
        )
        if overlapping_location:
            raise ConflictError(self._build_error_message_overlapping_location())
        # As we don't have it, we can check if all the device properties
        # that are used for the dynamic location action are mounted
        # for the whole time of the location action.
        non_available_device_property = (
            self._find_first_device_property_that_is_not_mounted_for_the_action_time(
                payload_dict, None, expected_date_time_range, configuration_id
            )
        )
        if non_available_device_property:
            raise ConflictError(
                self._build_error_message_non_available_device_property()
            )
        archived_device = self._find_first_archived_device(payload_dict)
        if archived_device:
            raise ConflictError("Usage of archived devices is not allowed")

    def validate_update(self, payload_dict, existing_location_id):
        """
        Validate that we can update a location action.

        Tests are the same as for the creation case:
        - Is there another action for a timepoint of this one after the update?
        - Are all the needed device properties still there?
        """
        existing_location = self._query_existing_location(existing_location_id)
        if not existing_location:
            raise NotFoundError(
                self._build_error_message_no_existing_location(existing_location_id)
            )

        updated_configuration_id = self._extract_updated_configuration_id(
            payload_dict, existing_location
        )
        expected_date_time_range = self._extract_updated_begin_and_end_dates(
            payload_dict, existing_location
        )

        overlapping_location = self._get_overlapping_location(
            updated_configuration_id,
            expected_date_time_range,
            ignore_id=existing_location_id,
        )
        if overlapping_location:
            raise ConflictError(self._build_error_message_overlapping_location())
        non_available_device_property = (
            self._find_first_device_property_that_is_not_mounted_for_the_action_time(
                payload_dict,
                existing_location,
                expected_date_time_range,
                updated_configuration_id,
            )
        )
        if non_available_device_property:
            raise ConflictError(
                self._build_error_message_non_available_device_property()
            )
        archived_device = self._find_first_archived_device(
            payload_dict, existing_location
        )
        if archived_device:
            raise ConflictError("Usage of archived devices is not allowed")

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
            return dateutil.parser.parse(date_as_string)
        except dateutil.parser.ParserError:
            raise BadRequestError(
                f"'{date_as_string}' is not valid according to ISO 8601"
            )

    @staticmethod
    def _extract_configuration_id(payload_dict):
        """Return the configuration id for the new configuration."""
        return payload_dict["relationships"]["configuration"]["data"]["id"]

    @staticmethod
    def _build_error_message_overlapping_location():
        """Build the error message in case we have an overlapping location."""
        return "".join(
            [
                "There is already a location action that is active ",
                "for parts of the expected location timeline.",
            ]
        )

    @staticmethod
    def _build_error_message_non_available_device_property():
        """Build the error message in case we don't have needed coverage for device property."""
        return "".join(
            [
                "One of the measured quantities is not available ",
                "for the whole location timeline.",
            ]
        )

    @staticmethod
    def _extract_updated_configuration_id(payload_dict, existing_location):
        """
        Extract the configuration id for the update validation case.

        It could be set in the payload or it should still be the one of
        the location action.
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
        return existing_location.configuration_id

    def _extract_updated_begin_and_end_dates(self, payload_dict, existing_location):
        """Extract the begin and end dates for the update case."""
        if "begin_date" in payload_dict["attributes"].keys():
            begin_date_as_string = payload_dict["attributes"]["begin_date"]
            begin_date = self._parse_datetime(begin_date_as_string)
        else:
            begin_date = existing_location.begin_date
        if "end_date" in payload_dict["attributes"].keys():
            end_date_as_string = payload_dict["attributes"]["end_date"]
            if end_date_as_string is not None:
                end_date = self._parse_datetime(end_date_as_string)
            else:
                end_date = None
        else:
            end_date = existing_location.end_date
        return DateTimeRange(begin_date, end_date)

    @abc.abstractmethod
    def _find_first_archived_device(self, payload_dict, existing_location=None):
        """Return an archived device or none."""
        pass


class StaticLocationActionValidator(AbstractLocationActionValidator):
    """Concrete validator implementation for the static location actions."""

    @staticmethod
    def _build_error_message_no_existing_location(id):
        return f"ConfigurationStaticLocationBeginAction(id={id}) not found"

    @staticmethod
    def _find_first_device_property_that_is_not_mounted_for_the_action_time(
        payload_dict,
        existing_location_action,
        expected_date_time_range,
        configuration_id,
    ):
        """Return None as static locations don't refer to device properties."""
        return None

    def _get_overlapping_location(
        self, configuration_id, expected_date_time_range, ignore_id=None
    ):
        """Return an action if there is one that intersects with the expected location timeline."""
        # First, check the static location actions.
        static_location_actions = db.session.query(
            ConfigurationStaticLocationBeginAction
        ).filter_by(configuration_id=configuration_id)
        for static_location_action in static_location_actions:
            # As we are in the validator for the static location actions & those are what we edit,
            # it could be necessary that we need to ignore one entry
            # (the entry that we want to edit for example; it is clear that we don't want to
            # have intersections with those as errors).
            if static_location_action.id != ignore_id:
                action_date_time_range = DateTimeRange(
                    static_location_action.begin_date, static_location_action.end_date
                )
                if expected_date_time_range.overlaps_with(action_date_time_range):
                    return static_location_action
        # Then the dynamic actions.
        dynamic_location_actions = db.session.query(
            ConfigurationDynamicLocationBeginAction
        ).filter_by(configuration_id=configuration_id)
        for dynamic_location_action in dynamic_location_actions:
            # Here we don't check for the id, as it is the other type.
            action_date_time_range = DateTimeRange(
                dynamic_location_action.begin_date, dynamic_location_action.end_date
            )
            if expected_date_time_range.overlaps_with(action_date_time_range):
                return dynamic_location_action
        return None

    def _query_existing_location(self, existing_location_id):
        """Find the static location action for the id or return None."""
        return (
            db.session.query(ConfigurationStaticLocationBeginAction)
            .filter_by(id=existing_location_id)
            .first()
        )

    @staticmethod
    def _find_first_archived_device(payload_dict, existing_location=None):
        return None


class DynamicLocationActionValidator(AbstractLocationActionValidator):
    """Concrete validator implementation for the dynamic location actions."""

    @staticmethod
    def _build_error_message_no_existing_location(id):
        return f"ConfigurationStaticLocationBeginAction(id={id}) not found"

    @staticmethod
    def _find_first_device_property_that_is_not_mounted_for_the_action_time(
        payload_dict,
        existing_location_action,
        expected_date_time_range,
        configuration_id,
    ):
        """
        Return an device property if it is needed but not mounted for the whole timeline.

        If no device property is linked or all are covered by their mounts for the
        whole location time, then return None.
        """
        # Firs extract the device properties that we need to care.
        device_property_ids_to_check = []
        for x in ["x_property", "y_property", "z_property"]:
            if x in payload_dict.get("relationships", {}).keys():
                if "data" in payload_dict["relationships"][x].keys():
                    if payload_dict["relationships"][x]["data"]:
                        device_property_id = payload_dict["relationships"][x][
                            "data"
                        ].get("id")
                        if device_property_id:
                            device_property_ids_to_check.append(device_property_id)
            elif existing_location_action is not None:
                device_property = getattr(existing_location_action, x, None)
                if device_property:
                    device_property_ids_to_check.append(device_property.id)
        device_properties = (
            db.session.query(DeviceProperty)
            .filter(DeviceProperty.id.in_(device_property_ids_to_check))
            .all()
        )
        # Then check each of them.
        # We want to have one mount for our configuration, that covers the whole location action.
        # If we would have only mounts that are unmounted before the end of the location action,
        # then we would have the situation that we could not extract coordinates for that time.
        for device_property in device_properties:
            device_id = device_property.device_id
            device_mounts = db.session.query(DeviceMountAction).filter(
                and_(
                    DeviceMountAction.device_id == device_id,
                    DeviceMountAction.configuration_id == configuration_id,
                )
            )
            is_covered = False
            for device_mount in device_mounts:
                device_mount_date_time_range = DateTimeRange(
                    device_mount.begin_date, device_mount.end_date
                )
                if device_mount_date_time_range.covers(expected_date_time_range):
                    is_covered = True
                    break
            if not is_covered:
                return device_property

        return None

    def _get_overlapping_location(
        self, configuration_id, expected_date_time_range, ignore_id=None
    ):
        """Return a location that overlaps with the planned one - or None."""
        # First check the static location actions.
        static_location_actions = db.session.query(
            ConfigurationStaticLocationBeginAction
        ).filter_by(configuration_id=configuration_id)
        for static_location_action in static_location_actions:
            # We don't filter for the id as this is a different type then we
            # Check (DynamicLocationActionValidator).
            action_date_time_range = DateTimeRange(
                static_location_action.begin_date, static_location_action.end_date
            )
            if expected_date_time_range.overlaps_with(action_date_time_range):
                return static_location_action
        # Then the dynamic location actions
        dynamic_location_actions = db.session.query(
            ConfigurationDynamicLocationBeginAction
        ).filter_by(configuration_id=configuration_id)
        for dynamic_location_action in dynamic_location_actions:
            # Here it can be that we want to update an existing action, so
            # we don't want to consider overlaps here as problems (say I want to
            # extend the location for some days more).
            if dynamic_location_action.id != ignore_id:
                action_date_time_range = DateTimeRange(
                    dynamic_location_action.begin_date, dynamic_location_action.end_date
                )
                if expected_date_time_range.overlaps_with(action_date_time_range):
                    return dynamic_location_action
        return None

    def _query_existing_location(self, existing_location_id):
        """Return the existing location if it is in the db - None otherwise."""
        return (
            db.session.query(ConfigurationDynamicLocationBeginAction)
            .filter_by(id=existing_location_id)
            .first()
        )

    @staticmethod
    def _find_first_archived_device(payload_dict, existing_location=None):
        device_property_ids_to_check = []
        for x in ["x_property", "y_property", "z_property"]:
            if x in payload_dict.get("relationships", {}).keys():
                if "data" in payload_dict["relationships"][x].keys():
                    if payload_dict["relationships"][x]["data"]:
                        device_property_id = payload_dict["relationships"][x][
                            "data"
                        ].get("id")
                        if device_property_id:
                            device_property_ids_to_check.append(device_property_id)
            if existing_location:
                existing_device_property = getattr(existing_location, x, None)
                if existing_device_property:
                    device_property_ids_to_check.append(existing_device_property.id)
        for device_property_id in device_property_ids_to_check:
            device_property = (
                db.session.query(DeviceProperty)
                .filter_by(id=device_property_id)
                .first()
            )
            if device_property:
                device = device_property.device
                if device.archived:
                    return device
        return None
