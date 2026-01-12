# SPDX-FileCopyrightText: 2021 - 2024
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Tests for the generic device actions api."""

import json
import os

from project import base_url, db
from project.api.models import (
    Contact,
    Device,
    GenericDeviceAction,
    PermissionGroup,
    PermissionGroupMembership,
    User,
)
from project.api.models.mixin import utc_now
from project.extensions.instances import mqtt
from project.tests.base import (
    BaseTestCase,
    fake,
    generate_userinfo_data,
    test_file_path,
)


class TestGenericDeviceAction(BaseTestCase):
    """Tests for the GenericDeviceAction endpoints."""

    url = base_url + "/generic-device-actions"
    platform_url = base_url + "/platforms"
    device_url = base_url + "/devices"
    contact_url = base_url + "/contacts"
    object_type = "generic_device_action"
    json_data_url = os.path.join(
        test_file_path, "drafts", "configurations_test_data.json"
    )
    device_json_data_url = os.path.join(
        test_file_path, "drafts", "devices_test_data.json"
    )
    platform_json_data_url = os.path.join(
        test_file_path, "drafts", "platforms_test_data.json"
    )

    def setUp(self):
        """Set some data up for the tests."""
        super().setUp()
        contact = Contact(
            given_name="normal", family_name="contact", email="normal.contact@localhost"
        )
        self.normal_user = User(contact=contact, subject=contact.email)
        self.permission_group = PermissionGroup(name="group1", entitlement="group1")
        self.membership = PermissionGroupMembership(
            user=self.normal_user, permission_group=self.permission_group
        )
        db.session.add_all(
            [contact, self.normal_user, self.permission_group, self.membership]
        )
        db.session.commit()

    def test_get_generic_device_action(self):
        """Ensure the GET /generic_device_action route behaves correctly."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        # no data yet
        self.assertEqual(response.json["data"], [])

    def test_add_generic_device_action(self):
        """Ensure POST a new generic device action can be added to the database."""
        data = self.make_generic_device_action_data()
        with self.run_requests_as(self.normal_user):
            result = super().add_object(
                url=f"{self.url}?include=device,contact",
                data_object=data,
                object_type=self.object_type,
            )
            device_id = result["data"]["relationships"]["device"]["data"]["id"]
            device = db.session.query(Device).filter_by(id=device_id).first()
            self.assertEqual(device.update_description, "create;action")
        # And ensure that we trigger the mqtt.
        mqtt.publish.assert_called_once()
        call_args = mqtt.publish.call_args[0]

        self.expect(call_args[0]).to_equal("sms/post-generic-device-action")
        notification_data = json.loads(call_args[1])["data"]
        self.expect(notification_data["type"]).to_equal("generic_device_action")
        self.expect(notification_data["attributes"]["description"]).to_equal(
            data["data"]["attributes"]["description"]
        )
        self.expect(str).of(notification_data["id"]).to_match(r"\d+")

    def make_generic_device_action_data(self):
        """
        Create the json payload for a generic device action.

        This also creates some associated objects in the database.
        """
        group_id_test_user_is_member_in_2 = [self.permission_group.id]

        device = Device(
            short_name=fake.pystr(),
            manufacturer_name=fake.company(),
            is_public=True,
            is_private=False,
            is_internal=False,
            group_ids=group_id_test_user_is_member_in_2,
        )
        db.session.add(device)
        db.session.commit()
        userinfo = generate_userinfo_data()
        contact = Contact(
            given_name=userinfo["given_name"],
            family_name=userinfo["family_name"],
            email=userinfo["email"],
            website=fake.url(),
        )
        db.session.add(contact)
        db.session.commit()
        data = {
            "data": {
                "type": self.object_type,
                "attributes": {
                    "description": fake.paragraph(nb_sentences=3),
                    "action_type_name": fake.lexify(
                        text="Random type: ??????????", letters="ABCDE"
                    ),
                    "action_type_uri": fake.uri(),
                    "begin_date": utc_now().__str__(),
                },
                "relationships": {
                    "device": {"data": {"type": "device", "id": device.id}},
                    "contact": {"data": {"type": "contact", "id": contact.id}},
                },
            }
        }
        return data

    def test_update_generic_device_action(self):
        """Ensure a generic_device_action can be updated."""
        generic_device_action_data = self.make_generic_device_action_data()
        with self.run_requests_as(self.normal_user):
            generic_device_action = super().add_object(
                url=f"{self.url}?include=device,contact",
                data_object=generic_device_action_data,
                object_type=self.object_type,
            )
            userinfo = generate_userinfo_data()
            contact = Contact(
                given_name=userinfo["given_name"],
                family_name=userinfo["family_name"],
                email=userinfo["email"],
            )
            db.session.add(contact)
            db.session.commit()
            new_description = fake.paragraph(nb_sentences=3)
            new_data = {
                "data": {
                    "type": self.object_type,
                    "id": generic_device_action["data"]["id"],
                    "attributes": {
                        "description": new_description,
                        "action_type_name": fake.lexify(
                            text="Random type: ??????????", letters="ABCDE"
                        ),
                        "action_type_uri": fake.uri(),
                        "begin_date": utc_now().__str__(),
                    },
                    "relationships": {
                        "device": {"data": {"type": "device", "id": "1"}},
                        "contact": {"data": {"type": "contact", "id": contact.id}},
                    },
                }
            }
            result = super().update_object(
                url=f"{self.url}/{generic_device_action['data']['id']}?include=device,contact",
                data_object=new_data,
                object_type=self.object_type,
            )
            device_id = result["data"]["relationships"]["device"]["data"]["id"]
            device = db.session.query(Device).filter_by(id=device_id).first()
            self.assertEqual(device.update_description, "update;action")
        # And ensure that we trigger the mqtt.
        mqtt.publish.assert_called()
        call_args = mqtt.publish.call_args[0]

        self.expect(call_args[0]).to_equal("sms/patch-generic-device-action")
        notification_data = json.loads(call_args[1])["data"]
        self.expect(notification_data["type"]).to_equal("generic_device_action")
        self.expect(notification_data["attributes"]["description"]).to_equal(
            new_description
        )
        self.expect(
            notification_data["relationships"]["device"]["data"]["id"]
        ).to_equal(str(device.id))

    def test_delete_generic_device_action(self):
        """Ensure a generic_device_action can be deleted."""
        data = self.make_generic_device_action_data()
        with self.run_requests_as(self.normal_user):
            obj = super().add_object(
                url=f"{self.url}?include=device,contact",
                data_object=data,
                object_type=self.object_type,
            )
            device_id = obj["data"]["relationships"]["device"]["data"]["id"]
            response = self.client.delete(
                f"{self.url}/{obj['data']['id']}",
                content_type="application/vnd.api+json",
            )
            self.assertEqual(response.status_code, 200)
            device = db.session.query(Device).filter_by(id=device_id).first()
            self.assertEqual(device.update_description, "delete;action")
        # And ensure that we trigger the mqtt.
        mqtt.publish.assert_called()
        call_args = mqtt.publish.call_args[0]

        self.expect(call_args[0]).to_equal("sms/delete-generic-device-action")
        self.expect(json.loads).of(call_args[1]).to_equal(
            {
                "data": {
                    "type": "generic_device_action",
                    "id": str(obj["data"]["id"]),
                }
            }
        )

    def test_filtered_by_device(self):
        """Ensure that I can prefilter by a specific device."""
        device1 = Device(
            short_name="sample device",
            manufacturer_name=fake.company(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        db.session.add(device1)
        device2 = Device(
            short_name="sample device II",
            manufacturer_name=fake.company(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        db.session.add(device2)

        contact = Contact(
            given_name="Nils", family_name="Brinckmann", email="nils@gfz-potsdam.de"
        )
        db.session.add(contact)

        action1 = GenericDeviceAction(
            device=device1,
            contact=contact,
            description="Some first action",
            begin_date=fake.date_time(),
            action_type_name="DeviceActivity",
        )
        db.session.add(action1)

        action2 = GenericDeviceAction(
            device=device2,
            contact=contact,
            description="Some other action",
            begin_date=fake.date_time(),
            action_type_name="DeviceActivity",
        )
        db.session.add(action2)
        db.session.commit()

        # first check to get them all
        with self.client:
            url_get_all = base_url + "/generic-device-actions"
            response = self.client.get(
                url_get_all, content_type="application/vnd.api+json"
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 2)

        # then test only for the first device
        with self.client:
            url_get_for_device1 = (
                base_url + f"/devices/{device1.id}/generic-device-actions"
            )
            response = self.client.get(
                url_get_for_device1, content_type="application/vnd.api+json"
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 1)
        self.assertEqual(
            response.json["data"][0]["attributes"]["description"], "Some first action"
        )

        # and test the second device
        with self.client:
            url_get_for_device2 = (
                base_url + f"/devices/{device2.id}/generic-device-actions"
            )
            response = self.client.get(
                url_get_for_device2, content_type="application/vnd.api+json"
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 1)
        self.assertEqual(
            response.json["data"][0]["attributes"]["description"], "Some other action"
        )

        # and for a non existing
        with self.client:
            url_get_for_non_existing_device = (
                base_url + f"/devices/{device2.id + 9999}/generic-device-actions"
            )
            response = self.client.get(
                url_get_for_non_existing_device, content_type="application/vnd.api+json"
            )
        self.assertEqual(response.status_code, 404)

    def test_filtered_by_device_id(self):
        """Ensure that I can prefilter using filter[device_id]."""
        device1 = Device(
            short_name="sample device",
            manufacturer_name=fake.company(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        db.session.add(device1)
        device2 = Device(
            short_name="sample device II",
            manufacturer_name=fake.company(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        db.session.add(device2)

        contact = Contact(
            given_name="Nils", family_name="Brinckmann", email="nils@gfz-potsdam.de"
        )
        db.session.add(contact)

        action1 = GenericDeviceAction(
            device=device1,
            contact=contact,
            description="Some first action",
            begin_date=fake.date_time(),
            action_type_name="DeviceActivity",
        )
        db.session.add(action1)

        action2 = GenericDeviceAction(
            device=device2,
            contact=contact,
            description="Some other action",
            begin_date=fake.date_time(),
            action_type_name="DeviceActivity",
        )
        db.session.add(action2)
        db.session.commit()

        with self.client:
            url_get_for_device1 = (
                base_url + f"/generic-device-actions?filter[device_id]={device1.id}"
            )
            response = self.client.get(
                url_get_for_device1, content_type="application/vnd.api+json"
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 1)
        self.assertEqual(
            response.json["data"][0]["attributes"]["description"], "Some first action"
        )

        # and test the second device
        with self.client:
            url_get_for_device2 = (
                base_url + f"/generic-device-actions?filter[device_id]={device2.id}"
            )
            response = self.client.get(
                url_get_for_device2, content_type="application/vnd.api+json"
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 1)
        self.assertEqual(
            response.json["data"][0]["attributes"]["description"], "Some other action"
        )

        # and for a non existing
        with self.client:
            url_get_for_non_existing_device = (
                base_url
                + f"/generic-device-actions?filter[device_id]={device2.id + 9999}"
            )
            response = self.client.get(
                url_get_for_non_existing_device, content_type="application/vnd.api+json"
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["data"]), 0)

    # def test_fail_delete_generic_device_action_with_link_to_an_attachment(self):
    #     """Ensure the generic_device_action and the link to the attachment can be deleted."""
    #     generic_device_action_attachment = add_generic_device_action_attachment_model()
    #     access_headers = create_token()
    #     with self.client:
    #         response = self.client.delete(
    #             f"{self.url}/{generic_device_action_attachment.id}",
    #             content_type="application/vnd.api+json",
    #             headers=access_headers,
    #         )
    #     self.assertNotEqual(response.status_code, 200)

    def test_http_response_not_found(self):
        """Make sure that the backend responds with 404 HTTP-Code if a resource was not found."""
        url = f"{self.url}/{fake.random_int()}"
        _ = super().http_code_404_when_resource_not_found(url)
