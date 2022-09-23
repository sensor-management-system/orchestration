"""
Test cases for the validation procedures for changes on mount actions.

As mount actions tell us which devices and platforms are available in
a configuration (or are blocked currently), we need to make sure that
we check if modifications here are valid or not.
"""
import datetime

import pytz

from project.api.helpers.errors import ConflictError, NotFoundError
from project.api.helpers.mounting_checks import (
    DeviceMountActionValidator,
    PlatformMountActionValidator,
)
from project.api.models import (
    Configuration,
    ConfigurationDynamicLocationBeginAction,
    Contact,
    Device,
    DeviceMountAction,
    DeviceProperty,
    Platform,
    PlatformMountAction,
    User,
)
from project.api.models.base_model import db
from project.tests.base import BaseTestCase


class TestDeviceMountActionValidator(BaseTestCase):
    """Test cases for the DeviceMountActionValidator."""

    def setUp(self):
        """Set up some entries to work with in all the test cases."""
        super().setUp()
        self.device1 = Device(
            short_name="Device1",
            is_public=True,
        )
        self.device2 = Device(
            short_name="Device2",
            is_public=True,
        )
        self.configuration1 = Configuration(
            label="Configuration1",
            is_public=True,
        )
        self.configuration2 = Configuration(
            label="Configuration2",
            is_public=True,
        )
        self.contact1 = Contact(
            given_name="Dummy",
            family_name="Tests",
            email="dummy@tests",
        )
        self.user1 = User(
            subject=self.contact1.email,
            contact=self.contact1,
        )
        self.platform1 = Platform(
            short_name="Platform1",
            is_public=True,
        )
        db.session.add_all(
            [
                self.configuration1,
                self.configuration2,
                self.contact1,
                self.device1,
                self.device2,
                self.platform1,
                self.user1,
            ]
        )
        db.session.commit()

    def test_validate_create_passes(self):
        """Ensure that we can create a simple device mount action."""
        existing_device_mount_action = DeviceMountAction(
            configuration=self.configuration1,
            device=self.device1,
            begin_contact=self.contact1,
            begin_date=datetime.datetime(year=2022, month=1, day=1, tzinfo=pytz.UTC),
            end_date=datetime.datetime(year=2030, month=1, day=1, tzinfo=pytz.UTC),
        )
        db.session.add(existing_device_mount_action)
        db.session.commit()
        payload_dict = {
            "relationships": {
                "configuration": {
                    "data": {
                        "id": self.configuration2.id,
                    },
                },
                "device": {
                    "data": {"id": self.device1.id},
                },
            },
            "attributes": {
                "begin_date": "2031-01-01T00:00:00Z",
                "end_date": "2032-01-01T00:00:00Z",
            },
        }
        DeviceMountActionValidator().validate_create(payload_dict)

    def test_validate_create_passes_with_string_ids(self):
        """Ensure that we can create a simple device mount action - even with string ids."""
        existing_device_mount_action = DeviceMountAction(
            configuration=self.configuration1,
            device=self.device1,
            begin_contact=self.contact1,
            begin_date=datetime.datetime(year=2022, month=1, day=1, tzinfo=pytz.UTC),
            end_date=datetime.datetime(year=2030, month=1, day=1, tzinfo=pytz.UTC),
        )
        db.session.add(existing_device_mount_action)
        db.session.commit()
        payload_dict = {
            "relationships": {
                "configuration": {
                    "data": {
                        "id": str(self.configuration2.id),
                    },
                },
                "device": {
                    "data": {"id": str(self.device1.id)},
                },
            },
            "attributes": {
                "begin_date": "2031-01-01T00:00:00Z",
                "end_date": "2032-01-01T00:00:00Z",
            },
        }
        DeviceMountActionValidator().validate_create(payload_dict)

    def test_validate_create_overlapping_mount_for_same_device(self):
        """Ensure that we can't create a mount action if the device is already used."""
        existing_device_mount_action = DeviceMountAction(
            configuration=self.configuration1,
            device=self.device1,
            begin_contact=self.contact1,
            begin_date=datetime.datetime(year=2022, month=1, day=1, tzinfo=pytz.UTC),
            end_date=datetime.datetime(year=2030, month=1, day=1, tzinfo=pytz.UTC),
        )
        db.session.add(existing_device_mount_action)
        db.session.commit()
        payload_dict = {
            "relationships": {
                "configuration": {
                    "data": {"id": self.configuration2.id},
                },
                "device": {
                    "data": {"id": self.device1.id},
                },
            },
            "attributes": {
                "begin_date": "2023-01-01T00:00:00Z",
                "end_date": "2024-01-01T00:00:00Z",
            },
        }
        with self.assertRaises(ConflictError) as context:
            DeviceMountActionValidator().validate_create(payload_dict)
        str_exception = str(context.exception)
        expected_information = [
            "blocked",
            self.configuration1.label,
            str(existing_device_mount_action.begin_date),
            str(existing_device_mount_action.end_date),
        ]
        for information in expected_information:
            self.assertIn(information, str_exception)

    def test_validate_create_overlapping_mount_for_same_device_open_end_existing(self):
        """Ensure we can't use if as it is mounted already on an open interval."""
        existing_device_mount_action = DeviceMountAction(
            configuration=self.configuration1,
            device=self.device1,
            begin_contact=self.contact1,
            begin_date=datetime.datetime(year=2022, month=1, day=1, tzinfo=pytz.UTC),
        )
        db.session.add(existing_device_mount_action)
        db.session.commit()
        payload_dict = {
            "relationships": {
                "configuration": {
                    "data": {"id": self.configuration2.id},
                },
                "device": {
                    "data": {"id": self.device1.id},
                },
            },
            "attributes": {
                "begin_date": "2023-01-01T00:00:00Z",
                "end_date": "2024-01-01T00:00:00Z",
            },
        }
        with self.assertRaises(ConflictError) as context:
            DeviceMountActionValidator().validate_create(payload_dict)
        str_exception = str(context.exception)
        expected_information = [
            "blocked",
            self.configuration1.label,
            str(existing_device_mount_action.begin_date),
        ]
        for information in expected_information:
            self.assertIn(information, str_exception)

    def test_validate_create_no_parent_platform_mount(self):
        """Ensure we can't create if the parent platform is not mounted."""
        payload_dict = {
            "relationships": {
                "configuration": {
                    "data": {"id": self.configuration2.id},
                },
                "device": {
                    "data": {"id": self.device1.id},
                },
                "parent_platform": {
                    "data": {"id": self.platform1.id},
                },
            },
            "attributes": {
                "begin_date": "2023-01-01T00:00:00Z",
            },
        }
        with self.assertRaises(ConflictError) as context:
            DeviceMountActionValidator().validate_create(payload_dict)
        str_exception = str(context.exception)
        expected_information = [
            "Parent platform is not mounted",
            str(datetime.datetime(year=2023, month=1, day=1, tzinfo=pytz.UTC)),
        ]
        for information in expected_information:
            self.assertIn(information, str_exception)

    def test_validate_create_no_parent_platform_mount_for_config(self):
        """Ensure we can't create if the parent platform is not mounted for this config."""
        existing_platform_mount_action = PlatformMountAction(
            # Different configuration
            configuration=self.configuration1,
            platform=self.platform1,
            begin_contact=self.contact1,
            begin_date=datetime.datetime(year=2022, month=1, day=1, tzinfo=pytz.UTC),
        )
        db.session.add(existing_platform_mount_action)
        db.session.commit()
        payload_dict = {
            "relationships": {
                "configuration": {
                    "data": {"id": self.configuration2.id},
                },
                "device": {
                    "data": {"id": self.device1.id},
                },
                "parent_platform": {
                    "data": {"id": self.platform1.id},
                },
            },
            "attributes": {
                "begin_date": "2023-01-01T00:00:00Z",
            },
        }
        with self.assertRaises(ConflictError) as context:
            DeviceMountActionValidator().validate_create(payload_dict)
        str_exception = str(context.exception)
        expected_information = [
            "Parent platform is not mounted",
            str(datetime.datetime(year=2023, month=1, day=1, tzinfo=pytz.UTC)),
        ]
        for information in expected_information:
            self.assertIn(information, str_exception)

    def test_validate_create_no_full_parent_platform_mount_for_config(self):
        """Ensure we can't create if parent platform is not mounted for whole time."""
        existing_platform_mount_action = PlatformMountAction(
            configuration=self.configuration2,
            platform=self.platform1,
            begin_contact=self.contact1,
            begin_date=datetime.datetime(year=2022, month=1, day=1, tzinfo=pytz.UTC),
            end_date=datetime.datetime(year=2024, month=1, day=1, tzinfo=pytz.UTC),
        )
        db.session.add(existing_platform_mount_action)
        db.session.commit()
        payload_dict = {
            "relationships": {
                "configuration": {
                    "data": {"id": self.configuration2.id},
                },
                "device": {
                    "data": {"id": self.device1.id},
                },
                "parent_platform": {
                    "data": {"id": self.platform1.id},
                },
            },
            "attributes": {
                "begin_date": "2023-01-01T00:00:00Z",
            },
        }
        with self.assertRaises(ConflictError) as context:
            DeviceMountActionValidator().validate_create(payload_dict)
        str_exception = str(context.exception)
        expected_information = [
            "Parent platform is not mounted",
            str(datetime.datetime(year=2023, month=1, day=1, tzinfo=pytz.UTC)),
        ]
        for information in expected_information:
            self.assertIn(information, str_exception)

    def test_validate_create_full_parent_platform_mount_for_config(self):
        """Ensure we can create if parent platform is mounted for the interval."""
        existing_platform_mount_action = PlatformMountAction(
            configuration=self.configuration2,
            platform=self.platform1,
            begin_contact=self.contact1,
            begin_date=datetime.datetime(year=2022, month=1, day=1, tzinfo=pytz.UTC),
        )
        db.session.add(existing_platform_mount_action)
        db.session.commit()
        payload_dict = {
            "relationships": {
                "configuration": {
                    "data": {"id": self.configuration2.id},
                },
                "device": {
                    "data": {"id": self.device1.id},
                },
                "parent_platform": {
                    "data": {"id": self.platform1.id},
                },
            },
            "attributes": {
                "begin_date": "2023-01-01T00:00:00Z",
            },
        }
        DeviceMountActionValidator().validate_create(payload_dict)

    def test_validate_update_non_existing_id(self):
        """Ensure that we also check that the element with id exists."""
        with self.assertRaises(NotFoundError):
            DeviceMountActionValidator().validate_update({}, 100000)

    def test_validate_update_passes_simple_updates(self):
        """Ensure we can run simple updates."""
        existing_device_mount_action = DeviceMountAction(
            configuration=self.configuration1,
            device=self.device1,
            begin_contact=self.contact1,
            begin_date=datetime.datetime(year=2022, month=1, day=1, tzinfo=pytz.UTC),
        )
        db.session.add(existing_device_mount_action)
        db.session.commit()

        # Here we test some payloads that should work.
        # If we provide more sophisticated setups, some of
        # those cases may no longer work (if we have location actions
        # refering to the device properties for example.)
        # As we don't execute the changes we can test multiple settings
        # in this single test.
        payloads = [
            # Set end date & update begin_date
            {
                "relationships": {
                    "configuration": {
                        "data": {"id": self.configuration1.id},
                    },
                    "device": {
                        "data": {"id": self.device1.id},
                    },
                },
                "attributes": {
                    "begin_date": "2023-01-01T00:00:00Z",
                    "end_date": "2024-01-01T00:00:00Z",
                },
            },
            # Change the configuration id (works as we don't refer to
            # those device properties at some other point).
            {
                "relationships": {
                    "configuration": {
                        "data": {"id": self.configuration2.id},
                    },
                    "device": {
                        "data": {"id": self.device1.id},
                    },
                },
                "attributes": {
                    "begin_date": "2022-01-01T00:00:00Z",
                },
            },
            # Change the device.
            {
                "relationships": {
                    "configuration": {
                        "data": {"id": self.configuration1.id},
                    },
                    "device": {
                        "data": {"id": self.device2.id},
                    },
                },
                "attributes": {
                    "begin_date": "2022-01-01T00:00:00Z",
                },
            },
        ]
        for payload_dict in payloads:
            DeviceMountActionValidator().validate_update(
                payload_dict, existing_device_mount_action.id
            )

    def test_valdiate_update_overlapping_mount_for_same_device(self):
        """Ensure we can't introduce overlaps by updating the device mount."""
        existing_device_mount_action1 = DeviceMountAction(
            configuration=self.configuration1,
            device=self.device1,
            begin_contact=self.contact1,
            begin_date=datetime.datetime(year=2022, month=1, day=1, tzinfo=pytz.UTC),
            end_date=datetime.datetime(year=2023, month=1, day=1, tzinfo=pytz.UTC),
        )
        existing_device_mount_action2 = DeviceMountAction(
            configuration=self.configuration2,
            device=self.device1,
            begin_contact=self.contact1,
            begin_date=datetime.datetime(year=2024, month=1, day=1, tzinfo=pytz.UTC),
            end_date=datetime.datetime(year=2025, month=1, day=1, tzinfo=pytz.UTC),
        )
        db.session.add_all(
            [existing_device_mount_action1, existing_device_mount_action2]
        )
        db.session.commit()
        payload_dict = {
            "relationships": {
                "configuration": {
                    "data": {"id": self.configuration2.id},
                },
                "device": {
                    "data": {"id": self.device1.id},
                },
            },
            "attributes": {
                "begin_date": "2022-06-01T00:00:00Z",
                "end_date": "2025-01-01T00:00:00Z",
            },
        }
        with self.assertRaises(ConflictError) as context:
            DeviceMountActionValidator().validate_update(
                payload_dict, existing_device_mount_action2.id
            )
        str_exception = str(context.exception)
        expected_information = [
            "blocked",
            self.configuration1.label,
            str(existing_device_mount_action1.begin_date),
            str(existing_device_mount_action1.end_date),
        ]
        for information in expected_information:
            self.assertIn(information, str_exception)

    def test_valdiate_update_no_full_parent_platform_mount(self):
        """Ensure we also check for the parent platform for updates."""
        existing_platform_mount_action1 = PlatformMountAction(
            configuration=self.configuration1,
            platform=self.platform1,
            begin_contact=self.contact1,
            begin_date=datetime.datetime(year=2022, month=1, day=1, tzinfo=pytz.UTC),
            end_date=datetime.datetime(year=2023, month=1, day=1, tzinfo=pytz.UTC),
        )
        existing_device_mount_action1 = DeviceMountAction(
            configuration=self.configuration1,
            device=self.device1,
            parent_platform=self.platform1,
            begin_contact=self.contact1,
            begin_date=datetime.datetime(year=2022, month=1, day=1, tzinfo=pytz.UTC),
            end_date=datetime.datetime(year=2023, month=1, day=1, tzinfo=pytz.UTC),
        )
        db.session.add_all(
            [existing_device_mount_action1, existing_platform_mount_action1]
        )
        db.session.commit()
        payload_dict = {
            "relationships": {},
            "attributes": {
                "begin_date": "2022-06-01T00:00:00Z",
                "end_date": "2024-01-01T00:00:00Z",
            },
        }
        with self.assertRaises(ConflictError) as context:
            DeviceMountActionValidator().validate_update(
                payload_dict, existing_device_mount_action1.id
            )
        str_exception = str(context.exception)
        expected_information = [
            "Parent platform is not mounted",
            str(datetime.datetime(year=2024, month=1, day=1, tzinfo=pytz.UTC)),
        ]
        for information in expected_information:
            self.assertIn(information, str_exception)

        # However, it should work if we set the parent_platform_id explicitly to None
        payload_dict_no_parent_platform = {
            "relationships": {
                "parent_platform": {
                    "data": {"id": None},
                }
            },
            "attributes": {
                "begin_date": "2022-06-01T00:00:00Z",
                "end_date": "2024-01-01T00:00:00Z",
            },
        }
        DeviceMountActionValidator().validate_update(
            payload_dict_no_parent_platform, existing_device_mount_action1.id
        )

    def test_validate_update_still_dynamic_location_reference(self):
        """Ensure we can't remove intervals for that a dynamic location refers to mount."""
        x_coord = DeviceProperty(
            property_name="X coordinate",
            device=self.device1,
        )
        existing_device_mount_action1 = DeviceMountAction(
            configuration=self.configuration1,
            device=self.device1,
            begin_contact=self.contact1,
            begin_date=datetime.datetime(year=2022, month=1, day=1, tzinfo=pytz.UTC),
        )
        dynamic_location_begin = ConfigurationDynamicLocationBeginAction(
            configuration=self.configuration1,
            begin_contact=self.contact1,
            begin_date=datetime.datetime(year=2022, month=1, day=1, tzinfo=pytz.UTC),
            x_property=x_coord,
        )
        db.session.add_all(
            [x_coord, existing_device_mount_action1, dynamic_location_begin]
        )
        db.session.commit()
        payloads = [
            # First one that must fail is to change the configuration.
            # This way the dynamic location action would miss that device
            # property.
            {
                "relationships": {
                    "configuration": {
                        "data": {"id": self.configuration2.id},
                    },
                    "device": {
                        "data": {"id": self.device1.id},
                    },
                },
                "attributes": {
                    "begin_date": "2022-01-01T00:00:00Z",
                },
            },
            # Then we change the device. It fails as well as the
            # dynamic location should still refer to the device property.
            {
                "relationships": {
                    "configuration": {
                        "data": {"id": self.configuration1.id},
                    },
                    "device": {
                        "data": {"id": self.device2.id},
                    },
                },
                "attributes": {
                    "begin_date": "2022-01-01T00:00:00Z",
                },
            },
            # Another option is to take the mount out of scope for
            # the location action (starting the mount after the location action.).
            {
                "relationships": {
                    "configuration": {
                        "data": {"id": self.configuration1.id},
                    },
                    "device": {
                        "data": {"id": self.device1.id},
                    },
                },
                "attributes": {
                    "begin_date": "2022-07-01T00:00:00Z",
                },
            },
        ]
        for payload_dict in payloads:
            with self.assertRaises(ConflictError) as context:
                DeviceMountActionValidator().validate_update(
                    payload_dict, existing_device_mount_action1.id
                )

            str_exception = str(context.exception)
            expected_information = [
                "ConfigurationDynamicLocationBeginAction",
                "not covered",
            ]
            for information in expected_information:
                self.assertIn(information, str_exception)

    def test_validate_update_passes_for_valid_timeintercal_changes_with_dyn_location(
        self,
    ):
        """Ensure we can update intervals if dynamic location action is still covered."""
        x_coord = DeviceProperty(
            property_name="X coordinate",
            device=self.device1,
        )
        existing_device_mount_action1 = DeviceMountAction(
            configuration=self.configuration1,
            device=self.device1,
            begin_contact=self.contact1,
            begin_date=datetime.datetime(year=2022, month=1, day=1, tzinfo=pytz.UTC),
        )
        dynamic_location_begin1 = ConfigurationDynamicLocationBeginAction(
            configuration=self.configuration1,
            begin_contact=self.contact1,
            begin_date=datetime.datetime(year=2023, month=1, day=1, tzinfo=pytz.UTC),
            x_property=x_coord,
            end_date=datetime.datetime(year=2024, month=1, day=1, tzinfo=pytz.UTC),
            end_contact=self.contact1,
        )
        dynamic_location_begin2 = ConfigurationDynamicLocationBeginAction(
            configuration=self.configuration1,
            begin_contact=self.contact1,
            begin_date=datetime.datetime(year=2024, month=2, day=1, tzinfo=pytz.UTC),
            y_property=x_coord,
            end_date=datetime.datetime(year=2025, month=1, day=1, tzinfo=pytz.UTC),
            end_contact=self.contact1,
        )
        dynamic_location_begin3 = ConfigurationDynamicLocationBeginAction(
            configuration=self.configuration1,
            begin_contact=self.contact1,
            begin_date=datetime.datetime(year=2025, month=2, day=1, tzinfo=pytz.UTC),
            y_property=x_coord,
            end_date=datetime.datetime(year=2026, month=1, day=1, tzinfo=pytz.UTC),
            end_contact=self.contact1,
        )
        db.session.add_all(
            [
                x_coord,
                existing_device_mount_action1,
                dynamic_location_begin1,
                dynamic_location_begin2,
                dynamic_location_begin3,
            ]
        )
        db.session.commit()
        payload_dict = {
            "relationships": {
                "configuration": {
                    "data": {"id": self.configuration1.id},
                },
                "device": {
                    "data": {"id": self.device1.id},
                },
            },
            "attributes": {
                "begin_date": "2022-02-01T00:00:00Z",
                "end_date": "2027-01-01T00:00:00Z",
            },
        }
        DeviceMountActionValidator().validate_update(
            payload_dict, existing_device_mount_action1.id
        )

    def test_validate_delete_non_existing_id(self):
        """
        Ensure that we also check that the element with id exists before deletion.

        Normally the main resource handler would care, but we run our validation
        code before - so we have to check ourselves.
        """
        with self.assertRaises(NotFoundError):
            DeviceMountActionValidator().validate_delete(100000)

    def test_validate_delete_still_dynamic_location_reference(self):
        """Ensure we can't delete the mount for that a dynamic location refers to mount."""
        x_coord = DeviceProperty(
            property_name="X coordinate",
            device=self.device1,
        )
        existing_device_mount_action1 = DeviceMountAction(
            configuration=self.configuration1,
            device=self.device1,
            begin_contact=self.contact1,
            begin_date=datetime.datetime(year=2022, month=1, day=1, tzinfo=pytz.UTC),
        )
        dynamic_location_begin = ConfigurationDynamicLocationBeginAction(
            configuration=self.configuration1,
            begin_contact=self.contact1,
            begin_date=datetime.datetime(year=2022, month=1, day=1, tzinfo=pytz.UTC),
            x_property=x_coord,
        )
        db.session.add_all(
            [x_coord, existing_device_mount_action1, dynamic_location_begin]
        )
        db.session.commit()
        with self.assertRaises(ConflictError) as context:
            DeviceMountActionValidator().validate_delete(
                existing_device_mount_action1.id
            )

        str_exception = str(context.exception)
        expected_information = [
            "ConfigurationDynamicLocationBeginAction",
            "not covered",
        ]
        for information in expected_information:
            self.assertIn(information, str_exception)

    def test_validate_delete_passes(self):
        """Ensure we can delete for a simple use case."""
        existing_device_mount_action1 = DeviceMountAction(
            configuration=self.configuration1,
            device=self.device1,
            begin_contact=self.contact1,
            begin_date=datetime.datetime(year=2022, month=1, day=1, tzinfo=pytz.UTC),
        )
        db.session.add(existing_device_mount_action1)
        db.session.commit()
        DeviceMountActionValidator().validate_delete(existing_device_mount_action1.id)

    def test_extract_updated_begin_and_end_dates_no_dates_in_payload(self):
        """Ensure we can extract the dates from the object."""
        existing_device_mount_action1 = DeviceMountAction(
            configuration=self.configuration1,
            device=self.device1,
            begin_contact=self.contact1,
            begin_date=datetime.datetime(year=2022, month=1, day=1, tzinfo=pytz.UTC),
            end_date=datetime.datetime(year=2023, month=1, day=1, tzinfo=pytz.UTC),
        )
        existing_device_mount_action2 = DeviceMountAction(
            configuration=self.configuration1,
            device=self.device1,
            begin_contact=self.contact1,
            begin_date=datetime.datetime(year=2022, month=1, day=1, tzinfo=pytz.UTC),
            end_date=None,
        )
        payload_dict = {"attributes": {}}
        for mount in [existing_device_mount_action1, existing_device_mount_action2]:

            time_range = (
                DeviceMountActionValidator()._extract_updated_begin_and_end_dates(
                    payload_dict, mount
                )
            )
            self.assertEqual(time_range.begin_date, mount.begin_date)
            self.assertEqual(time_range.end_date, mount.end_date)

    def test_extract_updated_begin_and_end_dates_dates_in_payload(self):
        """Ensure we can extract the dates from the payload."""
        existing_device_mount_action1 = DeviceMountAction(
            configuration=self.configuration1,
            device=self.device1,
            begin_contact=self.contact1,
            begin_date=datetime.datetime(year=2022, month=1, day=1, tzinfo=pytz.UTC),
            end_date=datetime.datetime(year=2023, month=1, day=1, tzinfo=pytz.UTC),
        )
        payload_dict = {
            "attributes": {
                "begin_date": "2024-01-01T00:00:00Z",
                "end_date": "2026-01-01T00:00:00Z",
            }
        }

        time_range = DeviceMountActionValidator()._extract_updated_begin_and_end_dates(
            payload_dict, existing_device_mount_action1
        )
        self.assertEqual(
            time_range.begin_date,
            datetime.datetime(year=2024, month=1, day=1, tzinfo=pytz.UTC),
        )
        self.assertEqual(
            time_range.end_date,
            datetime.datetime(year=2026, month=1, day=1, tzinfo=pytz.UTC),
        )

    def test_extract_updated_begin_and_end_dates_none_end_date_from_payload(self):
        """Ensure we can extract the none end date from the payload."""
        existing_device_mount_action1 = DeviceMountAction(
            configuration=self.configuration1,
            device=self.device1,
            begin_contact=self.contact1,
            begin_date=datetime.datetime(year=2022, month=1, day=1, tzinfo=pytz.UTC),
            end_date=datetime.datetime(year=2023, month=1, day=1, tzinfo=pytz.UTC),
        )
        payload_dict = {
            "attributes": {
                "begin_date": "2024-01-01T00:00:00Z",
                "end_date": None,
            }
        }

        time_range = DeviceMountActionValidator()._extract_updated_begin_and_end_dates(
            payload_dict, existing_device_mount_action1
        )
        self.assertEqual(
            time_range.begin_date,
            datetime.datetime(year=2024, month=1, day=1, tzinfo=pytz.UTC),
        )
        self.assertEqual(time_range.end_date, None)


