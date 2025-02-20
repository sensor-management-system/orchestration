# SPDX-FileCopyrightText: 2021 - 2024
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Tests for the custom field endpoints."""

import json

from project import base_url
from project.api.models import Contact, CustomField, Device, User
from project.api.models.base_model import db
from project.extensions.instances import mqtt
from project.tests.base import (
    BaseTestCase,
    Fixtures,
    create_token,
    fake,
    query_result_to_list,
)

fixtures = Fixtures()


@fixtures.register("public_device1_in_group1", scope=lambda: db.session)
def create_public_device1_in_group1():
    """Create a public device that uses group 1 for permission management."""
    result = Device(
        short_name="public device1",
        is_internal=False,
        is_public=True,
        group_ids=["1"],
    )
    db.session.add(result)
    db.session.commit()
    return result


@fixtures.register("customfield1_of_public_device1_in_group1", scope=lambda: db.session)
@fixtures.use(["public_device1_in_group1"])
def create_customfield1_of_public_device1_in_group1(public_device1_in_group1):
    """Create an customfield for the public device."""
    result = CustomField(
        device=public_device1_in_group1, key="https://gfz-potsdam.de", value="GFZ"
    )
    db.session.add(result)
    db.session.commit()
    return result


@fixtures.register("super_user_contact", scope=lambda: db.session)
def create_super_user_contact():
    """Create a contact that can be used to make a super user."""
    result = Contact(
        given_name="super", family_name="contact", email="super.contact@localhost"
    )
    db.session.add(result)
    db.session.commit()
    return result


@fixtures.register("super_user", scope=lambda: db.session)
@fixtures.use(["super_user_contact"])
def create_super_user(super_user_contact):
    """Create super user to use it in the tests."""
    result = User(
        contact=super_user_contact, subject=super_user_contact.email, is_superuser=True
    )
    db.session.add(result)
    db.session.commit()
    return result


class TestCustomFieldServices(BaseTestCase):
    """Test customfields."""

    url = base_url + "/customfields"

    def test_post_customfield_api(self):
        """Ensure that we can add a custom field."""
        # First we need to make sure that we have a device
        device = Device(
            short_name="Very new device",
            manufacturer_name=fake.pystr(),
            is_public=False,
            is_private=False,
            is_internal=True,
        )
        db.session.add(device)
        db.session.commit()

        # Now as it is saved we can be sure that has an id
        self.assertTrue(device.id is not None)

        count_customfields = (
            db.session.query(CustomField)
            .filter_by(
                device_id=device.id,
            )
            .count()
        )
        # However, this new device for sure has no customfields
        self.assertEqual(count_customfields, 0)

        # Now we can write the request to add a customfield
        payload = {
            "data": {
                "type": "customfield",
                "attributes": {
                    "value": "https://www.gfz-potsdam.de",
                    "key": "GFZ Homepage",
                    "description": "The GFZ homepage",
                },
                "relationships": {
                    "device": {"data": {"type": "device", "id": str(device.id)}}
                },
            }
        }
        with self.client:
            url_post = base_url + "/customfields"
            # You may want to look up self.add_object in the BaseTestCase
            # and compare if something doesn't work anymore
            response = self.client.post(
                url_post,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
                headers=create_token(),
            )
        # We expect that it worked and that we have a new entry
        self.assertEqual(response.status_code, 201)
        # And we want to inspect our customfields list
        customfields = query_result_to_list(
            db.session.query(CustomField).filter_by(
                device_id=device.id,
            )
        )
        # We now have one customfield
        self.assertEqual(len(customfields), 1)

        # And it is as we specified it
        customfield = customfields[0]
        self.assertEqual(customfield.value, "https://www.gfz-potsdam.de")
        self.assertEqual(customfield.key, "GFZ Homepage")
        self.assertEqual(customfield.description, "The GFZ homepage")
        self.assertEqual(customfield.device_id, device.id)
        self.assertEqual(str(customfield.device_id), response.get_json()["data"]["id"])

        reloaded_device = db.session.query(Device).filter_by(id=device.id).first()
        self.assertEqual(reloaded_device.update_description, "create;custom field")

    def test_post_customfield_api_missing_key(self):
        """Ensure that we don't add a customfield with missing key."""
        device = Device(
            short_name="Very new device",
            manufacturer_name=fake.pystr(),
            is_public=False,
            is_private=False,
            is_internal=True,
        )
        db.session.add(device)
        db.session.commit()

        # Now we can write the request to add a customfield
        payload = {
            "data": {
                "type": "customfield",
                "attributes": {
                    "key": None,
                    "value": "GFZ Homepage",
                },
                "relationships": {
                    "device": {"data": {"type": "device", "id": str(device.id)}}
                },
            }
        }
        with self.client:
            url_post = base_url + "/customfields"
            response = self.client.post(
                url_post,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
                headers=create_token(),
            )
        # it will not work, as we miss an important part (the url)
        # 422 => unprocessable entity
        self.assertEqual(response.status_code, 422)
        count_customfields = (
            db.session.query(CustomField)
            .filter_by(
                device_id=device.id,
            )
            .count()
        )
        self.assertEqual(count_customfields, 0)

    def test_post_customfield_api_missing_device(self):
        """Ensure that we don't add a customfield with missing device."""
        count_customfields_before = db.session.query(CustomField).count()
        payload = {
            "data": {
                "type": "customfield",
                "attributes": {
                    "key": "GFZ",
                    "value": "GFZ Homepage",
                },
                "relationships": {"device": {"data": {"type": "device", "id": None}}},
            }
        }
        with self.client:
            url_post = base_url + "/customfields"
            response = self.client.post(
                url_post,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
                headers=create_token(),
            )
        # it will not work, as we miss an important part (the device)
        self.assertEqual(response.status_code, 422)
        count_customfields_after = db.session.query(CustomField).count()
        self.assertEqual(count_customfields_before, count_customfields_after)

    def test_get_customfields_api(self):
        """Ensure that we can get a list of customfields."""
        device1 = Device(
            short_name="Just a device",
            manufacturer_name=fake.pystr(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        device2 = Device(
            short_name="Another device",
            manufacturer_name=fake.pystr(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )

        db.session.add(device1)
        db.session.add(device2)
        db.session.commit()

        customfield1 = CustomField(
            key="GFZ",
            value="https://www.gfz-potsdam.de",
            description="The GFZ homepage",
            device=device1,
        )
        customfield2 = CustomField(
            key="UFZ",
            value="https://www.ufz.de",
            device=device1,
        )
        customfield3 = CustomField(
            key="PIK",
            value="https://www.pik-potsdam.de",
            device=device2,
        )

        db.session.add(customfield1)
        db.session.add(customfield2)
        db.session.add(customfield3)
        db.session.commit()

        all_customfields = [
            customfield1,
            customfield2,
            customfield3,
        ]

        with self.client:
            response = self.client.get(
                base_url + "/customfields",
                content_type="application/vnd.api+json",
            )
            self.assertEqual(response.status_code, 200)
            payload = response.get_json()

            self.assertEqual(len(payload["data"]), 3)

            customfield1_data = None
            for customfield in payload["data"]:
                customfield["id"] in [str(cf.id) for cf in all_customfields]
                customfield["attributes"]["key"] in [cf.key for cf in all_customfields]
                customfield["attributes"]["value"] in [
                    cf.value for cf in all_customfields
                ]

                if customfield["id"] == str(customfield1.id):
                    customfield1_data = customfield
                    self.assertEqual(customfield["attributes"]["key"], customfield1.key)
                    self.assertEqual(
                        customfield["attributes"]["value"], customfield1.value
                    )
                    self.assertEqual(
                        customfield["attributes"]["description"], "The GFZ homepage"
                    )
                    # and we want to check the link for the device as well
                    device_link = customfield["relationships"]["device"]["links"][
                        "related"
                    ]
                    resp_device = self.client.get(
                        device_link,
                        content_type="application/vnd.api+json",
                    )
                    self.assertEqual(resp_device.status_code, 200)
                    self.assertEqual(
                        resp_device.get_json()["data"]["id"],
                        str(customfield1.device_id),
                    )
                    self.assertEqual(
                        resp_device.get_json()["data"]["attributes"]["short_name"],
                        customfield1.device.short_name,
                    )

            self.assertTrue(customfield1_data is not None)

            # Now we tested the get request for the list response
            # It is time to check the detail one as well
            response = self.client.get(
                base_url + "/customfields/" + str(customfield1.id),
                content_type="application/vnd.api+json",
            )
            self.assertEqual(response.status_code, 200)
            # I already tested the response for this customfield
            self.assertEqual(response.get_json()["data"], customfield1_data)

            # And now we want to make sure that we already filter the customfields
            # with a given device id
            response = self.client.get(
                base_url + "/devices/" + str(device1.id) + "/customfields",
                content_type="application/vnd.api+json",
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.get_json()["data"]), 2)
            response = self.client.get(
                base_url + "/devices/" + str(device2.id) + "/customfields",
                content_type="application/vnd.api+json",
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.get_json()["data"]), 1)

    def test_get_customfields_filter_device_id(self):
        """Ensure that we can filter the list by filter[device_id]."""
        device1 = Device(
            short_name="Just a device",
            manufacturer_name=fake.pystr(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        device2 = Device(
            short_name="Another device",
            manufacturer_name=fake.pystr(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )

        db.session.add(device1)
        db.session.add(device2)
        db.session.commit()

        customfield1 = CustomField(
            key="GFZ",
            value="https://www.gfz-potsdam.de",
            description="The GFZ homepage",
            device=device1,
        )
        customfield2 = CustomField(
            key="UFZ",
            value="https://www.ufz.de",
            device=device1,
        )
        customfield3 = CustomField(
            key="PIK",
            value="https://www.pik-potsdam.de",
            device=device2,
        )

        db.session.add(customfield1)
        db.session.add(customfield2)
        db.session.add(customfield3)
        db.session.commit()

        with self.client:
            response = self.client.get(
                base_url + "/customfields?filter[device_id]=" + str(device1.id),
                content_type="application/vnd.api+json",
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.get_json()["data"]), 2)
            response = self.client.get(
                base_url + "/customfields?filter[device_id]=" + str(device2.id),
                content_type="application/vnd.api+json",
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.get_json()["data"]), 1)

    def test_patch_customfield_api_device(self):
        """Ensure that we can update a customfield by changing the device."""
        device1 = Device(
            short_name="Just a device",
            manufacturer_name=fake.pystr(),
            is_public=False,
            is_private=False,
            is_internal=True,
        )
        device2 = Device(
            short_name="Another device",
            manufacturer_name=fake.pystr(),
            is_public=False,
            is_private=False,
            is_internal=True,
        )

        db.session.add(device1)
        db.session.add(device2)
        db.session.commit()

        customfield1 = CustomField(
            key="GFZ",
            value="https://www.gfz-potsdam.de",
            device=device1,
        )
        db.session.add(customfield1)
        db.session.commit()

        payload = {
            "data": {
                "type": "customfield",
                "id": str(customfield1.id),
                "attributes": {
                    "key": "UFZ",
                    "value": "https://www.ufz.de",
                },
                "relationships": {
                    "device": {"data": {"type": "device", "id": str(device2.id)}}
                },
            }
        }
        with self.client:
            url_patch = base_url + "/customfields/" + str(customfield1.id)
            response = self.client.patch(
                url_patch,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
                headers=create_token(),
            )

        self.assertEqual(response.status_code, 200)

        customfield_reloaded = (
            db.session.query(CustomField).filter_by(id=customfield1.id).one()
        )
        self.assertEqual(customfield_reloaded.value, "https://www.ufz.de")
        self.assertEqual(customfield_reloaded.key, "UFZ")
        self.assertEqual(customfield_reloaded.device_id, device2.id)

    def test_patch_customfield_api_value(self):
        """Ensure that we can update a customfield by changing key & value."""
        device = Device(
            short_name="Just a device",
            manufacturer_name=fake.pystr(),
            is_public=False,
            is_private=False,
            is_internal=True,
        )

        db.session.add(device)
        db.session.add(device)
        db.session.commit()

        customfield1 = CustomField(
            key="GFZ",
            value="https://www.gfz-potsdam.de",
            device=device,
        )
        db.session.add(customfield1)
        db.session.commit()

        payload = {
            "data": {
                "type": "customfield",
                "id": str(customfield1.id),
                "attributes": {
                    "key": "UFZ",
                    "value": "https://www.ufz.de",
                },
            }
        }
        with self.client:
            url_patch = base_url + "/customfields/" + str(customfield1.id)
            response = self.client.patch(
                url_patch,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
                headers=create_token(),
            )

        self.assertEqual(response.status_code, 200)

        customfield_reloaded = (
            db.session.query(CustomField).filter_by(id=customfield1.id).one()
        )
        self.assertEqual(customfield_reloaded.value, "https://www.ufz.de")
        self.assertEqual(customfield_reloaded.key, "UFZ")

        reloaded_device = db.session.query(Device).filter_by(id=device.id).first()
        self.assertEqual(reloaded_device.update_description, "update;custom field")

    def test_http_response_not_found(self):
        """Make sure that the backend responds with 404 HTTP-Code if a resource was not found."""
        url = f"{self.url}/{fake.random_int()}"
        _ = super().http_code_404_when_resource_not_found(url)

    @fixtures.use(["super_user", "public_device1_in_group1"])
    def test_post_triggers_mqtt_notification(
        self, super_user, public_device1_in_group1
    ):
        """Ensure that we can post a customfield and publish the notification via mqtt."""
        payload = {
            "data": {
                "type": "customfield",
                "attributes": {
                    "key": "GFZ",
                    "value": "https://gfz-potsdam.de",
                },
                "relationships": {
                    "device": {
                        "data": {
                            "type": "device",
                            "id": str(public_device1_in_group1.id),
                        }
                    }
                },
            }
        }
        with self.run_requests_as(super_user):
            resp = self.client.post(
                self.url,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.expect(resp.status_code).to_equal(201)
        # And ensure that we trigger the mqtt.
        mqtt.mqtt.publish.assert_called_once()
        call_args = mqtt.mqtt.publish.call_args[0]

        self.expect(call_args[0]).to_equal("sms/post-customfield")
        notification_data = json.loads(call_args[1])["data"]
        self.expect(notification_data["type"]).to_equal("customfield")
        self.expect(notification_data["attributes"]["key"]).to_equal("GFZ")
        self.expect(str).of(notification_data["id"]).to_match(r"\d+")

    @fixtures.use(["super_user", "customfield1_of_public_device1_in_group1"])
    def test_patch_triggers_mqtt_notification(
        self, super_user, customfield1_of_public_device1_in_group1
    ):
        """Ensure that we can patch a customfield and publish the notification via mqtt."""
        with self.run_requests_as(super_user):
            resp = self.client.patch(
                f"{self.url}/{customfield1_of_public_device1_in_group1.id}",
                data=json.dumps(
                    {
                        "data": {
                            "type": "customfield",
                            "id": str(customfield1_of_public_device1_in_group1.id),
                            "attributes": {"value": "website"},
                        }
                    }
                ),
                content_type="application/vnd.api+json",
            )
        self.expect(resp.status_code).to_equal(200)
        # And ensure that we trigger the mqtt.
        mqtt.mqtt.publish.assert_called_once()
        call_args = mqtt.mqtt.publish.call_args[0]

        self.expect(call_args[0]).to_equal("sms/patch-customfield")
        notification_data = json.loads(call_args[1])["data"]
        self.expect(notification_data["type"]).to_equal("customfield")
        self.expect(notification_data["attributes"]["value"]).to_equal("website")
        self.expect(notification_data["attributes"]["key"]).to_equal(
            customfield1_of_public_device1_in_group1.key
        )

    @fixtures.use(["super_user", "customfield1_of_public_device1_in_group1"])
    def test_delete_triggers_mqtt_notification(
        self,
        super_user,
        customfield1_of_public_device1_in_group1,
    ):
        """Ensure that we can delete a customfield and publish the notification via mqtt."""
        with self.run_requests_as(super_user):
            resp = self.client.delete(
                f"{self.url}/{customfield1_of_public_device1_in_group1.id}",
            )
        self.expect(resp.status_code).to_equal(200)
        # And ensure that we trigger the mqtt.
        mqtt.mqtt.publish.assert_called_once()
        call_args = mqtt.mqtt.publish.call_args[0]

        self.expect(call_args[0]).to_equal("sms/delete-customfield")
        self.expect(json.loads).of(call_args[1]).to_equal(
            {
                "data": {
                    "type": "customfield",
                    "id": str(customfield1_of_public_device1_in_group1.id),
                }
            }
        )
