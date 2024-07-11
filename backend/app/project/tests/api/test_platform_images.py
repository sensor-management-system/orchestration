# SPDX-FileCopyrightText: 2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Tests for the platform image endpoints."""

import json
from unittest.mock import patch

from project import base_url
from project.api.models import (
    Contact,
    Platform,
    PlatformAttachment,
    PlatformImage,
    User,
)
from project.api.models.base_model import db
from project.extensions.idl.models.user_account import UserAccount
from project.extensions.instances import idl
from project.tests.base import BaseTestCase, Fixtures

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


@fixtures.register("contact2", scope=lambda: db.session)
def create_contact2():
    """Create a second contact so that it can be used within the tests."""
    result = Contact(
        given_name="second", family_name="contact", email="second.contact@localhost"
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


@fixtures.register("user1", scope=lambda: db.session)
@fixtures.use(["contact1"])
def create_user1(contact1):
    """Create a normal user to use it in the tests."""
    result = User(contact=contact1, subject=contact1.email)
    db.session.add(result)
    db.session.commit()
    return result


@fixtures.register("user2", scope=lambda: db.session)
@fixtures.use(["contact2"])
def create_user2(contact2):
    """Create a second user to use it in the tests."""
    result = User(contact=contact2, subject=contact2.email)
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


@fixtures.register("public_platform1_in_group1", scope=lambda: db.session)
def create_public_platform1_in_group1():
    """Create a public platform that uses group 1 for permission management."""
    result = Platform(
        short_name="public platform1",
        is_private=False,
        is_internal=False,
        is_public=True,
        group_ids=["1"],
    )
    db.session.add(result)
    db.session.commit()
    return result


@fixtures.register("public_platform2_in_group1", scope=lambda: db.session)
def create_public_platform2_in_group1():
    """Create another public platform that uses group 1 for permission management."""
    result = Platform(
        short_name="public platform2",
        is_private=False,
        is_internal=False,
        is_public=True,
        group_ids=["1"],
    )
    db.session.add(result)
    db.session.commit()
    return result


@fixtures.register("internal_platform1_in_group1", scope=lambda: db.session)
def create_internal_platform1_in_group1():
    """Create a internal platform that uses group 1 for permission management."""
    result = Platform(
        short_name="internal platform1",
        is_private=False,
        is_internal=True,
        is_public=False,
        group_ids=["1"],
    )
    db.session.add(result)
    db.session.commit()
    return result


@fixtures.register("private_platform_of_user1", scope=lambda: db.session)
@fixtures.use(["user1"])
def create_private_platform_of_user1(user1):
    """Create a private platform that user1 created."""
    result = Platform(
        short_name="private platform of user1",
        created_by=user1,
        is_private=True,
        is_internal=False,
        is_public=False,
    )
    db.session.add(result)
    db.session.commit()
    return result


@fixtures.register(
    "attachment1_of_public_platform1_in_group1", scope=lambda: db.session
)
@fixtures.use(["public_platform1_in_group1"])
def create_attachment1_of_public_platform1_in_group1(public_platform1_in_group1):
    """Create an attachment of public_platform1."""
    result = PlatformAttachment(
        platform=public_platform1_in_group1,
        label="specialvalue",
        url="http://locaohost/static/image1.png",
    )
    db.session.add(result)
    db.session.commit()
    return result


@fixtures.register(
    "attachment2_of_public_platform1_in_group1", scope=lambda: db.session
)
@fixtures.use(["public_platform1_in_group1"])
def create_attachment2_of_public_platform1_in_group1(public_platform1_in_group1):
    """Create another attachment of public_platform1."""
    result = PlatformAttachment(
        platform=public_platform1_in_group1,
        label="second attachment",
        url="http://locaohost/static/image2.png",
    )
    db.session.add(result)
    db.session.commit()
    return result


@fixtures.register(
    "attachment1_of_public_platform2_in_group1", scope=lambda: db.session
)
@fixtures.use(["public_platform2_in_group1"])
def create_attachment1_of_public_platform2_in_group1(public_platform2_in_group1):
    """Create an attachment of public_platform2."""
    result = PlatformAttachment(
        platform=public_platform2_in_group1,
        label="specialvalue",
        url="http://locaohost/static/image1.png",
    )
    db.session.add(result)
    db.session.commit()
    return result


@fixtures.register(
    "attachment1_of_internal_platform1_in_group1", scope=lambda: db.session
)
@fixtures.use(["internal_platform1_in_group1"])
def create_attachment1_of_internal_platform1_in_group1(internal_platform1_in_group1):
    """Create an attachment of internal_platform1."""
    result = PlatformAttachment(
        platform=internal_platform1_in_group1,
        label="specialvalue",
        url="http://locaohost/static/image1.png",
    )
    db.session.add(result)
    db.session.commit()
    return result


@fixtures.register("attachment1_of_private_platform_of_user1", scope=lambda: db.session)
@fixtures.use(["private_platform_of_user1"])
def create_attachment1_of_private_platform_of_user1(private_platform_of_user1):
    """Create an attachment of private platform of user1."""
    result = PlatformAttachment(
        platform=private_platform_of_user1,
        label="specialvalue",
        url="http://locaohost/static/image1.png",
    )
    db.session.add(result)
    db.session.commit()
    return result


@fixtures.register(
    "image1_of_attachment1_of_public_platform1_in_group1", scope=lambda: db.session
)
@fixtures.use(["attachment1_of_public_platform1_in_group1"])
def create_image1_of_attachment1_of_public_platform1_in_group1(
    attachment1_of_public_platform1_in_group1,
):
    """Create an image of attachment1 on public_platform1."""
    result = PlatformImage(
        platform=attachment1_of_public_platform1_in_group1.platform,
        attachment=attachment1_of_public_platform1_in_group1,
        order_index=100,
    )
    db.session.add(result)
    db.session.commit()
    return result


@fixtures.register(
    "image1_of_attachment1_of_public_platform2_in_group1", scope=lambda: db.session
)
@fixtures.use(["attachment1_of_public_platform2_in_group1"])
def create_image1_of_attachment1_of_public_platform2_in_group1(
    attachment1_of_public_platform2_in_group1,
):
    """Create an image of attachment1 on public_platform2."""
    result = PlatformImage(
        platform=attachment1_of_public_platform2_in_group1.platform,
        attachment=attachment1_of_public_platform2_in_group1,
        order_index=100,
    )
    db.session.add(result)
    db.session.commit()
    return result


@fixtures.register(
    "image1_of_attachment1_of_internal_platform1_in_group1", scope=lambda: db.session
)
@fixtures.use(["attachment1_of_internal_platform1_in_group1"])
def create_image1_of_attachment1_of_internal_platform1_in_group1(
    attachment1_of_internal_platform1_in_group1,
):
    """Create an image of attachment1 on internal_platform1."""
    result = PlatformImage(
        platform=attachment1_of_internal_platform1_in_group1.platform,
        attachment=attachment1_of_internal_platform1_in_group1,
        order_index=100,
    )
    db.session.add(result)
    db.session.commit()
    return result


@fixtures.register(
    "image1_of_attachment1_of_private_platform_of_user1", scope=lambda: db.session
)
@fixtures.use(["attachment1_of_private_platform_of_user1"])
def create_image1_of_attachment1_of_private_platform_of_user1(
    attachment1_of_private_platform_of_user1,
):
    """Create an image of attachment1 on private platform of user1."""
    result = PlatformImage(
        platform=attachment1_of_private_platform_of_user1.platform,
        attachment=attachment1_of_private_platform_of_user1,
        order_index=100,
    )
    db.session.add(result)
    db.session.commit()
    return result


class TestPlatformImageServices(BaseTestCase):
    """Tests for the platform images endpoints."""

    url = base_url + "/platform-images"

    def test_get_list_empty(self):
        """Ensure that we query the url and get an empty list if there is no data."""
        resp = self.client.get(self.url)
        self.expect(resp.status_code).to_equal(200)

    @fixtures.use(
        [
            "image1_of_attachment1_of_public_platform1_in_group1",
        ]
    )
    def test_get_list_for_public_platform_no_user(
        self, image1_of_attachment1_of_public_platform1_in_group1
    ):
        """Ensure we get public platform images without user."""
        resp = self.client.get(self.url)
        self.expect(resp.status_code).to_equal(200)
        self.expect(resp.json["data"]).to_have_length(1)

        self.expect(resp.json["data"][0]["id"]).to_equal(
            str(image1_of_attachment1_of_public_platform1_in_group1.id)
        )
        self.expect(resp.json["data"][0]["type"]).to_equal("platform_image")
        self.expect(resp.json["data"][0]["attributes"]["order_index"]).to_equal(
            image1_of_attachment1_of_public_platform1_in_group1.order_index
        )
        self.expect(
            resp.json["data"][0]["attributes"]["created_at"]
        ).to_be_a_datetime_string()
        self.expect(
            resp.json["data"][0]["attributes"]["updated_at"]
        ).to_be_a_datetime_string()

        self.expect(
            resp.json["data"][0]["relationships"]["platform"]["data"]["id"]
        ).to_equal(
            str(image1_of_attachment1_of_public_platform1_in_group1.platform_id),
        )
        self.expect(
            resp.json["data"][0]["relationships"]["platform"]["data"]["type"]
        ).to_equal("platform")
        self.expect(
            resp.json["data"][0]["relationships"]["attachment"]["data"]["id"]
        ).to_equal(
            str(image1_of_attachment1_of_public_platform1_in_group1.attachment_id),
        )
        self.expect(
            resp.json["data"][0]["relationships"]["attachment"]["data"]["type"]
        ).to_equal("platform_attachment")

    @fixtures.use(
        [
            "image1_of_attachment1_of_internal_platform1_in_group1",
        ]
    )
    def test_get_list_for_internal_platform_no_user(
        self, image1_of_attachment1_of_internal_platform1_in_group1
    ):
        """Ensure we don't include data for internal platforms if we don't have a user."""
        resp = self.client.get(self.url)
        self.expect(resp.status_code).to_equal(200)
        self.expect(resp.json["data"]).to_have_length(0)

    @fixtures.use(
        [
            "user1",
            "image1_of_attachment1_of_internal_platform1_in_group1",
        ]
    )
    def test_get_list_for_internal_platform_with_user(
        self, user1, image1_of_attachment1_of_internal_platform1_in_group1
    ):
        """Ensure we include data for internal platforms if we have a user."""
        with self.run_requests_as(user1):
            resp = self.client.get(self.url)
            self.expect(resp.status_code).to_equal(200)
            self.expect(resp.json["data"]).to_have_length(1)

    @fixtures.use(["user1", "image1_of_attachment1_of_private_platform_of_user1"])
    def test_get_list_for_private_platform_with_creator(
        self,
        user1,
        image1_of_attachment1_of_private_platform_of_user1,
    ):
        """Ensure we include data of private platforms if we are the creator of the platform."""
        with self.run_requests_as(user1):
            resp = self.client.get(self.url)
        self.expect(resp.status_code).to_equal(200)
        self.expect(resp.json["data"]).to_have_length(1)

    @fixtures.use(["user2", "image1_of_attachment1_of_private_platform_of_user1"])
    def test_get_list_for_private_platform_different_user(
        self,
        user2,
        image1_of_attachment1_of_private_platform_of_user1,
    ):
        """Ensure we don't include data of private platforms if we are not the creator of the platform."""
        with self.run_requests_as(user2):
            resp = self.client.get(self.url)
        self.expect(resp.status_code).to_equal(200)
        self.expect(resp.json["data"]).to_have_length(0)

    @fixtures.use(["super_user", "image1_of_attachment1_of_private_platform_of_user1"])
    def test_get_list_for_private_platform_with_super_user(
        self,
        super_user,
        image1_of_attachment1_of_private_platform_of_user1,
    ):
        """Ensure we include data of private platforms if we are a super user."""
        with self.run_requests_as(super_user):
            resp = self.client.get(self.url)
        self.expect(resp.status_code).to_equal(200)
        self.expect(resp.json["data"]).to_have_length(1)

    @fixtures.use(["image1_of_attachment1_of_private_platform_of_user1"])
    def test_get_list_for_private_platform_without_user(
        self,
        image1_of_attachment1_of_private_platform_of_user1,
    ):
        """Ensure we don't data of private platforms if we are the creator of the platform."""
        resp = self.client.get(self.url)
        self.expect(resp.status_code).to_equal(200)
        self.expect(resp.json["data"]).to_have_length(0)

    def test_get_one_non_existing(self):
        """Ensure that we get an 404 for a non existing platform image."""
        resp = self.client.get(self.url + "/12345678901234")
        self.expect(resp.status_code).to_equal(404)

    @fixtures.use(["image1_of_attachment1_of_public_platform1_in_group1"])
    def test_get_one_for_public_platform_no_user(
        self, image1_of_attachment1_of_public_platform1_in_group1
    ):
        """Ensure we get the images of public platforms even without user."""
        resp = self.client.get(
            f"{self.url}/{image1_of_attachment1_of_public_platform1_in_group1.id}"
        )
        self.expect(resp.status_code).to_equal(200)
        self.expect(resp.json["data"]["id"]).to_equal(
            str(image1_of_attachment1_of_public_platform1_in_group1.id)
        )
        self.expect(resp.json["data"]["type"]).to_equal("platform_image")
        self.expect(resp.json["data"]["attributes"]["order_index"]).to_equal(
            image1_of_attachment1_of_public_platform1_in_group1.order_index
        )
        self.expect(
            resp.json["data"]["attributes"]["created_at"]
        ).to_be_a_datetime_string()
        self.expect(
            resp.json["data"]["attributes"]["updated_at"]
        ).to_be_a_datetime_string()
        self.expect(
            resp.json["data"]["relationships"]["platform"]["data"]["id"]
        ).to_equal(
            str(image1_of_attachment1_of_public_platform1_in_group1.platform_id),
        )
        self.expect(
            resp.json["data"]["relationships"]["platform"]["data"]["type"]
        ).to_equal("platform")
        self.expect(
            resp.json["data"]["relationships"]["attachment"]["data"]["id"]
        ).to_equal(
            str(image1_of_attachment1_of_public_platform1_in_group1.attachment_id),
        )
        self.expect(
            resp.json["data"]["relationships"]["attachment"]["data"]["type"]
        ).to_equal("platform_attachment")

    @fixtures.use(["image1_of_attachment1_of_internal_platform1_in_group1"])
    def test_get_one_for_internal_platform_no_user(
        self, image1_of_attachment1_of_internal_platform1_in_group1
    ):
        """Ensure we get an 401 for intenral platform without a user."""
        resp = self.client.get(
            f"{self.url}/{image1_of_attachment1_of_internal_platform1_in_group1.id}"
        )
        self.expect(resp.status_code).to_equal(401)

    @fixtures.use(["user1", "image1_of_attachment1_of_internal_platform1_in_group1"])
    def test_get_one_for_internal_platform_with_user(
        self, user1, image1_of_attachment1_of_internal_platform1_in_group1
    ):
        """Ensure we can access data for internal platforms when we have a user."""
        with self.run_requests_as(user1):
            resp = self.client.get(
                f"{self.url}/{image1_of_attachment1_of_internal_platform1_in_group1.id}"
            )
        self.expect(resp.status_code).to_equal(200)

    @fixtures.use(["user1", "image1_of_attachment1_of_private_platform_of_user1"])
    def test_get_one_for_private_platform_with_creator(
        self, user1, image1_of_attachment1_of_private_platform_of_user1
    ):
        """Ensure we can access data of private platforms if we are the creator of the platform."""
        with self.run_requests_as(user1):
            resp = self.client.get(
                f"{self.url}/{image1_of_attachment1_of_private_platform_of_user1.id}"
            )
        self.expect(resp.status_code).to_equal(200)

    @fixtures.use(["user2", "image1_of_attachment1_of_private_platform_of_user1"])
    def test_get_one_for_private_platform_with_different_user(
        self, user2, image1_of_attachment1_of_private_platform_of_user1
    ):
        """Ensure we reaise 403 error if we try to access private data with different user."""
        with self.run_requests_as(user2):
            resp = self.client.get(
                f"{self.url}/{image1_of_attachment1_of_private_platform_of_user1.id}"
            )
        self.expect(resp.status_code).to_equal(403)

    @fixtures.use(["super_user", "image1_of_attachment1_of_private_platform_of_user1"])
    def test_get_one_for_private_platform_with_super_user(
        self, super_user, image1_of_attachment1_of_private_platform_of_user1
    ):
        """Ensure we can access private data with the super user."""
        with self.run_requests_as(super_user):
            resp = self.client.get(
                f"{self.url}/{image1_of_attachment1_of_private_platform_of_user1.id}"
            )
        self.expect(resp.status_code).to_equal(200)

    @fixtures.use(["image1_of_attachment1_of_private_platform_of_user1"])
    def test_get_one_for_private_platform_without_user(
        self, image1_of_attachment1_of_private_platform_of_user1
    ):
        """Ensure we raise 401 if we try to access private data without a user."""
        resp = self.client.get(
            f"{self.url}/{image1_of_attachment1_of_private_platform_of_user1.id}"
        )
        self.expect(resp.status_code).to_equal(401)

    @fixtures.use(
        [
            "image1_of_attachment1_of_public_platform1_in_group1",
            "image1_of_attachment1_of_public_platform2_in_group1",
        ]
    )
    def test_get_list_prefilted_by_platform(
        self,
        image1_of_attachment1_of_public_platform1_in_group1,
        image1_of_attachment1_of_public_platform2_in_group1,
    ):
        """Ensure we can prefilter by platform."""
        platform1 = image1_of_attachment1_of_public_platform1_in_group1.platform
        platform2 = image1_of_attachment1_of_public_platform2_in_group1.platform

        resp1 = self.client.get(f"{base_url}/platforms/{platform1.id}/platform-images")
        self.expect(resp1.status_code).to_equal(200)
        self.expect(resp1.json["data"]).to_have_length(1)
        self.expect(resp1.json["data"][0]["id"]).to_equal(
            str(image1_of_attachment1_of_public_platform1_in_group1.id)
        )

        resp2 = self.client.get(f"{base_url}/platforms/{platform2.id}/platform-images")
        self.expect(resp2.status_code).to_equal(200)
        self.expect(resp2.json["data"]).to_have_length(1)
        self.expect(resp2.json["data"][0]["id"]).to_equal(
            str(image1_of_attachment1_of_public_platform2_in_group1.id)
        )

        resp3 = self.client.get(f"{base_url}/platforms/9999999999/platform-images")
        self.expect(resp3.status_code).to_equal(404)

    @fixtures.use(
        [
            "image1_of_attachment1_of_public_platform1_in_group1",
            "image1_of_attachment1_of_public_platform2_in_group1",
        ]
    )
    def test_get_list_prefilted_by_filter_platform_id(
        self,
        image1_of_attachment1_of_public_platform1_in_group1,
        image1_of_attachment1_of_public_platform2_in_group1,
    ):
        """Ensure we can prefilter by filter[platform_id]."""
        platform1 = image1_of_attachment1_of_public_platform1_in_group1.platform
        platform2 = image1_of_attachment1_of_public_platform2_in_group1.platform

        resp1 = self.client.get(f"{self.url}?filter[platform_id]={platform1.id}")
        self.expect(resp1.status_code).to_equal(200)
        self.expect(resp1.json["data"]).to_have_length(1)
        self.expect(resp1.json["data"][0]["id"]).to_equal(
            str(image1_of_attachment1_of_public_platform1_in_group1.id)
        )

        resp2 = self.client.get(f"{self.url}?filter[platform_id]={platform2.id}")
        self.expect(resp2.status_code).to_equal(200)
        self.expect(resp2.json["data"]).to_have_length(1)
        self.expect(resp2.json["data"][0]["id"]).to_equal(
            str(image1_of_attachment1_of_public_platform2_in_group1.id)
        )

        resp3 = self.client.get(f"{self.url}?filter[platform_id]=999999999")
        self.expect(resp3.status_code).to_equal(200)
        self.expect(resp3.json["data"]).to_have_length(0)

    @fixtures.use(["attachment1_of_public_platform1_in_group1"])
    def test_post_no_user(self, attachment1_of_public_platform1_in_group1):
        """Ensure we can't post if we don't have a user."""
        payload = {
            "data": {
                "type": "platform_image",
                "attributes": {
                    "order_index": 10,
                },
                "relationships": {
                    "platform": {
                        "data": {
                            "id": str(
                                attachment1_of_public_platform1_in_group1.platform_id
                            ),
                            "type": "platform",
                        },
                    },
                    "attachment": {
                        "data": {
                            "id": str(attachment1_of_public_platform1_in_group1.id),
                            "type": "platform_attachment",
                        },
                    },
                },
            }
        }
        resp = self.client.post(self.url, data=json.dumps(payload))
        self.expect(resp.status_code).to_equal(401)

    @fixtures.use(["user1", "attachment1_of_public_platform1_in_group1"])
    def test_post_member(self, user1, attachment1_of_public_platform1_in_group1):
        """Ensure we can post of we are a member of one of the groups."""
        payload = {
            "data": {
                "type": "platform_image",
                "attributes": {
                    "order_index": 10,
                },
                "relationships": {
                    "platform": {
                        "data": {
                            "id": str(
                                attachment1_of_public_platform1_in_group1.platform_id
                            ),
                            "type": "platform",
                        },
                    },
                    "attachment": {
                        "data": {
                            "id": str(attachment1_of_public_platform1_in_group1.id),
                            "type": "platform_attachment",
                        },
                    },
                },
            }
        }
        with self.run_requests_as(user1):
            with patch.object(idl, "get_all_permission_groups_for_a_user") as mock:
                mock.return_value = UserAccount(
                    id=user1.subject,
                    username=user1.subject,
                    administrated_permission_groups=[],
                    membered_permission_groups=attachment1_of_public_platform1_in_group1.platform.group_ids,
                )
                resp = self.client.post(
                    self.url,
                    data=json.dumps(payload),
                    content_type="application/vnd.api+json",
                )
        self.expect(resp.status_code).to_equal(201)
        self.expect(resp.json["data"]["attributes"]["order_index"]).to_equal(10)
        self.expect(
            resp.json["data"]["relationships"]["created_by"]["data"]["id"]
        ).to_equal(str(user1.id))

        reloaded_platform = (
            db.session.query(Platform)
            .filter_by(id=attachment1_of_public_platform1_in_group1.platform_id)
            .first()
        )
        # Reason here is that the images can be seen as basic data.
        # At least they are on the panel in the sms frontend.
        self.expect(reloaded_platform.update_description).to_equal("update;basic data")

    @fixtures.use(["user1", "attachment1_of_public_platform1_in_group1"])
    def test_post_admin(self, user1, attachment1_of_public_platform1_in_group1):
        """Ensure we can post of we are an admin of one of the groups."""
        payload = {
            "data": {
                "type": "platform_image",
                "attributes": {
                    "order_index": 10,
                },
                "relationships": {
                    "platform": {
                        "data": {
                            "id": str(
                                attachment1_of_public_platform1_in_group1.platform_id
                            ),
                            "type": "platform",
                        },
                    },
                    "attachment": {
                        "data": {
                            "id": str(attachment1_of_public_platform1_in_group1.id),
                            "type": "platform_attachment",
                        },
                    },
                },
            }
        }
        with self.run_requests_as(user1):
            with patch.object(idl, "get_all_permission_groups_for_a_user") as mock:
                mock.return_value = UserAccount(
                    id=user1.subject,
                    username=user1.subject,
                    administrated_permission_groups=attachment1_of_public_platform1_in_group1.platform.group_ids,
                    membered_permission_groups=[],
                )
                resp = self.client.post(
                    self.url,
                    data=json.dumps(payload),
                    content_type="application/vnd.api+json",
                )
        self.expect(resp.status_code).to_equal(201)

    @fixtures.use(["user1", "attachment1_of_private_platform_of_user1"])
    def test_post_private_creator(
        self, user1, attachment1_of_private_platform_of_user1
    ):
        """Ensure we can post of we are the owner of a private platform."""
        payload = {
            "data": {
                "type": "platform_image",
                "attributes": {
                    "order_index": 10,
                },
                "relationships": {
                    "platform": {
                        "data": {
                            "id": str(
                                attachment1_of_private_platform_of_user1.platform_id
                            ),
                            "type": "platform",
                        },
                    },
                    "attachment": {
                        "data": {
                            "id": str(attachment1_of_private_platform_of_user1.id),
                            "type": "platform_attachment",
                        },
                    },
                },
            }
        }
        with self.run_requests_as(user1):
            resp = self.client.post(
                self.url,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.expect(resp.status_code).to_equal(201)

    @fixtures.use(["user2", "attachment1_of_private_platform_of_user1"])
    def test_post_private_other_user(
        self, user2, attachment1_of_private_platform_of_user1
    ):
        """Ensure we can't post if we are not the owner of a private platform."""
        payload = {
            "data": {
                "type": "platform_image",
                "attributes": {
                    "order_index": 10,
                },
                "relationships": {
                    "platform": {
                        "data": {
                            "id": str(
                                attachment1_of_private_platform_of_user1.platform_id
                            ),
                            "type": "platform",
                        },
                    },
                    "attachment": {
                        "data": {
                            "id": str(attachment1_of_private_platform_of_user1.id),
                            "type": "platform_attachment",
                        },
                    },
                },
            }
        }
        with self.run_requests_as(user2):
            resp = self.client.post(
                self.url,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.expect(resp.status_code).to_equal(403)

    @fixtures.use(["super_user", "attachment1_of_private_platform_of_user1"])
    def test_post_private_super_user(
        self, super_user, attachment1_of_private_platform_of_user1
    ):
        """Ensure we can post for a private platform if we are super user."""
        payload = {
            "data": {
                "type": "platform_image",
                "attributes": {
                    "order_index": 10,
                },
                "relationships": {
                    "platform": {
                        "data": {
                            "id": str(
                                attachment1_of_private_platform_of_user1.platform_id
                            ),
                            "type": "platform",
                        },
                    },
                    "attachment": {
                        "data": {
                            "id": str(attachment1_of_private_platform_of_user1.id),
                            "type": "platform_attachment",
                        },
                    },
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

    @fixtures.use(["user1", "attachment1_of_public_platform1_in_group1"])
    def test_post_not_in_group(self, user1, attachment1_of_public_platform1_in_group1):
        """Ensure we can't post of we are not a member of one of the groups."""
        payload = {
            "data": {
                "type": "platform_image",
                "attributes": {
                    "order_index": 10,
                },
                "relationships": {
                    "platform": {
                        "data": {
                            "id": str(
                                attachment1_of_public_platform1_in_group1.platform_id
                            ),
                            "type": "platform",
                        },
                    },
                    "attachment": {
                        "data": {
                            "id": str(attachment1_of_public_platform1_in_group1.id),
                            "type": "platform_attachment",
                        },
                    },
                },
            }
        }
        with self.run_requests_as(user1):
            with patch.object(idl, "get_all_permission_groups_for_a_user") as mock:
                mock.return_value = UserAccount(
                    id=user1.subject,
                    username=user1.subject,
                    administrated_permission_groups=[],
                    membered_permission_groups=[],
                )
                resp = self.client.post(
                    self.url,
                    data=json.dumps(payload),
                    content_type="application/vnd.api+json",
                )
        self.expect(resp.status_code).to_equal(403)

    @fixtures.use(["super_user", "attachment1_of_public_platform1_in_group1"])
    def test_post_not_in_group_super_user(
        self, super_user, attachment1_of_public_platform1_in_group1
    ):
        """Ensure we can post of we are super user."""
        payload = {
            "data": {
                "type": "platform_image",
                "attributes": {
                    "order_index": 10,
                },
                "relationships": {
                    "platform": {
                        "data": {
                            "id": str(
                                attachment1_of_public_platform1_in_group1.platform_id
                            ),
                            "type": "platform",
                        },
                    },
                    "attachment": {
                        "data": {
                            "id": str(attachment1_of_public_platform1_in_group1.id),
                            "type": "platform_attachment",
                        },
                    },
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

    @fixtures.use(["super_user", "attachment1_of_public_platform1_in_group1"])
    def test_post_archived(self, super_user, attachment1_of_public_platform1_in_group1):
        """Ensure not even super users can post for archived platforms."""
        platform = attachment1_of_public_platform1_in_group1.platform
        platform.archived = True
        db.session.add(platform)
        db.session.commit()

        payload = {
            "data": {
                "type": "platform_image",
                "attributes": {
                    "order_index": 10,
                },
                "relationships": {
                    "platform": {
                        "data": {
                            "id": str(platform.id),
                            "type": "platform",
                        },
                    },
                    "attachment": {
                        "data": {
                            "id": str(attachment1_of_public_platform1_in_group1.id),
                            "type": "platform_attachment",
                        },
                    },
                },
            }
        }
        with self.run_requests_as(super_user):
            resp = self.client.post(
                self.url,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.expect(resp.status_code).to_equal(403)

    @fixtures.use(
        [
            "super_user",
            "attachment1_of_public_platform1_in_group1",
            "attachment2_of_public_platform1_in_group1",
        ]
    )
    def test_post_missing_order_index(
        self,
        super_user,
        attachment1_of_public_platform1_in_group1,
        attachment2_of_public_platform1_in_group1,
    ):
        """Ensure we can post without the order index."""
        payload1 = {
            "data": {
                "type": "platform_image",
                "attributes": {},
                "relationships": {
                    "platform": {
                        "data": {
                            "id": str(
                                attachment1_of_public_platform1_in_group1.platform_id
                            ),
                            "type": "platform",
                        },
                    },
                    "attachment": {
                        "data": {
                            "id": str(attachment1_of_public_platform1_in_group1.id),
                            "type": "platform_attachment",
                        },
                    },
                },
            }
        }
        with self.run_requests_as(super_user):
            resp1 = self.client.post(
                self.url,
                data=json.dumps(payload1),
                content_type="application/vnd.api+json",
            )
        self.expect(resp1.status_code).to_equal(201)

        order_index1 = resp1.json["data"]["attributes"]["order_index"]
        self.expect(order_index1).to_have_type(int)
        self.expect(order_index1).to_be_greater_than(0)

        # And if we do that for another platform attachment, then we
        # should get a larger order_index.
        payload2 = {
            "data": {
                "type": "platform_image",
                "attributes": {},
                "relationships": {
                    "platform": {
                        "data": {
                            "id": str(
                                attachment2_of_public_platform1_in_group1.platform_id
                            ),
                            "type": "platform",
                        },
                    },
                    "attachment": {
                        "data": {
                            "id": str(attachment2_of_public_platform1_in_group1.id),
                            "type": "platform_attachment",
                        },
                    },
                },
            }
        }
        with self.run_requests_as(super_user):
            resp2 = self.client.post(
                self.url,
                data=json.dumps(payload2),
                content_type="application/vnd.api+json",
            )
        self.expect(resp2.status_code).to_equal(201)

        order_index2 = resp2.json["data"]["attributes"]["order_index"]
        self.expect(order_index2).to_be_greater_than(order_index1)

    @fixtures.use(["super_user", "attachment1_of_public_platform1_in_group1"])
    def test_post_missing_platform(
        self, super_user, attachment1_of_public_platform1_in_group1
    ):
        """Ensure we can't post if we don't provide a platform."""
        payload = {
            "data": {
                "type": "platform_image",
                "attributes": {
                    "order_index": 10,
                },
                "relationships": {
                    "platform": {
                        "data": None,
                    },
                    "attachment": {
                        "data": {
                            "id": str(attachment1_of_public_platform1_in_group1.id),
                            "type": "platform_attachment",
                        },
                    },
                },
            }
        }
        with self.run_requests_as(super_user):
            resp = self.client.post(
                self.url,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.expect(resp.status_code).to_equal(422)

    @fixtures.use(["super_user", "public_platform1_in_group1"])
    def test_post_missing_attachment(self, super_user, public_platform1_in_group1):
        """Ensure we can't post if we don't provide an attachment."""
        payload = {
            "data": {
                "type": "platform_image",
                "attributes": {
                    "order_index": 10,
                },
                "relationships": {
                    "platform": {
                        "data": {
                            "id": str(public_platform1_in_group1.id),
                            "type": "platform",
                        }
                    },
                    "attachment": {"data": None},
                },
            }
        }
        with self.run_requests_as(super_user):
            resp = self.client.post(
                self.url,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.expect(resp.status_code).to_equal(422)

    @fixtures.use(["super_user", "image1_of_attachment1_of_public_platform1_in_group1"])
    def test_post_for_attachment_that_doesnt_belong_to_platform(
        self, super_user, image1_of_attachment1_of_public_platform1_in_group1
    ):
        """Ensure we can't use attachments for images that don't belong to the platform."""
        payload = {
            "data": {
                "type": "platform_image",
                "attributes": {
                    "order_index": 10,
                },
                "relationships": {
                    "platform": {
                        "data": {
                            "id": str(
                                image1_of_attachment1_of_public_platform1_in_group1.platform_id
                            ),
                            "type": "platform",
                        }
                    },
                    "attachment": {
                        "data": {
                            "id": str(
                                image1_of_attachment1_of_public_platform1_in_group1.attachment_id
                            ),
                            "type": "platform_attachment",
                        }
                    },
                },
            }
        }
        with self.run_requests_as(super_user):
            resp = self.client.post(
                self.url,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.expect(resp.status_code).to_equal(409)

    @fixtures.use(
        [
            "super_user",
            "attachment1_of_public_platform1_in_group1",
            "public_platform2_in_group1",
        ]
    )
    def test_post_image_for_same_attachment_and_platform_again(
        self,
        super_user,
        attachment1_of_public_platform1_in_group1,
        public_platform2_in_group1,
    ):
        """Ensure we can't add an image if we have one already for the combination of platform and attachment."""
        payload = {
            "data": {
                "type": "platform_image",
                "attributes": {
                    "order_index": 10,
                },
                "relationships": {
                    "platform": {
                        "data": {
                            "id": str(public_platform2_in_group1.id),
                            "type": "platform",
                        }
                    },
                    "attachment": {
                        "data": {
                            "id": str(attachment1_of_public_platform1_in_group1.id),
                            "type": "platform_attachment",
                        }
                    },
                },
            }
        }
        with self.run_requests_as(super_user):
            resp = self.client.post(
                self.url,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.expect(resp.status_code).to_equal(409)

    @fixtures.use(["image1_of_attachment1_of_public_platform1_in_group1"])
    def test_patch_for_public_platform_no_user(
        self, image1_of_attachment1_of_public_platform1_in_group1
    ):
        """Ensure we can't patch without a user."""
        payload = {
            "data": {
                "type": "platform_image",
                "id": str(image1_of_attachment1_of_public_platform1_in_group1.id),
                "attributes": {
                    "order_index": 20,
                },
            }
        }

        resp = self.client.patch(
            f"{self.url}/{image1_of_attachment1_of_public_platform1_in_group1.id}",
            data=json.dumps(payload),
            content_type="application/vnd.api+json",
        )
        self.expect(resp.status_code).to_equal(401)

    @fixtures.use(["user1", "image1_of_attachment1_of_public_platform1_in_group1"])
    def test_patch_for_public_platform_member(
        self, user1, image1_of_attachment1_of_public_platform1_in_group1
    ):
        """Ensure we can patch if we are a member of one of the groups."""
        payload = {
            "data": {
                "type": "platform_image",
                "id": str(image1_of_attachment1_of_public_platform1_in_group1.id),
                "attributes": {
                    "order_index": 20,
                },
            }
        }

        with self.run_requests_as(user1):
            with patch.object(idl, "get_all_permission_groups_for_a_user") as mock:
                mock.return_value = UserAccount(
                    id=user1.subject,
                    username=user1.subject,
                    administrated_permission_groups=[],
                    membered_permission_groups=image1_of_attachment1_of_public_platform1_in_group1.platform.group_ids,
                )
                resp = self.client.patch(
                    f"{self.url}/{image1_of_attachment1_of_public_platform1_in_group1.id}",
                    data=json.dumps(payload),
                    content_type="application/vnd.api+json",
                )
        self.expect(resp.status_code).to_equal(200)
        self.expect(resp.json["data"]["attributes"]["order_index"]).to_equal(20)

        self.expect(
            resp.json["data"]["relationships"]["updated_by"]["data"]["id"]
        ).to_equal(str(user1.id))

        reloaded_platform = (
            db.session.query(Platform)
            .filter_by(
                id=image1_of_attachment1_of_public_platform1_in_group1.platform_id
            )
            .first()
        )
        # Reason here is that the images can be seen as basic data.
        # At least they are on the panel in the sms frontend.
        self.expect(reloaded_platform.update_description).to_equal("update;basic data")

    @fixtures.use(["user1", "image1_of_attachment1_of_public_platform1_in_group1"])
    def test_patch_for_public_platform_admin(
        self, user1, image1_of_attachment1_of_public_platform1_in_group1
    ):
        """Ensure we can patch if we are an admin of one of the groups."""
        payload = {
            "data": {
                "type": "platform_image",
                "id": str(image1_of_attachment1_of_public_platform1_in_group1.id),
                "attributes": {
                    "order_index": 20,
                },
            }
        }
        group_ids = (
            image1_of_attachment1_of_public_platform1_in_group1.platform.group_ids
        )

        with self.run_requests_as(user1):
            with patch.object(idl, "get_all_permission_groups_for_a_user") as mock:
                mock.return_value = UserAccount(
                    id=user1.subject,
                    username=user1.subject,
                    administrated_permission_groups=group_ids,
                    membered_permission_groups=[],
                )
                resp = self.client.patch(
                    f"{self.url}/{image1_of_attachment1_of_public_platform1_in_group1.id}",
                    data=json.dumps(payload),
                    content_type="application/vnd.api+json",
                )
        self.expect(resp.status_code).to_equal(200)

    @fixtures.use(["user1", "image1_of_attachment1_of_public_platform1_in_group1"])
    def test_patch_for_public_platform_no_member(
        self, user1, image1_of_attachment1_of_public_platform1_in_group1
    ):
        """Ensure we can't patch if we are an not a member of one of the groups."""
        payload = {
            "data": {
                "type": "platform_image",
                "id": str(image1_of_attachment1_of_public_platform1_in_group1.id),
                "attributes": {
                    "order_index": 20,
                },
            }
        }

        with self.run_requests_as(user1):
            with patch.object(idl, "get_all_permission_groups_for_a_user") as mock:
                mock.return_value = UserAccount(
                    id=user1.subject,
                    username=user1.subject,
                    administrated_permission_groups=[],
                    membered_permission_groups=[],
                )
                resp = self.client.patch(
                    f"{self.url}/{image1_of_attachment1_of_public_platform1_in_group1.id}",
                    data=json.dumps(payload),
                    content_type="application/vnd.api+json",
                )
        self.expect(resp.status_code).to_equal(403)

    @fixtures.use(["super_user", "image1_of_attachment1_of_public_platform1_in_group1"])
    def test_patch_for_public_platform_no_member_super_user(
        self, super_user, image1_of_attachment1_of_public_platform1_in_group1
    ):
        """Ensure we can patch if we are super user."""
        payload = {
            "data": {
                "type": "platform_image",
                "id": str(image1_of_attachment1_of_public_platform1_in_group1.id),
                "attributes": {
                    "order_index": 20,
                },
            }
        }

        with self.run_requests_as(super_user):
            resp = self.client.patch(
                f"{self.url}/{image1_of_attachment1_of_public_platform1_in_group1.id}",
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.expect(resp.status_code).to_equal(200)

    @fixtures.use(["user1", "image1_of_attachment1_of_private_platform_of_user1"])
    def test_patch_for_private_platform_creator(
        self, user1, image1_of_attachment1_of_private_platform_of_user1
    ):
        """Ensure we can patch for a private platform if we are the creator."""
        payload = {
            "data": {
                "type": "platform_image",
                "id": str(image1_of_attachment1_of_private_platform_of_user1.id),
                "attributes": {
                    "order_index": 20,
                },
            }
        }

        with self.run_requests_as(user1):
            resp = self.client.patch(
                f"{self.url}/{image1_of_attachment1_of_private_platform_of_user1.id}",
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.expect(resp.status_code).to_equal(200)

    @fixtures.use(["user2", "image1_of_attachment1_of_private_platform_of_user1"])
    def test_patch_for_private_platform_different_user(
        self, user2, image1_of_attachment1_of_private_platform_of_user1
    ):
        """Ensure we can't patch for a private platform if we aren't the creator."""
        payload = {
            "data": {
                "type": "platform_image",
                "id": str(image1_of_attachment1_of_private_platform_of_user1.id),
                "attributes": {
                    "order_index": 20,
                },
            }
        }

        with self.run_requests_as(user2):
            resp = self.client.patch(
                f"{self.url}/{image1_of_attachment1_of_private_platform_of_user1.id}",
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.expect(resp.status_code).to_equal(403)

    @fixtures.use(["super_user", "image1_of_attachment1_of_private_platform_of_user1"])
    def test_patch_for_private_platform_super_user(
        self, super_user, image1_of_attachment1_of_private_platform_of_user1
    ):
        """Ensure we can patch for a private platform if we are super user."""
        payload = {
            "data": {
                "type": "platform_image",
                "id": str(image1_of_attachment1_of_private_platform_of_user1.id),
                "attributes": {
                    "order_index": 20,
                },
            }
        }

        with self.run_requests_as(super_user):
            resp = self.client.patch(
                f"{self.url}/{image1_of_attachment1_of_private_platform_of_user1.id}",
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.expect(resp.status_code).to_equal(200)

    @fixtures.use(["super_user", "image1_of_attachment1_of_public_platform1_in_group1"])
    def test_patch_for_archived_platform_super_user(
        self,
        super_user,
        image1_of_attachment1_of_public_platform1_in_group1,
    ):
        """Ensure not even a super user can patch for archived platforms."""
        platform = image1_of_attachment1_of_public_platform1_in_group1.platform
        platform.archived = True
        db.session.add(platform)
        db.session.commit()

        payload = {
            "data": {
                "type": "platform_image",
                "id": str(image1_of_attachment1_of_public_platform1_in_group1.id),
                "attributes": {
                    "order_index": 20,
                },
            }
        }

        with self.run_requests_as(super_user):
            resp = self.client.patch(
                f"{self.url}/{image1_of_attachment1_of_public_platform1_in_group1.id}",
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.expect(resp.status_code).to_equal(403)

    @fixtures.use(
        [
            "super_user",
            "image1_of_attachment1_of_public_platform1_in_group1",
            "image1_of_attachment1_of_public_platform2_in_group1",
        ]
    )
    def test_patch_to_archived_platform_super_user(
        self,
        super_user,
        image1_of_attachment1_of_public_platform1_in_group1,
        image1_of_attachment1_of_public_platform2_in_group1,
    ):
        """Ensure not even a super user can patch to archived platforms."""
        platform = image1_of_attachment1_of_public_platform2_in_group1.platform
        platform.archived = True
        db.session.add(platform)
        db.session.commit()

        payload = {
            "data": {
                "type": "platform_image",
                "id": str(image1_of_attachment1_of_public_platform1_in_group1.id),
                "attributes": {
                    "order_index": 20,
                },
                "relationships": {
                    # When we change the platform, we must also
                    # change the platform attachment (so that they belong
                    # to each other).
                    "platform": {
                        "data": {
                            "id": str(platform.id),
                            "type": "platform",
                        },
                    },
                    "attachment": {
                        "data": {
                            "id": str(
                                image1_of_attachment1_of_public_platform2_in_group1.attachment.id
                            ),
                            "type": "platform_attachment",
                        }
                    },
                },
            }
        }

        with self.run_requests_as(super_user):
            resp = self.client.patch(
                f"{self.url}/{image1_of_attachment1_of_public_platform1_in_group1.id}",
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.expect(resp.status_code).to_equal(403)

    @fixtures.use(
        [
            "super_user",
            "image1_of_attachment1_of_public_platform1_in_group1",
            "public_platform2_in_group1",
        ]
    )
    def test_patch_for_attachment_that_doesnt_belong_to_platform(
        self,
        super_user,
        image1_of_attachment1_of_public_platform1_in_group1,
        public_platform2_in_group1,
    ):
        """Ensure we can't change an image for attachments for images that don't belong to the platform."""
        payload = {
            "data": {
                "type": "platform_image",
                "id": str(image1_of_attachment1_of_public_platform1_in_group1.id),
                "attributes": {
                    "order_index": 20,
                },
                "relationships": {
                    # When we change the platform, we must also
                    # change the platform attachment (so that they belong
                    # to each other).
                    "platform": {
                        "data": {
                            "id": str(public_platform2_in_group1.id),
                            "type": "platform",
                        },
                    },
                    "attachment": {
                        "data": {
                            "id": str(
                                image1_of_attachment1_of_public_platform1_in_group1.attachment.id
                            ),
                            "type": "platform_attachment",
                        }
                    },
                },
            }
        }
        with self.run_requests_as(super_user):
            resp = self.client.patch(
                f"{self.url}/{image1_of_attachment1_of_public_platform1_in_group1.id}",
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.expect(resp.status_code).to_equal(409)

    @fixtures.use(
        [
            "super_user",
            "image1_of_attachment1_of_public_platform1_in_group1",
            "image1_of_attachment1_of_public_platform2_in_group1",
        ]
    )
    def test_patch_image_for_same_attachment_and_platform_again(
        self,
        super_user,
        image1_of_attachment1_of_public_platform1_in_group1,
        image1_of_attachment1_of_public_platform2_in_group1,
    ):
        """Ensure we can't change an image if we have one already for the combination of platform and attachment."""
        payload = {
            "data": {
                "type": "platform_image",
                "id": str(image1_of_attachment1_of_public_platform1_in_group1.id),
                "attributes": {
                    "order_index": 20,
                },
                "relationships": {
                    # When we change the platform, we must also
                    # change the platform attachment (so that they belong
                    # to each other).
                    "platform": {
                        "data": {
                            "id": str(
                                image1_of_attachment1_of_public_platform2_in_group1.platform_id
                            ),
                            "type": "platform",
                        },
                    },
                    "attachment": {
                        "data": {
                            "id": str(
                                image1_of_attachment1_of_public_platform2_in_group1.attachment_id
                            ),
                            "type": "platform_attachment",
                        }
                    },
                },
            }
        }
        with self.run_requests_as(super_user):
            resp = self.client.patch(
                f"{self.url}/{image1_of_attachment1_of_public_platform1_in_group1.id}",
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.expect(resp.status_code).to_equal(409)

    @fixtures.use(["image1_of_attachment1_of_public_platform1_in_group1"])
    def test_delete_for_public_platform_no_user(
        self, image1_of_attachment1_of_public_platform1_in_group1
    ):
        """Ensure that we can't delete without a user."""
        resp = self.client.delete(
            f"{self.url}/{image1_of_attachment1_of_public_platform1_in_group1.id}",
        )
        self.expect(resp.status_code).to_equal(401)

    @fixtures.use(["user1", "image1_of_attachment1_of_public_platform1_in_group1"])
    def test_delete_for_public_platform_member(
        self, user1, image1_of_attachment1_of_public_platform1_in_group1
    ):
        """Ensure that we can delete if we are member of a group."""
        group_ids = image1_of_attachment1_of_public_platform1_in_group1.platform.group_ids
        with self.run_requests_as(user1):
            with patch.object(idl, "get_all_permission_groups_for_a_user") as mock:
                mock.return_value = UserAccount(
                    id=user1.subject,
                    username=user1.subject,
                    administrated_permission_groups=[],
                    membered_permission_groups=group_ids,
                )
                resp = self.client.delete(
                    f"{self.url}/{image1_of_attachment1_of_public_platform1_in_group1.id}",
                )
        self.expect(resp.status_code).to_equal(200)
        reloaded_platform = (
            db.session.query(Platform)
            .filter_by(
                id=image1_of_attachment1_of_public_platform1_in_group1.platform_id
            )
            .first()
        )
        # Reason here is that the images can be seen as basic data.
        # At least they are on the panel in the sms frontend.
        self.expect(reloaded_platform.update_description).to_equal("update;basic data")

    @fixtures.use(["user1", "image1_of_attachment1_of_public_platform1_in_group1"])
    def test_delete_for_public_platform_admin(
        self, user1, image1_of_attachment1_of_public_platform1_in_group1
    ):
        """Ensure that we can delete if we are admin of a group."""
        group_ids = image1_of_attachment1_of_public_platform1_in_group1.platform.group_ids
        with self.run_requests_as(user1):
            with patch.object(idl, "get_all_permission_groups_for_a_user") as mock:
                mock.return_value = UserAccount(
                    id=user1.subject,
                    username=user1.subject,
                    administrated_permission_groups=group_ids,
                    membered_permission_groups=[],
                )
                resp = self.client.delete(
                    f"{self.url}/{image1_of_attachment1_of_public_platform1_in_group1.id}",
                )
        self.expect(resp.status_code).to_equal(200)

    @fixtures.use(["user1", "image1_of_attachment1_of_public_platform1_in_group1"])
    def test_delete_for_public_platform_no_member(
        self, user1, image1_of_attachment1_of_public_platform1_in_group1
    ):
        """Ensure that we can't delete if we are not member of a group."""
        with self.run_requests_as(user1):
            with patch.object(idl, "get_all_permission_groups_for_a_user") as mock:
                mock.return_value = UserAccount(
                    id=user1.subject,
                    username=user1.subject,
                    administrated_permission_groups=[],
                    membered_permission_groups=[],
                )
                resp = self.client.delete(
                    f"{self.url}/{image1_of_attachment1_of_public_platform1_in_group1.id}",
                )
        self.expect(resp.status_code).to_equal(403)

    @fixtures.use(["super_user", "image1_of_attachment1_of_public_platform1_in_group1"])
    def test_delete_for_public_platform_no_member_super_user(
        self, super_user, image1_of_attachment1_of_public_platform1_in_group1
    ):
        """Ensure that we can delete if we are super user."""
        with self.run_requests_as(super_user):
            resp = self.client.delete(
                f"{self.url}/{image1_of_attachment1_of_public_platform1_in_group1.id}",
            )
        self.expect(resp.status_code).to_equal(200)

    @fixtures.use(["user1", "image1_of_attachment1_of_private_platform_of_user1"])
    def test_delete_for_private_platform_creator(
        self, user1, image1_of_attachment1_of_private_platform_of_user1
    ):
        """Ensure that we can delete for a private platform if we are its creator."""
        with self.run_requests_as(user1):
            resp = self.client.delete(
                f"{self.url}/{image1_of_attachment1_of_private_platform_of_user1.id}"
            )
        self.expect(resp.status_code).to_equal(200)

    @fixtures.use(["user2", "image1_of_attachment1_of_private_platform_of_user1"])
    def test_delete_for_private_platform_different_user(
        self, user2, image1_of_attachment1_of_private_platform_of_user1
    ):
        """Ensure that we can't delete for a private platform if we aren't its creator."""
        with self.run_requests_as(user2):
            resp = self.client.delete(
                f"{self.url}/{image1_of_attachment1_of_private_platform_of_user1.id}"
            )
        self.expect(resp.status_code).to_equal(403)

    @fixtures.use(["super_user", "image1_of_attachment1_of_private_platform_of_user1"])
    def test_delete_for_private_platform_super_user(
        self, super_user, image1_of_attachment1_of_private_platform_of_user1
    ):
        """Ensure that we can delete for a private platform if we are super user."""
        with self.run_requests_as(super_user):
            resp = self.client.delete(
                f"{self.url}/{image1_of_attachment1_of_private_platform_of_user1.id}"
            )
        self.expect(resp.status_code).to_equal(200)

    @fixtures.use(["super_user", "image1_of_attachment1_of_public_platform1_in_group1"])
    def test_delete_for_archived_platform(
        self, super_user, image1_of_attachment1_of_public_platform1_in_group1
    ):
        """Ensure not even a super user can delete for an archived platform."""
        platform = image1_of_attachment1_of_public_platform1_in_group1.platform
        platform.archived = True
        db.session.add(platform)
        db.session.commit()

        with self.run_requests_as(super_user):
            resp = self.client.delete(
                f"{self.url}/{image1_of_attachment1_of_public_platform1_in_group1.id}",
            )
        self.expect(resp.status_code).to_equal(403)

    @fixtures.use(["image1_of_attachment1_of_public_platform1_in_group1"])
    def test_platform_schema_includes_images(
        self, image1_of_attachment1_of_public_platform1_in_group1
    ):
        """Ensure we can get image information when querying the platform."""
        resp = self.client.get(f"{base_url}/platforms?include=platform_images")
        self.expect(resp.status_code).to_equal(200)

        included = resp.json["included"]
        self.expect(included).to_have_length(1)
        self.expect(included[0]["id"]).to_equal(
            str(image1_of_attachment1_of_public_platform1_in_group1.id)
        )
        self.expect(included[0]["type"]).to_equal("platform_image")
        self.expect(included[0]["attributes"]["order_index"]).to_equal(100)
        self.expect(included[0]["relationships"]["platform"]["data"]["id"]).to_equal(
            str(image1_of_attachment1_of_public_platform1_in_group1.platform_id)
        )

        self.expect(included[0]["relationships"]["attachment"]["data"]["id"]).to_equal(
            str(image1_of_attachment1_of_public_platform1_in_group1.attachment_id)
        )

    @fixtures.use(["super_user", "image1_of_attachment1_of_public_platform1_in_group1"])
    def test_platform_attachment_cant_be_deleted_when_linked_used_as_image(
        self, super_user, image1_of_attachment1_of_public_platform1_in_group1
    ):
        """Ensure we can't delete an platform attachment that we use for an image."""
        url = "/".join(
            [
                base_url,
                "platform-attachments",
                str(image1_of_attachment1_of_public_platform1_in_group1.attachment_id),
            ]
        )
        with self.run_requests_as(super_user):
            resp = self.client.delete(url)
        self.expect(resp.status_code).to_equal(409)

    @fixtures.use(["image1_of_attachment1_of_public_platform1_in_group1"])
    def test_platform_attachment_schema_includes_images(
        self, image1_of_attachment1_of_public_platform1_in_group1
    ):
        """Ensure we can get image information when querying the platform."""
        resp = self.client.get(
            f"{base_url}/platform-attachments?include=platform_images"
        )
        self.expect(resp.status_code).to_equal(200)

        included = resp.json["included"]
        self.expect(included).to_have_length(1)
        self.expect(included[0]["id"]).to_equal(
            str(image1_of_attachment1_of_public_platform1_in_group1.id)
        )
        self.expect(included[0]["type"]).to_equal("platform_image")
        self.expect(included[0]["attributes"]["order_index"]).to_equal(100)
        self.expect(included[0]["relationships"]["platform"]["data"]["id"]).to_equal(
            str(image1_of_attachment1_of_public_platform1_in_group1.platform_id)
        )

        self.expect(included[0]["relationships"]["attachment"]["data"]["id"]).to_equal(
            str(image1_of_attachment1_of_public_platform1_in_group1.attachment_id)
        )