class TestPlatformMountActionValidator(BaseTestCase):
    """Test cases for the PlatformMountActionValidator."""

    def setUp(self):
        """Set up some entries for the tests."""
        super().setUp()
        self.device1 = Device(
            short_name="Device1",
            is_public=True,
        )
        self.configuration1 = Configuration(
            label="Configuration1",
            is_public=True,
        )
        self.configuration2 = Configuration(
            label="Configuration2",
            is_public=True,
        )
        self.contact1 = Contact(
            given_name="Dummy",
            family_name="Tests",
            email="dummy@tests",
        )
        self.user1 = User(
            subject=self.contact1.email,
            contact=self.contact1,
        )
        self.platform1 = Platform(
            short_name="Platform1",
            is_public=True,
        )
        self.platform2 = Platform(
            short_name="Platform2",
            is_public=True,
        )
        db.session.add_all(
            [
                self.configuration1,
                self.configuration2,
                self.device1,
                self.platform1,
                self.platform2,
                self.user1,
            ]
        )
        db.session.commit()

    def test_validate_create_passes(self):
        """Ensure we can create platform mount actions."""
        existing_platform_mount_action = PlatformMountAction(
            configuration=self.configuration1,
            platform=self.platform1,
            begin_contact=self.contact1,
            begin_date=datetime.datetime(year=2022, month=1, day=1, tzinfo=pytz.UTC),
            end_date=datetime.datetime(year=2030, month=1, day=1, tzinfo=pytz.UTC),
        )
        db.session.add(existing_platform_mount_action)
        db.session.commit()
        payload_dict = {
            "relationships": {
                "configuration": {
                    "data": {"id": self.configuration2.id},
                },
                "platform": {
                    "data": {"id": self.platform1.id},
                },
            },
            "attributes": {
                "begin_date": "2031-01-01T00:00:00Z",
                "end_date": "2032-01-01T00:00:00Z",
            },
        }
        PlatformMountActionValidator().validate_create(payload_dict)

    def test_validate_create_overlapping_mount_for_same_platform(self):
        """Ensure we can't use a platform that is blocked for that interal already."""
        existing_platform_mount_action = PlatformMountAction(
            configuration=self.configuration1,
            platform=self.platform1,
            begin_contact=self.contact1,
            begin_date=datetime.datetime(year=2022, month=1, day=1, tzinfo=pytz.UTC),
            end_date=datetime.datetime(year=2030, month=1, day=1, tzinfo=pytz.UTC),
        )
        db.session.add(existing_platform_mount_action)
        db.session.commit()
        payload_dict = {
            "relationships": {
                "configuration": {
                    "data": {"id": self.configuration2.id},
                },
                "platform": {
                    "data": {"id": self.platform1.id},
                },
            },
            "attributes": {
                "begin_date": "2023-01-01T00:00:00Z",
                "end_date": "2024-01-01T00:00:00Z",
            },
        }
        with self.assertRaises(ConflictError) as context:
            PlatformMountActionValidator().validate_create(payload_dict)
        str_exception = str(context.exception)
        expected_information = [
            "blocked",
            self.configuration1.label,
            str(existing_platform_mount_action.begin_date),
            str(existing_platform_mount_action.end_date),
        ]
        for information in expected_information:
            self.assertIn(information, str_exception)

    def test_validate_create_overlapping_mount_for_same_platform_open_end_existing(
        self,
    ):
        """Ensure that we also check for open end intervals."""
        existing_platform_mount_action = PlatformMountAction(
            configuration=self.configuration1,
            platform=self.platform1,
            begin_contact=self.contact1,
            begin_date=datetime.datetime(year=2022, month=1, day=1, tzinfo=pytz.UTC),
        )
        db.session.add(existing_platform_mount_action)
        db.session.commit()
        payload_dict = {
            "relationships": {
                "configuration": {
                    "data": {"id": self.configuration2.id},
                },
                "platform": {
                    "data": {"id": self.platform1.id},
                },
            },
            "attributes": {
                "begin_date": "2023-01-01T00:00:00Z",
                "end_date": "2024-01-01T00:00:00Z",
            },
        }
        with self.assertRaises(ConflictError) as context:
            PlatformMountActionValidator().validate_create(payload_dict)
        str_exception = str(context.exception)
        expected_information = [
            "blocked",
            self.configuration1.label,
            str(existing_platform_mount_action.begin_date),
        ]
        for information in expected_information:
            self.assertIn(information, str_exception)

    def test_validate_create_no_parent_platform_mount(self):
        """Ensure we also check if the parent platform is mounted for that interval."""
        payload_dict = {
            "relationships": {
                "configuration": {
                    "data": {"id": self.configuration2.id},
                },
                "platform": {
                    "data": {"id": self.platform1.id},
                },
                "parent_platform": {
                    "data": {"id": self.platform2.id},
                },
            },
            "attributes": {
                "begin_date": "2023-01-01T00:00:00Z",
            },
        }
        with self.assertRaises(ConflictError) as context:
            PlatformMountActionValidator().validate_create(payload_dict)
        str_exception = str(context.exception)
        expected_information = [
            "Parent platform is not mounted",
            str(datetime.datetime(year=2023, month=1, day=1, tzinfo=pytz.UTC)),
        ]
        for information in expected_information:
            self.assertIn(information, str_exception)

    def test_validate_create_no_parent_platform_mount_for_config(self):
        """Ensure we check the parent platform for the current configuration."""
        existing_platform_mount_action = PlatformMountAction(
            # Different configuration
            configuration=self.configuration1,
            platform=self.platform2,
            begin_contact=self.contact1,
            begin_date=datetime.datetime(year=2022, month=1, day=1, tzinfo=pytz.UTC),
        )
        db.session.add(existing_platform_mount_action)
        db.session.commit()
        payload_dict = {
            "relationships": {
                "configuration": {
                    "data": {"id": self.configuration2.id},
                },
                "platform": {
                    "data": {"id": self.platform1.id},
                },
                "parent_platform": {
                    "data": {"id": self.platform2.id},
                },
            },
            "attributes": {
                "begin_date": "2023-01-01T00:00:00Z",
            },
        }
        with self.assertRaises(ConflictError) as context:
            PlatformMountActionValidator().validate_create(payload_dict)
        str_exception = str(context.exception)
        expected_information = [
            "Parent platform is not mounted",
            str(datetime.datetime(year=2023, month=1, day=1, tzinfo=pytz.UTC)),
        ]
        for information in expected_information:
            self.assertIn(information, str_exception)

    def test_validate_create_no_full_parent_platform_mount_for_config(self):
        """Ensure we need to cover all of the planned time range by the parent mount."""
        existing_platform_mount_action = PlatformMountAction(
            configuration=self.configuration2,
            platform=self.platform2,
            begin_contact=self.contact1,
            begin_date=datetime.datetime(year=2022, month=1, day=1, tzinfo=pytz.UTC),
            end_date=datetime.datetime(year=2024, month=1, day=1, tzinfo=pytz.UTC),
        )
        db.session.add(existing_platform_mount_action)
        db.session.commit()
        payload_dict = {
            "relationships": {
                "configuration": {
                    "data": {"id": self.configuration2.id},
                },
                "platform": {
                    "data": {"id": self.platform1.id},
                },
                "parent_platform": {
                    "data": {"id": self.platform2.id},
                },
            },
            "attributes": {
                "begin_date": "2023-01-01T00:00:00Z",
            },
        }
        with self.assertRaises(ConflictError) as context:
            PlatformMountActionValidator().validate_create(payload_dict)
        str_exception = str(context.exception)
        expected_information = [
            "Parent platform is not mounted",
            str(datetime.datetime(year=2023, month=1, day=1, tzinfo=pytz.UTC)),
        ]
        for information in expected_information:
            self.assertIn(information, str_exception)

    def test_validate_create_full_parent_platform_mount_for_config(self):
        """Ensure we can create the mount if the parent platform mount covers our time range."""
        existing_platform_mount_action = PlatformMountAction(
            configuration=self.configuration2,
            platform=self.platform2,
            begin_contact=self.contact1,
            begin_date=datetime.datetime(year=2022, month=1, day=1, tzinfo=pytz.UTC),
        )
        db.session.add(existing_platform_mount_action)
        db.session.commit()
        payload_dict = {
            "relationships": {
                "configuration": {
                    "data": {"id": self.configuration2.id},
                },
                "platform": {
                    "data": {"id": self.platform1.id},
                },
                "parent_platform": {
                    "data": {"id": self.platform2.id},
                },
            },
            "attributes": {
                "begin_date": "2023-01-01T00:00:00Z",
            },
        }
        PlatformMountActionValidator().validate_create(payload_dict)

    def test_validate_update_non_existing_id(self):
        """Ensure that we also check that the element with id exists."""
        with self.assertRaises(NotFoundError):
            PlatformMountActionValidator().validate_update({}, 100000)

    def test_validate_update_passes_simple_updates(self):
        """Ensure we can run simple updates."""
        existing_platform_mount_action = PlatformMountAction(
            configuration=self.configuration1,
            platform=self.platform1,
            begin_contact=self.contact1,
            begin_date=datetime.datetime(year=2022, month=1, day=1, tzinfo=pytz.UTC),
        )
        db.session.add(existing_platform_mount_action)
        db.session.commit()

        # Here we test some payloads that should work.
        # If we provide more sophisticated setups, some of
        # those cases may no longer work (if we have location actions
        # refering to the device properties for example.)
        # As we don't execute the changes we can test multiple settings
        # in this single test.
        payloads = [
            # Set end date & update begin_date
            {
                "relationships": {
                    "configuration": {
                        "data": {"id": self.configuration1.id},
                    },
                    "platform": {
                        "data": {"id": self.platform1.id},
                    },
                },
                "attributes": {
                    "begin_date": "2023-01-01T00:00:00Z",
                    "end_date": "2024-01-01T00:00:00Z",
                },
            },
            # Change the configuration id (works as we don't refer to
            # other mounts that have our platform as a parent_platform)
            {
                "relationships": {
                    "configuration": {
                        "data": {"id": self.configuration2.id},
                    },
                    "platform": {
                        "data": {"id": self.platform1.id},
                    },
                },
                "attributes": {
                    "begin_date": "2022-01-01T00:00:00Z",
                },
            },
            # Change the platform.
            {
                "relationships": {
                    "configuration": {
                        "data": {"id": self.configuration1.id},
                    },
                    "platform": {
                        "data": {"id": self.platform2.id},
                    },
                },
                "attributes": {
                    "begin_date": "2022-01-01T00:00:00Z",
                },
            },
        ]
        for payload_dict in payloads:
            PlatformMountActionValidator().validate_update(
                payload_dict, existing_platform_mount_action.id
            )

    def test_valdiate_update_overlapping_mount_for_same_platform(self):
        """Ensure we can't introduce overlaps in platform use by updating."""
        existing_platform_mount_action1 = PlatformMountAction(
            configuration=self.configuration1,
            platform=self.platform1,
            begin_contact=self.contact1,
            begin_date=datetime.datetime(year=2022, month=1, day=1, tzinfo=pytz.UTC),
            end_date=datetime.datetime(year=2023, month=1, day=1, tzinfo=pytz.UTC),
        )
        existing_platform_mount_action2 = PlatformMountAction(
            configuration=self.configuration2,
            platform=self.platform1,
            begin_contact=self.contact1,
            begin_date=datetime.datetime(year=2024, month=1, day=1, tzinfo=pytz.UTC),
            end_date=datetime.datetime(year=2025, month=1, day=1, tzinfo=pytz.UTC),
        )
        db.session.add_all(
            [existing_platform_mount_action1, existing_platform_mount_action2]
        )
        db.session.commit()
        payload_dict = {
            "relationships": {
                "configuration": {
                    "data": {"id": self.configuration2.id},
                },
                "platform": {
                    "data": {"id": self.platform1.id},
                },
            },
            "attributes": {
                "begin_date": "2022-06-01T00:00:00Z",
                "end_date": "2025-01-01T00:00:00Z",
            },
        }
        with self.assertRaises(ConflictError) as context:
            PlatformMountActionValidator().validate_update(
                payload_dict, existing_platform_mount_action2.id
            )
        str_exception = str(context.exception)
        expected_information = [
            "blocked",
            self.configuration1.label,
            str(existing_platform_mount_action1.begin_date),
            str(existing_platform_mount_action1.end_date),
        ]
        for information in expected_information:
            self.assertIn(information, str_exception)

    def test_valdiate_update_no_full_parent_platform_mount(self):
        """Ensure we check for the parent platform coverage on updating."""
        existing_platform_mount_action1 = PlatformMountAction(
            configuration=self.configuration1,
            platform=self.platform1,
            begin_contact=self.contact1,
            begin_date=datetime.datetime(year=2022, month=1, day=1, tzinfo=pytz.UTC),
            end_date=datetime.datetime(year=2023, month=1, day=1, tzinfo=pytz.UTC),
        )
        existing_platform_mount_action2 = PlatformMountAction(
            configuration=self.configuration1,
            platform=self.platform2,
            parent_platform=self.platform1,
            begin_contact=self.contact1,
            begin_date=datetime.datetime(year=2022, month=1, day=1, tzinfo=pytz.UTC),
            end_date=datetime.datetime(year=2023, month=1, day=1, tzinfo=pytz.UTC),
        )
        db.session.add_all(
            [existing_platform_mount_action1, existing_platform_mount_action2]
        )
        db.session.commit()
        payload_dict = {
            "relationships": {},
            "attributes": {
                "begin_date": "2022-06-01T00:00:00Z",
                "end_date": "2024-01-01T00:00:00Z",
            },
        }
        with self.assertRaises(ConflictError) as context:
            PlatformMountActionValidator().validate_update(
                payload_dict, existing_platform_mount_action2.id
            )
        str_exception = str(context.exception)
        expected_information = [
            "Parent platform is not mounted",
            str(datetime.datetime(year=2024, month=1, day=1, tzinfo=pytz.UTC)),
        ]
        for information in expected_information:
            self.assertIn(information, str_exception)

        # However, it should work if we set the parent_platform_id explicitly to None
        payload_dict_no_parent_platform = {
            "relationships": {
                "parent_platform": {
                    "data": {"id": None},
                }
            },
            "attributes": {
                "begin_date": "2022-06-01T00:00:00Z",
                "end_date": "2024-01-01T00:00:00Z",
            },
        }
        PlatformMountActionValidator().validate_update(
            payload_dict_no_parent_platform, existing_platform_mount_action2.id
        )

    def test_validate_update_still_child_mounts(self):
        """Ensure we check if the child mounts are also covered after the change."""
        existing_platform_mount_action1 = PlatformMountAction(
            configuration=self.configuration1,
            platform=self.platform1,
            begin_contact=self.contact1,
            begin_date=datetime.datetime(year=2022, month=1, day=1, tzinfo=pytz.UTC),
        )
        existing_device_mount_action1 = DeviceMountAction(
            configuration=self.configuration1,
            device=self.device1,
            parent_platform=self.platform1,
            begin_contact=self.contact1,
            begin_date=datetime.datetime(year=2022, month=1, day=1, tzinfo=pytz.UTC),
        )
        db.session.add_all(
            [
                existing_platform_mount_action1,
                existing_device_mount_action1,
            ]
        )
        db.session.commit()
        payloads = [
            # First one that must fail is to change the configuration.
            # This way the dynamic location action would miss that device
            # property.
            {
                "relationships": {
                    "configuration": {
                        "data": {"id": self.configuration2.id},
                    },
                    "platform": {
                        "data": {"id": self.platform1.id},
                    },
                },
                "attributes": {
                    "begin_date": "2022-01-01T00:00:00Z",
                },
            },
            # Then we change the platform. It fails as well as the
            # child mounts still refer to the parent platform.
            {
                "relationships": {
                    "configuration": {
                        "data": {"id": self.configuration1.id},
                    },
                    "platform": {
                        "data": {"id": self.platform2.id},
                    },
                },
                "attributes": {
                    "begin_date": "2022-01-01T00:00:00Z",
                },
            },
            # Another option is to take the mount out of scope for
            # the sub mounts.
            {
                "relationships": {
                    "configuration": {
                        "data": {"id": self.configuration1.id},
                    },
                    "platform": {
                        "data": {"id": self.platform1.id},
                    },
                },
                "attributes": {
                    "begin_date": "2022-07-01T00:00:00Z",
                },
            },
        ]
        for payload_dict in payloads:
            with self.assertRaises(ConflictError) as context:
                PlatformMountActionValidator().validate_update(
                    payload_dict, existing_platform_mount_action1.id
                )

            str_exception = str(context.exception)
            expected_information = [
                "child mount",
                "not covered",
            ]
            for information in expected_information:
                self.assertIn(information, str_exception)

    def test_validate_update_pass_example(self):
        """
        Test that the validation passes for an example.

        This example was made by Tim.
        """
        db.drop_all()
        db.create_all()
        db.session.commit()

        contact = Contact(given_name="T", family_name="E", email="t.e@ufz.de")
        device = Device(short_name="dummy device")
        platform = Platform(short_name="dummy platform")
        configuration = Configuration(label="dummy config")

        platform_mount = PlatformMountAction(
            platform=platform,
            configuration=configuration,
            begin_contact=contact,
            end_contact=None,
            begin_date=datetime.datetime(
                year=2022, month=8, day=19, hour=9, minute=8, second=57, tzinfo=pytz.UTC
            ),
            begin_description="",
            offset_x=0,
            offset_y=0,
            offset_z=0,
        )
        device_mount = DeviceMountAction(
            parent_platform=platform,
            configuration=configuration,
            device=device,
            begin_contact=contact,
            end_contact=contact,
            begin_date=datetime.datetime(
                year=2022, month=8, day=19, hour=9, minute=9, second=17, tzinfo=pytz.UTC
            ),
            end_date=datetime.datetime(
                year=2022, month=8, day=19, hour=9, minute=9, second=35, tzinfo=pytz.UTC
            ),
            begin_description="",
            end_description="",
            offset_x=0,
            offset_y=0,
            offset_z=0,
        )
        db.session.add_all(
            [contact, device, platform, configuration, platform_mount, device_mount]
        )
        db.session.commit()

        payload_dict = {
            "type": "platform_mount_action",
            "attributes": {
                "offset_x": 0,
                "offset_y": 0,
                "offset_z": 0,
                "begin_description": "",
                "end_description": "",
                "begin_date": "2022-08-19T09:08:57.658Z",
                "end_date": "2022-08-19T09:10:20.530Z",
            },
            "relationships": {
                "platform": {"data": {"type": "platform", "id": str(platform.id)}},
                "begin_contact": {"data": {"type": "contact", "id": str(contact.id)}},
                "configuration": {
                    "data": {"type": "configuration", "id": str(configuration.id)}
                },
                "end_contact": {"data": {"type": "contact", "id": str(contact.id)}},
            },
        }
        PlatformMountActionValidator().validate_update(payload_dict, platform_mount.id)

    def test_validate_delete_non_existing_id(self):
        """
        Ensure that we also check that the element with id exists before deletion.

        Normally the main resource handler would care, but we run our validation
        code before - so we have to check ourselves.
        """
        with self.assertRaises(NotFoundError):
            PlatformMountActionValidator().validate_delete(100000)

    def test_validate_delete_still_child_mounts(self):
        """Ensure we can't delete if we still have child mounts."""
        existing_platform_mount_action1 = PlatformMountAction(
            configuration=self.configuration1,
            platform=self.platform1,
            begin_contact=self.contact1,
            begin_date=datetime.datetime(year=2022, month=1, day=1, tzinfo=pytz.UTC),
        )
        existing_device_mount_action1 = DeviceMountAction(
            configuration=self.configuration1,
            device=self.device1,
            parent_platform=self.platform1,
            begin_contact=self.contact1,
            begin_date=datetime.datetime(year=2022, month=1, day=1, tzinfo=pytz.UTC),
        )
        db.session.add_all(
            [
                existing_platform_mount_action1,
                existing_device_mount_action1,
            ]
        )
        db.session.commit()
        with self.assertRaises(ConflictError) as context:
            PlatformMountActionValidator().validate_delete(
                existing_platform_mount_action1.id
            )

        str_exception = str(context.exception)
        expected_information = [
            "child mount",
            "not covered",
        ]
        for information in expected_information:
            self.assertIn(information, str_exception)

    def test_validate_delete_still_child_mount_platform(self):
        """Ensure we can't delete if we still have child mounts (platforms)."""
        existing_platform_mount_action1 = PlatformMountAction(
            configuration=self.configuration1,
            platform=self.platform1,
            begin_contact=self.contact1,
            begin_date=datetime.datetime(year=2022, month=1, day=1, tzinfo=pytz.UTC),
        )
        existing_platform_mount_action2 = PlatformMountAction(
            configuration=self.configuration1,
            platform=self.platform2,
            parent_platform=self.platform1,
            begin_contact=self.contact1,
            begin_date=datetime.datetime(year=2022, month=1, day=1, tzinfo=pytz.UTC),
        )
        db.session.add_all(
            [
                existing_platform_mount_action1,
                existing_platform_mount_action2,
            ]
        )
        db.session.commit()
        with self.assertRaises(ConflictError) as context:
            PlatformMountActionValidator().validate_delete(
                existing_platform_mount_action1.id
            )

        str_exception = str(context.exception)
        expected_information = [
            "child mount",
            "not covered",
        ]
        for information in expected_information:
            self.assertIn(information, str_exception)

    def test_validate_delete_passes(self):
        """Ensure we can delete in simple cases."""
        existing_platform_mount_action1 = PlatformMountAction(
            configuration=self.configuration1,
            platform=self.platform1,
            begin_contact=self.contact1,
            begin_date=datetime.datetime(year=2022, month=1, day=1, tzinfo=pytz.UTC),
        )
        db.session.add(existing_platform_mount_action1)
        db.session.commit()
        PlatformMountActionValidator().validate_delete(
            existing_platform_mount_action1.id
        )
