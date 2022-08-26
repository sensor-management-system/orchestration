"""Tests for the device mount action api."""

import datetime
import json

from dateutil.relativedelta import relativedelta

from project import base_url
from project.api.models import (
    Configuration,
    Contact,
    Device,
    DeviceMountAction,
    Platform,
    PlatformMountAction,
)
from project.api.models.base_model import db
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
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        parent_platform = Platform(
            short_name="device parent platform",
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
            url=f"{self.url}?include=device,begin_contact,end_contact,parent_platform,configuration",
            data_object=data,
            object_type=self.object_type,
        )
        result_id = response["data"]["id"]
        result_device_mount_action = db.session.query(DeviceMountAction).filter_by(id=result_id).first()

        msg = "create;device mount action"
        self.assertEqual(msg, result_device_mount_action.configuration.update_description)

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
        result_device_mount_action = db.session.query(DeviceMountAction).filter_by(id=result_id).first()

        msg = "update;device mount action"
        self.assertEqual(msg, result_device_mount_action.configuration.update_description)

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

        related_configuration = db.session.query(Configuration).filter_by(id=related_configuration_id).first()
        msg = "delete;device mount action"
        self.assertEqual(msg, related_configuration.update_description)

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
            short_name="device1", is_public=True, is_private=False, is_internal=False,
        )
        db.session.add(device1)

        device2 = Device(
            short_name="device2", is_public=True, is_private=False, is_internal=False,
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
            short_name="device1", is_public=True, is_private=False, is_internal=False,
        )
        db.session.add(device1)

        device2 = Device(
            short_name="device2", is_public=True, is_private=False, is_internal=False,
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
            short_name="platform1", is_public=True, is_private=False, is_internal=False,
        )
        db.session.add(platform1)

        platform2 = Platform(
            short_name="platform2", is_public=True, is_private=False, is_internal=False,
        )
        db.session.add(platform2)

        device1 = Device(
            short_name="device1", is_public=True, is_private=False, is_internal=False,
        )
        db.session.add(device1)

        device2 = Device(
            short_name="device2", is_public=True, is_private=False, is_internal=False,
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
                url_get_for_non_existing, content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 404)

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
                "attributes": {"begin_description": "updated",},
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

        self.assertEqual(response.status_code, 404)

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
                "attributes": {"begin_description": "updated",},
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
        self.assertEqual(response.status_code, 404)

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

    def test_update_device_mount_action_add_parent_platform_id_if_there_is_no_parent(
        self,
    ):
        """Make sure parent platform id can be add if it is None."""
        d = Device(
            short_name=fake.linux_processor(),
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
                    "parent_platform": {"data": {"type": "platform", "id": p_p.id,}},
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

        # This Should Work as we will deliver a valid time-interval
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
        # end_date should not work
        mount_device_action_with_conflict_on_end_date = {
            "data": {
                "type": self.object_type,
                "id": device_mount_action_1.id,
                "attributes": {"end_date": "2023-11-08T07:25:00.782000",},
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
