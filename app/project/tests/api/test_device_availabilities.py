"""Tests mount device availablities."""

import datetime

from project import base_url
from project.api.models import Configuration, Contact, Device, DeviceMountAction, User
from project.api.models.base_model import db
from project.tests.base import BaseTestCase, fake


class TestDeviceAvailabilities(BaseTestCase):
    """Tests for the controller to get the mounting device availabilities."""

    url = f"{base_url}/controller/device-availabilities"

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

    def mount_a_device(self, begin_date=None, end_date=None):
        """Mount a device to enrich the test setup."""
        device = Device(
            short_name=fake.pystr(),
            is_internal=True,
            manufacturer_name=fake.company(),
            model=fake.pystr(),
            serial_number=fake.pyint(),
            device_type_name=fake.pystr(),
        )
        device_mount_action = DeviceMountAction(
            configuration=self.configuration,
            device=device,
            offset_x=fake.pyint(),
            offset_y=fake.pyint(),
            offset_z=fake.pyint(),
            begin_description=fake.text(),
            begin_contact=self.u.contact,
            begin_date=begin_date or fake.date_time_this_month(),
            end_date=end_date,
            end_description=fake.text(),
            end_contact=self.u.contact,
        )
        db.session.add_all([device, device_mount_action])
        db.session.commit()
        return device, device_mount_action

    def test_get_without_user(self):
        """Ensure we get 401 if we don't provide user information."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)

    def test_get_without_time_point(self):
        """Ensure we get 400 if we miss the time-point parameters."""
        with self.run_requests_as(self.u):
            response = self.client.get(self.url)
        self.assertEqual(response.status_code, 400)
        # without from time-point
        with self.run_requests_as(self.u):
            response = self.client.get(
                self.url, query_string={"to": "2020-01-01T00:00:00"}
            )
        self.assertEqual(response.status_code, 400)
        # However, the to end point is different.
        # It is completely optional.
        # But in order to have a valid response we have to provide an
        # ids parmaeter as well.
        with self.run_requests_as(self.u):
            response = self.client.get(
                self.url, query_string={"from": "2022-01-01T00:00:00", "ids": ""}
            )
        self.assertEqual(response.status_code, 200)

    def test_get_without_time_point_valid_time_point(self):
        """Ensure we get 400 if we don't provide a valid time-point."""
        with self.run_requests_as(self.u):
            response = self.client.get(
                self.url,
                query_string={
                    "from": "someday",
                    "to": "another day",
                },
            )
        self.assertEqual(response.status_code, 400)

    def test_get_without_ids(self):
        """Ensure we get 400 if we don't provide the ids parameter."""
        with self.run_requests_as(self.u):
            response = self.client.get(
                self.url,
                query_string={
                    "from": "2011-01-01T00:00:00Z",
                    "to": "2099-12-12T23:59:00Z",
                },
            )
        self.assertEqual(response.status_code, 400)

    def test_get_empty_result(self):
        """Ensure we get an empty result if we query for time-point without data."""
        with self.run_requests_as(self.u):
            response = self.client.get(
                self.url,
                query_string={
                    "from": datetime.datetime(1970, 1, 1),
                    "to": datetime.datetime(1970, 1, 12),
                    "ids": ",".join([str(x.id) for x in db.session.query(Device)]),
                },
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])

    def test_get_one_device_is_available_for_mount(self):
        """Ensure we get a one device available."""
        available_device, _ = self.mount_a_device(
            begin_date=datetime.datetime(2022, 1, 1, 0, 0, 0),
            end_date=datetime.datetime(2022, 1, 30, 0, 0, 0),
        )
        for _ in range(3):
            self.mount_a_device()
        with self.run_requests_as(self.u):
            response = self.client.get(
                self.url,
                query_string={
                    "from": fake.date_time_this_month(),
                    "to": datetime.datetime(2025, 12, 1, 0, 0, 0),
                    "ids": ",".join([str(x.id) for x in db.session.query(Device)]),
                },
            )
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertEqual(len(data), 4)
        # One device should be available
        self.assertEqual(
            list(filter(lambda item: item["id"] == str(available_device.id), data))[0][
                "available"
            ],
            True,
        )

    def test_get_one_device_is_available_for_mount_without_end_date_in_query(self):
        """Ensure we get a one device available."""
        available_device, _ = self.mount_a_device(
            begin_date=datetime.datetime(2022, 1, 1, 0, 0, 0),
            end_date=datetime.datetime(2022, 1, 30, 0, 0, 0),
        )
        for _ in range(3):
            self.mount_a_device()
        with self.run_requests_as(self.u):
            response = self.client.get(
                self.url,
                query_string={
                    "from": fake.date_time_this_month(),
                    "ids": ",".join([str(x.id) for x in db.session.query(Device)]),
                },
            )
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertEqual(len(data), 4)
        # One device should be available
        self.assertEqual(
            list(filter(lambda item: item["id"] == str(available_device.id), data))[0][
                "available"
            ],
            True,
        )

    def test_get_no_device_available(self):
        """Ensure we get a one device entry per blocking mount."""
        unavailable_device_1, _ = self.mount_a_device(
            begin_date=datetime.datetime(2022, 1, 1, 0, 0, 0),
            end_date=datetime.datetime(2022, 1, 30, 0, 0, 0),
        )
        unavailable_device_2, _ = self.mount_a_device(
            begin_date=datetime.datetime(2022, 1, 13, 0, 0, 0),
            end_date=datetime.datetime(2022, 1, 30, 0, 0, 0),
        )
        with self.run_requests_as(self.u):
            response = self.client.get(
                self.url,
                query_string={
                    "from": datetime.datetime(2022, 1, 1, 0, 0, 0),
                    "to": datetime.datetime(2022, 1, 15, 0, 0, 0),
                    "ids": ",".join([str(x.id) for x in db.session.query(Device)]),
                },
            )
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertEqual(len(data), 2)
        # Both devices should be unavailable
        self.assertEqual(
            list(filter(lambda item: item["id"] == str(unavailable_device_1.id), data))[
                0
            ]["available"],
            False,
        )
        self.assertEqual(
            list(filter(lambda item: item["id"] == str(unavailable_device_2.id), data))[
                0
            ]["available"],
            False,
        )

    def test_post_is_forbidden(self):
        """Ensure post request is forbidden."""
        with self.run_requests_as(self.u):
            response = self.client.post(
                self.url,
                content_type="application/vnd.api+json",
                query_string={
                    "from": "someday",
                    "to": "another day",
                    "ids": ",".join([str(x.id) for x in db.session.query(Device)]),
                },
            )
        self.assertEqual(response.status_code, 405)

    def test_device_with_multiple_mounting_actions(self):
        """Ensure get a platform with multiple mounting actions."""
        device, device_mount_action_1 = self.mount_a_device(
            begin_date=datetime.datetime(2020, 1, 1, 0, 0, 0),
            end_date=datetime.datetime(2021, 1, 30, 0, 0, 0),
        )
        device_mount_action_2 = DeviceMountAction(
            configuration=self.configuration,
            device=device,
            offset_x=fake.pyint(),
            offset_y=fake.pyint(),
            offset_z=fake.pyint(),
            begin_description=fake.text(),
            begin_contact=self.u.contact,
            begin_date=datetime.datetime(2022, 1, 1, 0, 0, 0),
            end_date=datetime.datetime(2025, 1, 1, 0, 0, 0),
            end_description=fake.text(),
            end_contact=self.u.contact,
        )
        db.session.add(device_mount_action_2)
        db.session.commit()
        with self.run_requests_as(self.u):
            response = self.client.get(
                self.url,
                query_string={
                    "from": datetime.datetime(2023, 1, 1, 0, 0, 0),
                    "to": datetime.datetime(2025, 1, 15, 0, 0, 0),
                    "ids": ",".join([str(x.id) for x in db.session.query(Device)]),
                },
            )
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertEqual(len(data), 1)
        self.assertEqual(
            list(filter(lambda item: item["id"] == str(device.id), data))[0][
                "available"
            ],
            False,
        )
        expected_output = [
            {
                "id": str(device.id),
                "available": False,
                "mount": str(device_mount_action_2.id),
                "configuration": str(self.configuration.id),
                "begin_date": "2022-01-01T00:00:00",
                "end_date": "2025-01-01T00:00:00",
            }
        ]
        self.assertEqual(expected_output, data)
        # Now we ask for a bigger time interval
        with self.run_requests_as(self.u):
            response = self.client.get(
                self.url,
                query_string={
                    "from": datetime.datetime(2021, 1, 1, 0, 0, 0),
                    "to": datetime.datetime(2025, 1, 15, 0, 0, 0),
                    "ids": ",".join([str(x.id) for x in db.session.query(Device)]),
                },
            )
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertEqual(len(data), 2)
        self.assertEqual(
            list(filter(lambda item: item["id"] == str(device.id), data))[0][
                "available"
            ],
            False,
        )
        expected_output = [
            {
                "id": str(device.id),
                "available": False,
                "mount": str(device_mount_action_1.id),
                "configuration": str(self.configuration.id),
                "begin_date": "2020-01-01T00:00:00",
                "end_date": "2021-01-30T00:00:00",
            },
            {
                "id": str(device.id),
                "available": False,
                "mount": str(device_mount_action_2.id),
                "configuration": str(self.configuration.id),
                "begin_date": "2022-01-01T00:00:00",
                "end_date": "2025-01-01T00:00:00",
            },
        ]

        self.assertEqual(expected_output, data)

    def test_filter_one_or_multiple_devices(self):
        """Test that we can filter for specific devices."""
        available_device, _ = self.mount_a_device(
            begin_date=datetime.datetime(2022, 1, 1, 0, 0, 0),
            end_date=datetime.datetime(2022, 1, 30, 0, 0, 0),
        )
        for _ in range(4):
            self.mount_a_device()
        # With the largest possible filter for the ids
        with self.run_requests_as(self.u):
            response = self.client.get(
                self.url,
                query_string={
                    "from": fake.date_time_this_month(),
                    "to": datetime.datetime(2025, 12, 1, 0, 0, 0),
                    "ids": ",".join([str(x.id) for x in db.session.query(Device)]),
                },
            )
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertEqual(len(data), 5)

        # filter for one device
        with self.run_requests_as(self.u):
            response = self.client.get(
                self.url,
                query_string={
                    "from": fake.date_time_this_month(),
                    "to": datetime.datetime(2025, 12, 1, 0, 0, 0),
                    "ids": available_device.id,
                },
            )
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertEqual(len(data), 1)

        expected_output = [{"id": str(available_device.id), "available": True}]
        self.assertEqual(expected_output, data)

        # With more than one id
        available_device_2, device_mount_action_2 = self.mount_a_device(
            begin_date=datetime.datetime(2022, 3, 1, 0, 0, 0),
            end_date=datetime.datetime(2022, 12, 30, 0, 0, 0),
        )
        with self.run_requests_as(self.u):
            response = self.client.get(
                self.url,
                query_string={
                    "from": fake.date_time_this_month(),
                    "to": datetime.datetime(2025, 12, 1, 0, 0, 0),
                    "ids": f"{available_device.id},{available_device_2.id}",
                },
            )
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertEqual(len(data), 2)
        expected_output = [
            {
                "id": str(available_device_2.id),
                "available": False,
                "mount": str(device_mount_action_2.id),
                "configuration": str(self.configuration.id),
                "begin_date": "2022-03-01T00:00:00",
                "end_date": "2022-12-30T00:00:00",
            },
            {"id": str(available_device.id), "available": True},
        ]
        self.assertEqual(expected_output, data)

    def test_dont_show_private_devices(self):
        """Ensure that we don't show information about private devices."""
        private_device = Device(
            short_name="private device",
            is_private=True,
        )
        db.session.add(private_device)
        db.session.commit()

        with self.run_requests_as(self.u):
            response = self.client.get(
                self.url,
                query_string={
                    "from": datetime.datetime(2021, 1, 1, 0, 0, 0),
                    "to": datetime.datetime(2025, 1, 15, 0, 0, 0),
                    "ids": ",".join([str(x.id) for x in db.session.query(Device)]),
                },
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])
