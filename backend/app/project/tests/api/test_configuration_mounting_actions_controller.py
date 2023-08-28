# SPDX-FileCopyrightText: 2022 - 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Tests for the mounting actions controller to get the hierarchy."""

import datetime

from project import base_url
from project.api.models import (
    Configuration,
    Contact,
    Device,
    DeviceMountAction,
    Platform,
    PlatformMountAction,
    User,
)
from project.api.models.base_model import db
from project.api.schemas.device_schema import DeviceSchema
from project.api.schemas.mount_actions_schema import (
    DeviceMountActionSchema,
    PlatformMountActionSchema,
)
from project.api.schemas.platform_schema import PlatformSchema
from project.tests.base import BaseTestCase


class TestControllerConfigurationsMountingActions(BaseTestCase):
    """Tests for the controller to get the mounting actions with a given timepoint."""

    def setUp(self):
        """Set up some example data that will be used in most of  the tests."""
        super().setUp()

        contact = Contact(given_name="D", family_name="U", email="d.u@localhost")
        self.u = User(subject="du", contact=contact)

        self.configuration = Configuration(
            label="dummy configuration", is_internal=True
        )
        db.session.add_all([contact, self.u, self.configuration])
        db.session.commit()

    def test_get_without_configuration_id(self):
        """Ensure that we get a 404 for a non existing configuration."""
        url = f"{base_url}/controller/configurations/999999/mounting-actions"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_get_internal_without_user(self):
        """Ensure we get 40x if user isn't authenticated when accessing an internal config."""
        url = f"{base_url}/controller/configurations/{self.configuration.id}/mounting-actions"
        response = self.client.get(url)
        self.assertIn(response.status_code, [401, 403])

    def test_get_without_timepoint(self):
        """Ensure we get 400 if we miss the timepoint parameter."""
        url = f"{base_url}/controller/configurations/{self.configuration.id}/mounting-actions"
        with self.run_requests_as(self.u):
            response = self.client.get(url)
        self.assertEqual(response.status_code, 400)

    def test_get_without_timepoint_valid_timepoint(self):
        """Ensure we get 400 if we don't provide a valid timepoint."""
        url = f"{base_url}/controller/configurations/{self.configuration.id}/mounting-actions"
        with self.run_requests_as(self.u):
            response = self.client.get(url, query_string={"timepoint": "someday"})
        self.assertEqual(response.status_code, 400)

    def test_get_empty_result(self):
        """Ensure we get an empty result if we query for timepoint without data."""
        url = f"{base_url}/controller/configurations/{self.configuration.id}/mounting-actions"
        with self.run_requests_as(self.u):
            response = self.client.get(
                url, query_string={"timepoint": datetime.datetime(1970, 1, 1)}
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])

    def test_get_active_device_mount(self):
        """Ensure we get an one device entry for the mount."""
        device = Device(
            short_name="Some device",
            is_internal=True,
            manufacturer_name="OTT HydroMet",
            model="OTT CTD Sensor",
            serial_number="345146",
            device_type_name="Sensor",
        )
        device_mount_action = DeviceMountAction(
            configuration=self.configuration,
            device=device,
            offset_x=1,
            offset_y=2,
            offset_z=3,
            begin_description="Some data",
            begin_contact=self.u.contact,
            begin_date=datetime.datetime(2022, 5, 18, 12, 0, 0),
        )
        db.session.add_all([device, device_mount_action])
        db.session.commit()
        url = f"{base_url}/controller/configurations/{self.configuration.id}/mounting-actions"
        with self.run_requests_as(self.u):
            response = self.client.get(
                url, query_string={"timepoint": datetime.datetime(2022, 5, 19, 0, 0, 0)}
            )
        self.assertEqual(response.status_code, 200)
        expected = [
            {
                "action": DeviceMountActionSchema().dump(device_mount_action),
                "entity": DeviceSchema().dump(device),
                "children": [],
            }
        ]
        self.assertEqual(response.json, expected)

    def test_get_inactive_device_mount_before(self):
        """Ensure we get an empty result if we query for timepoint without data."""
        device = Device(
            short_name="Some device",
            is_internal=True,
            manufacturer_name="OTT HydroMet",
            model="OTT CTD Sensor",
            serial_number="345146",
            device_type_name="Sensor",
        )
        device_mount_action = DeviceMountAction(
            configuration=self.configuration,
            device=device,
            offset_x=1,
            offset_y=2,
            offset_z=3,
            begin_description="Some data",
            begin_contact=self.u.contact,
            begin_date=datetime.datetime(2022, 5, 18, 12, 0, 0),
        )
        db.session.add_all([device, device_mount_action])
        db.session.commit()
        url = f"{base_url}/controller/configurations/{self.configuration.id}/mounting-actions"
        with self.run_requests_as(self.u):
            response = self.client.get(
                url, query_string={"timepoint": datetime.datetime(2022, 2, 19, 0, 0, 0)}
            )
        self.assertEqual(response.status_code, 200)
        expected = []
        self.assertEqual(response.json, expected)

    def test_get_inactive_device_mount_after(self):
        """Ensure we get an empty result if we query for timepoint without data."""
        device = Device(
            short_name="Some device",
            is_internal=True,
            manufacturer_name="OTT HydroMet",
            model="OTT CTD Sensor",
            serial_number="345146",
            device_type_name="Sensor",
        )
        device_mount_action = DeviceMountAction(
            configuration=self.configuration,
            device=device,
            offset_x=1,
            offset_y=2,
            offset_z=3,
            begin_description="Some data",
            begin_contact=self.u.contact,
            begin_date=datetime.datetime(2022, 5, 18, 12, 0, 0),
            end_date=datetime.datetime(2022, 5, 19, 5, 0, 0),
        )
        db.session.add_all([device, device_mount_action])
        db.session.commit()
        url = f"{base_url}/controller/configurations/{self.configuration.id}/mounting-actions"
        with self.run_requests_as(self.u):
            response = self.client.get(
                url, query_string={"timepoint": datetime.datetime(2022, 6, 19, 0, 0, 0)}
            )
        self.assertEqual(response.status_code, 200)
        expected = []
        self.assertEqual(response.json, expected)

    def test_get_active_platform_mount(self):
        """Ensure we get an one platform entry for the mount."""
        platform = Platform(
            short_name="Some platform",
            is_internal=True,
            manufacturer_name="OTT HydroMet",
            model="OTT CTD Sensor",
            serial_number="345146",
            platform_type_name="Sensor",
        )
        platform_mount_action = PlatformMountAction(
            configuration=self.configuration,
            platform=platform,
            offset_x=1,
            offset_y=2,
            offset_z=3,
            begin_description="Some data",
            begin_contact=self.u.contact,
            begin_date=datetime.datetime(2022, 5, 18, 12, 0, 0),
        )
        db.session.add_all([platform, platform_mount_action])
        db.session.commit()
        url = f"{base_url}/controller/configurations/{self.configuration.id}/mounting-actions"
        with self.run_requests_as(self.u):
            response = self.client.get(
                url, query_string={"timepoint": datetime.datetime(2022, 5, 19, 0, 0, 0)}
            )
        self.assertEqual(response.status_code, 200)
        expected = [
            {
                "action": PlatformMountActionSchema().dump(platform_mount_action),
                "entity": PlatformSchema().dump(platform),
                "children": [],
            }
        ]
        self.assertEqual(response.json, expected)

    def test_get_active_platform_mount_with_same_dates(self):
        """Ensure we get an one platform entry for the mount with the same begin and end dates."""
        platform = Platform(
            short_name="Some platform",
            is_internal=True,
            manufacturer_name="OTT HydroMet",
            model="OTT CTD Sensor",
            serial_number="345146",
            platform_type_name="Sensor",
        )
        platform_mount_action = PlatformMountAction(
            configuration=self.configuration,
            platform=platform,
            offset_x=1,
            offset_y=2,
            offset_z=3,
            begin_description="Some data",
            begin_contact=self.u.contact,
            begin_date=datetime.datetime(2022, 5, 18, 12, 0, 0),
            end_date=datetime.datetime(2022, 5, 18, 12, 0, 0),
        )
        db.session.add_all([platform, platform_mount_action])
        db.session.commit()
        url = f"{base_url}/controller/configurations/{self.configuration.id}/mounting-actions"
        with self.run_requests_as(self.u):
            response = self.client.get(
                url,
                query_string={"timepoint": datetime.datetime(2022, 5, 18, 12, 0, 0)},
            )
        self.assertEqual(response.status_code, 200)
        expected = [
            {
                "action": PlatformMountActionSchema().dump(platform_mount_action),
                "entity": PlatformSchema().dump(platform),
                "children": [],
            }
        ]
        self.assertEqual(response.json, expected)

    def test_get_inactive_platform_mount_before(self):
        """Ensure we get an empty result if we query for timepoint without data."""
        platform = Platform(
            short_name="Some platform",
            is_internal=True,
            manufacturer_name="OTT HydroMet",
            model="OTT CTD Sensor",
            serial_number="345146",
            platform_type_name="Sensor",
        )
        platform_mount_action = PlatformMountAction(
            configuration=self.configuration,
            platform=platform,
            offset_x=1,
            offset_y=2,
            offset_z=3,
            begin_description="Some data",
            begin_contact=self.u.contact,
            begin_date=datetime.datetime(2022, 5, 18, 12, 0, 0),
        )
        db.session.add_all([platform, platform_mount_action])
        db.session.commit()
        url = f"{base_url}/controller/configurations/{self.configuration.id}/mounting-actions"
        with self.run_requests_as(self.u):
            response = self.client.get(
                url, query_string={"timepoint": datetime.datetime(2022, 2, 19, 0, 0, 0)}
            )
        self.assertEqual(response.status_code, 200)
        expected = []
        self.assertEqual(response.json, expected)

    def test_get_inactive_platform_mount_after(self):
        """Ensure we get an empty result if we query for timepoint without data."""
        platform = Platform(
            short_name="Some platform",
            is_internal=True,
            manufacturer_name="OTT HydroMet",
            model="OTT CTD Sensor",
            serial_number="345146",
            platform_type_name="Sensor",
        )
        platform_mount_action = PlatformMountAction(
            configuration=self.configuration,
            platform=platform,
            offset_x=1,
            offset_y=2,
            offset_z=3,
            begin_description="Some data",
            begin_contact=self.u.contact,
            begin_date=datetime.datetime(2022, 5, 18, 12, 0, 0),
            end_date=datetime.datetime(2022, 5, 19, 5, 0, 0),
        )
        db.session.add_all([platform, platform_mount_action])
        db.session.commit()
        url = f"{base_url}/controller/configurations/{self.configuration.id}/mounting-actions"
        with self.run_requests_as(self.u):
            response = self.client.get(
                url, query_string={"timepoint": datetime.datetime(2022, 6, 19, 0, 0, 0)}
            )
        self.assertEqual(response.status_code, 200)
        expected = []
        self.assertEqual(response.json, expected)

    def test_get_hierarchy(self):
        """Ensure that we can return a complex hierarchy."""
        platform1 = Platform(
            short_name="Platform 1",
            is_internal=True,
            manufacturer_name="OTT HydroMet",
            model="OTT CTD Sensor",
            serial_number="345146",
            platform_type_name="Sensor",
        )
        platform2 = Platform(
            short_name="Platform 2",
            is_internal=True,
            manufacturer_name="OTT HydroMet",
            model="OTT CTD Sensor",
            serial_number="345146",
            platform_type_name="Sensor",
        )
        platform_mount_action1 = PlatformMountAction(
            configuration=self.configuration,
            platform=platform1,
            offset_x=1,
            offset_y=2,
            offset_z=3,
            begin_description="Some data",
            begin_contact=self.u.contact,
            begin_date=datetime.datetime(2022, 5, 18, 12, 0, 0),
            end_date=datetime.datetime(2022, 5, 19, 5, 0, 0),
        )
        platform_mount_action2 = PlatformMountAction(
            configuration=self.configuration,
            platform=platform2,
            offset_x=1,
            offset_y=2,
            offset_z=3,
            parent_platform=platform1,
            begin_description="Some data",
            begin_contact=self.u.contact,
            begin_date=datetime.datetime(2022, 5, 18, 12, 5, 0),
            end_date=datetime.datetime(2022, 5, 19, 4, 55, 0),
        )
        device = Device(
            short_name="Some device",
            is_internal=True,
            manufacturer_name="OTT HydroMet",
            model="OTT CTD Sensor",
            serial_number="345146",
            device_type_name="Sensor",
        )
        device_mount_action = DeviceMountAction(
            configuration=self.configuration,
            device=device,
            offset_x=1,
            offset_y=2,
            offset_z=3,
            begin_description="Some data",
            begin_contact=self.u.contact,
            parent_platform=platform2,
            begin_date=datetime.datetime(2022, 5, 18, 12, 10, 0),
            end_date=datetime.datetime(2022, 5, 19, 4, 0, 0),
        )
        db.session.add_all(
            [
                device,
                device_mount_action,
                platform1,
                platform2,
                platform_mount_action1,
                platform_mount_action2,
            ]
        )
        url = f"{base_url}/controller/configurations/{self.configuration.id}/mounting-actions"
        with self.run_requests_as(self.u):
            response = self.client.get(
                url, query_string={"timepoint": datetime.datetime(2022, 5, 19, 0, 0, 0)}
            )
        self.assertEqual(response.status_code, 200)
        expected = [
            {
                "action": PlatformMountActionSchema().dump(platform_mount_action1),
                "entity": PlatformSchema().dump(platform1),
                "children": [
                    {
                        "action": PlatformMountActionSchema().dump(
                            platform_mount_action2
                        ),
                        "entity": PlatformSchema().dump(platform2),
                        "children": [
                            {
                                "action": DeviceMountActionSchema().dump(
                                    device_mount_action
                                ),
                                "entity": DeviceSchema().dump(device),
                                "children": [],
                            }
                        ],
                    }
                ],
            }
        ]
        self.assertEqual(response.json, expected)
