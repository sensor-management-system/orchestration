#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0


"""Tests for the datastream links."""

import datetime
import json

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
from project.tests.base import (
    BaseTestCase,
    create_token,
    fake,
    generate_userinfo_data,
    query_result_to_list,
)
from project.tests.models.test_configurations_model import generate_configuration_model


class TestDatastreamLinks(BaseTestCase):
    """Test class for the datastream links."""

    url = base_url + "/datastream-links"

    def test_get_empty(self):
        """Ensure we can get an empty list if there are no data."""
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json["data"], [])

    def test_post_datastream_link(self):
        """Create datastream link."""
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
        configuration = generate_configuration_model()
        configuration.cfg_permission_group = "123"
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
                device_property,
                begin_contact,
                configuration,
                device_mount,
                user,
            ]
        )
        db.session.commit()
        payload = {
            "data": {
                "type": "datastream_link",
                "relationships": {
                    "device_property": {
                        "data": {"type": "device_property", "id": device_property.id}
                    },
                    "device_mount_action": {
                        "data": {"type": "device_mount_action", "id": device_mount.id}
                    },
                },
                "attributes": {
                    "datastream_id": "22",
                    "datastream_name": "AirTemp+22m",
                    "thing_id": "1",
                    "thing_name": "Station1",
                    "tsm_endpoint": "foo",
                    "datasource_id": "1",
                    "datasource_name": "DB1",
                    "begin_date": str(begin_date),
                    "end_date": str(end_date),
                },
            }
        }

        with self.run_requests_as(user):
            with self.client:
                # You may want to look up self.add_object in the BaseTestCase
                # and compare if something doesn't work anymore
                response = self.client.post(
                    self.url,
                    data=json.dumps(payload),
                    content_type="application/vnd.api+json",
                )

        # We expect that it worked and that we have a new entry
        self.assertEqual(response.status_code, 201)

        # And we want to inspect our datastream links
        datastream_links = query_result_to_list(db.session.query(DatastreamLink))

        # We now have one datastream link
        self.assertEqual(len(datastream_links), 1)

        # And it is as we specified it
        datastream_link = datastream_links[0]
        self.assertEqual(datastream_link.thing_id, "1")
        self.assertEqual(datastream_link.thing_name, "Station1")
        self.assertEqual(datastream_link.datastream_id, "22")
        self.assertEqual(datastream_link.datastream_name, "AirTemp+22m")
        self.assertEqual(datastream_link.datasource_id, "1")
        self.assertEqual(datastream_link.datasource_name, "DB1")
        self.assertEqual(datastream_link.device_property_id, device_property.id)
        self.assertEqual(datastream_link.device_mount_action_id, device_mount.id)
        self.assertEqual(datastream_link.tsm_endpoint, "foo")
        self.assertEqual(datastream_link.created_by, user)
        self.assertEqual(datastream_link.created_at.year, datetime.datetime.now().year)
        # And we also want to make sure that we fill the update description of the configuration

        reloaded_configuration = db.session.query(Configuration).get(configuration.id)
        self.assertEqual(
            reloaded_configuration.update_description, "create;datastream link"
        )

    def test_post_datastream_link_api_missing_mount(self):
        """Ensure that we don't add a datastream link with missing device mount action."""
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
        configuration = generate_configuration_model()
        begin_date = fake.future_datetime()
        end_date = begin_date + datetime.timedelta(days=2)
        device_property = DeviceProperty(
            label="device property1",
            property_name="device_property1",
            device=device,
        )

        db.session.add_all(
            [
                device,
                device_property,
                begin_contact,
                configuration,
            ]
        )
        db.session.commit()
        payload = {
            "data": {
                "type": "datastream_link",
                "relationships": {
                    "device_property": {
                        "data": {"type": "device_property", "id": device_property.id}
                    },
                    "device_mount_action": {
                        "data": None,
                    },
                },
                "attributes": {
                    "datastream_id": "22",
                    "datastream_name": "AirTemp+22m",
                    "thing_id": "1",
                    "thing_name": "Station1",
                    "tsm_endpoint": "foo",
                    "datasource_id": "1",
                    "datasource_name": "DB1",
                    "begin_date": str(begin_date),
                    "end_date": str(end_date),
                },
            }
        }

        with self.client:
            # You may want to look up self.add_object in the BaseTestCase
            # and compare if something doesn't work anymore
            response = self.client.post(
                self.url,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
                headers=create_token(),
            )

        self.assertEqual(response.status_code, 422)

    def test_post_datastream_link_with_device_mismatch(self):
        """Ensure we can't add a link if device doesn't match between mount & property."""
        configuration = generate_configuration_model()
        configuration.public = True
        configuration.internal = False
        configuration.cfg_permission_group = "123"
        device1 = Device(
            short_name=fake.linux_processor(),
            manufacturer_name=fake.company(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        device2 = Device(
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
            device=device1,
        )
        device_property = DeviceProperty(
            label="device property1",
            property_name="device_property1",
            device=device2,
        )
        db.session.add_all(
            [
                device1,
                device2,
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
        self.assertEqual(response.status_code, 409)

    def test_get_detail_missing(self):
        """Test that we return a 404 for datastream details that aren't there."""
        with self.client:
            response = self.client.get(f"{self.url}/1234567")
        self.assertEqual(response.status_code, 404)

    def test_patch_datastream_link_with_device_mismatch(self):
        """Ensure we can't update a link if device doesn't match between mount & property."""
        configuration = generate_configuration_model()
        configuration.public = True
        configuration.internal = False
        configuration.cfg_permission_group = "123"
        device1 = Device(
            short_name=fake.linux_processor(),
            manufacturer_name=fake.company(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        device2 = Device(
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
            device=device1,
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
            datasource_id="1",
            thing_id="2",
            datastream_id="3",
            tsm_endpoint="somewhere",
            device_mount_action=device_mount,
            device_property=device_property1,
        )
        db.session.add_all(
            [
                device1,
                device2,
                begin_contact,
                datastream_link,
                device_mount,
                device_property1,
                device_property2,
                user,
            ]
        )
        db.session.commit()

        payload = {
            "data": {
                "type": "datastream_link",
                "id": datastream_link.id,
                "attributes": {},
                "relationships": {
                    "device_property": {
                        "data": {
                            "id": device_property2.id,
                            "type": "device_property",
                        }
                    },
                },
            }
        }
        with self.run_requests_as(user):
            with self.client:
                response = self.client.patch(
                    f"{self.url}/{datastream_link.id}",
                    data=json.dumps(payload),
                    content_type="application/vnd.api+json",
                )
        self.assertEqual(response.status_code, 409)

    def test_get_empty_with_configuration(self):
        """Ensure we can get an empty list for an configuration, if there are no data."""
        configuration = Configuration(
            label="c1", is_public=True, is_internal=False, cfg_permission_group="123"
        )
        db.session.add(configuration)
        db.session.commit()
        url = (
            f"{base_url}/configurations/{configuration.id}/datastream-links"
            + "?include=device_mount_action,device_mount_action.device,device_property"
        )
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json["data"], [])

    def test_get_elements_by_configuration(self):
        """Ensure we can get a filtered list for an configuration."""
        configuration1 = Configuration(
            label="c1", is_public=True, is_internal=False, cfg_permission_group="123"
        )
        configuration2 = Configuration(
            label="c2", is_public=True, is_internal=False, cfg_permission_group="123"
        )
        device1 = Device(short_name="d1", is_public=True, is_internal=False)
        device2 = Device(short_name="d2", is_public=True, is_internal=False)
        begin_contact = Contact(
            given_name="begin", family_name="contact", email="begin.contact@localhost"
        )
        mount1 = DeviceMountAction(
            configuration=configuration1,
            device=device1,
            begin_contact=begin_contact,
            begin_date=datetime.datetime.now(),
        )
        mount2 = DeviceMountAction(
            configuration=configuration2,
            device=device2,
            begin_contact=begin_contact,
            begin_date=datetime.datetime.now(),
        )
        property1 = DeviceProperty(device=device1, property_name="prop1")
        property2 = DeviceProperty(device=device2, property_name="prop2")

        linking1 = DatastreamLink(
            device_mount_action=mount1,
            device_property=property1,
            tsm_endpoint="tsm1",
            datasource_id="1",
            thing_id="1",
            datastream_id="1",
        )
        linking2 = DatastreamLink(
            device_mount_action=mount2,
            device_property=property2,
            tsm_endpoint="tsm2",
            datasource_id="2",
            thing_id="2",
            datastream_id="2",
        )
        db.session.add_all(
            [
                configuration1,
                configuration2,
                device1,
                device2,
                begin_contact,
                mount1,
                mount2,
                property1,
                property2,
                linking1,
                linking2,
            ]
        )
        db.session.commit()
        url1 = f"{base_url}/configurations/{configuration1.id}/datastream-links"
        url2 = f"{base_url}/configurations/{configuration2.id}/datastream-links"
        resp1 = self.client.get(url1)
        resp2 = self.client.get(url2)
        self.assertEqual(resp1.status_code, 200)
        self.assertEqual(resp2.status_code, 200)
        self.assertEqual(len(resp1.json["data"]), 1)
        self.assertEqual(len(resp2.json["data"]), 1)
        self.assertEqual(resp1.json["data"][0]["id"], str(linking1.id))
        self.assertEqual(resp2.json["data"][0]["id"], str(linking2.id))
