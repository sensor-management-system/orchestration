# SPDX-FileCopyrightText: 2021 - 2023
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Tests for the devices."""
import json
from unittest.mock import patch

from project import base_url
from project.api.models import Contact, Device, User
from project.api.models.base_model import db
from project.extensions.idl.models.user_account import UserAccount
from project.extensions.instances import idl
from project.tests.base import BaseTestCase, create_token, fake
from project.tests.permissions import (
    create_a_test_contact,
    create_a_test_device,
    create_superuser_token,
)
from project.tests.permissions.test_platforms import IDL_USER_ACCOUNT


class TestDevicePermissions(BaseTestCase):
    """Tests for the Device Permissions."""

    device_url = base_url + "/devices"
    object_type = "device"

    def test_add_public_device(self):
        """Ensure a new device can be public."""
        public_sensor = create_a_test_device(
            public=True,
            private=False,
            internal=False,
        )
        db.session.add(public_sensor)
        db.session.commit()

        device = db.session.query(Device).filter_by(id=public_sensor.id).one()
        self.assertEqual(device.is_public, True)
        self.assertEqual(device.is_internal, False)
        self.assertEqual(device.is_private, False)

    def test_add_private_device(self):
        """Ensure a new device can be private."""
        private_sensor = create_a_test_device(
            public=False,
            private=True,
            internal=False,
        )
        db.session.add(private_sensor)
        db.session.commit()

        device = db.session.query(Device).filter_by(id=private_sensor.id).one()
        self.assertEqual(device.is_public, False)
        self.assertEqual(device.is_internal, False)
        self.assertEqual(device.is_private, True)

    def test_add_device_model(self):
        """Ensure a new device model can be internal."""
        internal_sensor = create_a_test_device(
            internal=True,
            public=False,
            private=False,
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
                    "manufacturer_name": fake.company(),
                    "is_public": False,
                    "is_internal": False,
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
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data["data"]["attributes"]["is_internal"], False)
        self.assertEqual(data["data"]["attributes"]["is_public"], False)
        self.assertEqual(data["data"]["attributes"]["is_private"], True)

    def test_get_as_anonymous_user(self):
        """Ensure anonymous user can only see public objects."""
        public_sensor = create_a_test_device(
            private=False,
            internal=False,
            public=True,
        )

        internal_sensor = create_a_test_device(
            public=False,
            private=False,
            internal=True,
        )
        private_sensor = create_a_test_device(
            public=False,
            internal=False,
            private=True,
        )
        db.session.add_all([public_sensor, internal_sensor, private_sensor])
        db.session.commit()

        response = self.client.get(self.device_url)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertEqual(len(data["data"]), 1)
        self.assertEqual(data["data"][0]["id"], str(public_sensor.id))

    def test_get_as_registered_user(self):
        """Ensure a registered user can see public, internal, and only his own private objects."""
        public_sensor = create_a_test_device(
            public=True,
            private=False,
            internal=False,
        )

        internal_sensor = create_a_test_device(
            public=False,
            private=False,
            internal=True,
        )
        private_sensor = create_a_test_device(
            public=False,
            internal=False,
            private=True,
        )
        private_sensor_1 = create_a_test_device(
            public=False,
            private=True,
            internal=False,
        )

        contact = create_a_test_contact()
        contact_1 = create_a_test_contact()

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
        """Ensure an object can't have two True permission stati at the same time."""
        device_data = {
            "data": {
                "type": "device",
                "attributes": {
                    "short_name": fake.pystr(),
                    "manufacturer_name": fake.company(),
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
                    "manufacturer_name": fake.company(),
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
                    "manufacturer_name": fake.company(),
                    "is_public": True,
                    "is_internal": True,
                    "is_private": True,
                },
            }
        }
        access_headers = create_superuser_token()
        with self.client:
            with patch.object(
                idl, "get_all_permission_groups_for_a_user"
            ) as test_get_all_permission_groups:
                test_get_all_permission_groups.return_value = IDL_USER_ACCOUNT
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
        """Ensure a device with groups ids can be created."""
        group_id_test_user_is_member_in_2 = IDL_USER_ACCOUNT.membered_permission_groups
        access_headers = create_token()
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups:
            test_get_all_permission_groups.return_value = IDL_USER_ACCOUNT
            device_data = {
                "data": {
                    "type": "device",
                    "attributes": {
                        "short_name": "Test device associated to a group",
                        "manufacturer_name": fake.company(),
                        "is_public": False,
                        "is_internal": True,
                        "is_private": False,
                        "group_ids": group_id_test_user_is_member_in_2,
                    },
                }
            }
            with self.client:
                response = self.client.post(
                    self.device_url,
                    data=json.dumps(device_data),
                    content_type="application/vnd.api+json",
                    headers=access_headers,
                )

            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 201)

        self.assertEqual(
            data["data"]["attributes"]["group_ids"], group_id_test_user_is_member_in_2
        )

    def test_get_an_internal_device_as_an_unregistered_user(self):
        """Ensure an unregistered user can't view an internal device."""
        internal_sensor = Device(
            short_name=fake.pystr(),
            manufacturer_name=fake.company(),
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
        """Ensure a normal user is not allowed a view a not owned private device."""
        c = create_a_test_contact()
        user = User(subject="test_user1@test.test", contact=c)

        db.session.add_all([c, user])
        db.session.commit()

        private_sensor = Device(
            short_name=fake.pystr(),
            manufacturer_name=fake.company(),
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

    def test_get_an_private_device_as_anonymous(self):
        """Ensure an anonymous user is not allowed to view a private device."""
        c = create_a_test_contact()
        user = User(subject="test_user1@test.test", contact=c)

        db.session.add_all([c, user])
        db.session.commit()

        private_sensor = Device(
            short_name=fake.pystr(),
            manufacturer_name=fake.company(),
            is_public=False,
            is_private=True,
            is_internal=False,
            created_by_id=user.id,
        )
        db.session.add(private_sensor)
        db.session.commit()

        url = f"{self.device_url}/{private_sensor.id}"
        response = self.client.get(url)
        self.assertIn(response.status_code, [401, 403])

    def test_patch_device_as_a_member_in_a_permission_group(self):
        """Ensure a member in a group (admin/member) can change the device."""
        group_id_test_user_is_member_in_2 = IDL_USER_ACCOUNT.membered_permission_groups
        devices = preparation_of_public_and_internal_device_data(
            group_id_test_user_is_member_in_2
        )
        access_headers = create_token()
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups:
            test_get_all_permission_groups.return_value = IDL_USER_ACCOUNT
            for device_data in devices:
                with self.client:
                    response = self.client.post(
                        self.device_url,
                        data=json.dumps(device_data),
                        content_type="application/vnd.api+json",
                        headers=access_headers,
                    )

                data = json.loads(response.data.decode())
                # print(data)
                self.assertEqual(response.status_code, 201)

            self.assertIn(
                group_id_test_user_is_member_in_2[0],
                data["data"]["attributes"]["group_ids"],
            )
            with patch.object(
                idl, "get_all_permission_groups_for_a_user"
            ) as test_get_all_permission_groups:
                test_get_all_permission_groups.return_value = IDL_USER_ACCOUNT
                device_data_changed = {
                    "data": {
                        "type": "device",
                        "id": data["data"]["id"],
                        "attributes": {
                            "short_name": "Changed device name",
                        },
                    }
                }
                url = f"{self.device_url}/{data['data']['id']}"
                res = super().update_object(url, device_data_changed, self.object_type)
                self.assertEqual(
                    res["data"]["attributes"]["short_name"],
                    device_data_changed["data"]["attributes"]["short_name"],
                )

    def test_patch_archived_device_as_a_member_in_a_permission_group(self):
        """Ensure a member in a group (admin/member) can patch the device."""
        group_id_test_user_is_member_in_2 = IDL_USER_ACCOUNT.membered_permission_groups
        devices = preparation_of_public_and_internal_device_data(
            group_id_test_user_is_member_in_2
        )
        access_headers = create_token()
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups:
            test_get_all_permission_groups.return_value = IDL_USER_ACCOUNT
            for device_data in devices:
                with self.client:
                    response = self.client.post(
                        self.device_url,
                        data=json.dumps(device_data),
                        content_type="application/vnd.api+json",
                        headers=access_headers,
                    )

                data = json.loads(response.data.decode())
                # print(data)
                self.assertEqual(response.status_code, 201)
                device = (
                    db.session.query(Device).filter_by(id=data["data"]["id"]).first()
                )
                device.archived = True
                db.session.add(device)
                db.session.commit()

            self.assertIn(
                group_id_test_user_is_member_in_2[0],
                data["data"]["attributes"]["group_ids"],
            )
            with patch.object(
                idl, "get_all_permission_groups_for_a_user"
            ) as test_get_all_permission_groups:
                test_get_all_permission_groups.return_value = IDL_USER_ACCOUNT
                device_data_changed = {
                    "data": {
                        "type": "device",
                        "id": data["data"]["id"],
                        "attributes": {
                            "short_name": "Changed device name",
                        },
                    }
                }
                url = f"{self.device_url}/{data['data']['id']}"
                _ = super().try_update_object_with_status_code(
                    url, device_data_changed, expected_status_code=403
                )

    def test_patch_device_user_not_in_any_permission_group(self):
        """Ensure a user can only do changes in devices, where he/she is involved."""
        public_sensor = create_a_test_device(
            public=True, private=False, internal=False, group_ids=["13"]
        )

        db.session.add(public_sensor)
        db.session.commit()

        self.assertEqual(public_sensor.group_ids, ["13"])
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups:
            test_get_all_permission_groups.return_value = IDL_USER_ACCOUNT
            device_data_changed = {
                "data": {
                    "type": "device",
                    "id": public_sensor.id,
                    "attributes": {"short_name": "Forbidden"},
                }
            }
            url = f"{self.device_url}/{public_sensor.id}"
            access_headers = create_token()
            with self.client:
                response = self.client.patch(
                    url,
                    data=json.dumps(device_data_changed),
                    content_type="application/vnd.api+json",
                    headers=access_headers,
                )
            self.assertEqual(response.status, "403 FORBIDDEN")

    def test_add_internal_device_without_group(self):
        """Ensure a internal device can't be added without a group."""
        device_data = {
            "data": {
                "type": "device",
                "attributes": {
                    "short_name": fake.pystr(),
                    "manufacturer_name": fake.company(),
                    "is_public": False,
                    "is_internal": True,
                    "is_private": False,
                },
            }
        }
        access_headers = create_token()
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups:
            test_get_all_permission_groups.return_value = IDL_USER_ACCOUNT
            with self.client:
                response = self.client.post(
                    self.device_url,
                    data=json.dumps(device_data),
                    content_type="application/vnd.api+json",
                    headers=access_headers,
                )
        self.assertEqual(response.status_code, 403)

    def test_add_public_device_without_group(self):
        """Ensure a public device can't be added without a group."""
        device_data = {
            "data": {
                "type": "device",
                "attributes": {
                    "short_name": fake.pystr(),
                    "manufacturer_name": fake.company(),
                    "is_public": True,
                    "is_internal": False,
                    "is_private": False,
                },
            }
        }
        access_headers = create_token()
        with patch.object(
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups:
            test_get_all_permission_groups.return_value = IDL_USER_ACCOUNT
            with self.client:
                response = self.client.post(
                    self.device_url,
                    data=json.dumps(device_data),
                    content_type="application/vnd.api+json",
                    headers=access_headers,
                )
        self.assertEqual(response.status_code, 403)

    def test_add_private_device_without_group(self):
        """Ensure a new private device can be added without a group."""
        device_data = {
            "data": {
                "type": "device",
                "attributes": {
                    "short_name": fake.pystr(),
                    "manufacturer_name": fake.company(),
                    "is_public": False,
                    "is_internal": False,
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
        self.assertEqual(response.status_code, 201)

    def test_delete_device_as_member_in_a_permission_group(self):
        """Make sure that a normal member of a group can't delete a device."""
        group_id_test_user_is_member_in_2 = IDL_USER_ACCOUNT.membered_permission_groups
        devices = preparation_of_public_and_internal_device_data(
            group_id_test_user_is_member_in_2
        )
        access_headers = create_token()
        for device_data in devices:
            with patch.object(
                idl, "get_all_permission_groups_for_a_user"
            ) as test_get_all_permission_groups:
                test_get_all_permission_groups.return_value = IDL_USER_ACCOUNT
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
                url = f"{self.device_url}/{data['data']['id']}"
                delete_response = self.client.delete(url, headers=access_headers)
                self.assertEqual(delete_response.status_code, 403)
                delete_data = json.loads(delete_response.data.decode())
                self.assertEqual(delete_data["errors"][0]["status"], 403)

    def test_delete_public_device_as_an_admin_in_a_permission_group(self):
        """Make sure that a public device can't be deleted as an admin in the permission group."""
        group_id_test_user_is_admin_in_1 = (
            IDL_USER_ACCOUNT.administrated_permission_groups
        )
        devices = preparation_of_public_and_internal_device_data(
            group_id_test_user_is_admin_in_1
        )
        access_headers = create_token()
        for device_data in devices:
            with patch.object(
                idl, "get_all_permission_groups_for_a_user"
            ) as test_get_all_permission_groups:
                test_get_all_permission_groups.return_value = IDL_USER_ACCOUNT
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

                url = f"{self.device_url}/{data['data']['id']}"
                delete_response = self.client.delete(url, headers=access_headers)
                self.assertEqual(delete_response.status_code, 403)

    def test_delete_private_device_as_superuser(self):
        """Make sure that a superuser is allowed to delete not owned private devices."""
        device_data = {
            "data": {
                "type": "device",
                "attributes": {
                    "short_name": fake.pystr(),
                    "manufacturer_name": fake.company(),
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
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups:
            test_get_all_permission_groups.return_value = IDL_USER_ACCOUNT
            url = f"{self.device_url}/{data['data']['id']}"
            delete_response = self.client.delete(url, headers=access_headers)
            self.assertEqual(delete_response.status_code, 200)

    def test_delete_device_as_superuser_not_involved_in_permission_group(self):
        """Ensure a superuser can delete a device even if not admin in permission groups."""
        group_id_test_user_is_not_included = ["40"]
        device_data = {
            "data": {
                "type": "device",
                "attributes": {
                    "short_name": fake.pystr(),
                    "manufacturer_name": fake.company(),
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
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups:
            test_get_all_permission_groups.return_value = IDL_USER_ACCOUNT
            url = f"{self.device_url}/{data['data']['id']}"
            delete_response = self.client.delete(url, headers=access_headers)
            self.assertEqual(delete_response.status_code, 200)

    def test_delete_device_with_pid_as_superuser(self):
        """Make sure that even a superuser can't delete a device with pid."""
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
                    "persistent_identifier": "pid0-0000-0001-1234",
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
            idl, "get_all_permission_groups_for_a_user"
        ) as test_get_all_permission_groups:
            test_get_all_permission_groups.return_value = IDL_USER_ACCOUNT
            url = f"{self.device_url}/{data['data']['id']}"
            delete_response = self.client.delete(url, headers=access_headers)
            # Due to the pid, we can't delete it anymore
            self.assertEqual(delete_response.status_code, 403)

    def test_patch_to_different_permission_group(self):
        """Ensure we can't update to a permission group we aren't members."""
        device = Device(
            short_name="test device", is_public=False, is_internal=True, group_ids=["1"]
        )
        contact = Contact(
            given_name="first",
            family_name="contact",
            email="first.contact@localhost",
        )
        user = User(
            subject=contact.email,
            contact=contact,
        )
        db.session.add_all([device, contact, user])
        db.session.commit()

        payload = {
            "data": {
                "type": "device",
                "id": device.id,
                "attributes": {
                    "group_ids": ["2"],
                },
                "relationships": {},
            }
        }

        with self.run_requests_as(user):
            with patch.object(idl, "get_all_permission_groups_for_a_user") as mock:
                mock.return_value = UserAccount(
                    id="123",
                    username=user.subject,
                    administrated_permission_groups=[],
                    membered_permission_groups=[*device.group_ids],
                )
                with self.client:
                    response = self.client.patch(
                        f"{self.device_url}/{device.id}",
                        data=json.dumps(payload),
                        content_type="application/vnd.api+json",
                    )
        self.assertEqual(response.status_code, 403)

    def test_patch_to_remove_permission_group_non_admin(self):
        """Ensure we can't remove a permission group we aren't admins."""
        device = Device(
            short_name="test device", is_public=False, is_internal=True, group_ids=["1"]
        )
        contact = Contact(
            given_name="first",
            family_name="contact",
            email="first.contact@localhost",
        )
        user = User(
            subject=contact.email,
            contact=contact,
        )
        db.session.add_all([device, contact, user])
        db.session.commit()

        payload = {
            "data": {
                "type": "device",
                "id": device.id,
                "attributes": {
                    "group_ids": ["2"],
                },
                "relationships": {},
            }
        }

        with self.run_requests_as(user):
            with patch.object(idl, "get_all_permission_groups_for_a_user") as mock:
                mock.return_value = UserAccount(
                    id="123",
                    username=user.subject,
                    administrated_permission_groups=[],
                    membered_permission_groups=[*device.group_ids, "2"],
                )
                with self.client:
                    response = self.client.patch(
                        f"{self.device_url}/{device.id}",
                        data=json.dumps(payload),
                        content_type="application/vnd.api+json",
                    )
        self.assertEqual(response.status_code, 403)

    def test_patch_from_internal_to_private(self):
        """Ensure we can't set back to private once the device was visible."""
        device = Device(
            short_name="test device", is_public=False, is_internal=True, group_ids=["1"]
        )
        contact = Contact(
            given_name="first",
            family_name="contact",
            email="first.contact@localhost",
        )
        user = User(
            subject=contact.email,
            contact=contact,
        )
        db.session.add_all([device, contact, user])
        db.session.commit()

        payload = {
            "data": {
                "type": "device",
                "id": device.id,
                "attributes": {
                    "group_ids": [],
                    "is_private": True,
                    "is_internal": False,
                },
                "relationships": {},
            }
        }

        with self.run_requests_as(user):
            with patch.object(idl, "get_all_permission_groups_for_a_user") as mock:
                mock.return_value = UserAccount(
                    id="123",
                    username=user.subject,
                    administrated_permission_groups=[],
                    membered_permission_groups=[*device.group_ids],
                )
                with self.client:
                    response = self.client.patch(
                        f"{self.device_url}/{device.id}",
                        data=json.dumps(payload),
                        content_type="application/vnd.api+json",
                    )
        self.assertEqual(response.status_code, 403)


def preparation_of_public_and_internal_device_data(group_ids):
    """
    Prepare data to add an internal and a public device.

    :param group_ids: list of permission groups
    :return: list of data for two devices [public, internal]
    """
    public_device_data = {
        "data": {
            "type": "device",
            "attributes": {
                "short_name": fake.pystr(),
                "manufacturer_name": fake.company(),
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
                "manufacturer_name": fake.company(),
                "is_public": False,
                "is_internal": True,
                "is_private": False,
                "group_ids": group_ids,
            },
        }
    }
    devices = [public_device_data, internal_device_data]
    return devices
