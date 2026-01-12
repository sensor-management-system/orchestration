# SPDX-FileCopyrightText: 2021 - 2024
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Tests for the platform software update actions api."""

import json

from project import base_url, db
from project.api.models import Contact, Platform, PlatformSoftwareUpdateAction, User
from project.extensions.instances import mqtt
from project.tests.base import (
    BaseTestCase,
    Fixtures,
    create_token,
    fake,
    generate_userinfo_data,
)
from project.tests.models.test_software_update_actions_attachment_model import (
    add_platform_software_update_action_attachment_model,
)
from project.tests.models.test_software_update_actions_model import (
    add_platform_software_update_action_model,
)

fixtures = Fixtures()


@fixtures.register("contact1", scope=lambda: db.session)
def create_contact1():
    """Create a single contact so that it can be used within the tests."""
    result = Contact(
        given_name="first", family_name="contact", email="first.contact@localhost"
    )
    db.session.add(result)
    db.session.commit()
    return result


@fixtures.register("user1", scope=lambda: db.session)
@fixtures.use(["contact1"])
def create_user1(contact1):
    """Create a normal user to use it in the tests."""
    result = User(contact=contact1, subject=contact1.email)
    db.session.add(result)
    db.session.commit()
    return result


class TestPlatformSoftwareUpdateAction(BaseTestCase):
    """Tests for the PlatformSoftwareUpdateAction endpoints."""

    url = base_url + "/platform-software-update-actions"
    object_type = "platform_software_update_action"

    def test_get_platform_software_update_action(self):
        """Ensure the GET /platform_software_update_actions route reachable."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        # no data yet
        self.assertEqual(response.json["data"], [])

    def test_get_platform_software_update_action_collection(self):
        """Test retrieve a collection of PlatformSoftwareUpdateAction objects."""
        platform_software_update_action = add_platform_software_update_action_model()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        # should be only one
        self.assertEqual(response.json["meta"]["count"], 1)
        self.assertEqual(
            response.json["data"][0]["id"], str(platform_software_update_action.id)
        )

    @fixtures.use
    def test_post_platform_software_update_action(self, user1):
        """Create PlatformSoftwareUpdateAction."""
        userinfo = generate_userinfo_data()
        platform = Platform(
            short_name="Platform 111",
            manufacturer_name=fake.company(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )

        contact = Contact(
            given_name=userinfo["given_name"],
            family_name=userinfo["family_name"],
            email=userinfo["email"],
        )
        db.session.add_all([platform, contact])
        db.session.commit()
        data = {
            "data": {
                "type": self.object_type,
                "attributes": {
                    "description": "Test platform_software_update_action",
                    "version": f"v_{fake.pyint()}",
                    "software_type_name": fake.pystr(),
                    "software_type_uri": fake.uri(),
                    "repository_url": fake.url(),
                    "update_date": fake.future_datetime().__str__(),
                },
                "relationships": {
                    "platform": {"data": {"type": "platform", "id": platform.id}},
                    "contact": {"data": {"type": "contact", "id": contact.id}},
                },
            }
        }
        with self.run_requests_as(user1):
            _ = super().add_object(
                url=f"{self.url}?include=platform,contact",
                data_object=data,
                object_type=self.object_type,
            )
        # Reload
        platform = db.session.query(Platform).filter_by(id=platform.id).first()
        self.assertEqual(platform.update_description, "create;software update action")
        # And ensure that we trigger the mqtt.
        mqtt.publish.assert_called_once()
        call_args = mqtt.publish.call_args[0]

        self.expect(call_args[0]).to_equal("sms/post-platform-software-update-action")
        notification_data = json.loads(call_args[1])["data"]
        self.expect(notification_data["type"]).to_equal(
            "platform_software_update_action"
        )
        self.expect(notification_data["attributes"]["description"]).to_equal(
            "Test platform_software_update_action"
        )
        self.expect(str).of(notification_data["id"]).to_match(r"\d+")

    @fixtures.use
    def test_update_platform_software_update_action(self, user1):
        """Update PlatformSoftwareUpdateAction."""
        platform_software_update_action = add_platform_software_update_action_model()
        platform_software_update_action_updated = {
            "data": {
                "type": self.object_type,
                "id": platform_software_update_action.id,
                "attributes": {
                    "description": "updated",
                },
            }
        }
        with self.run_requests_as(user1):
            _ = super().update_object(
                url=f"{self.url}/{platform_software_update_action.id}",
                data_object=platform_software_update_action_updated,
                object_type=self.object_type,
            )
        # Reload
        platform = (
            db.session.query(Platform)
            .filter_by(id=platform_software_update_action.platform_id)
            .first()
        )
        self.assertEqual(platform.update_description, "update;software update action")
        # And ensure that we trigger the mqtt.
        mqtt.publish.assert_called_once()
        call_args = mqtt.publish.call_args[0]

        self.expect(call_args[0]).to_equal("sms/patch-platform-software-update-action")
        notification_data = json.loads(call_args[1])["data"]
        self.expect(notification_data["type"]).to_equal(
            "platform_software_update_action"
        )
        self.expect(notification_data["attributes"]["description"]).to_equal("updated")
        self.expect(notification_data["attributes"]["repository_url"]).to_equal(
            platform_software_update_action.repository_url
        )

    def test_delete_platform_software_update_action(self):
        """Test the deletion of a simple platform software update action."""
        # Those where we include groups, we test in the permissions folder.
        platform_software_update_action = add_platform_software_update_action_model()
        platform_id = platform_software_update_action.platform_id
        _ = super().delete_object(
            url=f"{self.url}/{platform_software_update_action.id}"
        )
        # Reload
        platform = db.session.query(Platform).filter_by(id=platform_id).first()
        self.assertEqual(platform.update_description, "delete;software update action")
        # And ensure that we trigger the mqtt.
        mqtt.publish.assert_called_once()
        call_args = mqtt.publish.call_args[0]

        self.expect(call_args[0]).to_equal("sms/delete-platform-software-update-action")
        self.expect(json.loads).of(call_args[1]).to_equal(
            {
                "data": {
                    "type": "platform_software_update_action",
                    "id": str(platform_software_update_action.id),
                }
            }
        )

    def test_filtered_by_platform(self):
        """Ensure that I can prefilter by a specific platform."""
        contact = Contact(
            given_name="Nils", family_name="Brinckmann", email="nils@gfz-potsdam.de"
        )
        db.session.add(contact)

        platform1 = Platform(
            short_name="platform1",
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        db.session.add(platform1)

        platform2 = Platform(
            short_name="platform2",
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        db.session.add(platform2)

        action1 = PlatformSoftwareUpdateAction(
            contact=contact,
            platform=platform1,
            description="Some first action",
            software_type_name="firmware",
            update_date=fake.date_time(),
        )
        db.session.add(action1)

        action2 = PlatformSoftwareUpdateAction(
            contact=contact,
            platform=platform2,
            description="Some other action",
            software_type_name="sampleScript",
            update_date=fake.date_time(),
        )
        db.session.add(action2)

        db.session.commit()

        # first check to get them all
        with self.client:
            url_get_all = base_url + "/platform-software-update-actions"
            response = self.client.get(
                url_get_all,
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 2)

        # test only for the first platform
        with self.client:
            url_get_for_platform1 = (
                base_url + f"/platforms/{platform1.id}/platform-software-update-actions"
            )
            response = self.client.get(
                url_get_for_platform1, content_type="application/vnd.api+json"
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 1)
        self.assertEqual(
            response.json["data"][0]["attributes"]["description"], "Some first action"
        )

        # and test the second platform
        with self.client:
            url_get_for_platform2 = (
                base_url + f"/platforms/{platform2.id}/platform-software-update-actions"
            )
            response = self.client.get(
                url_get_for_platform2, content_type="application/vnd.api+json"
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 1)
        self.assertEqual(
            response.json["data"][0]["attributes"]["description"], "Some other action"
        )

        # and for a non existing
        with self.client:
            url_get_for_non_existing_platform = (
                base_url
                + f"/platforms/{platform2.id + 9999}/platform-software-update-actions"
            )
            response = self.client.get(
                url_get_for_non_existing_platform,
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 404)

    def test_filtered_by_platform_id(self):
        """Ensure that I can prefilter by filter[platform_id]."""
        contact = Contact(
            given_name="Nils", family_name="Brinckmann", email="nils@gfz-potsdam.de"
        )
        db.session.add(contact)

        platform1 = Platform(
            short_name="platform1",
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        db.session.add(platform1)

        platform2 = Platform(
            short_name="platform2",
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        db.session.add(platform2)

        action1 = PlatformSoftwareUpdateAction(
            contact=contact,
            platform=platform1,
            description="Some first action",
            software_type_name="firmware",
            update_date=fake.date_time(),
        )
        db.session.add(action1)

        action2 = PlatformSoftwareUpdateAction(
            contact=contact,
            platform=platform2,
            description="Some other action",
            software_type_name="sampleScript",
            update_date=fake.date_time(),
        )
        db.session.add(action2)

        db.session.commit()

        # Test only for the first platform
        with self.client:
            url_get_for_platform1 = (
                base_url
                + f"/platform-software-update-actions?filter[platform_id]={platform1.id}"
            )
            response = self.client.get(
                url_get_for_platform1, content_type="application/vnd.api+json"
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 1)
        self.assertEqual(
            response.json["data"][0]["attributes"]["description"], "Some first action"
        )

        # and test the second platform
        with self.client:
            url_get_for_platform2 = (
                base_url
                + f"/platform-software-update-actions?filter[platform_id]={platform2.id}"
            )
            response = self.client.get(
                url_get_for_platform2, content_type="application/vnd.api+json"
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 1)
        self.assertEqual(
            response.json["data"][0]["attributes"]["description"], "Some other action"
        )

        # and for a non existing
        with self.client:
            url_get_for_non_existing_platform = (
                base_url
                + f"/platform-software-update-actions?filter[platform_id]={platform2.id + 9999}"
            )
            response = self.client.get(
                url_get_for_non_existing_platform,
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 0)

    def test_delete_platform_software_update_action_with_attachment_link(self):
        """Delete PlatformSoftwareUpdateAction with an attachment link."""
        platform_software_update_action = (
            add_platform_software_update_action_attachment_model()
        )
        access_headers = create_token()
        with self.client:
            response = self.client.delete(
                f"{self.url}/{platform_software_update_action.id}",
                content_type="application/vnd.api+json",
                headers=access_headers,
            )
        self.assertEqual(response.status_code, 200)

    def test_http_response_not_found(self):
        """Make sure that the backend responds with 404 HTTP-Code if a resource was not found."""
        url = f"{self.url}/{fake.random_int()}"
        _ = super().http_code_404_when_resource_not_found(url)
