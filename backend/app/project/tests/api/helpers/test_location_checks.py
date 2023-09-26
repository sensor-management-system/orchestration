# SPDX-FileCopyrightText: 2022
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""
Test cases for the validation procedures for changes on location actions.

Location actions should give us an idea about where the configuration
currently is.
So we should care that we don't have multiple location actions on the
same time, so that the question about where it is should not give
us ambiguities.

Also we need to make sure that if we link device properties, that
we can be sure that those are covered for the whole time.
"""

import datetime

from project.api.helpers.errors import ConflictError, NotFoundError
from project.api.helpers.location_checks import (
    DynamicLocationActionValidator,
    StaticLocationActionValidator,
)
from project.api.models import (
    Configuration,
    ConfigurationDynamicLocationBeginAction,
    ConfigurationStaticLocationBeginAction,
    Contact,
    Device,
    DeviceMountAction,
    DeviceProperty,
    User,
)
from project.api.models.base_model import db
from project.tests.base import BaseTestCase


class TestStaticLocationActionValidator(BaseTestCase):
    """Test cases for the static location validation."""

    def setUp(self):
        """Set the tests up."""
        super().setUp()
        self.contact1 = Contact(given_name="A", family_name="B", email="A@B")
        self.user1 = User(subject="A@B", contact=self.contact1)
        self.configuration1 = Configuration(is_public=True, label="Conf1")
        self.configuration2 = Configuration(is_public=True, label="Conf2")
        self.configuration3 = Configuration(is_public=True, label="Conf3")
        db.session.add_all(
            [
                self.contact1,
                self.user1,
                self.configuration1,
                self.configuration2,
                self.configuration3,
            ]
        )
        db.session.commit()

    def test_validate_create_pass_with_end(self):
        """Test that we can simply create a location if there is nothing."""
        payload_dict = {
            "relationships": {
                "configuration": {"data": {"id": self.configuration1.id}},
            },
            "attributes": {
                "begin_date": "2022-08-30T15:50:00.00Z",
                "end_date": "2022-08-31T11:11:11.00Z",
            },
        }
        StaticLocationActionValidator().validate_create(payload_dict)

    def test_validate_create_pass_no_end(self):
        """Test that we can also set the end date to none if there is nothing yet."""
        payload_dict = {
            "relationships": {
                "configuration": {"data": {"id": self.configuration1.id}},
            },
            "attributes": {
                "begin_date": "2022-08-30T15:50:00.00Z",
                "end_date": None,
            },
        }
        StaticLocationActionValidator().validate_create(payload_dict)

    def test_validate_create_pass_as_other_configuration(self):
        """Test that we can create as the other ones are in a different configuration."""
        static_location_action = ConfigurationStaticLocationBeginAction(
            configuration=self.configuration2,
            begin_date=datetime.datetime(2022, 8, 30, 0, 0, 0),
            end_date=datetime.datetime(2022, 9, 2, 23, 59, 59),
            begin_contact=self.contact1,
            end_contact=self.contact1,
            begin_description="begin",
        )
        dynamic_location_action = ConfigurationDynamicLocationBeginAction(
            configuration=self.configuration3,
            begin_date=datetime.datetime(2022, 8, 30, 0, 0, 0),
            end_date=datetime.datetime(2022, 9, 2, 23, 59, 59),
            begin_contact=self.contact1,
            end_contact=self.contact1,
            begin_description="begin",
        )
        db.session.add_all(
            [
                static_location_action,
                dynamic_location_action,
            ]
        )
        db.session.commit()

        payload_dict = {
            "relationships": {
                "configuration": {"data": {"id": self.configuration1.id}},
            },
            "attributes": {
                "begin_date": "2022-08-30T15:50:00.00Z",
                "end_date": None,
            },
        }
        StaticLocationActionValidator().validate_create(payload_dict)

    def test_validate_create_fail_as_intersecting_static_location_action(self):
        """Validate that we realize a possible overlap with a static location."""
        static_location_action = ConfigurationStaticLocationBeginAction(
            configuration=self.configuration1,
            begin_date=datetime.datetime(2022, 8, 30, 0, 0, 0),
            end_date=datetime.datetime(2022, 9, 2, 23, 59, 59),
            begin_contact=self.contact1,
            end_contact=self.contact1,
            begin_description="begin",
        )
        db.session.add_all(
            [
                static_location_action,
            ]
        )
        db.session.commit()

        payload_dict = {
            "relationships": {
                "configuration": {"data": {"id": self.configuration1.id}},
            },
            "attributes": {
                "begin_date": "2022-08-30T15:50:00.00Z",
                "end_date": None,
            },
        }
        with self.assertRaises(ConflictError):
            StaticLocationActionValidator().validate_create(payload_dict)

    def test_validate_create_pass_no_intersecting_static_location_action(self):
        """Allow the creation if we don't have an overlap with a static locaiton action."""
        static_location_action = ConfigurationStaticLocationBeginAction(
            configuration=self.configuration1,
            begin_date=datetime.datetime(2022, 8, 30, 0, 0, 0),
            end_date=datetime.datetime(2022, 9, 2, 23, 59, 59),
            begin_contact=self.contact1,
            end_contact=self.contact1,
            begin_description="begin",
        )
        db.session.add_all(
            [
                static_location_action,
            ]
        )
        db.session.commit()

        payload_dict = {
            "relationships": {
                "configuration": {"data": {"id": self.configuration1.id}},
            },
            "attributes": {
                "begin_date": "2022-10-30T15:50:00.00Z",
                "end_date": None,
            },
        }
        StaticLocationActionValidator().validate_create(payload_dict)

    def test_validate_create_pass_no_intersecting_dynamic_location_action(self):
        """Allow the creation if we don't have an overlap with a static locaiton action."""
        dynamic_location_action = ConfigurationDynamicLocationBeginAction(
            configuration=self.configuration1,
            begin_date=datetime.datetime(2022, 8, 30, 0, 0, 0),
            end_date=datetime.datetime(2022, 9, 2, 23, 59, 59),
            begin_contact=self.contact1,
            end_contact=self.contact1,
            begin_description="begin",
        )
        db.session.add_all(
            [
                dynamic_location_action,
            ]
        )
        db.session.commit()

        payload_dict = {
            "relationships": {
                "configuration": {"data": {"id": self.configuration1.id}},
            },
            "attributes": {
                "begin_date": "2022-10-30T15:50:00.00Z",
                "end_date": None,
            },
        }
        StaticLocationActionValidator().validate_create(payload_dict)

    def test_validate_create_fail_as_intersecting_dynamic_location_action(self):
        """Validate that we see a possible overlap with a dynamic location."""
        dynamic_location_action = ConfigurationDynamicLocationBeginAction(
            configuration=self.configuration1,
            begin_date=datetime.datetime(2022, 8, 30, 0, 0, 0),
            end_date=datetime.datetime(2022, 9, 2, 23, 59, 59),
            begin_contact=self.contact1,
            end_contact=self.contact1,
            begin_description="begin",
        )
        db.session.add_all(
            [
                dynamic_location_action,
            ]
        )
        db.session.commit()

        payload_dict = {
            "relationships": {
                "configuration": {"data": {"id": self.configuration1.id}},
            },
            "attributes": {
                "begin_date": "2022-08-30T15:50:00.00Z",
                "end_date": None,
            },
        }
        with self.assertRaises(ConflictError):
            StaticLocationActionValidator().validate_create(payload_dict)

    def test_validate_update_pass(self):
        """Validate that we can update an existing static location action."""
        static_location_action = ConfigurationStaticLocationBeginAction(
            configuration=self.configuration1,
            begin_date=datetime.datetime(2022, 8, 30, 0, 0, 0),
            end_date=datetime.datetime(2022, 9, 2, 23, 59, 59),
            begin_contact=self.contact1,
            end_contact=self.contact1,
            begin_description="begin",
        )
        db.session.add_all(
            [
                static_location_action,
            ]
        )
        db.session.commit()

        payload_dict = {"attributes": {"end_date": "2022-09-05T12:12:12.00Z"}}
        StaticLocationActionValidator().validate_update(
            payload_dict, static_location_action.id
        )

    def test_validate_update_fail_not_found(self):
        """Validate that we check if the static location action is there."""
        with self.assertRaises(NotFoundError):
            StaticLocationActionValidator().validate_update({}, 100000)

    def test_validate_update_fail_overlapping_static_location(self):
        """Validate that we don't allow overlapping static locations on update."""
        static_location_action1 = ConfigurationStaticLocationBeginAction(
            configuration=self.configuration1,
            begin_date=datetime.datetime(2022, 8, 30, 0, 0, 0),
            end_date=datetime.datetime(2022, 9, 2, 23, 59, 59),
            begin_contact=self.contact1,
            end_contact=self.contact1,
            begin_description="begin",
        )
        static_location_action2 = ConfigurationStaticLocationBeginAction(
            configuration=self.configuration1,
            begin_date=datetime.datetime(2022, 9, 3, 0, 0, 0),
            end_date=datetime.datetime(2022, 10, 2, 23, 59, 59),
            begin_contact=self.contact1,
            end_contact=self.contact1,
            begin_description="begin",
        )
        db.session.add_all(
            [
                static_location_action1,
                static_location_action2,
            ]
        )
        db.session.commit()

        payload_dict = {"attributes": {"end_date": "2022-09-05T12:12:12.00Z"}}
        with self.assertRaises(ConflictError):
            StaticLocationActionValidator().validate_update(
                payload_dict, static_location_action1.id
            )

    def test_validate_update_fail_overlapping_dynamic_location(self):
        """Validate that we don't allow overlaps with dynamic locations on update."""
        static_location_action1 = ConfigurationStaticLocationBeginAction(
            configuration=self.configuration1,
            begin_date=datetime.datetime(2022, 8, 30, 0, 0, 0),
            end_date=datetime.datetime(2022, 9, 2, 23, 59, 59),
            begin_contact=self.contact1,
            end_contact=self.contact1,
            begin_description="begin",
        )
        dynamic_location_action1 = ConfigurationDynamicLocationBeginAction(
            configuration=self.configuration1,
            begin_date=datetime.datetime(2022, 9, 3, 0, 0, 0),
            end_date=datetime.datetime(2022, 10, 2, 23, 59, 59),
            begin_contact=self.contact1,
            end_contact=self.contact1,
            begin_description="begin",
        )
        db.session.add_all(
            [
                static_location_action1,
                dynamic_location_action1,
            ]
        )
        db.session.commit()

        payload_dict = {"attributes": {"end_date": "2022-09-05T12:12:12.00Z"}}
        with self.assertRaises(ConflictError):
            StaticLocationActionValidator().validate_update(
                payload_dict, static_location_action1.id
            )

    def test_validate_update_pass_due_to_configuration_change(self):
        """Validate that we allow if we change to a configuration where there is no overlap."""
        static_location_action1 = ConfigurationStaticLocationBeginAction(
            configuration=self.configuration1,
            begin_date=datetime.datetime(2022, 8, 30, 0, 0, 0),
            end_date=datetime.datetime(2022, 9, 2, 23, 59, 59),
            begin_contact=self.contact1,
            end_contact=self.contact1,
            begin_description="begin",
        )
        dynamic_location_action1 = ConfigurationDynamicLocationBeginAction(
            configuration=self.configuration1,
            begin_date=datetime.datetime(2022, 9, 3, 0, 0, 0),
            end_date=datetime.datetime(2022, 10, 2, 23, 59, 59),
            begin_contact=self.contact1,
            end_contact=self.contact1,
            begin_description="begin",
        )
        configuration2 = Configuration(label="configuration2", is_public=True)
        db.session.add_all(
            [
                static_location_action1,
                dynamic_location_action1,
                configuration2,
            ]
        )
        db.session.commit()

        payload_dict = {
            "relationships": {"configuration": {"data": {"id": configuration2.id}}},
            "attributes": {"end_date": "2022-09-05T12:12:12.00Z"},
        }
        StaticLocationActionValidator().validate_update(
            payload_dict, static_location_action1.id
        )


