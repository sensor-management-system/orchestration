"""Tests for the devices."""
import json
from unittest.mock import patch

from project import base_url
from project.api.models import User, Device
from project.api.models.base_model import db
from project.api.services.idl_services import Idl
from project.tests.base import BaseTestCase
from project.tests.base import create_token
from project.tests.base import fake
from project.tests.permissions import add_a_contact
from project.tests.permissions import create_superuser_token
from project.tests.permissions.test_platforms import IDL_USER_ACCOUNT


class TestDevicePermissions(BaseTestCase):
    """Tests for the Device Permissions."""

    device_url = base_url + "/devices"
    object_type = "device"

    def test_add_public_device(self):
        """Ensure a new device can be public."""
        public_sensor = Device(
            id=15,
            short_name=fake.pystr(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        db.session.add(public_sensor)
        db.session.commit()

        device = db.session.query(Device).filter_by(id=public_sensor.id).one()
        self.assertEqual(device.is_public, True)
        self.assertEqual(device.is_internal, False)
        self.assertEqual(device.is_private, False)

    def test_add_private_device(self):
        """Ensure a new device can be private."""
        private_sensor = Device(
            id=1,
            short_name=fake.pystr(),
            is_public=False,
            is_private=True,
            is_internal=False,
        )
        db.session.add(private_sensor)
        db.session.commit()

        device = db.session.query(Device).filter_by(id=private_sensor.id).one()
        self.assertEqual(device.is_public, False)
        self.assertEqual(device.is_internal, False)
        self.assertEqual(device.is_private, True)

    def test_add_device_model(self):
        """Ensure a new device model can be internal."""
        internal_sensor = Device(
            id=33,
            short_name=fake.pystr(),
            is_internal=True,
            is_public=False,
            is_private=False,
        )
        db.session.add(internal_sensor)
        db.session.commit()

        device = db.session.query(Device).filter_by(id=internal_sensor.id).one()
        self.assertEqual(device.is_internal, True)
        self.assertEqual(device.is_public, False)
        self.assertEqual(device.is_private, False)

    def test_add_device(self):
        """Ensure a new device can be added to api and is internal."""
        device_data = {
            "data": {
                "type": "device",
                "attributes": {
                    "short_name": fake.pystr(),
                    "is_public": False,
                    "is_internal": True,
                    "is_private": False,
                },
            }
        }
        access_headers = create_token()
        with self.client:
            response = self.client.post(
                self.device_url,
                data=json.dumps(device_data),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data["data"]["attributes"]["is_internal"], True)
        self.assertEqual(data["data"]["attributes"]["is_public"], False)
        self.assertEqual(data["data"]["attributes"]["is_private"], False)

    def test_get_as_anonymous_user(self):
        """Ensure anonymous user can only see public objects."""
        public_sensor = Device(
            id=15,
            short_name=fake.pystr(),
            is_private=False,
            is_internal=False,
            is_public=True,
        )

        internal_sensor = Device(
            id=33,
            short_name=fake.pystr(),
            is_public=False,
            is_private=False,
            is_internal=True,
        )
        private_sensor = Device(
            id=1,
            short_name="private device",
            is_public=False,
            is_internal=False,
            is_private=True,
        )
        db.session.add_all([public_sensor, internal_sensor, private_sensor])
        db.session.commit()

        response = self.client.get(self.device_url)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertEqual(len(data["data"]), 1)
        self.assertEqual(data["data"][0]["id"], str(public_sensor.id))

    def test_get_as_registered_user(self):
        """Ensure that a registered user can see public, internal, and only his own private objects"""
        public_sensor = Device(
            id=15,
            short_name=fake.pystr(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )

        internal_sensor = Device(
            id=33,
            short_name=fake.pystr(),
            is_public=False,
            is_private=False,
            is_internal=True,
        )
        private_sensor = Device(
            id=1,
            short_name="private device",
            is_public=False,
            is_internal=False,
            is_private=True,
        )
        private_sensor_1 = Device(
            id=3,
            short_name="private device",
            is_public=False,
            is_private=True,
            is_internal=False,
        )

        contact = add_a_contact()
        contact_1 = add_a_contact()

        user = User(subject="test_user@test.test", contact=contact)
        user_1 = User(subject="test_user1@test.test", contact=contact_1)
        db.session.add_all(
            [
                public_sensor,
                internal_sensor,
                private_sensor,
                private_sensor_1,
                contact,
                user,
                contact_1,
                user_1,
            ]
        )
        db.session.commit()

        private_sensor.created_by_id = user.id
        private_sensor_1.created_by_id = user_1.id

        token_data = {
            "sub": user.subject,
            "iss": "SMS unittest",
            "family_name": contact.family_name,
            "given_name": contact.given_name,
            "email": contact.email,
            "aud": "SMS",
        }
        access_headers = create_token(token_data)
        response = self.client.get(self.device_url, headers=access_headers)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertEqual(len(data["data"]), 3)

    def test_add_device_with_multipel_true_status(self):
        """Make Sure that is an object can't have tow True status at the same time"""
        device_data = {
            "data": {
                "type": "device",
                "attributes": {
                    "short_name": fake.pystr(),
                    "is_public": True,
                    "is_internal": True,
                    "is_private": False,
                },
            }
        }
        device_data_1 = {
            "data": {
                "type": "device",
                "attributes": {
                    "short_name": fake.pystr(),
                    "is_public": False,
                    "is_internal": True,
                    "is_private": True,
                },
            }
        }
        device_data_2 = {
            "data": {
                "type": "device",
                "attributes": {
                    "short_name": fake.pystr(),
                    "is_public": True,
                    "is_internal": True,
                    "is_private": True,
                },
            }
        }
        access_headers = create_token()
        with self.client:
            response = self.client.post(
                self.device_url,
                data=json.dumps(device_data),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
            self.assertEqual(response.status_code, 409)

            response_1 = self.client.post(
                self.device_url,
                data=json.dumps(device_data_1),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
            self.assertEqual(response_1.status_code, 409)

            response_2 = self.client.post(
                self.device_url,
                data=json.dumps(device_data_2),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
            self.assertEqual(response_2.status_code, 409)

    def test_add_groups_ids(self):
        """Make sure that a device with groups-ids can be created"""
        device_data = {
            "data": {
                "type": "device",
                "attributes": {
                    "short_name": "Test device associated to a group",
                    "is_public": False,
                    "is_internal": True,
                    "is_private": False,
                    "group_ids": ["12"],
                },
            }
        }
        access_headers = create_token()
        with self.client:
            response = self.client.post(
                self.device_url,
                data=json.dumps(device_data),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )

        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 201)

        self.assertEqual(data["data"]["attributes"]["group_ids"], ["12"])

    def test_get_an_internal_device_as_an_unregistered_user(self):
        """An unregistered user should not be able to
        retrieve an internal Device."""

        internal_sensor = Device(
            short_name=fake.pystr(),
            is_public=False,
            is_private=False,
            is_internal=True,
        )
        db.session.add(internal_sensor)
        db.session.commit()
        url = f"{self.device_url}/{internal_sensor.id}"
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)

    def test_get_an_private_device_as_not_owner_user(self):
        """Make sure that a normal user is not allowed a retrieve a not owned
        private device."""

        c = add_a_contact()
        user = User(subject="test_user1@test.test", contact=c)

        db.session.add_all([c, user])
        db.session.commit()

        private_sensor = Device(
            short_name=fake.pystr(),
            is_public=False,
            is_private=True,
            is_internal=False,
            created_by_id=user.id,
        )
        db.session.add(private_sensor)
        db.session.commit()

        access_headers = create_token()
        url = f"{self.device_url}/{private_sensor.id}"
        response = self.client.get(url, headers=access_headers)
        self.assertEqual(response.status, "403 FORBIDDEN")

    def test_patch_device_as_a_member_in_a_permission_group(self):
        """Make sure that a member in a group (admin/member) can change
         the device data per patch request"""
        group_id_test_user_is_member_in_2 = IDL_USER_ACCOUNT.membered_permission_groups
        devices = preparation_of_public_and_internal_device_data(
            group_id_test_user_is_member_in_2
        )
        access_headers = create_token()
        for device_data in devices:
            with self.client:
                response = self.client.post(
                    self.device_url,
                    data=json.dumps(device_data),
                    content_type="application/vnd.api+json",
                    headers=access_headers,
                )

            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 201)

            self.assertIn(
                group_id_test_user_is_member_in_2[0],
                data["data"]["attributes"]["group_ids"],
            )
            with patch.object(
                Idl, "get_all_permission_groups_for_a_user"
            ) as test_get_all_permission_groups:
                test_get_all_permission_groups.return_value = IDL_USER_ACCOUNT
                device_data_changed = {
                    "data": {
                        "type": "device",
                        "id": data["data"]["id"],
                        "attributes": {"short_name": "Changed device name",},
                    }
                }
                url = f"{self.device_url}/{data['data']['id']}"
                res = super().update_object(url, device_data_changed, self.object_type)
                self.assertEqual(
                    res["data"]["attributes"]["short_name"],
                    device_data_changed["data"]["attributes"]["short_name"],
                )

    def test_patch_device_user_not_in_any_permission_group(self):
        """Make sure that a user can only do changes in devices, where he/she is involved."""
        group_id_test_user_is_not_included = ["13"]
        devices = preparation_of_public_and_internal_device_data(
            group_id_test_user_is_not_included
        )
        access_headers = create_token()
        for device_data in devices:
            with self.client:
                response = self.client.post(
                    self.device_url,
                    data=json.dumps(device_data),
                    content_type="application/vnd.api+json",
                    headers=access_headers,
                )

            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 201)

            self.assertEqual(data["data"]["attributes"]["group_ids"], ["13"])
            with patch.object(
                Idl, "get_all_permission_groups_for_a_user"
            ) as test_get_all_permission_groups:
                test_get_all_permission_groups.return_value = IDL_USER_ACCOUNT
                device_data_changed = {
                    "data": {
                        "type": "device",
                        "id": data["data"]["id"],
                        "attributes": {"short_name": "Forbidden"},
                    }
                }
                url = f"{self.device_url}/{data['data']['id']}"
                access_headers = create_token()
                with self.client:
                    response = self.client.patch(
                        url,
                        data=json.dumps(device_data_changed),
                        content_type="application/vnd.api+json",
                        headers=access_headers,
                    )
                self.assertEqual(response.status, "403 FORBIDDEN")

    def test_delete_device_as_an_admin_in_a_permission_group(self):
        """Make sure that an admin can delete a device in the same permission group."""
        group_id_test_user_is_member_in_2 = IDL_USER_ACCOUNT.membered_permission_groups
        devices = preparation_of_public_and_internal_device_data(
            group_id_test_user_is_member_in_2
        )
        access_headers = create_token()
        for device_data in devices:
            with self.client:
                response = self.client.post(
                    self.device_url,
                    data=json.dumps(device_data),
                    content_type="application/vnd.api+json",
                    headers=access_headers,
                )

            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 201)

            self.assertIn(
                group_id_test_user_is_member_in_2[0],
                data["data"]["attributes"]["group_ids"],
            )
            with patch.object(
                Idl, "get_all_permission_groups_for_a_user"
            ) as test_get_all_permission_groups:
                test_get_all_permission_groups.return_value = IDL_USER_ACCOUNT
                url = f"{self.device_url}/{data['data']['id']}"
                delete_response = self.client.delete(url, headers=access_headers)
                delete_data = json.loads(delete_response.data.decode())
                self.assertEqual(delete_data["errors"][0]["status"], 403)

    def test_delete_public_device_as_an_admin_in_a_permission_group(self):
        """Make sure that a public device can be deleted as an admin in the permission group."""
        group_id_test_user_is_admin_in_1 = (
            IDL_USER_ACCOUNT.administrated_permission_groups
        )
        devices = preparation_of_public_and_internal_device_data(
            group_id_test_user_is_admin_in_1
        )
        access_headers = create_token()
        for device_data in devices:
            with self.client:
                response = self.client.post(
                    self.device_url,
                    data=json.dumps(device_data),
                    content_type="application/vnd.api+json",
                    headers=access_headers,
                )

            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 201)

            self.assertEqual(data["data"]["attributes"]["group_ids"], ["1"])

        with patch.object(
            Idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups:
            test_get_all_permission_groups.return_value = IDL_USER_ACCOUNT
            url = f"{self.device_url}/{data['data']['id']}"
            delete_response = self.client.delete(url, headers=access_headers)
            self.assertEqual(delete_response.status_code, 200)

    def test_delete_private_device_as_superuser(self):
        """Make sure that a superuser is allowed to delete not owned private devices."""
        device_data = {
            "data": {
                "type": "device",
                "attributes": {
                    "short_name": fake.pystr(),
                    "is_public": False,
                    "is_internal": False,
                    "is_private": True,
                },
            }
        }
        access_headers = create_superuser_token()
        with self.client:
            response = self.client.post(
                self.device_url,
                data=json.dumps(device_data),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )

        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 201)

        with patch.object(
            Idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups:
            test_get_all_permission_groups.return_value = IDL_USER_ACCOUNT
            url = f"{self.device_url}/{data['data']['id']}"
            delete_response = self.client.delete(url, headers=access_headers)
            self.assertEqual(delete_response.status_code, 200)

    def test_delete_device_as_superuser_not_involved_in_permission_group(self):
        """Make sure that a superuser can delete a device even if he/she is not admin in
        the corresponding permission group."""
        group_id_test_user_is_not_included = ["40"]
        device_data = {
            "data": {
                "type": "device",
                "attributes": {
                    "short_name": fake.pystr(),
                    "is_public": True,
                    "is_internal": False,
                    "is_private": False,
                    "group_ids": group_id_test_user_is_not_included,
                },
            }
        }
        access_headers = create_superuser_token()
        with self.client:
            response = self.client.post(
                self.device_url,
                data=json.dumps(device_data),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )

        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 201)

        self.assertEqual(data["data"]["attributes"]["group_ids"], ["40"])

        with patch.object(
            Idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups:
            test_get_all_permission_groups.return_value = IDL_USER_ACCOUNT
            url = f"{self.device_url}/{data['data']['id']}"
            delete_response = self.client.delete(url, headers=access_headers)
            self.assertEqual(delete_response.status_code, 200)


def preparation_of_public_and_internal_device_data(group_ids):
    """
    Data to add an internal and a public device.

    :param group_ids: list of permission groups
    :return: list of data for two devices [public, internal]
    """
    public_device_data = {
        "data": {
            "type": "device",
            "attributes": {
                "short_name": fake.pystr(),
                "is_public": True,
                "is_internal": False,
                "is_private": False,
                "group_ids": group_ids,
            },
        }
    }
    internal_device_data = {
        "data": {
            "type": "device",
            "attributes": {
                "short_name": fake.pystr(),
                "is_public": False,
                "is_internal": True,
                "is_private": False,
                "group_ids": group_ids,
            },
        }
    }
    devices = [public_device_data, internal_device_data]
    return devices
