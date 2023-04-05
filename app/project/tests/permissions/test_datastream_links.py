# SPDX-FileCopyrightText: 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Tests for the permission handling for datastream_link resources."""

import datetime
import json
import time
from unittest.mock import patch

from project import base_url
from project.api.models import (
    Configuration,
    Contact,
    DatastreamLink,
    Device,
    DeviceMountAction,
    DeviceProperty,
    User,
)
from project.api.models.base_model import db
from project.extensions.idl.models.user_account import UserAccount
from project.extensions.instances import idl
from project.tests.base import BaseTestCase, create_token, fake, generate_userinfo_data
from project.tests.permissions import create_a_test_configuration


class TestDatastreamLinks(BaseTestCase):
    """Test DatastreamLink."""

    url = base_url + "/datastream-links"

    def test_get_public_datastream_links(self):
        """Ensure that we can get a list of public datastream links."""
        configuration1 = create_a_test_configuration(
            public=True,
            internal=False,
        )
        configuration2 = create_a_test_configuration(
            public=True,
            internal=False,
        )
        userinfo = generate_userinfo_data()
        device = Device(
            short_name=fake.linux_processor(),
            manufacturer_name=fake.company(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        begin_contact = Contact(
            given_name=userinfo["given_name"],
            family_name=userinfo["family_name"],
            email=userinfo["email"],
        )
        begin_date = fake.future_datetime()
        end_date = begin_date + datetime.timedelta(days=2)
        device_mount1 = DeviceMountAction(
            begin_date=begin_date,
            end_date=end_date,
            configuration=configuration1,
            begin_contact=begin_contact,
            device=device,
        )
        device_mount2 = DeviceMountAction(
            begin_date=begin_date,
            end_date=end_date,
            configuration=configuration2,
            begin_contact=begin_contact,
            device=device,
        )
        device_property = DeviceProperty(
            label="device property1",
            property_name="device_property1",
            device=device,
        )
        datastream_link1 = DatastreamLink(
            device_property=device_property,
            device_mount_action=device_mount1,
            datasource_id="1",
            thing_id="1",
            datastream_id="1",
        )
        datastream_link2 = DatastreamLink(
            device_property=device_property,
            device_mount_action=device_mount2,
            datasource_id="1",
            thing_id="1",
            datastream_id="1",
        )
        db.session.add_all(
            [
                device,
                begin_contact,
                device_mount1,
                device_mount2,
                device_property,
                datastream_link1,
                datastream_link2,
            ]
        )
        db.session.commit()

        with self.client:
            response = self.client.get(
                self.url,
                content_type="application/vnd.api+json",
            )
            self.assertEqual(response.status_code, 200)
            payload = response.get_json()

            self.assertEqual(len(payload["data"]), 2)

    def test_get_internal_datastream_links(self):
        """Ensure that we get internal datastream links only for authenticate users."""
        configuration1 = create_a_test_configuration(
            public=False,
            internal=True,
        )
        configuration2 = create_a_test_configuration(
            public=False,
            internal=True,
        )
        userinfo = generate_userinfo_data()
        device = Device(
            short_name=fake.linux_processor(),
            manufacturer_name=fake.company(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        begin_contact = Contact(
            given_name=userinfo["given_name"],
            family_name=userinfo["family_name"],
            email=userinfo["email"],
        )
        begin_date = fake.future_datetime()
        end_date = begin_date + datetime.timedelta(days=2)
        device_mount1 = DeviceMountAction(
            begin_date=begin_date,
            end_date=end_date,
            configuration=configuration1,
            begin_contact=begin_contact,
            device=device,
        )
        device_mount2 = DeviceMountAction(
            begin_date=begin_date,
            end_date=end_date,
            configuration=configuration2,
            begin_contact=begin_contact,
            device=device,
        )
        device_property = DeviceProperty(
            label="device property1",
            property_name="device_property1",
            device=device,
        )
        datastream_link1 = DatastreamLink(
            device_property=device_property,
            device_mount_action=device_mount1,
            datasource_id="1",
            thing_id="1",
            datastream_id="1",
        )
        datastream_link2 = DatastreamLink(
            device_property=device_property,
            device_mount_action=device_mount2,
            datasource_id="1",
            thing_id="1",
            datastream_id="1",
        )
        db.session.add_all(
            [
                device,
                begin_contact,
                device_mount1,
                device_mount2,
                device_property,
                datastream_link1,
                datastream_link2,
            ]
        )
        db.session.commit()

        with self.client:
            response = self.client.get(
                self.url,
                content_type="application/vnd.api+json",
            )
            self.assertEqual(response.status_code, 200)
            payload = response.get_json()

            self.assertEqual(len(payload["data"]), 0)

        # With a valid JWT
        access_headers = create_token()
        response = self.client.get(self.url, headers=access_headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 2)

    def test_create_datastream_link_anonymous(self):
        """Ensure we can't add a datastream link without login."""
        configuration = create_a_test_configuration(
            public=True,
            internal=False,
        )
        device = Device(
            short_name=fake.linux_processor(),
            manufacturer_name=fake.company(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        begin_contact = Contact(
            given_name="begin",
            family_name="contact",
            email="begin@contact.org",
        )
        begin_date = fake.future_datetime()
        end_date = begin_date + datetime.timedelta(days=2)
        device_mount = DeviceMountAction(
            begin_date=begin_date,
            end_date=end_date,
            configuration=configuration,
            begin_contact=begin_contact,
            device=device,
        )
        device_property = DeviceProperty(
            label="device property1",
            property_name="device_property1",
            device=device,
        )
        db.session.add_all(
            [
                device,
                begin_contact,
                device_mount,
                device_property,
            ]
        )
        db.session.commit()

        payload = {
            "data": {
                "type": "datastream_link",
                "attributes": {},
                "relationships": {
                    "device_mount_action": {
                        "data": {
                            "id": device_mount.id,
                            "type": "device_mount_action",
                        }
                    },
                    "device_property": {
                        "data": {
                            "id": device_property.id,
                            "type": "device_property",
                        }
                    },
                },
            }
        }
        with self.client:
            response = self.client.post(
                self.url,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 401)

    def test_create_datastream_link_normal_user(self):
        """Ensure we can add a datastream link."""
        configuration = create_a_test_configuration(
            public=True,
            internal=False,
            cfg_permission_group="123",
        )
        device = Device(
            short_name=fake.linux_processor(),
            manufacturer_name=fake.company(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        begin_contact = Contact(
            given_name="begin",
            family_name="contact",
            email="begin@contact.org",
        )
        user = User(
            subject=begin_contact.email,
            contact=begin_contact,
        )
        begin_date = fake.future_datetime()
        end_date = begin_date + datetime.timedelta(days=2)
        device_mount = DeviceMountAction(
            begin_date=begin_date,
            end_date=end_date,
            configuration=configuration,
            begin_contact=begin_contact,
            device=device,
        )
        device_property = DeviceProperty(
            label="device property1",
            property_name="device_property1",
            device=device,
        )
        db.session.add_all(
            [
                device,
                begin_contact,
                device_mount,
                device_property,
                user,
            ]
        )
        db.session.commit()

        payload = {
            "data": {
                "type": "datastream_link",
                "attributes": {
                    "datasource_id": "1",
                    "thing_id": "2",
                    "datastream_id": "3",
                    "tsm_endpoint": "somewhere",
                },
                "relationships": {
                    "device_mount_action": {
                        "data": {
                            "id": device_mount.id,
                            "type": "device_mount_action",
                        }
                    },
                    "device_property": {
                        "data": {
                            "id": device_property.id,
                            "type": "device_property",
                        }
                    },
                },
            }
        }
        with self.run_requests_as(user):
            with patch.object(idl, "get_all_permission_groups_for_a_user") as mock:
                mock.return_value = UserAccount(
                    id="123",
                    username=user.subject,
                    administrated_permission_groups=[],
                    membered_permission_groups=[configuration.cfg_permission_group],
                )
                with self.client:
                    response = self.client.post(
                        self.url,
                        data=json.dumps(payload),
                        content_type="application/vnd.api+json",
                    )
        self.assertEqual(response.status_code, 201)

    def test_create_datastream_link_normal_user_no_matching_group(self):
        """Ensure we can't add a datastream link without a matching group."""
        configuration = create_a_test_configuration(
            public=True,
            internal=False,
            cfg_permission_group="123",
        )
        device = Device(
            short_name=fake.linux_processor(),
            manufacturer_name=fake.company(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        begin_contact = Contact(
            given_name="begin",
            family_name="contact",
            email="begin@contact.org",
        )
        user = User(
            subject=begin_contact.email,
            contact=begin_contact,
        )
        begin_date = fake.future_datetime()
        end_date = begin_date + datetime.timedelta(days=2)
        device_mount = DeviceMountAction(
            begin_date=begin_date,
            end_date=end_date,
            configuration=configuration,
            begin_contact=begin_contact,
            device=device,
        )
        device_property = DeviceProperty(
            label="device property1",
            property_name="device_property1",
            device=device,
        )
        db.session.add_all(
            [
                device,
                begin_contact,
                device_mount,
                device_property,
                user,
            ]
        )
        db.session.commit()

        payload = {
            "data": {
                "type": "datastream_link",
                "attributes": {
                    "datasource_id": "1",
                    "thing_id": "2",
                    "datastream_id": "3",
                    "tsm_endpoint": "somewhere",
                },
                "relationships": {
                    "device_mount_action": {
                        "data": {
                            "id": device_mount.id,
                            "type": "device_mount_action",
                        }
                    },
                    "device_property": {
                        "data": {
                            "id": device_property.id,
                            "type": "device_property",
                        }
                    },
                },
            }
        }
        with self.run_requests_as(user):
            with patch.object(idl, "get_all_permission_groups_for_a_user") as mock:
                mock.return_value = UserAccount(
                    id="123",
                    username=user.subject,
                    administrated_permission_groups=[],
                    membered_permission_groups=[],
                )
                with self.client:
                    response = self.client.post(
                        self.url,
                        data=json.dumps(payload),
                        content_type="application/vnd.api+json",
                    )
        self.assertEqual(response.status_code, 403)

    def test_create_datastream_link_archived_configuration(self):
        """Ensure we can't add a datastream link for an archived config."""
        configuration = create_a_test_configuration(
            public=True,
            internal=False,
            cfg_permission_group="123",
        )
        configuration.archived = True
        device = Device(
            short_name=fake.linux_processor(),
            manufacturer_name=fake.company(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        begin_contact = Contact(
            given_name="begin",
            family_name="contact",
            email="begin@contact.org",
        )
        user = User(
            subject=begin_contact.email,
            contact=begin_contact,
        )
        begin_date = fake.future_datetime()
        end_date = begin_date + datetime.timedelta(days=2)
        device_mount = DeviceMountAction(
            begin_date=begin_date,
            end_date=end_date,
            configuration=configuration,
            begin_contact=begin_contact,
            device=device,
        )
        device_property = DeviceProperty(
            label="device property1",
            property_name="device_property1",
            device=device,
        )
        db.session.add_all(
            [
                device,
                begin_contact,
                device_mount,
                device_property,
                user,
            ]
        )
        db.session.commit()

        payload = {
            "data": {
                "type": "datastream_link",
                "attributes": {
                    "datasource_id": "1",
                    "thing_id": "2",
                    "datastream_id": "3",
                    "tsm_endpoint": "somewhere",
                },
                "relationships": {
                    "device_mount_action": {
                        "data": {
                            "id": device_mount.id,
                            "type": "device_mount_action",
                        }
                    },
                    "device_property": {
                        "data": {
                            "id": device_property.id,
                            "type": "device_property",
                        }
                    },
                },
            }
        }
        with self.run_requests_as(user):
            with patch.object(idl, "get_all_permission_groups_for_a_user") as mock:
                mock.return_value = UserAccount(
                    id="123",
                    username=user.subject,
                    administrated_permission_groups=[],
                    membered_permission_groups=[configuration.cfg_permission_group],
                )
                with self.client:
                    response = self.client.post(
                        self.url,
                        data=json.dumps(payload),
                        content_type="application/vnd.api+json",
                    )
        self.assertEqual(response.status_code, 403)

    def test_create_datastream_link_super_user(self):
        """Ensure we can add a datastream link with a super user."""
        configuration = create_a_test_configuration(
            public=True,
            internal=False,
            cfg_permission_group="123",
        )
        device = Device(
            short_name=fake.linux_processor(),
            manufacturer_name=fake.company(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        begin_contact = Contact(
            given_name="begin",
            family_name="contact",
            email="begin@contact.org",
        )
        user = User(
            subject=begin_contact.email,
            contact=begin_contact,
            is_superuser=True,
        )
        begin_date = fake.future_datetime()
        end_date = begin_date + datetime.timedelta(days=2)
        device_mount = DeviceMountAction(
            begin_date=begin_date,
            end_date=end_date,
            configuration=configuration,
            begin_contact=begin_contact,
            device=device,
        )
        device_property = DeviceProperty(
            label="device property1",
            property_name="device_property1",
            device=device,
        )
        db.session.add_all(
            [
                device,
                begin_contact,
                device_mount,
                device_property,
                user,
            ]
        )
        db.session.commit()

        payload = {
            "data": {
                "type": "datastream_link",
                "attributes": {
                    "datasource_id": "1",
                    "thing_id": "2",
                    "datastream_id": "3",
                    "tsm_endpoint": "somewhere",
                },
                "relationships": {
                    "device_mount_action": {
                        "data": {
                            "id": device_mount.id,
                            "type": "device_mount_action",
                        }
                    },
                    "device_property": {
                        "data": {
                            "id": device_property.id,
                            "type": "device_property",
                        }
                    },
                },
            }
        }
        with self.run_requests_as(user):
            with self.client:
                response = self.client.post(
                    self.url,
                    data=json.dumps(payload),
                    content_type="application/vnd.api+json",
                )
        self.assertEqual(response.status_code, 201)

    def test_get_internal_datastream_link_details(self):
        """Ensure that we get details of internal datastream links only for authenticate users."""
        configuration1 = create_a_test_configuration(
            public=False,
            internal=True,
        )
        userinfo = generate_userinfo_data()
        device = Device(
            short_name=fake.linux_processor(),
            manufacturer_name=fake.company(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        begin_contact = Contact(
            given_name=userinfo["given_name"],
            family_name=userinfo["family_name"],
            email=userinfo["email"],
        )
        begin_date = fake.future_datetime()
        end_date = begin_date + datetime.timedelta(days=2)
        device_mount1 = DeviceMountAction(
            begin_date=begin_date,
            end_date=end_date,
            configuration=configuration1,
            begin_contact=begin_contact,
            device=device,
        )
        device_property = DeviceProperty(
            label="device property1",
            property_name="device_property1",
            device=device,
        )
        datastream_link1 = DatastreamLink(
            device_property=device_property,
            device_mount_action=device_mount1,
            datasource_id="1",
            thing_id="1",
            datastream_id="1",
        )
        db.session.add_all(
            [
                device,
                begin_contact,
                device_mount1,
                device_property,
                datastream_link1,
            ]
        )
        db.session.commit()

        with self.client:
            response = self.client.get(
                f"{self.url}/{datastream_link1.id}",
                content_type="application/vnd.api+json",
            )
            self.assertEqual(response.status_code, 401)

        # With a valid JWT
        access_headers = create_token()
        with self.client:
            response = self.client.get(
                f"{self.url}/{datastream_link1.id}",
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
        self.assertEqual(response.status_code, 200)

    def test_patch_anonymous(self):
        """Ensure we are not allowed to patch a datastream link without login."""
        configuration1 = create_a_test_configuration(
            public=False,
            internal=True,
        )
        userinfo = generate_userinfo_data()
        device = Device(
            short_name=fake.linux_processor(),
            manufacturer_name=fake.company(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        begin_contact = Contact(
            given_name=userinfo["given_name"],
            family_name=userinfo["family_name"],
            email=userinfo["email"],
        )
        begin_date = fake.future_datetime()
        end_date = begin_date + datetime.timedelta(days=2)
        device_mount1 = DeviceMountAction(
            begin_date=begin_date,
            end_date=end_date,
            configuration=configuration1,
            begin_contact=begin_contact,
            device=device,
        )
        device_property = DeviceProperty(
            label="device property1",
            property_name="device_property1",
            device=device,
        )
        datastream_link1 = DatastreamLink(
            device_property=device_property,
            device_mount_action=device_mount1,
            datasource_id="1",
            thing_id="1",
            datastream_id="1",
        )
        db.session.add_all(
            [
                device,
                begin_contact,
                device_mount1,
                device_property,
                datastream_link1,
            ]
        )
        db.session.commit()

        payload = {
            "data": {
                "type": "datastream_link",
                "id": datastream_link1.id,
                "attributes": {
                    "datastream_id": "different",
                },
            }
        }

        with self.client:
            response = self.client.patch(
                f"{self.url}/{datastream_link1.id}",
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 401)

    def test_patch_normal_user_not_in_group(self):
        """Ensure we are not allowed to patch a datastream link without group membership."""
        configuration1 = create_a_test_configuration(
            public=False,
            internal=True,
            cfg_permission_group="123",
        )
        userinfo = generate_userinfo_data()
        device = Device(
            short_name=fake.linux_processor(),
            manufacturer_name=fake.company(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        begin_contact = Contact(
            given_name=userinfo["given_name"],
            family_name=userinfo["family_name"],
            email=userinfo["email"],
        )
        user = User(
            subject=begin_contact.email,
            contact=begin_contact,
        )
        begin_date = fake.future_datetime()
        end_date = begin_date + datetime.timedelta(days=2)
        device_mount1 = DeviceMountAction(
            begin_date=begin_date,
            end_date=end_date,
            configuration=configuration1,
            begin_contact=begin_contact,
            device=device,
        )
        device_property = DeviceProperty(
            label="device property1",
            property_name="device_property1",
            device=device,
        )
        datastream_link1 = DatastreamLink(
            device_property=device_property,
            device_mount_action=device_mount1,
            datasource_id="1",
            thing_id="1",
            datastream_id="1",
        )
        db.session.add_all(
            [
                device,
                begin_contact,
                device_mount1,
                device_property,
                datastream_link1,
            ]
        )
        db.session.commit()

        payload = {
            "data": {
                "type": "datastream_link",
                "id": datastream_link1.id,
                "attributes": {
                    "datastream_id": "different",
                },
            }
        }

        with self.run_requests_as(user):
            with patch.object(idl, "get_all_permission_groups_for_a_user") as mock:
                mock.return_value = UserAccount(
                    id="123",
                    username=user.subject,
                    administrated_permission_groups=[],
                    membered_permission_groups=[],
                )
                with self.client:
                    response = self.client.patch(
                        f"{self.url}/{datastream_link1.id}",
                        data=json.dumps(payload),
                        content_type="application/vnd.api+json",
                    )
        self.assertEqual(response.status_code, 403)

    def test_patch_normal_user_in_group(self):
        """Ensure we are allowed to patch a datastream link with group membership."""
        configuration1 = create_a_test_configuration(
            public=False,
            internal=True,
            cfg_permission_group="123",
        )
        userinfo = generate_userinfo_data()
        device = Device(
            short_name=fake.linux_processor(),
            manufacturer_name=fake.company(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        begin_contact = Contact(
            given_name=userinfo["given_name"],
            family_name=userinfo["family_name"],
            email=userinfo["email"],
        )
        user = User(
            subject=begin_contact.email,
            contact=begin_contact,
        )
        begin_date = fake.future_datetime()
        end_date = begin_date + datetime.timedelta(days=2)
        device_mount1 = DeviceMountAction(
            begin_date=begin_date,
            end_date=end_date,
            configuration=configuration1,
            begin_contact=begin_contact,
            device=device,
        )
        device_property = DeviceProperty(
            label="device property1",
            property_name="device_property1",
            device=device,
        )
        datastream_link1 = DatastreamLink(
            device_property=device_property,
            device_mount_action=device_mount1,
            datasource_id="1",
            thing_id="1",
            datastream_id="1",
        )
        db.session.add_all(
            [
                device,
                begin_contact,
                device_mount1,
                device_property,
                datastream_link1,
            ]
        )
        db.session.commit()

        payload = {
            "data": {
                "type": "datastream_link",
                "id": datastream_link1.id,
                "attributes": {
                    "datastream_id": "different",
                },
            }
        }

        with self.run_requests_as(user):
            with patch.object(idl, "get_all_permission_groups_for_a_user") as mock:
                mock.return_value = UserAccount(
                    id="123",
                    username=user.subject,
                    administrated_permission_groups=[],
                    membered_permission_groups=[configuration1.cfg_permission_group],
                )
                with self.client:
                    response = self.client.patch(
                        f"{self.url}/{datastream_link1.id}",
                        data=json.dumps(payload),
                        content_type="application/vnd.api+json",
                    )
        self.assertEqual(response.status_code, 200)

    def test_patch_super_user(self):
        """Ensure we are allowed to patch a datastream link as super user."""
        configuration1 = create_a_test_configuration(
            public=False,
            internal=True,
            cfg_permission_group="123",
        )
        userinfo = generate_userinfo_data()
        device = Device(
            short_name=fake.linux_processor(),
            manufacturer_name=fake.company(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        begin_contact = Contact(
            given_name=userinfo["given_name"],
            family_name=userinfo["family_name"],
            email=userinfo["email"],
        )
        other_contact = Contact(
            given_name="other", family_name="contact", email="other@contact.xyz"
        )
        user = User(subject=other_contact.email, contact=other_contact)
        super_user = User(
            subject=begin_contact.email,
            contact=begin_contact,
            is_superuser=True,
        )
        begin_date = fake.future_datetime()
        end_date = begin_date + datetime.timedelta(days=2)
        device_mount1 = DeviceMountAction(
            begin_date=begin_date,
            end_date=end_date,
            configuration=configuration1,
            begin_contact=begin_contact,
            device=device,
        )
        device_property = DeviceProperty(
            label="device property1",
            property_name="device_property1",
            device=device,
        )
        datastream_link1 = DatastreamLink(
            device_property=device_property,
            device_mount_action=device_mount1,
            datasource_id="1",
            thing_id="1",
            datastream_id="1",
            created_by=user,
        )
        db.session.add_all(
            [
                device,
                begin_contact,
                other_contact,
                device_mount1,
                device_property,
                datastream_link1,
                user,
                super_user,
            ]
        )
        db.session.commit()

        payload = {
            "data": {
                "type": "datastream_link",
                "id": datastream_link1.id,
                "attributes": {
                    "datastream_id": "different",
                },
            }
        }

        # To check the updated_at field
        time.sleep(1)

        with self.run_requests_as(super_user):
            with self.client:
                response = self.client.patch(
                    f"{self.url}/{datastream_link1.id}",
                    data=json.dumps(payload),
                    content_type="application/vnd.api+json",
                )
        self.assertEqual(response.status_code, 200)

        reloaded_datastream_link = db.session.query(DatastreamLink).get(
            datastream_link1.id
        )

        self.assertEqual(
            reloaded_datastream_link.updated_at.year, datetime.datetime.now().year
        )
        self.assertNotEqual(
            reloaded_datastream_link.updated_at, reloaded_datastream_link.created_at
        )

        self.assertEqual(reloaded_datastream_link.updated_by, super_user)
        self.assertNotEqual(
            reloaded_datastream_link.updated_by, reloaded_datastream_link.created_by
        )

        reloaded_configuration = db.session.query(Configuration).get(configuration1.id)
        self.assertEqual(
            reloaded_configuration.update_description, "update;datastream link"
        )

    def test_patch_archived_configuration(self):
        """Ensure we are not allowed to patch a datastream link for an archived configuration."""
        configuration1 = create_a_test_configuration(
            public=False,
            internal=True,
        )
        configuration1.archived = True
        userinfo = generate_userinfo_data()
        device = Device(
            short_name=fake.linux_processor(),
            manufacturer_name=fake.company(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        begin_contact = Contact(
            given_name=userinfo["given_name"],
            family_name=userinfo["family_name"],
            email=userinfo["email"],
        )
        user = User(
            subject=begin_contact.email,
            contact=begin_contact,
            is_superuser=True,
        )
        begin_date = fake.future_datetime()
        end_date = begin_date + datetime.timedelta(days=2)
        device_mount1 = DeviceMountAction(
            begin_date=begin_date,
            end_date=end_date,
            configuration=configuration1,
            begin_contact=begin_contact,
            device=device,
        )
        device_property = DeviceProperty(
            label="device property1",
            property_name="device_property1",
            device=device,
        )
        datastream_link1 = DatastreamLink(
            device_property=device_property,
            device_mount_action=device_mount1,
            datasource_id="1",
            thing_id="1",
            datastream_id="1",
        )
        db.session.add_all(
            [
                configuration1,
                device,
                begin_contact,
                device_mount1,
                device_property,
                datastream_link1,
            ]
        )
        db.session.commit()

        payload = {
            "data": {
                "type": "datastream_link",
                "id": datastream_link1.id,
                "attributes": {
                    "datastream_id": "different",
                },
            }
        }

        with self.run_requests_as(user):
            with self.client:
                response = self.client.patch(
                    f"{self.url}/{datastream_link1.id}",
                    data=json.dumps(payload),
                    content_type="application/vnd.api+json",
                )
        self.assertEqual(response.status_code, 403)

    def test_delete_anonymous(self):
        """Ensure we are not allowed to delete a datastream link without login."""
        configuration1 = create_a_test_configuration(
            public=False,
            internal=True,
        )
        userinfo = generate_userinfo_data()
        device = Device(
            short_name=fake.linux_processor(),
            manufacturer_name=fake.company(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        begin_contact = Contact(
            given_name=userinfo["given_name"],
            family_name=userinfo["family_name"],
            email=userinfo["email"],
        )
        begin_date = fake.future_datetime()
        end_date = begin_date + datetime.timedelta(days=2)
        device_mount1 = DeviceMountAction(
            begin_date=begin_date,
            end_date=end_date,
            configuration=configuration1,
            begin_contact=begin_contact,
            device=device,
        )
        device_property = DeviceProperty(
            label="device property1",
            property_name="device_property1",
            device=device,
        )
        datastream_link1 = DatastreamLink(
            device_property=device_property,
            device_mount_action=device_mount1,
            datasource_id="1",
            thing_id="1",
            datastream_id="1",
        )
        db.session.add_all(
            [
                device,
                begin_contact,
                device_mount1,
                device_property,
                datastream_link1,
            ]
        )
        db.session.commit()

        with self.client:
            response = self.client.delete(
                f"{self.url}/{datastream_link1.id}",
            )
        self.assertEqual(response.status_code, 401)

    def test_delete_normal_user_not_in_group(self):
        """Ensure we are not allowed to delete a datastream link without group membership."""
        configuration1 = create_a_test_configuration(
            public=False,
            internal=True,
            cfg_permission_group="123",
        )
        userinfo = generate_userinfo_data()
        device = Device(
            short_name=fake.linux_processor(),
            manufacturer_name=fake.company(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        begin_contact = Contact(
            given_name=userinfo["given_name"],
            family_name=userinfo["family_name"],
            email=userinfo["email"],
        )
        user = User(
            subject=begin_contact.email,
            contact=begin_contact,
        )
        begin_date = fake.future_datetime()
        end_date = begin_date + datetime.timedelta(days=2)
        device_mount1 = DeviceMountAction(
            begin_date=begin_date,
            end_date=end_date,
            configuration=configuration1,
            begin_contact=begin_contact,
            device=device,
        )
        device_property = DeviceProperty(
            label="device property1",
            property_name="device_property1",
            device=device,
        )
        datastream_link1 = DatastreamLink(
            device_property=device_property,
            device_mount_action=device_mount1,
            datasource_id="1",
            thing_id="1",
            datastream_id="1",
        )
        db.session.add_all(
            [
                device,
                begin_contact,
                device_mount1,
                device_property,
                datastream_link1,
            ]
        )
        db.session.commit()

        with self.run_requests_as(user):
            with patch.object(idl, "get_all_permission_groups_for_a_user") as mock:
                mock.return_value = UserAccount(
                    id="123",
                    username=user.subject,
                    administrated_permission_groups=[],
                    membered_permission_groups=[],
                )
                with self.client:
                    response = self.client.delete(
                        f"{self.url}/{datastream_link1.id}",
                    )
        self.assertEqual(response.status_code, 403)

    def test_delete_normal_user_in_group(self):
        """Ensure we are allowed to delete a datastream link with group membership."""
        configuration1 = create_a_test_configuration(
            public=False,
            internal=True,
            cfg_permission_group="123",
        )
        userinfo = generate_userinfo_data()
        device = Device(
            short_name=fake.linux_processor(),
            manufacturer_name=fake.company(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        begin_contact = Contact(
            given_name=userinfo["given_name"],
            family_name=userinfo["family_name"],
            email=userinfo["email"],
        )
        user = User(
            subject=begin_contact.email,
            contact=begin_contact,
        )
        begin_date = fake.future_datetime()
        end_date = begin_date + datetime.timedelta(days=2)
        device_mount1 = DeviceMountAction(
            begin_date=begin_date,
            end_date=end_date,
            configuration=configuration1,
            begin_contact=begin_contact,
            device=device,
        )
        device_property = DeviceProperty(
            label="device property1",
            property_name="device_property1",
            device=device,
        )
        datastream_link1 = DatastreamLink(
            device_property=device_property,
            device_mount_action=device_mount1,
            datasource_id="1",
            thing_id="1",
            datastream_id="1",
        )
        db.session.add_all(
            [
                device,
                begin_contact,
                device_mount1,
                device_property,
                datastream_link1,
            ]
        )
        db.session.commit()

        with self.run_requests_as(user):
            with patch.object(idl, "get_all_permission_groups_for_a_user") as mock:
                mock.return_value = UserAccount(
                    id="123",
                    username=user.subject,
                    administrated_permission_groups=[],
                    membered_permission_groups=[configuration1.cfg_permission_group],
                )
                with self.client:
                    response = self.client.delete(
                        f"{self.url}/{datastream_link1.id}",
                    )
        self.assertEqual(response.status_code, 200)

    def test_delete_super_user(self):
        """Ensure we are allowed to delete a datastream link as super user."""
        configuration1 = create_a_test_configuration(
            public=False,
            internal=True,
            cfg_permission_group="123",
        )
        userinfo = generate_userinfo_data()
        device = Device(
            short_name=fake.linux_processor(),
            manufacturer_name=fake.company(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        begin_contact = Contact(
            given_name=userinfo["given_name"],
            family_name=userinfo["family_name"],
            email=userinfo["email"],
        )
        other_contact = Contact(
            given_name="other", family_name="contact", email="other@contact.xyz"
        )
        user = User(subject=other_contact.email, contact=other_contact)
        super_user = User(
            subject=begin_contact.email,
            contact=begin_contact,
            is_superuser=True,
        )
        begin_date = fake.future_datetime()
        end_date = begin_date + datetime.timedelta(days=2)
        device_mount1 = DeviceMountAction(
            begin_date=begin_date,
            end_date=end_date,
            configuration=configuration1,
            begin_contact=begin_contact,
            device=device,
        )
        device_property = DeviceProperty(
            label="device property1",
            property_name="device_property1",
            device=device,
        )
        datastream_link1 = DatastreamLink(
            device_property=device_property,
            device_mount_action=device_mount1,
            datasource_id="1",
            thing_id="1",
            datastream_id="1",
            created_by=user,
        )
        db.session.add_all(
            [
                device,
                begin_contact,
                other_contact,
                device_mount1,
                device_property,
                datastream_link1,
                user,
                super_user,
            ]
        )
        db.session.commit()

        with self.run_requests_as(super_user):
            with self.client:
                response = self.client.delete(
                    f"{self.url}/{datastream_link1.id}",
                )
        self.assertEqual(response.status_code, 200)

        reloaded_configuration = db.session.query(Configuration).get(configuration1.id)
        self.assertEqual(
            reloaded_configuration.update_description, "delete;datastream link"
        )

    def test_delete_archived_configuration(self):
        """Ensure we are not allowed to delete a datastream link for an archived configuration."""
        configuration1 = create_a_test_configuration(
            public=False,
            internal=True,
        )
        configuration1.archived = True
        userinfo = generate_userinfo_data()
        device = Device(
            short_name=fake.linux_processor(),
            manufacturer_name=fake.company(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        begin_contact = Contact(
            given_name=userinfo["given_name"],
            family_name=userinfo["family_name"],
            email=userinfo["email"],
        )
        user = User(
            subject=begin_contact.email,
            contact=begin_contact,
            is_superuser=True,
        )
        begin_date = fake.future_datetime()
        end_date = begin_date + datetime.timedelta(days=2)
        device_mount1 = DeviceMountAction(
            begin_date=begin_date,
            end_date=end_date,
            configuration=configuration1,
            begin_contact=begin_contact,
            device=device,
        )
        device_property = DeviceProperty(
            label="device property1",
            property_name="device_property1",
            device=device,
        )
        datastream_link1 = DatastreamLink(
            device_property=device_property,
            device_mount_action=device_mount1,
            datasource_id="1",
            thing_id="1",
            datastream_id="1",
        )
        db.session.add_all(
            [
                configuration1,
                device,
                begin_contact,
                device_mount1,
                device_property,
                datastream_link1,
            ]
        )
        db.session.commit()

        with self.run_requests_as(user):
            with self.client:
                response = self.client.delete(
                    f"{self.url}/{datastream_link1.id}",
                )
        self.assertEqual(response.status_code, 403)

    def test_patch_to_non_editable_device(self):
        """Ensure we can't update to a device we can't edit."""
        configuration = create_a_test_configuration(
            public=False,
            internal=True,
        )
        device1 = Device(
            short_name=fake.linux_processor(),
            manufacturer_name=fake.company(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        device1.group_ids = ["1"]
        device2 = Device(
            short_name=fake.linux_processor(),
            manufacturer_name=fake.company(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        device2.group_ids = ["2"]
        begin_contact = Contact(
            given_name="first",
            family_name="contact",
            email="first.contact@localhost",
        )
        user = User(
            subject=begin_contact.email,
            contact=begin_contact,
        )
        begin_date = fake.future_datetime()
        end_date = begin_date + datetime.timedelta(days=2)
        device_mount1 = DeviceMountAction(
            begin_date=begin_date,
            end_date=end_date,
            configuration=configuration,
            begin_contact=begin_contact,
            device=device1,
        )
        device_mount2 = DeviceMountAction(
            begin_date=begin_date,
            end_date=end_date,
            configuration=configuration,
            begin_contact=begin_contact,
            device=device2,
        )
        device_property1 = DeviceProperty(
            label="device property1",
            property_name="device_property1",
            device=device1,
        )
        device_property2 = DeviceProperty(
            label="device property2",
            property_name="device_property2",
            device=device2,
        )
        datastream_link = DatastreamLink(
            device_property=device_property1,
            device_mount_action=device_mount1,
            datasource_id="1",
            thing_id="1",
            datastream_id="1",
        )
        db.session.add_all(
            [
                configuration,
                device1,
                device2,
                begin_contact,
                user,
                device_mount1,
                device_mount2,
                device_property1,
                device_property2,
                datastream_link,
            ]
        )
        db.session.commit()

        payload = {
            "data": {
                "type": "datastream_link",
                "id": datastream_link.id,
                "attributes": {},
                "relationships": {
                    # We try to switch here to another device for
                    # which we have no edit permissions.
                    "device_mount_action": {
                        "data": {
                            "type": "device_mount_action",
                            "id": device_mount2.id,
                        }
                    },
                    "device_property": {
                        "data": {
                            "type": "device_property",
                            "id": device_property2.id,
                        }
                    },
                },
            }
        }

        with self.run_requests_as(user):
            with patch.object(idl, "get_all_permission_groups_for_a_user") as mock:
                mock.return_value = UserAccount(
                    id="123",
                    username=user.subject,
                    administrated_permission_groups=[],
                    membered_permission_groups=[*device1.group_ids],
                )
                with self.client:
                    response = self.client.patch(
                        f"{self.url}/{datastream_link.id}",
                        data=json.dumps(payload),
                        content_type="application/vnd.api+json",
                    )
        self.assertEqual(response.status_code, 403)