class TestDynamicLocationActionValidator(BaseTestCase):
    """Tests for the validation of dynamic location actions."""

    def setUp(self):
        """Set the tests up."""
        super().setUp()
        self.contact1 = Contact(given_name="A", family_name="B", email="A@B")
        self.user1 = User(subject="A@B", contact=self.contact1)
        self.configuration1 = Configuration(is_public=True, label="Conf1")
        self.configuration2 = Configuration(is_public=True, label="Conf2")
        self.configuration3 = Configuration(is_public=True, label="Conf3")
        self.device1 = Device(
            short_name="dev1", manufacturer_name="Man", is_public=True
        )
        self.device2 = Device(
            short_name="dev2", manufacturer_name="Man", is_public=True
        )
        self.device_property1 = DeviceProperty(
            device=self.device1, label="abc", property_name="measurement1"
        )
        self.device_property2 = DeviceProperty(
            device=self.device2, label="abc", property_name="measurement1"
        )
        db.session.add_all(
            [
                self.contact1,
                self.user1,
                self.configuration1,
                self.configuration2,
                self.configuration3,
                self.device1,
                self.device2,
                self.device_property1,
                self.device_property2,
            ]
        )
        db.session.commit()

    def test_validate_create_pass_with_end(self):
        """Test that we can simply create a location if there is nothing."""
        payload_dict = {
            "relationships": {
                "configuration": {"data": {"id": self.configuration1.id}},
            },
            "attributes": {
                "begin_date": "2022-08-30T15:50:00.00Z",
                "end_date": "2022-08-31T11:11:11.00Z",
            },
        }
        DynamicLocationActionValidator().validate_create(payload_dict)

    def test_validate_create_pass_no_end(self):
        """Test that we can also set the end date to none if there is nothing yet."""
        payload_dict = {
            "relationships": {
                "configuration": {"data": {"id": self.configuration1.id}},
            },
            "attributes": {
                "begin_date": "2022-08-30T15:50:00.00Z",
                "end_date": None,
            },
        }
        DynamicLocationActionValidator().validate_create(payload_dict)

    def test_validate_create_pass_as_other_configuration(self):
        """Test that we can create as the other ones are in a different configuration."""
        static_location_action = ConfigurationStaticLocationBeginAction(
            configuration=self.configuration2,
            begin_date=datetime.datetime(2022, 8, 30, 0, 0, 0),
            end_date=datetime.datetime(2022, 9, 2, 23, 59, 59),
            begin_contact=self.contact1,
            end_contact=self.contact1,
            begin_description="begin",
        )
        dynamic_location_action = ConfigurationDynamicLocationBeginAction(
            configuration=self.configuration3,
            begin_date=datetime.datetime(2022, 8, 30, 0, 0, 0),
            end_date=datetime.datetime(2022, 9, 2, 23, 59, 59),
            begin_contact=self.contact1,
            end_contact=self.contact1,
            begin_description="begin",
        )
        db.session.add_all(
            [
                static_location_action,
                dynamic_location_action,
            ]
        )
        db.session.commit()

        payload_dict = {
            "relationships": {
                "configuration": {"data": {"id": self.configuration1.id}},
            },
            "attributes": {
                "begin_date": "2022-08-30T15:50:00.00Z",
                "end_date": None,
            },
        }
        DynamicLocationActionValidator().validate_create(payload_dict)

    def test_validate_create_fail_as_intersecting_static_location_action(self):
        """Validate that we realize a possible overlap with a static location."""
        static_location_action = ConfigurationStaticLocationBeginAction(
            configuration=self.configuration1,
            begin_date=datetime.datetime(2022, 8, 30, 0, 0, 0),
            end_date=datetime.datetime(2022, 9, 2, 23, 59, 59),
            begin_contact=self.contact1,
            end_contact=self.contact1,
            begin_description="begin",
        )
        db.session.add_all(
            [
                static_location_action,
            ]
        )
        db.session.commit()

        payload_dict = {
            "relationships": {
                "configuration": {"data": {"id": self.configuration1.id}},
            },
            "attributes": {
                "begin_date": "2022-08-30T15:50:00.00Z",
                "end_date": None,
            },
        }
        with self.assertRaises(ConflictError):
            DynamicLocationActionValidator().validate_create(payload_dict)

    def test_validate_create_pass_no_intersecting_static_location_action(self):
        """Allow the creation if we don't have an overlap with a static locaiton action."""
        static_location_action = ConfigurationStaticLocationBeginAction(
            configuration=self.configuration1,
            begin_date=datetime.datetime(2022, 8, 30, 0, 0, 0),
            end_date=datetime.datetime(2022, 9, 2, 23, 59, 59),
            begin_contact=self.contact1,
            end_contact=self.contact1,
            begin_description="begin",
        )
        db.session.add_all(
            [
                static_location_action,
            ]
        )
        db.session.commit()

        payload_dict = {
            "relationships": {
                "configuration": {"data": {"id": self.configuration1.id}},
            },
            "attributes": {
                "begin_date": "2022-10-30T15:50:00.00Z",
                "end_date": None,
            },
        }
        DynamicLocationActionValidator().validate_create(payload_dict)

    def test_validate_create_pass_no_intersecting_dynamic_location_action(self):
        """Allow the creation if we don't have an overlap with a static locaiton action."""
        dynamic_location_action = ConfigurationDynamicLocationBeginAction(
            configuration=self.configuration1,
            begin_date=datetime.datetime(2022, 8, 30, 0, 0, 0),
            end_date=datetime.datetime(2022, 9, 2, 23, 59, 59),
            begin_contact=self.contact1,
            end_contact=self.contact1,
            begin_description="begin",
        )
        db.session.add_all(
            [
                dynamic_location_action,
            ]
        )
        db.session.commit()

        payload_dict = {
            "relationships": {
                "configuration": {"data": {"id": self.configuration1.id}},
            },
            "attributes": {
                "begin_date": "2022-10-30T15:50:00.00Z",
                "end_date": None,
            },
        }
        DynamicLocationActionValidator().validate_create(payload_dict)

    def test_validate_create_fail_as_intersecting_dynamic_location_action(self):
        """Validate that we see a possible overlap with a dynamic location."""
        dynamic_location_action = ConfigurationDynamicLocationBeginAction(
            configuration=self.configuration1,
            begin_date=datetime.datetime(2022, 8, 30, 0, 0, 0),
            end_date=datetime.datetime(2022, 9, 2, 23, 59, 59),
            begin_contact=self.contact1,
            end_contact=self.contact1,
            begin_description="begin",
        )
        db.session.add_all(
            [
                dynamic_location_action,
            ]
        )
        db.session.commit()

        payload_dict = {
            "relationships": {
                "configuration": {"data": {"id": self.configuration1.id}},
            },
            "attributes": {
                "begin_date": "2022-08-30T15:50:00.00Z",
                "end_date": None,
            },
        }
        with self.assertRaises(ConflictError):
            DynamicLocationActionValidator().validate_create(payload_dict)

    def test_validate_update_pass(self):
        """Validate that we can update an existing dynamic location action."""
        dynamic_location_action = ConfigurationDynamicLocationBeginAction(
            configuration=self.configuration1,
            begin_date=datetime.datetime(2022, 8, 30, 0, 0, 0),
            end_date=datetime.datetime(2022, 9, 2, 23, 59, 59),
            begin_contact=self.contact1,
            end_contact=self.contact1,
            begin_description="begin",
        )
        db.session.add_all(
            [
                dynamic_location_action,
            ]
        )
        db.session.commit()

        payload_dict = {"attributes": {"end_date": "2022-09-05T12:12:12.00Z"}}
        DynamicLocationActionValidator().validate_update(
            payload_dict, dynamic_location_action.id
        )

    def test_validate_update_fail_not_found(self):
        """Validate that we check if the static location action is there."""
        with self.assertRaises(NotFoundError):
            DynamicLocationActionValidator().validate_update({}, 100000)

    def test_validate_update_fail_overlapping_static_location(self):
        """Validate that we don't allow overlapping static locations on update."""
        dynamic_location_action1 = ConfigurationDynamicLocationBeginAction(
            configuration=self.configuration1,
            begin_date=datetime.datetime(2022, 8, 30, 0, 0, 0),
            end_date=datetime.datetime(2022, 9, 2, 23, 59, 59),
            begin_contact=self.contact1,
            end_contact=self.contact1,
            begin_description="begin",
        )
        static_location_action1 = ConfigurationStaticLocationBeginAction(
            configuration=self.configuration1,
            begin_date=datetime.datetime(2022, 9, 3, 0, 0, 0),
            end_date=datetime.datetime(2022, 10, 2, 23, 59, 59),
            begin_contact=self.contact1,
            end_contact=self.contact1,
            begin_description="begin",
        )
        db.session.add_all(
            [
                dynamic_location_action1,
                static_location_action1,
            ]
        )
        db.session.commit()

        payload_dict = {"attributes": {"end_date": "2022-09-05T12:12:12.00Z"}}
        with self.assertRaises(ConflictError):
            DynamicLocationActionValidator().validate_update(
                payload_dict, dynamic_location_action1.id
            )

    def test_validate_update_fail_overlapping_dynamic_location(self):
        """Validate that we don't allow overlaps with dynamic locations on update."""
        dynamic_location_action1 = ConfigurationDynamicLocationBeginAction(
            configuration=self.configuration1,
            begin_date=datetime.datetime(2022, 8, 30, 0, 0, 0),
            end_date=datetime.datetime(2022, 9, 2, 23, 59, 59),
            begin_contact=self.contact1,
            end_contact=self.contact1,
            begin_description="begin",
        )
        dynamic_location_action2 = ConfigurationDynamicLocationBeginAction(
            configuration=self.configuration1,
            begin_date=datetime.datetime(2022, 9, 3, 0, 0, 0),
            end_date=datetime.datetime(2022, 10, 2, 23, 59, 59),
            begin_contact=self.contact1,
            end_contact=self.contact1,
            begin_description="begin",
        )
        db.session.add_all(
            [
                dynamic_location_action1,
                dynamic_location_action2,
            ]
        )
        db.session.commit()

        payload_dict = {"attributes": {"end_date": "2022-09-05T12:12:12.00Z"}}
        with self.assertRaises(ConflictError):
            DynamicLocationActionValidator().validate_update(
                payload_dict, dynamic_location_action1.id
            )

    def test_validate_update_pass_due_to_configuration_change(self):
        """Validate that we allow if we change to a configuration where there is no overlap."""
        dynamic_location_action1 = ConfigurationDynamicLocationBeginAction(
            configuration=self.configuration1,
            begin_date=datetime.datetime(2022, 8, 30, 0, 0, 0),
            end_date=datetime.datetime(2022, 9, 2, 23, 59, 59),
            begin_contact=self.contact1,
            end_contact=self.contact1,
            begin_description="begin",
        )
        dynamic_location_action2 = ConfigurationDynamicLocationBeginAction(
            configuration=self.configuration1,
            begin_date=datetime.datetime(2022, 9, 3, 0, 0, 0),
            end_date=datetime.datetime(2022, 10, 2, 23, 59, 59),
            begin_contact=self.contact1,
            end_contact=self.contact1,
            begin_description="begin",
        )
        configuration2 = Configuration(label="configuration2", is_public=True)
        db.session.add_all(
            [
                dynamic_location_action1,
                dynamic_location_action2,
                configuration2,
            ]
        )
        db.session.commit()

        payload_dict = {
            "relationships": {"configuration": {"data": {"id": configuration2.id}}},
            "attributes": {"end_date": "2022-09-05T12:12:12.00Z"},
        }
        DynamicLocationActionValidator().validate_update(
            payload_dict, dynamic_location_action1.id
        )

    def test_validate_create_fail_due_to_missing_device_mount(self):
        """Ensure that we see if a device property is not mounted for the location time."""
        for xyz_property in ["x_property", "y_property", "z_property"]:
            payload_dict = {
                "relationships": {
                    "configuration": {"data": {"id": self.configuration1.id}},
                    xyz_property: {"data": {"id": self.device_property1.id}},
                },
                "attributes": {"begin_date": "2022-09-05T12:12:12.00Z"},
            }
            with self.assertRaises(ConflictError):
                DynamicLocationActionValidator().validate_create(payload_dict)

    def test_validate_create_pass_with_device_mount(self):
        """Ensure that we check that the device property is mounted for the location time."""
        device_mount_action1 = DeviceMountAction(
            configuration=self.configuration1,
            device=self.device1,
            begin_date=datetime.datetime(2021, 1, 1, 12, 0, 0),
            end_date=datetime.datetime(2021, 3, 1, 12, 0, 0),
            begin_contact=self.contact1,
            end_contact=self.contact1,
            begin_description="dev1 mount1",
        )
        device_mount_action2 = DeviceMountAction(
            configuration=self.configuration1,
            device=self.device1,
            begin_date=datetime.datetime(2022, 1, 1, 12, 0, 0),
            end_date=datetime.datetime(2023, 1, 1, 12, 0, 0),
            begin_contact=self.contact1,
            end_contact=self.contact1,
            begin_description="dev1 mount2",
        )
        device_mount_action3 = DeviceMountAction(
            configuration=self.configuration1,
            device=self.device1,
            begin_date=datetime.datetime(2024, 1, 1, 12, 0, 0),
            end_date=datetime.datetime(2026, 3, 1, 12, 0, 0),
            begin_contact=self.contact1,
            end_contact=self.contact1,
            begin_description="dev1 mount3",
        )
        db.session.add_all(
            [device_mount_action1, device_mount_action2, device_mount_action3]
        )
        db.session.commit()
        payload_dict = {
            "relationships": {
                "configuration": {"data": {"id": self.configuration1.id}},
                "x_property": {"data": {"id": self.device_property1.id}},
                "y_property": {"data": {"id": self.device_property1.id}},
                "z_property": {"data": {"id": self.device_property1.id}},
            },
            "attributes": {
                "begin_date": "2022-09-05T12:12:12.00Z",
                "end_date": "2022-09-06T12:12:12.00Z",
            },
        }
        DynamicLocationActionValidator().validate_create(payload_dict)

    def test_validate_create_pass_with_device_mount_without_z(self):
        """Ensure that we check that the device property - but no z -is mounted for the location time."""
        device_mount_action1 = DeviceMountAction(
            configuration=self.configuration1,
            device=self.device1,
            begin_date=datetime.datetime(2021, 1, 1, 12, 0, 0),
            end_date=datetime.datetime(2021, 3, 1, 12, 0, 0),
            begin_contact=self.contact1,
            end_contact=self.contact1,
            begin_description="dev1 mount1",
        )
        device_mount_action2 = DeviceMountAction(
            configuration=self.configuration1,
            device=self.device1,
            begin_date=datetime.datetime(2022, 1, 1, 12, 0, 0),
            end_date=datetime.datetime(2023, 1, 1, 12, 0, 0),
            begin_contact=self.contact1,
            end_contact=self.contact1,
            begin_description="dev1 mount2",
        )
        device_mount_action3 = DeviceMountAction(
            configuration=self.configuration1,
            device=self.device1,
            begin_date=datetime.datetime(2024, 1, 1, 12, 0, 0),
            end_date=datetime.datetime(2026, 3, 1, 12, 0, 0),
            begin_contact=self.contact1,
            end_contact=self.contact1,
            begin_description="dev1 mount3",
        )
        db.session.add_all(
            [device_mount_action1, device_mount_action2, device_mount_action3]
        )
        db.session.commit()
        payload_dict = {
            "relationships": {
                "configuration": {"data": {"id": self.configuration1.id}},
                "x_property": {"data": {"id": self.device_property1.id}},
                "y_property": {"data": {"id": self.device_property1.id}},
                "z_property": {"data": None},
            },
            "attributes": {
                "begin_date": "2022-09-05T12:12:12.00Z",
                "end_date": "2022-09-06T12:12:12.00Z",
            },
        }
        DynamicLocationActionValidator().validate_create(payload_dict)

    def test_validate_update_fail_due_to_missing_device_mount(self):
        """Ensure that we see if device property is not mounted for location time on update."""
        dynamic_location_action = ConfigurationDynamicLocationBeginAction(
            configuration=self.configuration1,
            begin_date=datetime.datetime(2022, 9, 6, 12, 12),
            begin_contact=self.contact1,
        )
        db.session.add_all([dynamic_location_action])
        db.session.commit()

        for xyz_property in ["x_property", "y_property", "z_property"]:
            payload_dict = {
                "relationships": {
                    xyz_property: {"data": {"id": self.device_property1.id}}
                },
                "attributes": {"begin_date": "2022-09-05T12:12:12.00Z"},
            }
            with self.assertRaises(ConflictError):
                DynamicLocationActionValidator().validate_update(
                    payload_dict, dynamic_location_action.id
                )

    def test_validate_update_fail_due_to_missing_device_mount_for_one_property(self):
        """Ensure that we see if one device property is not mounted for location time on update."""
        device_mount_action1 = DeviceMountAction(
            configuration=self.configuration1,
            device=self.device1,
            begin_date=datetime.datetime(2022, 1, 1, 12, 0, 0),
            end_date=datetime.datetime(2023, 1, 1, 12, 0, 0),
            begin_contact=self.contact1,
            end_contact=self.contact1,
            begin_description="dev1 mount1",
        )
        dynamic_location_action = ConfigurationDynamicLocationBeginAction(
            configuration=self.configuration1,
            begin_date=datetime.datetime(2022, 9, 6, 12, 12),
            end_date=datetime.datetime(2022, 10, 6, 12, 12),
            begin_contact=self.contact1,
            x_property=self.device_property1,
        )
        db.session.add_all([device_mount_action1, dynamic_location_action])
        db.session.commit()

        for xyz_property in ["y_property", "z_property"]:
            payload_dict = {
                "relationships": {
                    xyz_property: {"data": {"id": self.device_property2.id}}
                },
                "attributes": {"begin_date": "2022-09-05T12:12:12.00Z"},
            }
            with self.assertRaises(ConflictError):
                DynamicLocationActionValidator().validate_update(
                    payload_dict, dynamic_location_action.id
                )

    def test_validate_update_pass_with_device_mount(self):
        """Ensure that we check that device property is mounted the location time on update."""
        dynamic_location_action = ConfigurationDynamicLocationBeginAction(
            configuration=self.configuration1,
            begin_date=datetime.datetime(2022, 9, 6, 12, 12),
            begin_contact=self.contact1,
        )
        device_mount_action1 = DeviceMountAction(
            configuration=self.configuration1,
            device=self.device1,
            begin_date=datetime.datetime(2021, 1, 1, 12, 0, 0),
            end_date=datetime.datetime(2021, 3, 1, 12, 0, 0),
            begin_contact=self.contact1,
            end_contact=self.contact1,
            begin_description="dev1 mount1",
        )
        device_mount_action2 = DeviceMountAction(
            configuration=self.configuration1,
            device=self.device1,
            begin_date=datetime.datetime(2022, 1, 1, 12, 0, 0),
            end_date=datetime.datetime(2023, 1, 1, 12, 0, 0),
            begin_contact=self.contact1,
            end_contact=self.contact1,
            begin_description="dev1 mount2",
        )
        device_mount_action3 = DeviceMountAction(
            configuration=self.configuration1,
            device=self.device1,
            begin_date=datetime.datetime(2024, 1, 1, 12, 0, 0),
            end_date=datetime.datetime(2026, 3, 1, 12, 0, 0),
            begin_contact=self.contact1,
            end_contact=self.contact1,
            begin_description="dev1 mount3",
        )
        db.session.add_all(
            [
                device_mount_action1,
                device_mount_action2,
                device_mount_action3,
                dynamic_location_action,
            ]
        )
        db.session.commit()
        payload_dict = {
            "relationships": {
                "x_property": {"data": {"id": self.device_property1.id}},
                "y_property": {"data": {"id": self.device_property1.id}},
                "z_property": {"data": {"id": self.device_property1.id}},
            },
            "attributes": {
                "begin_date": "2022-09-05T12:12:12.00Z",
                "end_date": "2022-09-06T12:12:12.00Z",
            },
        }
        DynamicLocationActionValidator().validate_update(
            payload_dict, dynamic_location_action.id
        )
