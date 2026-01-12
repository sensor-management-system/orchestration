# SPDX-FileCopyrightText: 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Tests for the permission handling for datastream_link resources."""

import datetime
import json
import time

from project import base_url
from project.api.models import (
    Configuration,
    Contact,
    DatastreamLink,
    Device,
    DeviceMountAction,
    DeviceProperty,
    PermissionGroup,
    PermissionGroupMembership,
    TsmEndpoint,
    User,
)
from project.api.models.base_model import db
from project.tests.base import BaseTestCase, create_token, fake, generate_userinfo_data
from project.tests.permissions import create_a_test_configuration


class TestDatastreamLinks(BaseTestCase):
    """Test DatastreamLink."""

    url = base_url + "/datastream-links"

    def setUp(self):
        """Set stuff up for the tests."""
        super().setUp()
        normal_contact = Contact(
            given_name="normal", family_name="user", email="normal.user@localhost"
        )
        self.normal_user = User(subject=normal_contact.email, contact=normal_contact)
        contact = Contact(
            given_name="super", family_name="user", email="super.user@localhost"
        )
        self.super_user = User(
            subject=contact.email, contact=contact, is_superuser=True
        )

        self.permission_group = PermissionGroup(name="test", entitlement="test")
        self.other_group = PermissionGroup(name="other", entitlement="other")
        self.membership = PermissionGroupMembership(
            permission_group=self.permission_group, user=self.normal_user
        )
        db.session.add_all(
            [
                contact,
                normal_contact,
                self.normal_user,
                self.super_user,
                self.permission_group,
                self.other_group,
                self.membership,
            ]
        )
        db.session.commit()

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
        tsm_endpoint = TsmEndpoint(name="XYZ", url="https://somewhere")
        datastream_link1 = DatastreamLink(
            device_property=device_property,
            device_mount_action=device_mount1,
            tsm_endpoint=tsm_endpoint,
            datasource_id="1",
            thing_id="1",
            datastream_id="1",
        )
        datastream_link2 = DatastreamLink(
            device_property=device_property,
            device_mount_action=device_mount2,
            tsm_endpoint=tsm_endpoint,
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
                tsm_endpoint,
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
        tsm_endpoint = TsmEndpoint(name="XYZ", url="https://somewhere")
        datastream_link1 = DatastreamLink(
            device_property=device_property,
            device_mount_action=device_mount1,
            tsm_endpoint=tsm_endpoint,
            datasource_id="1",
            thing_id="1",
            datastream_id="1",
        )
        datastream_link2 = DatastreamLink(
            device_property=device_property,
            device_mount_action=device_mount2,
            tsm_endpoint=tsm_endpoint,
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
                tsm_endpoint,
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
        tsm_endpoint = TsmEndpoint(name="XYZ", url="https://somewhere")
        db.session.add_all(
            [
                device,
                begin_contact,
                device_mount,
                device_property,
                tsm_endpoint,
            ]
        )
        db.session.commit()

        payload = {
            "data": {
                "type": "datastream_link",
                "attributes": {
                    "datasource_id": "123",
                    "thing_id": "456",
                    "datastream_id": "789",
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
                    "tsm_endpoint": {
                        "data": {
                            "id": tsm_endpoint.id,
                            "type": "tsm_endpoint",
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
            cfg_permission_group=str(self.permission_group.id),
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
        tsm_endpoint = TsmEndpoint(name="XYZ", url="https://somewhere")
        db.session.add_all(
            [
                device,
                begin_contact,
                device_mount,
                device_property,
                tsm_endpoint,
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
                    "tsm_endpoint": {
                        "data": {
                            "id": tsm_endpoint.id,
                            "type": "tsm_endpoint",
                        }
                    },
                },
            }
        }
        with self.run_requests_as(self.normal_user):
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
            cfg_permission_group=str(self.other_group.id),
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
        tsm_endpoint = TsmEndpoint(name="XYZ", url="https://somewhere")
        db.session.add_all(
            [
                device,
                begin_contact,
                device_mount,
                device_property,
                tsm_endpoint,
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
                    "tsm_endpoint": {
                        "data": {
                            "id": tsm_endpoint.id,
                            "type": "tsm_endpoint",
                        }
                    },
                },
            }
        }
        with self.run_requests_as(self.normal_user):
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
            cfg_permission_group=str(self.permission_group.id),
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
        tsm_endpoint = TsmEndpoint(name="XYZ", url="https://somewhere")
        db.session.add_all(
            [
                device,
                begin_contact,
                device_mount,
                device_property,
                tsm_endpoint,
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
                    "tsm_endpoint": {
                        "data": {
                            "id": tsm_endpoint.id,
                            "type": "tsm_endpoint",
                        }
                    },
                },
            }
        }
        with self.run_requests_as(self.normal_user):
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
            cfg_permission_group=str(self.other_group.id),
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
        tsm_endpoint = TsmEndpoint(name="XYZ", url="https://somewhere")
        db.session.add_all(
            [
                device,
                begin_contact,
                device_mount,
                device_property,
                tsm_endpoint,
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
                    "tsm_endpoint": {
                        "data": {
                            "id": tsm_endpoint.id,
                            "type": "tsm_endpoint",
                        }
                    },
                },
            }
        }
        with self.run_requests_as(self.super_user):
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
        tsm_endpoint = TsmEndpoint(name="XYZ", url="https://somewhere")
        datastream_link1 = DatastreamLink(
            device_property=device_property,
            device_mount_action=device_mount1,
            tsm_endpoint=tsm_endpoint,
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
                tsm_endpoint,
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
        tsm_endpoint = TsmEndpoint(name="XYZ", url="https://somewhere")
        datastream_link1 = DatastreamLink(
            device_property=device_property,
            device_mount_action=device_mount1,
            tsm_endpoint=tsm_endpoint,
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
                tsm_endpoint,
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
            cfg_permission_group=str(self.other_group.id),
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
        tsm_endpoint = TsmEndpoint(name="XYZ", url="https://somewhere")
        datastream_link1 = DatastreamLink(
            device_property=device_property,
            device_mount_action=device_mount1,
            tsm_endpoint=tsm_endpoint,
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
                tsm_endpoint,
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

        with self.run_requests_as(self.normal_user):
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
            cfg_permission_group=str(self.permission_group.id),
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
        tsm_endpoint = TsmEndpoint(name="XYZ", url="https://somewhere")
        datastream_link1 = DatastreamLink(
            device_property=device_property,
            device_mount_action=device_mount1,
            tsm_endpoint=tsm_endpoint,
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
                tsm_endpoint,
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

        with self.run_requests_as(self.normal_user):
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
            cfg_permission_group=str(self.other_group.id),
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
        tsm_endpoint = TsmEndpoint(name="XYZ", url="https://somewhere")
        datastream_link1 = DatastreamLink(
            device_property=device_property,
            device_mount_action=device_mount1,
            tsm_endpoint=tsm_endpoint,
            datasource_id="1",
            thing_id="1",
            datastream_id="1",
            created_by=self.normal_user,
        )
        db.session.add_all(
            [
                device,
                begin_contact,
                other_contact,
                device_mount1,
                device_property,
                datastream_link1,
                tsm_endpoint,
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

        with self.run_requests_as(self.super_user):
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

        self.assertEqual(reloaded_datastream_link.updated_by, self.super_user)
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
        tsm_endpoint = TsmEndpoint(name="XYZ", url="https://somewhere")
        datastream_link1 = DatastreamLink(
            device_property=device_property,
            device_mount_action=device_mount1,
            tsm_endpoint=tsm_endpoint,
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
                tsm_endpoint,
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

        with self.run_requests_as(self.super_user):
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
        tsm_endpoint = TsmEndpoint(name="XYZ", url="https://somewhere")
        datastream_link1 = DatastreamLink(
            device_property=device_property,
            device_mount_action=device_mount1,
            tsm_endpoint=tsm_endpoint,
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
                tsm_endpoint,
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
            cfg_permission_group=str(self.other_group.id),
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
        tsm_endpoint = TsmEndpoint(name="XYZ", url="https://somewhere")
        datastream_link1 = DatastreamLink(
            device_property=device_property,
            device_mount_action=device_mount1,
            tsm_endpoint=tsm_endpoint,
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
                tsm_endpoint,
            ]
        )
        db.session.commit()

        with self.run_requests_as(self.normal_user):
            response = self.client.delete(
                f"{self.url}/{datastream_link1.id}",
            )
        self.assertEqual(response.status_code, 403)

    def test_delete_normal_user_in_group(self):
        """Ensure we are allowed to delete a datastream link with group membership."""
        configuration1 = create_a_test_configuration(
            public=False,
            internal=True,
            cfg_permission_group=str(self.permission_group.id),
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
        tsm_endpoint = TsmEndpoint(name="XYZ", url="https://somewhere")
        datastream_link1 = DatastreamLink(
            device_property=device_property,
            device_mount_action=device_mount1,
            tsm_endpoint=tsm_endpoint,
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
                tsm_endpoint,
            ]
        )
        db.session.commit()

        with self.run_requests_as(self.normal_user):
            response = self.client.delete(
                f"{self.url}/{datastream_link1.id}",
            )
        self.assertEqual(response.status_code, 200)

    def test_delete_super_user(self):
        """Ensure we are allowed to delete a datastream link as super user."""
        configuration1 = create_a_test_configuration(
            public=False,
            internal=True,
            cfg_permission_group=str(self.other_group.id),
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
        tsm_endpoint = TsmEndpoint(name="XYZ", url="https://somewhere")
        datastream_link1 = DatastreamLink(
            device_property=device_property,
            device_mount_action=device_mount1,
            tsm_endpoint=tsm_endpoint,
            datasource_id="1",
            thing_id="1",
            datastream_id="1",
            created_by=self.normal_user,
        )
        db.session.add_all(
            [
                device,
                begin_contact,
                other_contact,
                device_mount1,
                device_property,
                datastream_link1,
                tsm_endpoint,
            ]
        )
        db.session.commit()

        with self.run_requests_as(self.super_user):
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
        tsm_endpoint = TsmEndpoint(name="XYZ", url="https://somewhere")
        datastream_link1 = DatastreamLink(
            device_property=device_property,
            device_mount_action=device_mount1,
            tsm_endpoint=tsm_endpoint,
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
                tsm_endpoint,
            ]
        )
        db.session.commit()

        with self.run_requests_as(self.super_user):
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
        device1.group_ids = [str(self.permission_group.id)]
        device2 = Device(
            short_name=fake.linux_processor(),
            manufacturer_name=fake.company(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        device2.group_ids = [str(self.other_group.id)]
        begin_contact = Contact(
            given_name="first",
            family_name="contact",
            email="first.contact@localhost",
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
        tsm_endpoint = TsmEndpoint(name="XYZ", url="https://somewhere")
        datastream_link = DatastreamLink(
            device_property=device_property1,
            device_mount_action=device_mount1,
            tsm_endpoint=tsm_endpoint,
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
                device_mount1,
                device_mount2,
                device_property1,
                device_property2,
                datastream_link,
                tsm_endpoint,
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

        with self.run_requests_as(self.normal_user):
            response = self.client.patch(
                f"{self.url}/{datastream_link.id}",
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 403)
