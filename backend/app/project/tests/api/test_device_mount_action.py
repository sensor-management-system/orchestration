# SPDX-FileCopyrightText: 2021 - 2023
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Tests for the device mount action api."""

import datetime
import json
from unittest.mock import patch

from dateutil.relativedelta import relativedelta
from flask import current_app

from project import base_url
from project.api.models import (
    Configuration,
    Contact,
    DatastreamLink,
    Device,
    DeviceMountAction,
    DeviceProperty,
    Platform,
    PlatformMountAction,
    TsmEndpoint,
)
from project.api.models.base_model import db
from project.extensions.instances import pidinst
from project.tests.base import BaseTestCase, create_token, fake, generate_userinfo_data
from project.tests.models.test_configurations_model import generate_configuration_model
from project.tests.models.test_mount_actions_model import add_mount_device_action_model


class TestDeviceMountAction(BaseTestCase):
    """Tests for the DeviceMountAction endpoints."""

    url = base_url + "/device-mount-actions"
    object_type = "device_mount_action"

    def test_get_device_mount_action(self):
        """Ensure the GET /device_mount_actions route reachable."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        # no data yet
        self.assertEqual(response.json["data"], [])

    def test_get_device_mount_action_collection(self):
        """Test retrieve a collection of DeviceMountAction objects."""
        mount_device_action = add_mount_device_action_model()
        configuration = mount_device_action.configuration
        configuration.is_public = True
        configuration.is_internal = False
        db.session.add(configuration)
        db.session.commit()

        with self.client:
            response = self.client.get(self.url)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            mount_device_action.begin_description,
            data["data"][0]["attributes"]["begin_description"],
        )

    def test_post_device_mount_action(self):
        """Create DeviceMountAction."""
        userinfo = generate_userinfo_data()
        device = Device(
            short_name=fake.linux_processor(),
            manufacturer_name=fake.company(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        parent_platform = Platform(
            short_name="device parent platform",
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
        end_contact = Contact(
            given_name="C. " + userinfo["given_name"],
            family_name="C. " + userinfo["family_name"],
            email="c." + userinfo["email"],
        )
        configuration = generate_configuration_model()
        begin_date = fake.future_datetime()
        end_date = begin_date + datetime.timedelta(days=2)

        # And to make sure that we already have a parent platform mount
        platform_mount = PlatformMountAction(
            begin_date=begin_date,
            end_date=end_date,
            configuration=configuration,
            begin_contact=begin_contact,
            platform=parent_platform,
        )
        db.session.add_all(
            [
                device,
                parent_platform,
                begin_contact,
                end_contact,
                configuration,
                platform_mount,
            ]
        )
        db.session.commit()

        data = {
            "data": {
                "type": self.object_type,
                "attributes": {
                    "begin_description": "Test DeviceMountAction",
                    "begin_date": str(begin_date),
                    "offset_x": str(fake.coordinate()),
                    "offset_y": str(fake.coordinate()),
                    "offset_z": str(fake.coordinate()),
                    "end_description": "Test DeviceUnMountAction",
                    "end_date": str(end_date),
                },
                "relationships": {
                    "device": {"data": {"type": "device", "id": device.id}},
                    "begin_contact": {
                        "data": {"type": "contact", "id": begin_contact.id}
                    },
                    "end_contact": {"data": {"type": "contact", "id": end_contact.id}},
                    "parent_platform": {
                        "data": {"type": "platform", "id": parent_platform.id}
                    },
                    "configuration": {
                        "data": {"type": "configuration", "id": configuration.id}
                    },
                },
            }
        }
        response = super().add_object(
            url=f"{self.url}?include="
            + "device,begin_contact,end_contact,parent_platform,configuration",
            data_object=data,
            object_type=self.object_type,
        )
        result_id = response["data"]["id"]
        result_device_mount_action = (
            db.session.query(DeviceMountAction).filter_by(id=result_id).first()
        )

        msg = "create;device mount action"
        self.assertEqual(
            msg, result_device_mount_action.configuration.update_description
        )

    def test_post_device_mount_action_with_parent_device(self):
        """Create DeviceMountAction with a parent device."""
        userinfo = generate_userinfo_data()
        device = Device(
            short_name=fake.linux_processor(),
            manufacturer_name=fake.company(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        parent_device = Device(
            short_name="device parent device",
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
        end_contact = Contact(
            given_name="C. " + userinfo["given_name"],
            family_name="C. " + userinfo["family_name"],
            email="c." + userinfo["email"],
        )
        configuration = generate_configuration_model()
        begin_date = fake.future_datetime()
        end_date = begin_date + datetime.timedelta(days=2)

        # And to make sure that we already have a parent device mount
        parent_device_mount = DeviceMountAction(
            begin_date=begin_date,
            end_date=end_date,
            configuration=configuration,
            begin_contact=begin_contact,
            device=parent_device,
        )
        db.session.add_all(
            [
                device,
                parent_device,
                begin_contact,
                end_contact,
                configuration,
                parent_device_mount,
            ]
        )
        db.session.commit()

        data = {
            "data": {
                "type": self.object_type,
                "attributes": {
                    "begin_description": "Test DeviceMountAction",
                    "begin_date": str(begin_date),
                    "offset_x": str(fake.coordinate()),
                    "offset_y": str(fake.coordinate()),
                    "offset_z": str(fake.coordinate()),
                    "end_description": "Test DeviceUnMountAction",
                    "end_date": str(end_date),
                },
                "relationships": {
                    "device": {"data": {"type": "device", "id": device.id}},
                    "begin_contact": {
                        "data": {"type": "contact", "id": begin_contact.id}
                    },
                    "end_contact": {"data": {"type": "contact", "id": end_contact.id}},
                    "parent_device": {
                        "data": {"type": "device", "id": parent_device.id}
                    },
                    "configuration": {
                        "data": {"type": "configuration", "id": configuration.id}
                    },
                },
            }
        }
        response = super().add_object(
            url=f"{self.url}?include="
            + "device,begin_contact,end_contact,parent_device,configuration",
            data_object=data,
            object_type=self.object_type,
        )
        result_id = response["data"]["id"]
        result_device_mount_action = (
            db.session.query(DeviceMountAction).filter_by(id=result_id).first()
        )

        msg = "create;device mount action"
        self.assertEqual(
            msg, result_device_mount_action.configuration.update_description
        )

    def test_update_device_mount_action(self):
        """Update DeviceMountAction."""
        mount_device_action = add_mount_device_action_model()
        # We don't want to deal with the parent platform mount at the moment.
        mount_device_action.parent_platform = None
        db.session.add(mount_device_action)
        db.session.add(mount_device_action)
        mount_device_action_updated = {
            "data": {
                "type": self.object_type,
                "id": mount_device_action.id,
                "attributes": {"begin_description": "updated"},
            }
        }
        response = super().update_object(
            url=f"{self.url}/{mount_device_action.id}",
            data_object=mount_device_action_updated,
            object_type=self.object_type,
        )
        result_id = response["data"]["id"]
        result_device_mount_action = (
            db.session.query(DeviceMountAction).filter_by(id=result_id).first()
        )

        msg = "update;device mount action"
        self.assertEqual(
            msg, result_device_mount_action.configuration.update_description
        )

    def test_delete_device_mount_action(self):
        """Delete DeviceMountAction should fail without permission."""
        mount_device_action = add_mount_device_action_model()
        access_headers = create_token()
        related_configuration_id = mount_device_action.configuration.id
        # As long as there is no permission group for the configuration,
        # an authentificated user is allowed to delete the action.
        # (At least in our current implementation.)
        with self.client:
            response = self.client.delete(
                f"{self.url}/{mount_device_action.id}",
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
        self.assertEqual(response.status_code, 200)

        related_configuration = (
            db.session.query(Configuration)
            .filter_by(id=related_configuration_id)
            .first()
        )
        msg = "delete;device mount action"
        self.assertEqual(msg, related_configuration.update_description)

    def test_delete_device_mount_action_with_datastream(self):
        """Ensure we can't delete a device mount that is associated with a datastream."""
        mount_device_action = add_mount_device_action_model()
        device = mount_device_action.device
        device_property = DeviceProperty(
            device=device,
            label="example device property",
            property_name="measurment",
        )
        tsm_endpoint = TsmEndpoint(name="example", url="http://somewhere")
        datastream = DatastreamLink(
            device_mount_action=mount_device_action,
            device_property=device_property,
            tsm_endpoint=tsm_endpoint,
            datasource_name="1",
            datasource_id="1",
            thing_name="2",
            thing_id="2",
            datastream_id="3",
            datastream_name="3",
        )
        db.session.add_all([device_property, tsm_endpoint, datastream])
        db.session.commit()
        access_headers = create_token()
        # As long as there is no permission group for the configuration,
        # an authentificated user is allowed to delete the action.
        # (At least in our current implementation.)
        with self.client:
            response = self.client.delete(
                f"{self.url}/{mount_device_action.id}",
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
        self.assertEqual(response.status_code, 409)

    def test_filtered_by_configuration(self):
        """Ensure that I can prefilter by a specific configuration."""
        configuration1 = Configuration(
            label="sample configuration",
            is_public=True,
            is_internal=False,
        )
        db.session.add(configuration1)
        configuration2 = Configuration(
            label="sample configuration II",
            is_public=True,
            is_internal=False,
        )
        db.session.add(configuration2)

        contact = Contact(
            given_name="Nils", family_name="Brinckmann", email="nils@gfz-potsdam.de"
        )
        db.session.add(contact)

        device1 = Device(
            short_name="device1",
            manufacturer_name=fake.company(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        db.session.add(device1)

        device2 = Device(
            short_name="device2",
            manufacturer_name=fake.company(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        db.session.add(device2)

        action1 = DeviceMountAction(
            configuration=configuration1,
            begin_contact=contact,
            device=device1,
            parent_platform=None,
            begin_description="Some first action",
            begin_date=fake.date_time(),
        )
        db.session.add(action1)

        action2 = DeviceMountAction(
            configuration=configuration2,
            begin_contact=contact,
            device=device2,
            begin_description="Some other action",
            begin_date=fake.date_time(),
        )
        db.session.add(action2)
        db.session.commit()

        # first check to get them all
        with self.client:
            url_get_all = base_url + "/device-mount-actions"
            response = self.client.get(
                url_get_all, content_type="application/vnd.api+json"
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 2)

        # then test only for the first configuration
        with self.client:
            url_get_for_configuration1 = (
                base_url + f"/configurations/{configuration1.id}/device-mount-actions"
            )
            response = self.client.get(
                url_get_for_configuration1, content_type="application/vnd.api+json"
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 1)
        self.assertEqual(
            response.json["data"][0]["attributes"]["begin_description"],
            "Some first action",
        )

        # and test the second configuration
        with self.client:
            url_get_for_configuration2 = (
                base_url + f"/configurations/{configuration2.id}/device-mount-actions"
            )
            response = self.client.get(
                url_get_for_configuration2, content_type="application/vnd.api+json"
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 1)
        self.assertEqual(
            response.json["data"][0]["attributes"]["begin_description"],
            "Some other action",
        )

        # and for a non existing
        with self.client:
            url_get_for_non_existing_configuration = (
                base_url
                + f"/configurations/{configuration2.id + 9999}/device-mount-actions"
            )
            response = self.client.get(
                url_get_for_non_existing_configuration,
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 404)

    def test_filtered_by_configuration_id(self):
        """Ensure that I can prefilter by filter[configuration_id]."""
        configuration1 = Configuration(
            label="sample configuration",
            is_public=True,
            is_internal=False,
        )
        db.session.add(configuration1)
        configuration2 = Configuration(
            label="sample configuration II",
            is_public=True,
            is_internal=False,
        )
        db.session.add(configuration2)

        contact = Contact(
            given_name="Nils", family_name="Brinckmann", email="nils@gfz-potsdam.de"
        )
        db.session.add(contact)

        device1 = Device(
            short_name="device1",
            manufacturer_name=fake.company(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        db.session.add(device1)

        device2 = Device(
            short_name="device2",
            manufacturer_name=fake.company(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        db.session.add(device2)

        action1 = DeviceMountAction(
            configuration=configuration1,
            begin_contact=contact,
            device=device1,
            parent_platform=None,
            begin_description="Some first action",
            begin_date=fake.date_time(),
        )
        db.session.add(action1)

        action2 = DeviceMountAction(
            configuration=configuration2,
            begin_contact=contact,
            device=device2,
            begin_description="Some other action",
            begin_date=fake.date_time(),
        )
        db.session.add(action2)
        db.session.commit()

        with self.client:
            url_get_for_configuration1 = (
                base_url
                + f"/device-mount-actions?filter[configuration_id]={configuration1.id}"
            )
            response = self.client.get(
                url_get_for_configuration1, content_type="application/vnd.api+json"
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 1)
        self.assertEqual(
            response.json["data"][0]["attributes"]["begin_description"],
            "Some first action",
        )

        # and test the second configuration
        with self.client:
            url_get_for_configuration2 = (
                base_url
                + f"/device-mount-actions?filter[configuration_id]={configuration2.id}"
            )
            response = self.client.get(
                url_get_for_configuration2, content_type="application/vnd.api+json"
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 1)
        self.assertEqual(
            response.json["data"][0]["attributes"]["begin_description"],
            "Some other action",
        )

        # and for a non existing
        with self.client:
            url_get_for_non_existing_configuration = (
                base_url
                + f"/device-mount-actions?filter[configuration_id]={configuration2.id + 9999}"
            )
            response = self.client.get(
                url_get_for_non_existing_configuration,
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 0)

    def test_filtered_by_device(self):
        """Ensure that I can prefilter by a specific devices."""
        configuration1 = Configuration(
            label="sample configuration",
            is_public=True,
            is_internal=False,
        )
        db.session.add(configuration1)
        configuration2 = Configuration(
            label="sample configuration II",
            is_public=True,
            is_internal=False,
        )
        db.session.add(configuration2)

        contact = Contact(
            given_name="Nils", family_name="Brinckmann", email="nils@gfz-potsdam.de"
        )
        db.session.add(contact)

        device1 = Device(
            short_name="device1",
            manufacturer_name=fake.company(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        db.session.add(device1)

        device2 = Device(
            short_name="device2",
            manufacturer_name=fake.company(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        db.session.add(device2)

        action1 = DeviceMountAction(
            configuration=configuration1,
            begin_contact=contact,
            device=device1,
            parent_platform=None,
            begin_description="Some first action",
            begin_date=fake.date_time(),
        )
        db.session.add(action1)

        action2 = DeviceMountAction(
            configuration=configuration2,
            begin_contact=contact,
            device=device2,
            begin_description="Some other action",
            begin_date=fake.date_time(),
        )
        db.session.add(action2)

        db.session.commit()

        # test only for the first device
        with self.client:
            url_get_for_device1 = (
                base_url + f"/devices/{device1.id}/device-mount-actions"
            )
            response = self.client.get(
                url_get_for_device1, content_type="application/vnd.api+json"
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 1)
        self.assertEqual(
            response.json["data"][0]["attributes"]["begin_description"],
            "Some first action",
        )

        # and test the second device
        with self.client:
            url_get_for_device2 = (
                base_url + f"/devices/{device2.id}/device-mount-actions"
            )
            response = self.client.get(
                url_get_for_device2, content_type="application/vnd.api+json"
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 1)
        self.assertEqual(
            response.json["data"][0]["attributes"]["begin_description"],
            "Some other action",
        )

        # and for a non existing
        with self.client:
            url_get_for_non_existing_device = (
                base_url + f"/devices/{device2.id + 9999}/device-mount-actions"
            )
            response = self.client.get(
                url_get_for_non_existing_device,
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 404)

    def test_filtered_by_device_id(self):
        """Ensure that I can prefilter by filter[device_id]."""
        configuration1 = Configuration(
            label="sample configuration",
            is_public=True,
            is_internal=False,
        )
        db.session.add(configuration1)
        configuration2 = Configuration(
            label="sample configuration II",
            is_public=True,
            is_internal=False,
        )
        db.session.add(configuration2)

        contact = Contact(
            given_name="Nils", family_name="Brinckmann", email="nils@gfz-potsdam.de"
        )
        db.session.add(contact)

        device1 = Device(
            short_name="device1",
            manufacturer_name=fake.company(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        db.session.add(device1)

        device2 = Device(
            short_name="device2",
            manufacturer_name=fake.company(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        db.session.add(device2)

        action1 = DeviceMountAction(
            configuration=configuration1,
            begin_contact=contact,
            device=device1,
            parent_platform=None,
            begin_description="Some first action",
            begin_date=fake.date_time(),
        )
        db.session.add(action1)

        action2 = DeviceMountAction(
            configuration=configuration2,
            begin_contact=contact,
            device=device2,
            begin_description="Some other action",
            begin_date=fake.date_time(),
        )
        db.session.add(action2)

        db.session.commit()

        # test only for the first device
        with self.client:
            url_get_for_device1 = (
                base_url + f"/device-mount-actions?filter[device_id]={device1.id}"
            )
            response = self.client.get(
                url_get_for_device1, content_type="application/vnd.api+json"
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 1)
        self.assertEqual(
            response.json["data"][0]["attributes"]["begin_description"],
            "Some first action",
        )

        # and test the second device
        with self.client:
            url_get_for_device2 = (
                base_url + f"/device-mount-actions?filter[device_id]={device2.id}"
            )
            response = self.client.get(
                url_get_for_device2, content_type="application/vnd.api+json"
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 1)
        self.assertEqual(
            response.json["data"][0]["attributes"]["begin_description"],
            "Some other action",
        )

        # and for a non existing
        with self.client:
            url_get_for_non_existing_device = (
                base_url
                + f"/device-mount-actions?filter[device_id]={device2.id + 9999}"
            )
            response = self.client.get(
                url_get_for_non_existing_device,
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 0)

    def test_filtered_by_platform(self):
        """Ensure that I can prefilter by a specific (parent) platform."""
        configuration1 = Configuration(
            label="sample configuration",
            is_public=True,
            is_internal=False,
        )
        db.session.add(configuration1)
        configuration2 = Configuration(
            label="sample configuration II",
            is_public=True,
            is_internal=False,
        )
        db.session.add(configuration2)

        contact = Contact(
            given_name="Nils", family_name="Brinckmann", email="nils@gfz-potsdam.de"
        )
        db.session.add(contact)

        platform1 = Platform(
            short_name="platform1",
            manufacturer_name=fake.company(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        db.session.add(platform1)

        platform2 = Platform(
            short_name="platform2",
            manufacturer_name=fake.company(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        db.session.add(platform2)

        device1 = Device(
            short_name="device1",
            manufacturer_name=fake.company(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        db.session.add(device1)

        device2 = Device(
            short_name="device2",
            manufacturer_name=fake.company(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        db.session.add(device2)

        action1 = DeviceMountAction(
            configuration=configuration1,
            begin_contact=contact,
            device=device1,
            parent_platform=platform1,
            begin_description="Some first action",
            begin_date=fake.date_time(),
        )
        db.session.add(action1)

        action2 = DeviceMountAction(
            configuration=configuration2,
            parent_platform=platform2,
            begin_contact=contact,
            device=device2,
            begin_description="Some other action",
            begin_date=fake.date_time(),
        )
        db.session.add(action2)

        db.session.commit()

        # test only for the first platform
        with self.client:
            url_get_for_platform1 = (
                base_url + f"/platforms/{platform1.id}/device-mount-actions"
            )
            response = self.client.get(
                url_get_for_platform1, content_type="application/vnd.api+json"
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 1)
        self.assertEqual(
            response.json["data"][0]["attributes"]["begin_description"],
            "Some first action",
        )

        # and test the second platform
        with self.client:
            url_get_for_platform2 = (
                base_url + f"/platforms/{platform2.id}/device-mount-actions"
            )
            response = self.client.get(
                url_get_for_platform2, content_type="application/vnd.api+json"
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 1)
        self.assertEqual(
            response.json["data"][0]["attributes"]["begin_description"],
            "Some other action",
        )

        # and for a non existing
        with self.client:
            url_get_for_non_existing = (
                base_url + f"/platforms/{platform2.id + 9999}/device-mount-actions"
            )
            response = self.client.get(
                url_get_for_non_existing,
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 404)

    def test_filtered_by_parent_platform_id(self):
        """Ensure that I can prefilter by filter[parent_platform_id]."""
        configuration1 = Configuration(
            label="sample configuration",
            is_public=True,
            is_internal=False,
        )
        db.session.add(configuration1)
        configuration2 = Configuration(
            label="sample configuration II",
            is_public=True,
            is_internal=False,
        )
        db.session.add(configuration2)

        contact = Contact(
            given_name="Nils", family_name="Brinckmann", email="nils@gfz-potsdam.de"
        )
        db.session.add(contact)

        platform1 = Platform(
            short_name="platform1",
            manufacturer_name=fake.company(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        db.session.add(platform1)

        platform2 = Platform(
            short_name="platform2",
            manufacturer_name=fake.company(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        db.session.add(platform2)

        device1 = Device(
            short_name="device1",
            manufacturer_name=fake.company(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        db.session.add(device1)

        device2 = Device(
            short_name="device2",
            manufacturer_name=fake.company(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        db.session.add(device2)

        action1 = DeviceMountAction(
            configuration=configuration1,
            begin_contact=contact,
            device=device1,
            parent_platform=platform1,
            begin_description="Some first action",
            begin_date=fake.date_time(),
        )
        db.session.add(action1)

        action2 = DeviceMountAction(
            configuration=configuration2,
            parent_platform=platform2,
            begin_contact=contact,
            device=device2,
            begin_description="Some other action",
            begin_date=fake.date_time(),
        )
        db.session.add(action2)

        db.session.commit()

        # test only for the first platform
        with self.client:
            url_get_for_platform1 = (
                base_url
                + f"/device-mount-actions?filter[parent_platform_id]={platform1.id}"
            )
            response = self.client.get(
                url_get_for_platform1, content_type="application/vnd.api+json"
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 1)
        self.assertEqual(
            response.json["data"][0]["attributes"]["begin_description"],
            "Some first action",
        )

        # and test the second platform
        with self.client:
            url_get_for_platform2 = (
                base_url
                + f"/device-mount-actions?filter[parent_platform_id]={platform2.id}"
            )
            response = self.client.get(
                url_get_for_platform2, content_type="application/vnd.api+json"
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 1)
        self.assertEqual(
            response.json["data"][0]["attributes"]["begin_description"],
            "Some other action",
        )

        # and for a non existing
        with self.client:
            url_get_for_non_existing = (
                base_url
                + f"/device-mount-actions?filter[parent_platform_id]={platform2.id + 9999}"
            )
            response = self.client.get(
                url_get_for_non_existing,
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 0)

    def test_filtered_by_parent_device_id(self):
        """Ensure that I can prefilter by filter[parent_device_id]."""
        configuration1 = Configuration(
            label="sample configuration",
            is_public=True,
            is_internal=False,
        )
        db.session.add(configuration1)
        configuration2 = Configuration(
            label="sample configuration II",
            is_public=True,
            is_internal=False,
        )
        db.session.add(configuration2)

        contact = Contact(
            given_name="Nils", family_name="Brinckmann", email="nils@gfz-potsdam.de"
        )
        db.session.add(contact)

        parent_device1 = Device(
            short_name="parent device1",
            manufacturer_name=fake.company(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        db.session.add(parent_device1)

        parent_device2 = Device(
            short_name="parent device2",
            manufacturer_name=fake.company(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        db.session.add(parent_device2)

        device1 = Device(
            short_name="device1",
            manufacturer_name=fake.company(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        db.session.add(device1)

        device2 = Device(
            short_name="device2",
            manufacturer_name=fake.company(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        db.session.add(device2)

        action1 = DeviceMountAction(
            configuration=configuration1,
            begin_contact=contact,
            device=device1,
            parent_device=parent_device1,
            begin_description="Some first action",
            begin_date=fake.date_time(),
        )
        db.session.add(action1)

        action2 = DeviceMountAction(
            configuration=configuration2,
            parent_device=parent_device2,
            begin_contact=contact,
            device=device2,
            begin_description="Some other action",
            begin_date=fake.date_time(),
        )
        db.session.add(action2)

        db.session.commit()

        # test only for the first parent device
        with self.client:
            url_get_for_parent_device1 = (
                base_url
                + f"/device-mount-actions?filter[parent_device_id]={parent_device1.id}"
            )
            response = self.client.get(
                url_get_for_parent_device1, content_type="application/vnd.api+json"
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 1)
        self.assertEqual(
            response.json["data"][0]["attributes"]["begin_description"],
            "Some first action",
        )

        # and test the second parent device
        with self.client:
            url_get_for_parent_device2 = (
                base_url
                + f"/device-mount-actions?filter[parent_device_id]={parent_device2.id}"
            )
            response = self.client.get(
                url_get_for_parent_device2, content_type="application/vnd.api+json"
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 1)
        self.assertEqual(
            response.json["data"][0]["attributes"]["begin_description"],
            "Some other action",
        )

        # and for a non existing
        with self.client:
            url_get_for_non_existing = (
                base_url
                + f"/device-mount-actions?filter[parent_device_id]={parent_device2.id + 9999}"
            )
            response = self.client.get(
                url_get_for_non_existing,
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 0)

    def test_http_response_not_found(self):
        """Make sure that the backend responds with 404 HTTP-Code if a resource was not found."""
        url = f"{self.url}/{fake.random_int()}"
        _ = super().http_code_404_when_resource_not_found(url)

    def test_update_device_mount_action_change_device_id(self):
        """Make sure device id can not be changed if new device doesn't exist."""
        mount_device_action = add_mount_device_action_model()
        mount_device_action.parent_platform = None
        db.session.add(mount_device_action)
        db.session.commit()
        mount_device_action_updated = {
            "data": {
                "type": self.object_type,
                "id": mount_device_action.id,
                "attributes": {
                    "begin_description": "updated",
                },
                "relationships": {
                    "device": {
                        "data": {
                            "type": "device",
                            "id": mount_device_action.device.id + 1,
                        }
                    },
                },
            }
        }
        access_headers = create_token()
        with self.client:
            response = self.client.patch(
                f"{self.url}/{mount_device_action.id}",
                data=json.dumps(mount_device_action_updated),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )

        # It looks a little bit strange to have the 403 here.
        # This is due to the permission management checks that
        # we run before putting the device mount action to the new
        # device: The user must not only be able to edit
        # the device to that the mount action belong before
        # doing the request, but also for the one that we want
        # to use as the target.
        # As this doesn't exist, we don't allow the change.
        self.assertEqual(response.status_code, 403)

    def test_update_device_mount_action_change_configuration_id(self):
        """Make sure configuration id can not be changed if new config doesn't exist."""
        mount_device_action = add_mount_device_action_model()
        mount_device_action.parent_platform = None
        db.session.add(mount_device_action)
        db.session.commit()
        mount_device_action_updated = {
            "data": {
                "type": self.object_type,
                "id": mount_device_action.id,
                "attributes": {
                    "begin_description": "updated",
                },
                "relationships": {
                    "configuration": {
                        "data": {
                            "type": "configuration",
                            "id": mount_device_action.configuration.id + 1,
                        }
                    },
                },
            }
        }
        access_headers = create_token()
        with self.client:
            response = self.client.patch(
                f"{self.url}/{mount_device_action.id}",
                data=json.dumps(mount_device_action_updated),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
        # It looks a little bit strange to have the 403 here.
        # This is due to the permission management checks that
        # we run before putting the device mount action to the new
        # configuration: The user must not only be able to edit
        # the configuration to that the mount action belong before
        # doing the request, but also for the one that we want
        # to use as the target.
        # As this doesn't exist, we don't allow the change.
        self.assertEqual(response.status_code, 403)

    def test_update_device_mount_action_change_parent_platform_id(self):
        """Make sure parent platform id can not be changed without platform mount."""
        mount_device_action = add_mount_device_action_model()
        mount_device_action_updated = {
            "data": {
                "type": self.object_type,
                "id": mount_device_action.id,
                "attributes": {"begin_description": "updated"},
                "relationships": {
                    "parent_platform": {
                        "data": {
                            "type": "platform",
                            # We don't have a platform mount action for this
                            # parent platform for the whole time.
                            "id": mount_device_action.parent_platform.id + 1,
                        }
                    },
                },
            }
        }
        access_headers = create_token()
        with self.client:
            response = self.client.patch(
                f"{self.url}/{mount_device_action.id}",
                data=json.dumps(mount_device_action_updated),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
        self.assertEqual(response.status_code, 409)

    def test_update_device_mount_action_change_parent_device_id(self):
        """Make sure parent device id can not be changed without extra device mount."""
        mount_device_action = add_mount_device_action_model()
        mount_device_action_updated = {
            "data": {
                "type": self.object_type,
                "id": mount_device_action.id,
                "attributes": {"begin_description": "updated"},
                "relationships": {
                    "parent_device": {
                        "data": {
                            "type": "device",
                            # We don't have a platform mount action for this
                            # parent platform for the whole time.
                            "id": 999,
                        }
                    },
                },
            }
        }
        access_headers = create_token()
        with self.client:
            response = self.client.patch(
                f"{self.url}/{mount_device_action.id}",
                data=json.dumps(mount_device_action_updated),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
        self.assertEqual(response.status_code, 409)

    def test_update_device_mount_action_add_parent_platform_id_if_there_is_no_parent(
        self,
    ):
        """Make sure parent platform id can be add if it is None."""
        d = Device(
            short_name=fake.linux_processor(),
            manufacturer_name=fake.company(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        userinfo = generate_userinfo_data()
        c1 = Contact(
            given_name=userinfo["given_name"],
            family_name=userinfo["family_name"],
            email=userinfo["email"],
        )

        config = generate_configuration_model()
        device_mount_action = DeviceMountAction(
            begin_date=fake.date(),
            begin_description="test mount device action model",
            offset_x=fake.coordinate(),
            offset_y=fake.coordinate(),
            offset_z=fake.coordinate(),
            device=d,
        )
        device_mount_action.configuration = config
        device_mount_action.begin_contact = c1

        p_p = Platform(
            short_name="device parent platform",
            manufacturer_name=fake.company(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        platform_mount_action = PlatformMountAction(
            begin_date=device_mount_action.begin_date,
            begin_description="test mount device action model",
            offset_x=fake.coordinate(),
            offset_y=fake.coordinate(),
            offset_z=fake.coordinate(),
            platform=p_p,
            begin_contact=c1,
            configuration=config,
        )
        db.session.add_all(
            [d, c1, p_p, config, device_mount_action, platform_mount_action]
        )
        db.session.commit()
        self.assertEqual(device_mount_action.parent_platform, None)

        mount_device_action_updated = {
            "data": {
                "type": self.object_type,
                "id": device_mount_action.id,
                "attributes": {"begin_description": "updated"},
                "relationships": {
                    "parent_platform": {
                        "data": {
                            "type": "platform",
                            "id": p_p.id,
                        }
                    },
                },
            }
        }
        access_headers = create_token()
        with self.client:
            response = self.client.patch(
                f"{self.url}/{device_mount_action.id}",
                data=json.dumps(mount_device_action_updated),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
        self.assertEqual(response.status_code, 200)

    def test_update_device_mount_action_add_parent_device_id_if_there_is_no_parent(
        self,
    ):
        """Make sure parent device id can be add if it is None."""
        d = Device(
            short_name=fake.linux_processor(),
            manufacturer_name=fake.company(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        userinfo = generate_userinfo_data()
        c1 = Contact(
            given_name=userinfo["given_name"],
            family_name=userinfo["family_name"],
            email=userinfo["email"],
        )

        config = generate_configuration_model()
        device_mount_action = DeviceMountAction(
            begin_date=fake.date(),
            begin_description="test mount device action model",
            offset_x=fake.coordinate(),
            offset_y=fake.coordinate(),
            offset_z=fake.coordinate(),
            device=d,
        )
        device_mount_action.configuration = config
        device_mount_action.begin_contact = c1

        p_d = Device(
            short_name="device parent device",
            manufacturer_name=fake.company(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        parent_mount_action = DeviceMountAction(
            begin_date=device_mount_action.begin_date,
            begin_description="test mount device action model",
            offset_x=fake.coordinate(),
            offset_y=fake.coordinate(),
            offset_z=fake.coordinate(),
            device=p_d,
            begin_contact=c1,
            configuration=config,
        )
        db.session.add_all(
            [d, c1, p_d, config, device_mount_action, parent_mount_action]
        )
        db.session.commit()
        self.assertEqual(device_mount_action.parent_device, None)

        mount_device_action_updated = {
            "data": {
                "type": self.object_type,
                "id": device_mount_action.id,
                "attributes": {"begin_description": "updated"},
                "relationships": {
                    "parent_device": {
                        "data": {
                            "type": "device",
                            "id": p_d.id,
                        }
                    },
                },
            }
        }
        access_headers = create_token()
        with self.client:
            response = self.client.patch(
                f"{self.url}/{device_mount_action.id}",
                data=json.dumps(mount_device_action_updated),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
        self.assertEqual(response.status_code, 200)

    def test_update_device_mount_and_unmount_a_device(self):
        """Make sure device can be unmounted."""
        mount_device_action = add_mount_device_action_model()
        # Make sure we don't have to deal with the parent platform mount
        # at this moment.
        mount_device_action.parent_platform = None
        db.session.add(mount_device_action)
        db.session.commit()
        end_date = mount_device_action.begin_date + relativedelta(years=+1)
        mount_device_action_updated = {
            "data": {
                "type": self.object_type,
                "id": mount_device_action.id,
                "attributes": {"end_date": end_date.isoformat()},
                "relationships": {
                    "end_contact": {
                        "data": {
                            "type": "contact",
                            "id": mount_device_action.begin_contact.id,
                        }
                    },
                },
            }
        }
        access_headers = create_token()
        with self.client:
            response = self.client.patch(
                f"{self.url}/{mount_device_action.id}",
                data=json.dumps(mount_device_action_updated),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
        self.assertEqual(response.status_code, 200)
        data = response.json["data"]
        self.assertEqual(data["attributes"]["end_date"], end_date.isoformat())

    def test_update_device_mount_and_unmount_set_end_contact_to_none(self):
        """Make sure end contact can be reset to none."""
        mount_device_action = add_mount_device_action_model()
        contact = Contact(given_name="d", family_name="u", email="du@localhost")
        mount_device_action.end_contact = contact
        # Make sure we don't have to deal with the parent platform mount
        # at this moment.
        mount_device_action.parent_platform = None
        db.session.add_all([mount_device_action, contact])
        db.session.commit()
        end_date = mount_device_action.begin_date + relativedelta(years=+1)
        mount_device_action_updated = {
            "data": {
                "type": self.object_type,
                "id": mount_device_action.id,
                "attributes": {"end_date": end_date.isoformat()},
                "relationships": {
                    "end_contact": {
                        "data": None,
                    },
                },
            }
        }
        access_headers = create_token()
        with self.client:
            response = self.client.patch(
                f"{self.url}/{mount_device_action.id}",
                data=json.dumps(mount_device_action_updated),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
        self.assertEqual(response.status_code, 200)
        data = response.json["data"]
        self.assertEqual(data["attributes"]["end_date"], end_date.isoformat())

    def test_update_device_mount_and_change_the_time_intervall(self):
        """Make sure device con not be unmounted."""
        d = Device(
            short_name=fake.linux_processor(),
            manufacturer_name=fake.company(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        userinfo = generate_userinfo_data()
        c1 = Contact(
            given_name=userinfo["given_name"],
            family_name=userinfo["family_name"],
            email=userinfo["email"],
        )

        config = generate_configuration_model()
        device_mount_action_1 = DeviceMountAction(
            begin_date="2022-06-08T07:25:00.782000",
            end_date="2023-06-08T07:25:00.782000",
            begin_description="test mount device action model",
            offset_x=fake.coordinate(),
            offset_y=fake.coordinate(),
            offset_z=fake.coordinate(),
            device=d,
        )
        device_mount_action_1.configuration = config
        device_mount_action_1.begin_contact = c1
        device_mount_action_1.end_contact = c1

        device_mount_action_2 = DeviceMountAction(
            begin_date="2024-06-08T07:25:00.782000",
            begin_description="test mount device action model",
            offset_x=fake.coordinate(),
            offset_y=fake.coordinate(),
            offset_z=fake.coordinate(),
            device=d,
        )
        device_mount_action_2.configuration = config
        device_mount_action_2.begin_contact = c1

        p_p = Platform(
            short_name="device parent platform",
            manufacturer_name=fake.company(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        db.session.add_all(
            [d, c1, p_p, config, device_mount_action_1, device_mount_action_2]
        )
        db.session.commit()
        end_date = device_mount_action_2.begin_date + relativedelta(years=+1)
        # try to change it with an intervall, where the device mounted.
        mount_device_action_updated = {
            "data": {
                "type": self.object_type,
                "id": device_mount_action_2.id,
                "attributes": {
                    "begin_date": "2022-08-08T07:25:00.782000",
                    "end_date": end_date.isoformat(),
                },
                "relationships": {
                    "end_contact": {
                        "data": {
                            "type": "contact",
                            "id": device_mount_action_2.begin_contact.id,
                        }
                    },
                },
            }
        }
        access_headers = create_token()
        with self.client:
            response = self.client.patch(
                f"{self.url}/{device_mount_action_2.id}",
                data=json.dumps(mount_device_action_updated),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
        self.assertEqual(response.status_code, 409)

        # This should work as we will deliver a valid time-interval
        mount_device_action_with_no_conflicts = {
            "data": {
                "type": self.object_type,
                "id": device_mount_action_2.id,
                "attributes": {
                    "begin_date": "2023-08-08T07:25:00.782000",
                    "end_date": end_date.isoformat(),
                },
                "relationships": {
                    "end_contact": {
                        "data": {
                            "type": "contact",
                            "id": device_mount_action_2.begin_contact.id,
                        }
                    },
                },
            }
        }
        access_headers = create_token()
        with self.client:
            response = self.client.patch(
                f"{self.url}/{device_mount_action_2.id}",
                data=json.dumps(mount_device_action_with_no_conflicts),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
        self.assertEqual(response.status_code, 200)

        # And also if we try to change the time-intervall with a conflict in
        # end_date should not work.
        # Reason here is that the time intervals for the both mount actions
        # for the very same device are overlapping.
        mount_device_action_with_conflict_on_end_date = {
            "data": {
                "type": self.object_type,
                "id": device_mount_action_1.id,
                "attributes": {
                    "end_date": "2023-11-08T07:25:00.782000",
                },
            }
        }
        access_headers = create_token()
        with self.client:
            response = self.client.patch(
                f"{self.url}/{device_mount_action_1.id}",
                data=json.dumps(mount_device_action_with_conflict_on_end_date),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
        self.assertEqual(response.status_code, 409)

    def test_update_external_metadata_after_post_of_device_mount_action(self):
        """Ensure we trigger the update_external_metadata when posting a device mount action."""
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
        configuration.b2inst_record_id = "42"
        begin_date = fake.future_datetime()

        db.session.add_all(
            [
                device,
                begin_contact,
                configuration,
            ]
        )
        db.session.commit()

        data = {
            "data": {
                "type": self.object_type,
                "attributes": {
                    "begin_description": "Test DeviceMountAction",
                    "begin_date": str(begin_date),
                    "offset_x": str(fake.coordinate()),
                    "offset_y": str(fake.coordinate()),
                    "offset_z": str(fake.coordinate()),
                },
                "relationships": {
                    "device": {"data": {"type": "device", "id": device.id}},
                    "begin_contact": {
                        "data": {"type": "contact", "id": begin_contact.id}
                    },
                    "configuration": {
                        "data": {"type": "configuration", "id": configuration.id}
                    },
                },
            }
        }
        current_app.config.update({"B2INST_TOKEN": "123"})
        with patch.object(
            pidinst, "update_external_metadata"
        ) as update_external_metadata:
            update_external_metadata.return_value = None
            super().add_object(
                url=f"{self.url}?include="
                + "device,begin_contact,end_contact,parent_platform,configuration",
                data_object=data,
                object_type=self.object_type,
            )
            update_external_metadata.assert_called_once()
            self.assertEqual(
                update_external_metadata.call_args.args[0].id, configuration.id
            )

    def test_update_external_metadata_after_patch_of_device_mount_action(self):
        """Ensure we trigger the update_external_metadata when patching a device mount action."""
        mount_device_action = add_mount_device_action_model()
        mount_device_action.parent_platform = None
        configuration = mount_device_action.configuration
        configuration.b2inst_record_id = "42"
        db.session.add_all([configuration, mount_device_action])
        mount_device_action_updated = {
            "data": {
                "type": self.object_type,
                "id": mount_device_action.id,
                "attributes": {"begin_description": "updated"},
            }
        }
        current_app.config.update({"B2INST_TOKEN": "123"})
        with patch.object(
            pidinst, "update_external_metadata"
        ) as update_external_metadata:
            update_external_metadata.return_value = None
            super().update_object(
                url=f"{self.url}/{mount_device_action.id}",
                data_object=mount_device_action_updated,
                object_type=self.object_type,
            )
            update_external_metadata.assert_called_once()
            self.assertEqual(
                update_external_metadata.call_args.args[0].id, configuration.id
            )

    def test_update_external_metadata_after_delete_of_device_mount_action(self):
        """Ensure we trigger the update_external_metadata when deleting a device mount action."""
        mount_device_action = add_mount_device_action_model()
        mount_device_action.parent_platform = None
        configuration = mount_device_action.configuration
        configuration.b2inst_record_id = "42"
        db.session.add_all([configuration, mount_device_action])
        current_app.config.update({"B2INST_TOKEN": "123"})
        with patch.object(
            pidinst, "update_external_metadata"
        ) as update_external_metadata:
            update_external_metadata.return_value = None
            super().delete_object(
                url=f"{self.url}/{mount_device_action.id}",
            )
            update_external_metadata.assert_called_once()
            self.assertEqual(
                update_external_metadata.call_args.args[0].id, configuration.id
            )
