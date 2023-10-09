# SPDX-FileCopyrightText: 2021 - 2023
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Tests for the device attachment endpoints."""

import json
import time
from unittest.mock import patch

from flask import url_for

from project import base_url
from project.api import minio
from project.api.models import Contact, Device, DeviceAttachment, User
from project.api.models.base_model import db
from project.tests.base import BaseTestCase, create_token, fake, query_result_to_list


class TestDeviceAttachmentServices(BaseTestCase):
    """Test device attachments."""

    url = base_url + "/device-attachments"

    def test_post_device_attachment_api(self):
        """Ensure that we can add a device attachment."""
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

        count_device_attachments = (
            db.session.query(DeviceAttachment)
            .filter_by(
                device_id=device.id,
            )
            .count()
        )
        # However, this new device for sure has no attachments
        self.assertEqual(count_device_attachments, 0)

        # Now we can write the request to add a device attachment
        payload = {
            "data": {
                "type": "device_attachment",
                "attributes": {
                    "url": "https://www.gfz-potsdam.de",
                    "label": "GFZ Homepage",
                    "description": "The GFZ homepage",
                },
                "relationships": {
                    "device": {"data": {"type": "device", "id": str(device.id)}}
                },
            }
        }
        with self.client:
            url_post = base_url + "/device-attachments"
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
        # And we want to inspect our attachment list
        device_attachments = query_result_to_list(
            db.session.query(DeviceAttachment).filter_by(
                device_id=device.id,
            )
        )
        # We now have one attachment
        self.assertEqual(len(device_attachments), 1)

        # And it is as we specified it
        device_attachment = device_attachments[0]
        self.assertEqual(device_attachment.url, "https://www.gfz-potsdam.de")
        self.assertEqual(device_attachment.label, "GFZ Homepage")
        self.assertEqual(device_attachment.description, "The GFZ homepage")
        self.assertEqual(device_attachment.device_id, device.id)
        self.assertEqual(
            str(device_attachment.device_id), response.get_json()["data"]["id"]
        )
        msg = "create;attachment"
        self.assertEqual(msg, device_attachment.device.update_description)

    def test_post_device_attachment_api_missing_url(self):
        """Ensure that we don't add a device attachment with missing url."""
        device = Device(
            short_name="Very new device",
            manufacturer_name=fake.pystr(),
            is_public=False,
            is_private=False,
            is_internal=True,
        )
        db.session.add(device)
        db.session.commit()

        # Now we can write the request to add a device attachment
        payload = {
            "data": {
                "type": "device_attachment",
                "attributes": {
                    "url": None,
                    "label": "GFZ Homepage",
                },
                "relationships": {
                    "device": {"data": {"type": "device", "id": str(device.id)}}
                },
            }
        }
        with self.client:
            url_post = base_url + "/device-attachments"
            response = self.client.post(
                url_post,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
                headers=create_token(),
            )
        # it will not work, as we miss an important part (the url)
        # 422 => unprocessable entity
        self.assertEqual(response.status_code, 422)
        count_attachments = (
            db.session.query(DeviceAttachment)
            .filter_by(
                device_id=device.id,
            )
            .count()
        )
        self.assertEqual(count_attachments, 0)

    def test_post_device_attachment_api_missing_device(self):
        """Ensure that we don't add a device attachment with missing device."""
        count_device_attachments_before = db.session.query(DeviceAttachment).count()
        payload = {
            "data": {
                "type": "device_attachment",
                "attributes": {
                    "url": "GFZ",
                    "label": "GFZ Homepage",
                },
                "relationships": {"device": {"data": {"type": "device", "id": None}}},
            }
        }
        with self.client:
            url_post = base_url + "/device-attachments"
            response = self.client.post(
                url_post,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
                headers=create_token(),
            )
        # it will not work, as we miss an important part (the device)
        self.assertEqual(response.status_code, 422)
        count_device_attachments_after = db.session.query(DeviceAttachment).count()
        self.assertEqual(
            count_device_attachments_before, count_device_attachments_after
        )

    def test_get_device_attachment_api(self):
        """Ensure that we can get a list of device attachments."""
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

        device_attachment1 = DeviceAttachment(
            label="GFZ",
            url="https://www.gfz-potsdam.de",
            description="The GFZ homepage",
            device=device1,
        )
        device_attachment2 = DeviceAttachment(
            label="UFZ",
            url="https://www.ufz.de",
            device=device1,
        )
        device_attachment3 = DeviceAttachment(
            label="PIK",
            url="https://www.pik-potsdam.de",
            device=device2,
        )

        db.session.add(device_attachment1)
        db.session.add(device_attachment2)
        db.session.add(device_attachment3)
        db.session.commit()

        all_device_attachments = [
            device_attachment1,
            device_attachment2,
            device_attachment3,
        ]

        with self.client:
            response = self.client.get(
                base_url + "/device-attachments",
                content_type="application/vnd.api+json",
            )
            self.assertEqual(response.status_code, 200)
            payload = response.get_json()

            self.assertEqual(len(payload["data"]), 3)

            device_attachment1_data = None
            for attachment in payload["data"]:
                attachment["id"] in [str(da.id) for da in all_device_attachments]
                attachment["attributes"]["url"] in [
                    da.url for da in all_device_attachments
                ]
                attachment["attributes"]["label"] in [
                    da.label for da in all_device_attachments
                ]

                if attachment["id"] == str(device_attachment1.id):
                    device_attachment1_data = attachment
                    self.assertEqual(
                        attachment["attributes"]["url"], device_attachment1.url
                    )
                    self.assertEqual(
                        attachment["attributes"]["label"], device_attachment1.label
                    )
                    self.assertEqual(
                        attachment["attributes"]["description"], "The GFZ homepage"
                    )
                    # and we want to check the link for the device as well
                    device_link = attachment["relationships"]["device"]["links"][
                        "related"
                    ]
                    resp_device = self.client.get(
                        device_link,
                        content_type="application/vnd.api+json",
                    )
                    self.assertEqual(resp_device.status_code, 200)
                    self.assertEqual(
                        resp_device.get_json()["data"]["id"],
                        str(device_attachment1.device_id),
                    )
                    self.assertEqual(
                        resp_device.get_json()["data"]["attributes"]["short_name"],
                        device_attachment1.device.short_name,
                    )

            self.assertTrue(device_attachment1_data is not None)

            # Now we tested the get request for the list response
            # It is time to check the detail one as well
            response = self.client.get(
                base_url + "/device-attachments/" + str(device_attachment1.id),
                content_type="application/vnd.api+json",
            )
            self.assertEqual(response.status_code, 200)
            # I already tested the response for this attachment
            self.assertEqual(response.get_json()["data"], device_attachment1_data)

            # And now we want to make sure that we already filter the device attachments
            # with a given device id
            response = self.client.get(
                base_url + "/devices/" + str(device1.id) + "/device-attachments",
                content_type="application/vnd.api+json",
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.get_json()["data"]), 2)
            response = self.client.get(
                base_url + "/devices/" + str(device2.id) + "/device-attachments",
                content_type="application/vnd.api+json",
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.get_json()["data"]), 1)

    def test_patch_device_attachment_api(self):
        """Ensure that we can update a device attachment."""
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

        device_attachment1 = DeviceAttachment(
            label="GFZ",
            url="https://www.gfz-potsdam.de",
            device=device1,
        )
        db.session.add(device_attachment1)
        db.session.commit()

        payload = {
            "data": {
                "type": "device_attachment",
                "id": str(device_attachment1.id),
                "attributes": {
                    "label": "UFZ",
                    "url": "https://www.ufz.de",
                },
                "relationships": {
                    "device": {"data": {"type": "device", "id": str(device2.id)}}
                },
            }
        }
        with self.client:
            url_patch = base_url + "/device-attachments/" + str(device_attachment1.id)
            response = self.client.patch(
                url_patch,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
                headers=create_token(),
            )

        self.assertEqual(response.status_code, 200)

        device_attachment_reloaded = (
            db.session.query(DeviceAttachment).filter_by(id=device_attachment1.id).one()
        )
        self.assertEqual(device_attachment_reloaded.url, "https://www.ufz.de")
        self.assertEqual(device_attachment_reloaded.label, "UFZ")
        self.assertEqual(device_attachment_reloaded.device_id, device2.id)
        msg = "update;attachment"
        self.assertEqual(msg, device_attachment_reloaded.device.update_description)

    def test_http_response_not_found(self):
        """Make sure that the backend responds with 404 HTTP-Code if a resource was not found."""
        url = f"{self.url}/{fake.random_int()}"
        _ = super().http_code_404_when_resource_not_found(url)

    def test_post_device_attachment_with_no_label(self):
        """Ensure that we can not add a device attachment without a label."""
        device = Device(
            short_name="anew device",
            manufacturer_name=fake.pystr(),
            is_public=False,
            is_private=True,
            is_internal=False,
        )
        db.session.add(device)
        db.session.commit()
        self.assertTrue(device.id is not None)

        count_device_attachments = (
            db.session.query(DeviceAttachment)
            .filter_by(
                device_id=device.id,
            )
            .count()
        )
        self.assertEqual(count_device_attachments, 0)

        payload = {
            "data": {
                "type": "device_attachment",
                "attributes": {
                    "url": "https://www.ufz.de",
                    "label": None,
                },
                "relationships": {
                    "device": {"data": {"type": "device", "id": str(device.id)}}
                },
            }
        }
        with self.client:
            url_post = base_url + "/device-attachments"
            response = self.client.post(
                url_post,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
                headers=create_token(),
            )
        self.assertEqual(response.status_code, 422)

    def test_post_minio_url(self):
        """
        Test when we post an attachment with a minio url.

        The system should replace the original url with an internal
        one & should set the is_upload entry.
        """
        device = Device(
            short_name="a new device",
            manufacturer_name=fake.pystr(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        db.session.add(device)
        db.session.commit()
        self.assertTrue(device.id is not None)

        with patch.object(minio, "download_endpoint") as mock:
            mock.return_value = "http://minio:8080"
            payload = {
                "data": {
                    "type": "device_attachment",
                    "attributes": {
                        "url": "http://minio:8080/some-bucket/somefile.txt",
                        "label": "Some upload",
                    },
                    "relationships": {
                        "device": {"data": {"type": "device", "id": str(device.id)}}
                    },
                }
            }
            with self.client:
                url_post = base_url + "/device-attachments"
                response = self.client.post(
                    url_post,
                    data=json.dumps(payload),
                    content_type="application/vnd.api+json",
                    headers=create_token(),
                )
        self.assertEqual(response.status_code, 201)
        data = response.json
        attachment = (
            db.session.query(DeviceAttachment).filter_by(id=data["data"]["id"]).first()
        )
        self.assertTrue(attachment.is_upload)
        self.assertTrue(data["data"]["attributes"]["is_upload"])
        self.assertEqual(
            attachment.internal_url, "http://minio:8080/some-bucket/somefile.txt"
        )
        self.assertFalse("internal_url" in data["data"]["attributes"].keys())
        expected_url = url_for(
            "download.get_device_attachment_content",
            id=attachment.id,
            filename="somefile.txt",
            _external=True,
        )
        self.assertEqual(expected_url, attachment.url)
        self.assertEqual(attachment.url, data["data"]["attributes"]["url"])

    def test_patch_url_for_uploads(self):
        """Ensure that we can't change the url for uploaded files."""
        device = Device(
            short_name="a new device",
            manufacturer_name=fake.pystr(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        attachment = DeviceAttachment(
            device=device,
            label="File upload",
            url="http://localhost/.../file",
            internal_url="http://minio/.../file",
        )
        db.session.add_all([device, attachment])
        db.session.commit()

        self.assertTrue(attachment.is_upload)

        payload = {
            "data": {
                "type": "device_attachment",
                "id": str(attachment.id),
                "attributes": {
                    "label": "UFZ",
                    "url": "https://www.ufz.de",
                },
                "relationships": {
                    "device": {"data": {"type": "device", "id": str(device.id)}}
                },
            }
        }
        with self.client:
            url_patch = base_url + "/device-attachments/" + str(attachment.id)
            response = self.client.patch(
                url_patch,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
                headers=create_token(),
            )

        self.assertEqual(response.status_code, 409)

    def test_created_and_updated_fields(self):
        """Ensure we set & update the created & updated metainformation."""
        contact1 = Contact(
            given_name="first", family_name="contact", email="first@contact.org"
        )
        contact2 = Contact(
            given_name="second", family_name="contact", email="second@contact.org"
        )
        user1 = User(contact=contact1, subject=contact1.email, is_superuser=True)
        user2 = User(contact=contact2, subject=contact2.email, is_superuser=True)
        device1 = Device(short_name="dummy device", is_public=True)

        db.session.add_all([contact1, contact2, user1, user2, device1])
        db.session.commit()

        with self.run_requests_as(user1):
            response1 = self.client.post(
                self.url,
                data=json.dumps(
                    {
                        "data": {
                            "type": "device_attachment",
                            "attributes": {
                                "url": "https://gfz-potsdam.de",
                                "label": "GFZ",
                            },
                            "relationships": {
                                "device": {"data": {"type": "device", "id": device1.id}}
                            },
                        }
                    }
                ),
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response1.status_code, 201)
        attachment_id = response1.json["data"]["id"]

        one_second = 1
        time.sleep(one_second)

        with self.run_requests_as(user2):
            response2 = self.client.patch(
                f"{self.url}/{attachment_id}",
                data=json.dumps(
                    {
                        "data": {
                            "type": "device_attachment",
                            "id": attachment_id,
                            "attributes": {
                                "label": "GFZ Landing page",
                            },
                        }
                    }
                ),
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response2.status_code, 200)

        self.assertEqual(
            response1.json["data"]["attributes"]["created_at"],
            response2.json["data"]["attributes"]["created_at"],
        )

        self.assertEqual(
            response1.json["data"]["relationships"]["created_by"]["data"]["id"],
            response2.json["data"]["relationships"]["created_by"]["data"]["id"],
        )
        self.assertEqual(
            response1.json["data"]["relationships"]["created_by"]["data"]["id"],
            str(user1.id),
        )

        self.assertEqual(
            response2.json["data"]["relationships"]["updated_by"]["data"]["id"],
            str(user2.id),
        )

        self.assertTrue(
            # Due to the iso format it is enought to compare them as stirngs
            # here, as 2023-03-14T12:00:00 is < then 2023-03-14T12:00:01.
            response1.json["data"]["attributes"]["updated_at"]
            < response2.json["data"]["attributes"]["updated_at"]
        )
