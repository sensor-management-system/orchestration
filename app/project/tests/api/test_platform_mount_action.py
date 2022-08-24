"""Tests for the platform mount action api."""

import datetime
import json

from dateutil.relativedelta import relativedelta

from project import base_url
from project.api.models import Configuration, Contact, Platform, PlatformMountAction
from project.api.models.base_model import db
from project.tests.base import BaseTestCase, create_token, fake, generate_userinfo_data
from project.tests.models.test_configurations_model import generate_configuration_model
from project.tests.models.test_mount_actions_model import (
    add_mount_platform_action_model,
)


class TestPlatformMountAction(BaseTestCase):
    """Tests for the PlatformMountAction endpoints."""

    url = base_url + "/platform-mount-actions"
    object_type = "platform_mount_action"

    def test_filtered_by_configuration(self):
        """Ensure that I can prefilter by a specific configuration."""
        configuration1 = Configuration(
            label="sample configuration",
            location_type="static",
            is_public=True,
            is_internal=False,
        )
        db.session.add(configuration1)
        configuration2 = Configuration(
            label="sample configuration II",
            location_type="static",
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
            short_name="Platform2", is_public=True, is_private=False, is_internal=False,
        )
        db.session.add(platform2)

        action1 = PlatformMountAction(
            configuration=configuration1,
            begin_contact=contact,
            parent_platform=None,
            platform=platform1,
            begin_description="Some first action",
            begin_date=fake.date_time(),
        )
        db.session.add(action1)

        action2 = PlatformMountAction(
            configuration=configuration2,
            begin_contact=contact,
            platform=platform2,
            parent_platform=None,
            begin_description="Some other action",
            begin_date=fake.date_time(),
        )
        db.session.add(action2)
        db.session.commit()

        # first check to get them all
        with self.client:
            url_get_all = base_url + "/platform-mount-actions"
            response = self.client.get(
                url_get_all, content_type="application/vnd.api+json"
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 2)

        # then test only for the first configuration
        with self.client:
            url_get_for_configuration1 = (
                base_url + f"/configurations/{configuration1.id}/platform-mount-actions"
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
                base_url + f"/configurations/{configuration2.id}/platform-mount-actions"
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
                + f"/configurations/{configuration2.id + 9999}/platform-mount-actions"
            )
            response = self.client.get(
                url_get_for_non_existing_configuration,
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 404)

    def test_filtered_by_platform(self):
        """Ensure that I can prefilter by a specific platform."""
        configuration1 = Configuration(
            label="sample configuration",
            location_type="static",
            is_public=True,
            is_internal=False,
        )
        db.session.add(configuration1)
        configuration2 = Configuration(
            label="sample configuration II",
            location_type="static",
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
            short_name="Platform2", is_public=True, is_private=False, is_internal=False,
        )
        db.session.add(platform2)

        action1 = PlatformMountAction(
            configuration=configuration1,
            begin_contact=contact,
            parent_platform=None,
            platform=platform1,
            begin_description="Some first action",
            begin_date=fake.date_time(),
        )
        db.session.add(action1)

        action2 = PlatformMountAction(
            configuration=configuration2,
            begin_contact=contact,
            platform=platform2,
            parent_platform=None,
            begin_description="Some other action",
            begin_date=fake.date_time(),
        )
        db.session.add(action2)
        db.session.commit()

        # test only for the first platform
        with self.client:
            url_get_for_platform1 = (
                base_url + f"/platforms/{platform1.id}/platform-mount-actions"
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
                base_url + f"/platforms/{platform2.id}/platform-mount-actions"
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
                base_url + f"/platforms/{platform2.id + 9999}/platform-mount-actions"
            )
            response = self.client.get(
                url_get_for_non_existing, content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 404)

    def test_filtered_by_parent_platform(self):
        """Ensure filter by a specific parent platform works well."""
        configuration1 = Configuration(
            label="sample configuration",
            location_type="static",
            is_public=True,
            is_internal=False,
        )

        configuration2 = Configuration(
            label="sample configuration II",
            location_type="static",
            is_public=True,
            is_internal=False,
        )

        contact = Contact(
            given_name="Nils", family_name="Brinckmann", email="nils@gfz-potsdam.de"
        )

        platform1 = Platform(
            short_name="platform1", is_public=True, is_private=False, is_internal=False,
        )

        platform2 = Platform(
            short_name="Platform2", is_public=True, is_private=False, is_internal=False,
        )

        platform3 = Platform(
            short_name="platform3", is_public=True, is_private=False, is_internal=False,
        )

        platform4 = Platform(
            short_name="Platform4", is_public=True, is_private=False, is_internal=False,
        )

        action1 = PlatformMountAction(
            configuration=configuration1,
            begin_contact=contact,
            parent_platform=platform3,
            platform=platform1,
            begin_description="Some first action",
            begin_date=fake.date_time(),
        )

        action2 = PlatformMountAction(
            configuration=configuration2,
            begin_contact=contact,
            platform=platform2,
            parent_platform=platform4,
            begin_description="Some other action",
            begin_date=fake.date_time(),
        )
        db.session.add_all(
            [
                configuration1,
                configuration2,
                contact,
                platform1,
                platform2,
                platform3,
                platform4,
                action1,
                action2,
            ]
        )
        db.session.commit()

        # test only for the first platform
        with self.client:
            url_get_for_platform1 = (
                base_url + f"/platforms/{platform3.id}/parent-platform-mount-actions"
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
                base_url + f"/platforms/{platform4.id}/parent-platform-mount-actions"
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
                + f"/platforms/{platform2.id + 9999}/parent-platform-mount-actions"
            )
            response = self.client.get(
                url_get_for_non_existing, content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 404)

    def test_get_platform_mount_action(self):
        """Ensure the GET /platform_mount_actions route reachable."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        # no data yet
        self.assertEqual(response.json["data"], [])

    def test_get_platform_mount_action_collection(self):
        """Test retrieve a collection of PlatformMountAction objects."""
        mount_platform_action = add_mount_platform_action_model()
        with self.client:
            response = self.client.get(self.url)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            mount_platform_action.begin_description,
            data["data"][0]["attributes"]["begin_description"],
        )

    def test_post_platfrom_mount_action(self):
        """Create PlatformMountAction."""
        platform = Platform(
            short_name=fake.linux_processor(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        parent_platform = Platform(
            short_name="platform parent-platform",
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        userinfo = generate_userinfo_data()
        begin_contact = Contact(
            given_name=userinfo["given_name"],
            family_name=userinfo["family_name"],
            email=userinfo["email"],
        )
        end_contact = Contact(
            given_name="F. " + userinfo["given_name"],
            family_name="F. " + userinfo["family_name"],
            email="f." + userinfo["email"],
        )
        configuration = generate_configuration_model()
        begin_date = fake.future_datetime()
        p_platform_mount = PlatformMountAction(
            configuration=configuration,
            begin_contact=begin_contact,
            begin_date=begin_date,
            platform=parent_platform,
        )
        db.session.add_all(
            [
                platform,
                parent_platform,
                begin_contact,
                end_contact,
                configuration,
                p_platform_mount,
            ]
        )
        db.session.commit()
        end_date = begin_date + datetime.timedelta(days=2)
        data = {
            "data": {
                "type": self.object_type,
                "attributes": {
                    "begin_description": "Test PlatformMountAction",
                    "begin_date": begin_date.__str__(),
                    "offset_x": str(fake.coordinate()),
                    "offset_y": str(fake.coordinate()),
                    "offset_z": str(fake.coordinate()),
                    "end_date": end_date.__str__(),
                    "end_description": "Test PlatformUnmountAction",
                },
                "relationships": {
                    "platform": {"data": {"type": "platform", "id": platform.id}},
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
            url=f"{self.url}?include=platform,begin_contact,end_contact,parent_platform,configuration",
            data_object=data,
            object_type=self.object_type,
        )
        result_id = response["data"]["id"]
        result_platform_mount_action = (
            db.session.query(PlatformMountAction).filter_by(id=result_id).first()
        )

        msg = "create;platform mount action"
        self.assertEqual(
            msg, result_platform_mount_action.configuration.update_description
        )

    def test_update_platform_mount_action(self):
        """Update PlatformMountAction."""
        mount_platform_action = add_mount_platform_action_model()
        # Don't deal with the constraints for a platform mount for this test.
        mount_platform_action.parent_platform = None
        db.session.add(mount_platform_action)
        db.session.commit()
        mount_platform_action_updated = {
            "data": {
                "type": self.object_type,
                "id": mount_platform_action.id,
                "attributes": {"begin_description": "updated",},
            }
        }
        response = super().update_object(
            url=f"{self.url}/{mount_platform_action.id}",
            data_object=mount_platform_action_updated,
            object_type=self.object_type,
        )
        result_id = response["data"]["id"]
        result_platform_mount_action = (
            db.session.query(PlatformMountAction).filter_by(id=result_id).first()
        )

        msg = "update;platform mount action"
        self.assertEqual(
            msg, result_platform_mount_action.configuration.update_description
        )

    def test_update_platform_mount_action_set_end_contact_to_none(self):
        """Ensure we can set the end contact back to none."""
        mount_platform_action = add_mount_platform_action_model()
        contact = Contact(given_name="d", family_name="u", email="du@localhost")
        mount_platform_action.end_contact = contact
        # Don't deal with the constraints for a platform mount for this test.
        mount_platform_action.parent_platform = None
        db.session.add_all([mount_platform_action, contact])
        db.session.commit()
        mount_platform_action_updated = {
            "data": {
                "type": self.object_type,
                "id": mount_platform_action.id,
                "attributes": {
                    "begin_description": "updated",
                },
                "relationships": {
                    "end_contact": {
                        "data": None,
                    }
                },
            }
        }
        _ = super().update_object(
            url=f"{self.url}/{mount_platform_action.id}",
            data_object=mount_platform_action_updated,
            object_type=self.object_type,
        )

    def test_fail_delete_platform_mount_action(self):
        """Fail to delete PlatformMountAction when not logged in."""
        mount_platform_action = add_mount_platform_action_model()
        with self.client:
            response = self.client.delete(
                f"{self.url}/{mount_platform_action.id}",
                content_type="application/vnd.api+json",
            )
        self.assertNotEqual(response.status_code, 200)

    def test_delete_platform_mount_action(self):
        """Delete PlatformMountAction."""
        mount_platform_action = add_mount_platform_action_model()
        related_configuration_id = mount_platform_action.configuration.id
        with self.client:
            response = self.client.delete(
                f"{self.url}/{mount_platform_action.id}",
                content_type="application/vnd.api+json",
                headers=create_token(),
            )
        self.assertEqual(response.status_code, 200)
        related_configuration = (
            db.session.query(Configuration)
            .filter_by(id=related_configuration_id)
            .first()
        )
        msg = "delete;platform mount action"
        self.assertEqual(msg, related_configuration.update_description)

    def test_http_response_not_found(self):
        """Make sure that the backend responds with 404 HTTP-Code if a resource was not found."""
        url = f"{self.url}/{fake.random_int()}"
        _ = super().http_code_404_when_resource_not_found(url)

    def test_update_platform_mount_action_change_platform_id(self):
        """Make sure platform id can not be changed if the platform doesn't exist."""
        mount_platform_action = add_mount_platform_action_model()
        # Don't deal with the constraints for a platform mount for this test.
        mount_platform_action.parent_platform = None
        db.session.add(mount_platform_action)
        db.session.commit()
        mount_platform_action_updated = {
            "data": {
                "type": self.object_type,
                "id": mount_platform_action.id,
                "attributes": {"begin_description": "updated",},
                "relationships": {
                    "platform": {
                        "data": {
                            "type": "platform",
                            "id": mount_platform_action.platform.id + 10000,
                        }
                    },
                },
            }
        }
        access_headers = create_token()
        with self.client:
            response = self.client.patch(
                f"{self.url}/{mount_platform_action.id}",
                data=json.dumps(mount_platform_action_updated),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
        self.assertEqual(response.status_code, 404)

    def test_update_platform_mount_action_change_configuration_id(self):
        """Make sure configuration id can not be changed if the config doesn't exist."""
        mount_platform_action = add_mount_platform_action_model()
        # Don't deal with the constraints for a platform mount for this test.
        mount_platform_action.parent_platform = None
        db.session.add(mount_platform_action)
        db.session.commit()
        mount_platform_action_updated = {
            "data": {
                "type": self.object_type,
                "id": mount_platform_action.id,
                "attributes": {"begin_description": "updated",},
                "relationships": {
                    "configuration": {
                        "data": {
                            "type": "configuration",
                            "id": mount_platform_action.configuration.id + 1,
                        }
                    },
                },
            }
        }
        access_headers = create_token()
        with self.client:
            response = self.client.patch(
                f"{self.url}/{mount_platform_action.id}",
                data=json.dumps(mount_platform_action_updated),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
        # New configuration id is not associated with an entry.
        self.assertEqual(response.status_code, 404)

    def test_update_platform_mount_action_change_parent_platform_id(self):
        """Make sure parent platform id can not be changed if the parent platform is not mounted before."""
        mount_platform_action = add_mount_platform_action_model()
        mount_platform_action_updated = {
            "data": {
                "type": self.object_type,
                "id": mount_platform_action.id,
                "attributes": {"begin_description": "updated"},
                "relationships": {
                    "parent_platform": {
                        "data": {
                            "type": "platform",
                            "id": mount_platform_action.parent_platform.id + 1,
                        }
                    },
                },
            }
        }
        access_headers = create_token()
        with self.client:
            response = self.client.patch(
                f"{self.url}/{mount_platform_action.id}",
                data=json.dumps(mount_platform_action_updated),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
        self.assertEqual(response.status_code, 409)

    def test_update_platform_mount_action_add_parent_platform_id_if_there_is_no_parent(
        self,
    ):
        """Make sure parent platform id con be add if it is None."""
        p = Platform(
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
        platform_mount_action = PlatformMountAction(
            begin_date=fake.date(),
            begin_description="test mount platform action model",
            offset_x=fake.coordinate(),
            offset_y=fake.coordinate(),
            offset_z=fake.coordinate(),
            platform=p,
        )
        platform_mount_action.configuration = config
        platform_mount_action.begin_contact = c1

        p_p = Platform(
            short_name="platform parent platform",
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        p_platform_mount_action = PlatformMountAction(
            begin_date=platform_mount_action.begin_date,
            begin_description="test mount platform action model",
            offset_x=fake.coordinate(),
            offset_y=fake.coordinate(),
            offset_z=fake.coordinate(),
            platform=p_p,
        )
        p_platform_mount_action.configuration = config
        p_platform_mount_action.begin_contact = c1
        db.session.add_all(
            [p, c1, p_p, config, platform_mount_action, p_platform_mount_action]
        )
        db.session.commit()
        self.assertEqual(platform_mount_action.parent_platform, None)

        mount_platform_action_updated = {
            "data": {
                "type": self.object_type,
                "id": platform_mount_action.id,
                "attributes": {"begin_description": "updated"},
                "relationships": {
                    "parent_platform": {"data": {"type": "platform", "id": p_p.id,}},
                },
            }
        }
        access_headers = create_token()
        with self.client:
            response = self.client.patch(
                f"{self.url}/{platform_mount_action.id}",
                data=json.dumps(mount_platform_action_updated),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
        self.assertEqual(response.status_code, 200)

    def test_update_platform_mount_and_unmount_a_platform(self):
        """Make sure platform con not be unmounted."""
        mount_platform_action = add_mount_platform_action_model()
        # Don't deal with the constraints for a platform mount for this test.
        mount_platform_action.parent_platform = None
        db.session.add(mount_platform_action)
        db.session.commit()
        end_date = mount_platform_action.begin_date + relativedelta(years=+1)
        mount_platform_action_updated = {
            "data": {
                "type": self.object_type,
                "id": mount_platform_action.id,
                "attributes": {"end_date": end_date.isoformat()},
                "relationships": {
                    "end_contact": {
                        "data": {
                            "type": "contact",
                            "id": mount_platform_action.begin_contact.id,
                        }
                    },
                },
            }
        }
        access_headers = create_token()
        with self.client:
            response = self.client.patch(
                f"{self.url}/{mount_platform_action.id}",
                data=json.dumps(mount_platform_action_updated),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
        self.assertEqual(response.status_code, 200)
        data = response.json["data"]
        self.assertEqual(data["attributes"]["end_date"], end_date.isoformat())

    def test_update_platform_mount_and_change_the_time_intervall(self):
        """Make sure platform con not be unmounted."""
        p = Platform(
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
        platform_mount_action_1 = PlatformMountAction(
            begin_date="2022-06-08T07:25:00.782000",
            end_date="2023-06-08T07:25:00.782000",
            begin_description="test mount platform action model",
            offset_x=fake.coordinate(),
            offset_y=fake.coordinate(),
            offset_z=fake.coordinate(),
            platform=p,
        )
        platform_mount_action_1.configuration = config
        platform_mount_action_1.begin_contact = c1
        platform_mount_action_1.end_contact = c1

        platform_mount_action_2 = PlatformMountAction(
            begin_date="2024-06-08T07:25:00.782000",
            begin_description="test mount platform action model",
            offset_x=fake.coordinate(),
            offset_y=fake.coordinate(),
            offset_z=fake.coordinate(),
            platform=p,
        )
        platform_mount_action_2.configuration = config
        platform_mount_action_2.begin_contact = c1

        p_p = Platform(
            short_name="platform parent platform",
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        db.session.add_all(
            [p, c1, p_p, config, platform_mount_action_1, platform_mount_action_2]
        )
        db.session.commit()
        end_date = platform_mount_action_2.begin_date + relativedelta(years=+1)
        # try to change it with an intervall, where the platform mounted.
        mount_platform_action_updated = {
            "data": {
                "type": self.object_type,
                "id": platform_mount_action_2.id,
                "attributes": {
                    "begin_date": "2022-08-08T07:25:00.782000",
                    "end_date": end_date.isoformat(),
                },
                "relationships": {
                    "end_contact": {
                        "data": {
                            "type": "contact",
                            "id": platform_mount_action_2.begin_contact.id,
                        }
                    },
                },
            }
        }
        access_headers = create_token()
        with self.client:
            response = self.client.patch(
                f"{self.url}/{platform_mount_action_2.id}",
                data=json.dumps(mount_platform_action_updated),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
        self.assertEqual(response.status_code, 409)

        # This Should Work as we will deliver a valid time-interval
        mount_platform_action_with_no_conflicts = {
            "data": {
                "type": self.object_type,
                "id": platform_mount_action_2.id,
                "attributes": {
                    "begin_date": "2023-08-08T07:25:00.782000",
                    "end_date": end_date.isoformat(),
                },
                "relationships": {
                    "end_contact": {
                        "data": {
                            "type": "contact",
                            "id": platform_mount_action_2.begin_contact.id,
                        }
                    },
                },
            }
        }
        access_headers = create_token()
        with self.client:
            response = self.client.patch(
                f"{self.url}/{platform_mount_action_2.id}",
                data=json.dumps(mount_platform_action_with_no_conflicts),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
        self.assertEqual(response.status_code, 200)

        # And also if we try to change the time-intervall with a conflict in
        # end_date should not work
        mount_platform_action_with_conflict_on_end_date = {
            "data": {
                "type": self.object_type,
                "id": platform_mount_action_1.id,
                "attributes": {"end_date": "2023-11-08T07:25:00.782000",},
            }
        }
        access_headers = create_token()
        with self.client:
            response = self.client.patch(
                f"{self.url}/{platform_mount_action_1.id}",
                data=json.dumps(mount_platform_action_with_conflict_on_end_date),
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
        self.assertEqual(response.status_code, 409)
