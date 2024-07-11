# SPDX-FileCopyrightText: 2021 - 2023
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Tests for the platforms."""

import datetime
import json
import os
from unittest.mock import patch

import pytz
from flask import current_app

from project import base_url
from project.api.models import (
    Configuration,
    Contact,
    Platform,
    PlatformAttachment,
    PlatformMountAction,
    PlatformParameter,
    PlatformParameterValueChangeAction,
    User,
)
from project.api.models.base_model import db
from project.extensions.instances import pidinst
from project.tests.base import (
    BaseTestCase,
    fake,
    generate_userinfo_data,
    test_file_path,
)
from project.tests.models.test_generic_action_attachment_model import (
    add_generic_platform_action_model,
)
from project.tests.models.test_software_update_actions_model import (
    add_platform_software_update_action_model,
)
from project.tests.models.test_user_model import add_user
from project.tests.read_from_json import extract_data_from_json_file


class TestPlatformServices(BaseTestCase):
    """Test Platform Services."""

    platform_url = base_url + "/platforms"
    contact_url = base_url + "/contacts"
    object_type = "platform"
    json_data_url = os.path.join(test_file_path, "drafts", "platforms_test_data.json")

    def setUp(self):
        """Set up some data to test with."""
        super().setUp()
        contact1 = Contact(
            given_name="test", family_name="user", email="test.user@localhost"
        )
        contact2 = Contact(
            given_name="super", family_name="user", email="super.user@localhost"
        )
        self.normal_user = User(subject=contact1.email, contact=contact1)
        self.super_user = User(
            subject=contact2.email, contact=contact2, is_superuser=True
        )
        db.session.add_all([contact1, contact2, self.normal_user, self.super_user])
        db.session.commit()

    def test_add_platform(self):
        """Ensure a new platform can be added to the database."""
        platforms_json = extract_data_from_json_file(self.json_data_url, "platforms")

        platform_data = {"data": {"type": "platform", "attributes": platforms_json[0]}}

        super().add_object(
            url=self.platform_url,
            data_object=platform_data,
            object_type=self.object_type,
        )

    def test_add_platform_contacts_relationship(self):
        """Ensure a new relationship between a platform & contact can be created."""
        userinfo = generate_userinfo_data()
        contact_data = {
            "data": {
                "type": "contact",
                "attributes": {
                    "given_name": userinfo["given_name"],
                    "family_name": userinfo["family_name"],
                    "email": userinfo["email"],
                    "website": fake.url(),
                },
            }
        }
        contact = super().add_object(
            url=self.contact_url, data_object=contact_data, object_type="contact"
        )
        platform_json = extract_data_from_json_file(self.json_data_url, "platforms")

        platform_data = {
            "data": {
                "type": "platform",
                "attributes": platform_json[0],
                "relationships": {
                    "contacts": {
                        "data": [{"type": "contact", "id": contact["data"]["id"]}]
                    },
                },
            }
        }
        data = super().add_object(
            url=self.platform_url + "?include=contacts",
            data_object=platform_data,
            object_type=self.object_type,
        )

        result_contact_ids = [
            x["id"] for x in data["data"]["relationships"]["contacts"]["data"]
        ]

        self.assertIn(contact["data"]["id"], result_contact_ids)

    def test_add_platform_platform_attachment_included(self):
        """Ensure that we can include attachments on getting a platform."""
        # We want to create here a platform, add two platform attachments
        # and want to make sure that we can query the attachments
        # together with the platform itself.

        platform = Platform(
            short_name="platform",
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        db.session.add(platform)

        attachment1 = PlatformAttachment(
            url="www.gfz-potsdam.de", label="GFZ", platform=platform
        )
        db.session.add(attachment1)
        attachment2 = PlatformAttachment(
            url="www.ufz.de", label="UFZ", platform=platform
        )
        db.session.add(attachment2)
        db.session.commit()

        with self.client:
            response = self.client.get(
                base_url
                + "/platforms/"
                + str(platform.id)
                + "?include=platform_attachments",
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 200)

        response_data = response.get_json()

        self.assertEqual(response_data["data"]["id"], str(platform.id))

        attachment_ids = [
            x["id"]
            for x in response_data["data"]["relationships"]["platform_attachments"][
                "data"
            ]
        ]

        self.assertEqual(len(attachment_ids), 2)

        for attachment in [attachment1, attachment2]:
            self.assertIn(str(attachment.id), attachment_ids)

        included_attachments = {}

        for included_entry in response_data["included"]:
            if included_entry["type"] == "platform_attachment":
                attachment_id = included_entry["id"]
                included_attachments[attachment_id] = included_entry

        self.assertEqual(len(included_attachments.keys()), 2)

        for attachment in [attachment1, attachment2]:
            self.assertIn(str(attachment.id), included_attachments.keys())
            self.assertEqual(
                attachment.url,
                included_attachments[str(attachment.id)]["attributes"]["url"],
            )
            self.assertEqual(
                attachment.label,
                included_attachments[str(attachment.id)]["attributes"]["label"],
            )

    def test_http_response_not_found(self):
        """Make sure that the backend responds with 404 HTTP-Code if a resource was not found."""
        url = f"{self.platform_url}/{fake.random_int()}"
        _ = super().http_code_404_when_resource_not_found(url)

    def test_delete_platform_with_a_software_update_action(self):
        """Ensure a platform with software_update_action can be deleted."""
        platform_software_update_action = add_platform_software_update_action_model()
        platform_id = platform_software_update_action.platform_id
        with self.run_requests_as(self.super_user):
            _ = super().try_delete_object_with_status_code(
                url=f"{self.platform_url}/{platform_id}", expected_status_code=200
            )

    def test_delete_platform_with_a_generic_action(self):
        """Ensure a platform with generic action can be deleted."""
        generic_action = add_generic_platform_action_model()
        platform_id = generic_action.platform_id
        with self.run_requests_as(self.super_user):
            _ = super().try_delete_object_with_status_code(
                url=f"{self.platform_url}/{platform_id}", expected_status_code=200
            )

    def test_update_description_after_creation(self):
        """Make sure that update description field is set after post."""
        platforms_json = extract_data_from_json_file(self.json_data_url, "platforms")

        platform_data = {"data": {"type": "platform", "attributes": platforms_json[0]}}

        result = super().add_object(
            url=self.platform_url,
            data_object=platform_data,
            object_type=self.object_type,
        )
        result_id = result["data"]["id"]
        platform = db.session.query(Platform).filter_by(id=result_id).first()

        msg = "create;basic data"
        self.assertEqual(msg, platform.update_description)

    def test_update_description_after_update(self):
        """Make sure that update description field is updated after patch."""
        platforms_json = extract_data_from_json_file(self.json_data_url, "platforms")

        platform_data = {"data": {"type": "platform", "attributes": platforms_json[0]}}

        result = super().add_object(
            url=self.platform_url,
            data_object=platform_data,
            object_type=self.object_type,
        )
        result_id = result["data"]["id"]

        user = add_user()
        user.is_superuser = True
        db.session.add(user)
        db.session.commit()

        with self.run_requests_as(user):
            with self.client:
                resp = self.client.patch(
                    self.platform_url + "/" + result_id,
                    json={
                        "data": {
                            "id": result_id,
                            "type": "platform",
                            "attributes": {
                                "long_name": "updated long name",
                            },
                        }
                    },
                    headers={"Content-Type": "application/vnd.api+json"},
                )
                self.assertEqual(resp.status_code, 200)
        platform = db.session.query(Platform).filter_by(id=result_id).first()

        msg = "update;basic data"
        self.assertEqual(msg, platform.update_description)

    def test_get_list_no_archived_platforms_by_default(self):
        """Ensure that we don't list archived platforms by default."""
        visible_platform = Platform(
            short_name="visible platform",
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        archived_platform = Platform(
            short_name="archived platform",
            is_public=True,
            is_private=False,
            is_internal=False,
            archived=True,
        )
        db.session.add_all([visible_platform, archived_platform])

        with self.client:
            response = self.client.get(self.platform_url)
        self.assertEqual(response.status_code, 200)
        data = response.json["data"]
        # We have only one platform, not the second one
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["attributes"]["short_name"], "visible platform")
        self.assertEqual(data[0]["attributes"]["archived"], False)

    def test_get_list_with_archived_platforms_by_flag(self):
        """Ensure that we can list archived platforms if wished."""
        visible_platform = Platform(
            short_name="visible platform",
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        archived_platform = Platform(
            short_name="archived platform",
            is_public=True,
            is_private=False,
            is_internal=False,
            archived=True,
        )
        db.session.add_all([visible_platform, archived_platform])

        with self.client:
            response = self.client.get(self.platform_url + "?hide_archived=false")
        self.assertEqual(response.status_code, 200)
        data = response.json["data"]
        # We have only one platform, not the second one
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["attributes"]["short_name"], "visible platform")
        self.assertEqual(data[0]["attributes"]["archived"], False)
        self.assertEqual(data[1]["attributes"]["short_name"], "archived platform")
        self.assertEqual(data[1]["attributes"]["archived"], True)

    def test_delete_with_parameter_and_values(self):
        """
        Ensure we can delete a platform with parameter & associated values.

        We don't want users to delete parameters with associated values,
        but once we need to delete the complete platform it should be
        possible.
        """
        visible_platform = Platform(
            short_name="visible platform",
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        parameter = PlatformParameter(
            platform=visible_platform,
            label="specialvalue",
            description="some value",
            unit_name="count",
            unit_uri="http://foo/count",
        )
        value = PlatformParameterValueChangeAction(
            platform_parameter=parameter,
            contact=self.super_user.contact,
            date=datetime.datetime(2023, 5, 2, 15, 30, 00, tzinfo=pytz.utc),
            value="3",
        )
        db.session.add_all([visible_platform, parameter, value])
        db.session.commit()

        url = f"{self.platform_url}/{visible_platform.id}"
        with self.run_requests_as(self.super_user):
            response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)

    def test_update_external_b2inst_metadata(self):
        """Make sure that we ask the system to update the external metadata after a patch."""
        platforms_json = extract_data_from_json_file(self.json_data_url, "platforms")

        platform_data = {"data": {"type": "platform", "attributes": platforms_json[0]}}
        result = super().add_object(
            url=self.platform_url,
            data_object=platform_data,
            object_type=self.object_type,
        )
        result_id = result["data"]["id"]

        user = add_user()
        user.is_superuser = True
        db.session.add(user)
        db.session.commit()

        platform = db.session.query(Platform).filter_by(id=result_id).first()
        platform.b2inst_record_id = "123"
        db.session.add(platform)
        db.session.commit()

        current_app.config.update({"B2INST_TOKEN": "123"})

        with self.run_requests_as(user):
            with self.client:
                with patch.object(
                    pidinst, "update_external_metadata"
                ) as update_external_metadata:
                    update_external_metadata.return_value = None
                    resp = self.client.patch(
                        self.platform_url + "/" + result_id,
                        json={
                            "data": {
                                "id": result_id,
                                "type": "platform",
                                "attributes": {
                                    "long_name": "updated long name",
                                },
                            }
                        },
                        headers={"Content-Type": "application/vnd.api+json"},
                    )
                    update_external_metadata.assert_called_once()
                    self.assertEqual(
                        update_external_metadata.call_args.args[0].id, platform.id
                    )
        self.assertEqual(resp.status_code, 200)

    def test_update_external_b2inst_metadata_for_configuration(self):
        """Make sure that we ask the system to update the external metadata for configuration after a patch."""
        platforms_json = extract_data_from_json_file(self.json_data_url, "platforms")

        platform_data = {"data": {"type": "platform", "attributes": platforms_json[0]}}
        result = super().add_object(
            url=self.platform_url,
            data_object=platform_data,
            object_type=self.object_type,
        )
        result_id = result["data"]["id"]

        user = add_user()
        user.is_superuser = True
        db.session.add(user)
        db.session.commit()

        platform = db.session.query(Platform).filter_by(id=result_id).first()
        configuration = Configuration(label="Test config", b2inst_record_id="42")
        platform_mount_action = PlatformMountAction(
            configuration=configuration,
            platform=platform,
            begin_contact=user.contact,
            begin_date=datetime.datetime(2022, 1, 1, 0, 0, 0, tzinfo=pytz.utc),
            offset_x=0,
            offset_y=0,
            offset_z=0,
        )
        db.session.add_all([configuration, platform_mount_action])

        current_app.config.update({"B2INST_TOKEN": "123"})

        with self.run_requests_as(user):
            with self.client:
                with patch.object(
                    pidinst, "update_external_metadata"
                ) as update_external_metadata:
                    update_external_metadata.return_value = None
                    resp = self.client.patch(
                        self.platform_url + "/" + result_id,
                        json={
                            "data": {
                                "id": result_id,
                                "type": "platform",
                                "attributes": {
                                    "long_name": "updated long name",
                                },
                            }
                        },
                        headers={"Content-Type": "application/vnd.api+json"},
                    )
                    update_external_metadata.assert_called_once()
                    self.assertEqual(
                        update_external_metadata.call_args.args[0].id, configuration.id
                    )
        self.assertEqual(resp.status_code, 200)

    def test_post_keywords(self):
        """Ensure we can post keywords."""
        platform_data = {
            "data": {
                "type": "platform",
                "attributes": {
                    "short_name": "A test platform",
                    "keywords": ["word1", "word2"],
                    "is_public": True,
                    "is_private": False,
                    "is_internal": False,
                },
            }
        }
        with self.run_requests_as(self.super_user):
            response = self.client.post(
                self.platform_url,
                data=json.dumps(platform_data),
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 201)
        result = response.json

        result_id = result["data"]["id"]
        platform = db.session.query(Platform).filter_by(id=result_id).first()
        self.assertEqual(["word1", "word2"], platform.keywords)
        self.assertEqual(["word1", "word2"], result["data"]["attributes"]["keywords"])

    def test_countries(self):
        """Ensure that we can set a country."""
        with self.run_requests_as(self.super_user):
            response = self.client.post(
                self.platform_url,
                data=json.dumps(
                    {
                        "data": {
                            "type": "platform",
                            "attributes": {
                                "short_name": "test platform",
                                "country": "Germany",
                                "is_internal": False,
                                "is_private": False,
                                "is_public": True,
                            },
                        }
                    }
                ),
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 201)
        platform_id = response.json["data"]["id"]

        get_list_response = self.client.get(self.platform_url)
        self.assertEqual(get_list_response.status_code, 200)
        self.assertEqual(
            get_list_response.json["data"][0]["attributes"]["country"], "Germany"
        )

        get_one_response = self.client.get(f"{self.platform_url}/{platform_id}")
        self.assertEqual(get_one_response.status_code, 200)
        self.assertEqual(
            get_one_response.json["data"]["attributes"]["country"], "Germany"
        )
