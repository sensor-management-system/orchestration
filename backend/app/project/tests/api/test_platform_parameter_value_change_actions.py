# SPDX-FileCopyrightText: 2023 - 2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Tests for the platform parameter value change action endpoints."""

import datetime
import json
from unittest.mock import patch

from project import base_url
from project.api.models import (
    Contact,
    Platform,
    PlatformParameter,
    PlatformParameterValueChangeAction,
    User,
)
from project.api.models.base_model import db
from project.extensions.idl.models.user_account import UserAccount
from project.extensions.instances import idl, mqtt
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


@fixtures.register("user1", scope=lambda: db.session)
@fixtures.use(["contact1"])
def create_user1(contact1):
    """Create a normal user to use it in the tests."""
    result = User(contact=contact1, subject=contact1.email)
    db.session.add(result)
    db.session.commit()
    return result


@fixtures.register("contact2", scope=lambda: db.session)
def create_contact2():
    """Create a single contact so that it can be used within the tests."""
    result = Contact(
        given_name="second", family_name="contact", email="second.contact@localhost"
    )
    db.session.add(result)
    db.session.commit()
    return result


@fixtures.register("user2", scope=lambda: db.session)
@fixtures.use(["contact2"])
def create_user2(contact2):
    """Create a normal user to use it in the tests."""
    result = User(contact=contact2, subject=contact2.email)
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


@fixtures.register("archived_public_platform1_in_group1", scope=lambda: db.session)
@fixtures.use(["public_platform1_in_group1"])
def create_archvied_public_platform1_in_group1(public_platform1_in_group1):
    """Create an archived public platform that uses group 1 for permission management."""
    public_platform1_in_group1.archived = True
    db.session.add(public_platform1_in_group1)
    db.session.commit()
    return public_platform1_in_group1


@fixtures.register("public_platform2_in_group1", scope=lambda: db.session)
def create_public_platform2_in_group1():
    """Create a public platform that uses group 2 for permission management."""
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


@fixtures.register("archived_public_platform2_in_group1", scope=lambda: db.session)
@fixtures.use(["public_platform2_in_group1"])
def create_archvied_public_platform2_in_group1(public_platform2_in_group1):
    """Create an archived public platform that uses group 1 for permission management."""
    public_platform2_in_group1.archived = True
    db.session.add(public_platform2_in_group1)
    db.session.commit()
    return public_platform2_in_group1


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


@fixtures.register("parameter1_of_public_platform1_in_group1", scope=lambda: db.session)
@fixtures.use(["public_platform1_in_group1"])
def create_parameter1_of_public_platform1_in_group1(public_platform1_in_group1):
    """Create a parameter on public_platform1."""
    result = PlatformParameter(
        platform=public_platform1_in_group1,
        label="specialvalue",
        description="some value",
        unit_name="count",
        unit_uri="http://foo/count",
    )
    db.session.add(result)
    db.session.commit()
    return result


@fixtures.register("parameter1_of_public_platform2_in_group1", scope=lambda: db.session)
@fixtures.use(["public_platform2_in_group1"])
def create_parameter1_of_public_platform2_in_group1(public_platform2_in_group1):
    """Create a parameter on public_platform2."""
    result = PlatformParameter(
        platform=public_platform2_in_group1,
        label="specialvalue",
        description="some value",
        unit_name="count",
        unit_uri="http://foo/count",
    )
    db.session.add(result)
    db.session.commit()
    return result


@fixtures.register("parameter1_of_private_platform_of_user1", scope=lambda: db.session)
@fixtures.use(["private_platform_of_user1"])
def create_parameter1_of_private_platform_of_user1(private_platform_of_user1):
    """Create a parameter on private_platform1."""
    result = PlatformParameter(
        platform=private_platform_of_user1,
        label="specialvalue",
        description="some value",
        unit_name="count",
        unit_uri="http://foo/count",
    )
    db.session.add(result)
    db.session.commit()
    return result


@fixtures.register(
    "parameter1_of_internal_platform1_in_group1", scope=lambda: db.session
)
@fixtures.use(["internal_platform1_in_group1"])
def create_parameter1_of_internal_platform1_in_group1(internal_platform1_in_group1):
    """Create a parameter on internal_platform1."""
    result = PlatformParameter(
        platform=internal_platform1_in_group1,
        label="specialvalue",
        description="some value",
        unit_name="count",
        unit_uri="http://foo/count",
    )
    db.session.add(result)
    db.session.commit()
    return result


@fixtures.register(
    "value1_of_parameter1_of_public_platform1_in_group1", scope=lambda: db.session
)
@fixtures.use(["parameter1_of_public_platform1_in_group1", "contact1"])
def create_value1_of_parameter1_of_public_platform1_in_group1(
    parameter1_of_public_platform1_in_group1, contact1
):
    """Create a parameter value on public_platform1."""
    result = PlatformParameterValueChangeAction(
        contact=contact1,
        date=datetime.datetime(2023, 2, 28, 23, 59, 00, tzinfo=datetime.timezone.utc),
        value="3",
        description="The value 3",
        platform_parameter=parameter1_of_public_platform1_in_group1,
    )
    db.session.add(result)
    db.session.commit()
    return result


@fixtures.register(
    "value1_of_parameter1_of_public_platform2_in_group1", scope=lambda: db.session
)
@fixtures.use(["parameter1_of_public_platform2_in_group1", "contact1"])
def create_value1_of_parameter1_of_public_platform2_in_group1(
    parameter1_of_public_platform2_in_group1, contact1
):
    """Create a parameter value on public_platform2."""
    result = PlatformParameterValueChangeAction(
        contact=contact1,
        date=datetime.datetime(2023, 2, 28, 23, 59, 00, tzinfo=datetime.timezone.utc),
        value="3",
        description="The value 3",
        platform_parameter=parameter1_of_public_platform2_in_group1,
    )
    db.session.add(result)
    db.session.commit()
    return result


@fixtures.register(
    "value1_of_parameter1_of_internal_platform1_in_group1", scope=lambda: db.session
)
@fixtures.use(["parameter1_of_internal_platform1_in_group1", "contact1"])
def create_value1_of_parameter1_of_internal_platform1_in_group1(
    parameter1_of_internal_platform1_in_group1, contact1
):
    """Create a parameter value on internal_platform1."""
    result = PlatformParameterValueChangeAction(
        contact=contact1,
        date=datetime.datetime(2023, 2, 28, 23, 59, 00, tzinfo=datetime.timezone.utc),
        value="3",
        description="The value 3",
        platform_parameter=parameter1_of_internal_platform1_in_group1,
    )
    db.session.add(result)
    db.session.commit()
    return result


@fixtures.register(
    "value1_of_parameter1_of_private_platform_of_user1", scope=lambda: db.session
)
@fixtures.use(["parameter1_of_private_platform_of_user1", "contact1"])
def create_value1_of_parameter1_of_private_platform_of_user1(
    parameter1_of_private_platform_of_user1, contact1
):
    """Create a parameter value on private_platform1."""
    result = PlatformParameterValueChangeAction(
        contact=contact1,
        date=datetime.datetime(2023, 2, 28, 23, 59, 00, tzinfo=datetime.timezone.utc),
        value="3",
        description="The value 3",
        platform_parameter=parameter1_of_private_platform_of_user1,
    )
    db.session.add(result)
    db.session.commit()
    return result


class TestPlatformParameterValueChangeActionServices(BaseTestCase):
    """Test the urls to interact with the platform parameter value change actions."""

    url = base_url + "/platform-parameter-value-change-actions"

    def test_get_list_empty(self):
        """Ensure that we query the url and get an empty list if there are no data."""
        resp = self.client.get(self.url)
        self.expect(resp.status_code).to_equal(200)

    @fixtures.use(
        [
            "parameter1_of_public_platform1_in_group1",
            "value1_of_parameter1_of_public_platform1_in_group1",
            "contact1",
        ]
    )
    def test_get_list_for_public_platform_no_user(
        self,
        parameter1_of_public_platform1_in_group1,
        value1_of_parameter1_of_public_platform1_in_group1,
        contact1,
    ):
        """Ensure we get public platforms without user."""
        resp = self.client.get(self.url)
        self.expect(resp.status_code).to_equal(200)
        self.expect(resp.json["data"]).to_have_length(1)

        self.expect(resp.json["data"][0]["id"]).to_equal(
            str(parameter1_of_public_platform1_in_group1.id)
        )
        self.expect(resp.json["data"][0]["type"]).to_equal(
            "platform_parameter_value_change_action"
        )
        self.expect(resp.json["data"][0]["attributes"]["value"]).to_equal("3")
        self.expect(resp.json["data"][0]["attributes"]["description"]).to_equal(
            "The value 3"
        )
        self.expect(
            resp.json["data"][0]["attributes"]["created_at"]
        ).to_be_a_datetime_string()
        self.expect(
            resp.json["data"][0]["attributes"]["updated_at"]
        ).to_be_a_datetime_string()

        self.expect(
            resp.json["data"][0]["relationships"]["platform_parameter"]["data"]["id"]
        ).to_equal(
            str(parameter1_of_public_platform1_in_group1.id),
        )
        self.expect(
            resp.json["data"][0]["relationships"]["platform_parameter"]["data"]["type"]
        ).to_equal("platform_parameter")
        self.expect(
            resp.json["data"][0]["relationships"]["contact"]["data"]["id"]
        ).to_equal(str(contact1.id))
        self.expect(
            resp.json["data"][0]["relationships"]["contact"]["data"]["type"]
        ).to_equal("contact")

    @fixtures.use(
        [
            "value1_of_parameter1_of_internal_platform1_in_group1",
        ]
    )
    def test_get_list_for_internal_platform_no_user(
        self, value1_of_parameter1_of_internal_platform1_in_group1
    ):
        """Ensure we don't get data from internal platforms without a user."""
        resp = self.client.get(self.url)
        self.expect(resp.status_code).to_equal(200)
        self.expect(resp.json["data"]).to_have_length(0)

    @fixtures.use(["value1_of_parameter1_of_internal_platform1_in_group1", "user1"])
    def test_get_list_for_internal_platform_with_user(
        self, value1_of_parameter1_of_internal_platform1_in_group1, user1
    ):
        """Ensure we get data for internal platforms if we have a user."""
        with self.run_requests_as(user1):
            resp = self.client.get(self.url)
        self.expect(resp.status_code).to_equal(200)
        self.expect(resp.json["data"]).to_have_length(1)

    @fixtures.use(["user1", "value1_of_parameter1_of_private_platform_of_user1"])
    def test_get_list_for_private_platform_with_creator(
        self, user1, value1_of_parameter1_of_private_platform_of_user1
    ):
        """Ensure we get data for a private platform if we are the creator."""
        with self.run_requests_as(user1):
            resp = self.client.get(self.url)
        self.expect(resp.status_code).to_equal(200)
        self.expect(resp.json["data"]).to_have_length(1)

    @fixtures.use(["user2", "value1_of_parameter1_of_private_platform_of_user1"])
    def test_get_list_for_private_platform_with_different_user(
        self, user2, value1_of_parameter1_of_private_platform_of_user1
    ):
        """Ensure we don't get data for a private platform if we aren't the creator."""
        with self.run_requests_as(user2):
            resp = self.client.get(self.url)
        self.expect(resp.status_code).to_equal(200)
        self.expect(resp.json["data"]).to_have_length(0)

    @fixtures.use(["super_user", "value1_of_parameter1_of_private_platform_of_user1"])
    def test_get_list_for_private_platform_with_super_user(
        self, super_user, value1_of_parameter1_of_private_platform_of_user1
    ):
        """Ensure we get data for a private platform if we super user."""
        with self.run_requests_as(super_user):
            resp = self.client.get(self.url)
        self.expect(resp.status_code).to_equal(200)
        self.expect(resp.json["data"]).to_have_length(1)

    @fixtures.use(["value1_of_parameter1_of_private_platform_of_user1"])
    def test_get_list_for_private_platform_without_user(
        self, value1_of_parameter1_of_private_platform_of_user1
    ):
        """Ensure we can't get data for a private platform without user."""
        resp = self.client.get(self.url)
        self.expect(resp.status_code).to_equal(200)
        self.expect(resp.json["data"]).to_have_length(0)

    def test_get_one_non_existing(self):
        """Ensure we get an 404 for a non existing change action."""
        resp = self.client.get(self.url + "/12345678901234")
        self.expect(resp.status_code).to_equal(404)

    @fixtures.use(
        [
            "value1_of_parameter1_of_public_platform1_in_group1",
            "parameter1_of_public_platform1_in_group1",
        ]
    )
    def test_get_one_for_public_platform_no_user(
        self,
        value1_of_parameter1_of_public_platform1_in_group1,
        parameter1_of_public_platform1_in_group1,
    ):
        """Ensure we can get a change action for a public platform without a user."""
        resp = self.client.get(
            f"{self.url}/{value1_of_parameter1_of_public_platform1_in_group1.id}"
        )
        self.expect(resp.status_code).to_equal(200)

        self.expect(resp.json["data"]["id"]).to_equal(
            str(value1_of_parameter1_of_public_platform1_in_group1.id)
        )
        self.expect(resp.json["data"]["type"]).to_equal(
            "platform_parameter_value_change_action"
        )

        attributes = resp.json["data"]["attributes"]
        self.expect(attributes["created_at"]).to_be_a_datetime_string()
        self.expect(attributes["date"]).to_equal(
            value1_of_parameter1_of_public_platform1_in_group1.date.isoformat()
        )
        self.expect(attributes["description"]).to_equal("The value 3")
        self.expect(attributes["updated_at"]).to_be_a_datetime_string()
        self.expect(attributes["value"]).to_equal("3")

        relationships = resp.json["data"]["relationships"]
        self.expect(relationships["contact"]["data"]["id"]).to_equal(
            str(value1_of_parameter1_of_public_platform1_in_group1.contact.id)
        )
        self.expect(relationships["platform_parameter"]["data"]["id"]).to_equal(
            str(
                value1_of_parameter1_of_public_platform1_in_group1.platform_parameter.id
            )
        )

    @fixtures.use(["value1_of_parameter1_of_internal_platform1_in_group1"])
    def test_get_one_for_internal_platform_no_user(
        self, value1_of_parameter1_of_internal_platform1_in_group1
    ):
        """Ensure we don't get details for internal platforms without a user."""
        resp = self.client.get(
            f"{self.url}/{value1_of_parameter1_of_internal_platform1_in_group1.id}"
        )
        self.expect(resp.status_code).to_equal(401)

    @fixtures.use(["value1_of_parameter1_of_internal_platform1_in_group1", "user1"])
    def test_get_one_for_internal_platform_with_user(
        self, value1_of_parameter1_of_internal_platform1_in_group1, user1
    ):
        """Ensure we can get the details for internal platform if we have a user."""
        with self.run_requests_as(user1):
            resp = self.client.get(
                f"{self.url}/{value1_of_parameter1_of_internal_platform1_in_group1.id}"
            )
        self.expect(resp.status_code).to_equal(200)

    @fixtures.use(["value1_of_parameter1_of_private_platform_of_user1", "user1"])
    def test_get_one_for_private_platform_with_creator(
        self, value1_of_parameter1_of_private_platform_of_user1, user1
    ):
        """Ensure we get details for a private platform if we are the creator."""
        with self.run_requests_as(user1):
            resp = self.client.get(
                f"{self.url}/{value1_of_parameter1_of_private_platform_of_user1.id}"
            )
        self.expect(resp.status_code).to_equal(200)

    @fixtures.use(["value1_of_parameter1_of_private_platform_of_user1", "user2"])
    def test_get_one_for_private_platform_with_different_user(
        self, value1_of_parameter1_of_private_platform_of_user1, user2
    ):
        """Ensure we can't get details for a private platform if we are a different user."""
        with self.run_requests_as(user2):
            resp = self.client.get(
                f"{self.url}/{value1_of_parameter1_of_private_platform_of_user1.id}"
            )
        self.expect(resp.status_code).to_equal(403)

    @fixtures.use(["value1_of_parameter1_of_private_platform_of_user1", "super_user"])
    def test_get_one_for_private_platform_with_super_user(
        self, value1_of_parameter1_of_private_platform_of_user1, super_user
    ):
        """Ensure we can get details for a private platform if we are a super user."""
        with self.run_requests_as(super_user):
            resp = self.client.get(
                f"{self.url}/{value1_of_parameter1_of_private_platform_of_user1.id}"
            )
        self.expect(resp.status_code).to_equal(200)

    @fixtures.use(["value1_of_parameter1_of_private_platform_of_user1"])
    def test_get_one_for_private_platform_without_user(
        self, value1_of_parameter1_of_private_platform_of_user1
    ):
        """Ensure we can't get details for a private platform if there is no user."""
        resp = self.client.get(
            f"{self.url}/{value1_of_parameter1_of_private_platform_of_user1.id}"
        )
        self.expect(resp.status_code).to_equal(401)

    @fixtures.use(
        [
            "value1_of_parameter1_of_public_platform1_in_group1",
            "value1_of_parameter1_of_public_platform2_in_group1",
            "public_platform1_in_group1",
            "public_platform2_in_group1",
        ]
    )
    def test_get_list_prefiltered_by_platform(
        self,
        value1_of_parameter1_of_public_platform1_in_group1,
        value1_of_parameter1_of_public_platform2_in_group1,
        public_platform1_in_group1,
        public_platform2_in_group1,
    ):
        """Ensure we can prefilter by platform."""
        url1 = f"{base_url}/platforms/{public_platform1_in_group1.id}/platform-parameter-value-change-actions"
        resp1 = self.client.get(url1)
        self.expect(resp1.status_code).to_equal(200)
        self.expect(resp1.json["data"]).to_have_length(1)
        self.expect(resp1.json["data"][0]["id"]).to_equal(
            str(value1_of_parameter1_of_public_platform1_in_group1.id)
        )

        url2 = f"{base_url}/platforms/{public_platform2_in_group1.id}/platform-parameter-value-change-actions"
        resp2 = self.client.get(url2)
        self.expect(resp2.status_code).to_equal(200)
        self.expect(resp2.json["data"]).to_have_length(1)
        self.expect(resp2.json["data"][0]["id"]).to_equal(
            str(value1_of_parameter1_of_public_platform2_in_group1.id)
        )

    def test_get_list_prefiltered_invalid_platform_id(self):
        """Ensure we get an 404 if there is no such platform."""
        resp = self.client.get(
            f"{base_url}/platforms/12345678901234/platform-parameter-value-change-actions"
        )
        self.expect(resp.status_code).to_equal(404)

    @fixtures.use(["parameter1_of_public_platform1_in_group1", "contact1"])
    def test_post_no_user(self, parameter1_of_public_platform1_in_group1, contact1):
        """Ensure we can't post if we don't have a user."""
        payload = {
            "data": {
                "type": "platform_parameter_value_change_action",
                "attributes": {
                    "description": "The value 3",
                    "value": "3",
                    "date": "2023-05-02T13:17:00+00:00",
                },
                "relationships": {
                    "platform_parameter": {
                        "data": {
                            "id": str(parameter1_of_public_platform1_in_group1.id),
                            "type": "platform_parameter",
                        }
                    },
                    "contact": {
                        "data": {
                            "id": str(contact1.id),
                            "type": "contact",
                        }
                    },
                },
            }
        }
        resp = self.client.post(
            self.url, data=json.dumps(payload), content_type="application/vnd.api+json"
        )
        self.expect(resp.status_code).to_equal(401)

    @fixtures.use(
        [
            "user1",
            "parameter1_of_public_platform1_in_group1",
            "contact1",
            "public_platform1_in_group1",
        ]
    )
    def test_post_member(
        self,
        user1,
        parameter1_of_public_platform1_in_group1,
        contact1,
        public_platform1_in_group1,
    ):
        """Ensure we can post if we are a member of one of the groups."""
        payload = {
            "data": {
                "type": "platform_parameter_value_change_action",
                "attributes": {
                    "description": "The value 3",
                    "value": "3",
                    "date": "2023-05-02T13:17:00+00:00",
                },
                "relationships": {
                    "platform_parameter": {
                        "data": {
                            "id": str(parameter1_of_public_platform1_in_group1.id),
                            "type": "platform_parameter",
                        }
                    },
                    "contact": {
                        "data": {
                            "id": str(contact1.id),
                            "type": "contact",
                        }
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
                    membered_permission_groups=public_platform1_in_group1.group_ids,
                )
                resp = self.client.post(
                    self.url,
                    data=json.dumps(payload),
                    content_type="application/vnd.api+json",
                )
        self.expect(resp.status_code).to_equal(201)

        result = resp.json["data"]
        self.expect(result["attributes"]["description"]).to_equal("The value 3")
        self.expect(result["attributes"]["value"]).to_equal("3")
        self.expect(result["attributes"]["date"]).to_equal("2023-05-02T13:17:00+00:00")
        self.expect(result["attributes"]["created_at"]).to_be_a_datetime_string()

        self.expect(
            result["relationships"]["platform_parameter"]["data"]["id"]
        ).to_equal(str(parameter1_of_public_platform1_in_group1.id))
        self.expect(result["relationships"]["contact"]["data"]["id"]).to_equal(
            str(contact1.id)
        )

        self.expect(result["relationships"]["created_by"]["data"]["id"]).to_equal(
            str(user1.id)
        )

        platform = (
            db.session.query(Platform)
            .filter_by(id=parameter1_of_public_platform1_in_group1.platform_id)
            .first()
        )
        self.expect(platform.update_description).to_equal(
            "create;platform parameter value change action"
        )
        # And ensure that we trigger the mqtt.
        mqtt.mqtt.publish.assert_called_once()
        call_args = mqtt.mqtt.publish.call_args[0]

        self.expect(call_args[0]).to_equal(
            "sms/post-platform-parameter-value-change-action"
        )
        notification_data = json.loads(call_args[1])["data"]
        self.expect(notification_data["type"]).to_equal(
            "platform_parameter_value_change_action"
        )
        self.expect(notification_data["attributes"]["value"]).to_equal("3")
        self.expect(str).of(notification_data["id"]).to_match(r"\d+")

    @fixtures.use(
        [
            "user1",
            "parameter1_of_public_platform1_in_group1",
            "contact1",
            "public_platform1_in_group1",
        ]
    )
    def test_post_admin(
        self,
        user1,
        parameter1_of_public_platform1_in_group1,
        contact1,
        public_platform1_in_group1,
    ):
        """Ensure we can post if we are a admin of one of the groups."""
        payload = {
            "data": {
                "type": "platform_parameter_value_change_action",
                "attributes": {
                    "description": "The value 3",
                    "value": "3",
                    "date": "2023-05-02T13:17:00+00:00",
                },
                "relationships": {
                    "platform_parameter": {
                        "data": {
                            "id": str(parameter1_of_public_platform1_in_group1.id),
                            "type": "platform_parameter",
                        }
                    },
                    "contact": {
                        "data": {
                            "id": str(contact1.id),
                            "type": "contact",
                        }
                    },
                },
            }
        }
        with self.run_requests_as(user1):
            with patch.object(idl, "get_all_permission_groups_for_a_user") as mock:
                mock.return_value = UserAccount(
                    id=user1.subject,
                    username=user1.subject,
                    administrated_permission_groups=public_platform1_in_group1.group_ids,
                    membered_permission_groups=[],
                )
                resp = self.client.post(
                    self.url,
                    data=json.dumps(payload),
                    content_type="application/vnd.api+json",
                )
        self.expect(resp.status_code).to_equal(201)

    @fixtures.use(
        [
            "user1",
            "parameter1_of_private_platform_of_user1",
            "contact1",
        ]
    )
    def test_post_private_creator(
        self,
        user1,
        parameter1_of_private_platform_of_user1,
        contact1,
    ):
        """Ensure we can post if we are a creator of the private platform."""
        payload = {
            "data": {
                "type": "platform_parameter_value_change_action",
                "attributes": {
                    "description": "The value 3",
                    "value": "3",
                    "date": "2023-05-02T13:17:00+00:00",
                },
                "relationships": {
                    "platform_parameter": {
                        "data": {
                            "id": str(parameter1_of_private_platform_of_user1.id),
                            "type": "platform_parameter",
                        }
                    },
                    "contact": {
                        "data": {
                            "id": str(contact1.id),
                            "type": "contact",
                        }
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

    @fixtures.use(
        [
            "user2",
            "parameter1_of_private_platform_of_user1",
            "contact1",
        ]
    )
    def test_post_private_other_user(
        self,
        user2,
        parameter1_of_private_platform_of_user1,
        contact1,
    ):
        """Ensure we can't post if we are not the creator of the private platform."""
        payload = {
            "data": {
                "type": "platform_parameter_value_change_action",
                "attributes": {
                    "description": "The value 3",
                    "value": "3",
                    "date": "2023-05-02T13:17:00+00:00",
                },
                "relationships": {
                    "platform_parameter": {
                        "data": {
                            "id": str(parameter1_of_private_platform_of_user1.id),
                            "type": "platform_parameter",
                        }
                    },
                    "contact": {
                        "data": {
                            "id": str(contact1.id),
                            "type": "contact",
                        }
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

    @fixtures.use(
        [
            "super_user",
            "parameter1_of_private_platform_of_user1",
            "contact1",
        ]
    )
    def test_post_private_super_user(
        self,
        super_user,
        parameter1_of_private_platform_of_user1,
        contact1,
    ):
        """Ensure we can post if we are a super user."""
        payload = {
            "data": {
                "type": "platform_parameter_value_change_action",
                "attributes": {
                    "description": "The value 3",
                    "value": "3",
                    "date": "2023-05-02T13:17:00+00:00",
                },
                "relationships": {
                    "platform_parameter": {
                        "data": {
                            "id": str(parameter1_of_private_platform_of_user1.id),
                            "type": "platform_parameter",
                        }
                    },
                    "contact": {
                        "data": {
                            "id": str(contact1.id),
                            "type": "contact",
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
        self.expect(resp.status_code).to_equal(201)

    @fixtures.use(
        [
            "user1",
            "parameter1_of_public_platform1_in_group1",
            "contact1",
        ]
    )
    def test_post_not_in_group(
        self,
        user1,
        parameter1_of_public_platform1_in_group1,
        contact1,
    ):
        """Ensure we can't post if we are not even a member of one of the groups."""
        payload = {
            "data": {
                "type": "platform_parameter_value_change_action",
                "attributes": {
                    "description": "The value 3",
                    "value": "3",
                    "date": "2023-05-02T13:17:00+00:00",
                },
                "relationships": {
                    "platform_parameter": {
                        "data": {
                            "id": str(parameter1_of_public_platform1_in_group1.id),
                            "type": "platform_parameter",
                        }
                    },
                    "contact": {
                        "data": {
                            "id": str(contact1.id),
                            "type": "contact",
                        }
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

    @fixtures.use(
        [
            "super_user",
            "parameter1_of_public_platform1_in_group1",
            "contact1",
        ]
    )
    def test_post_not_in_group_super_user(
        self,
        super_user,
        parameter1_of_public_platform1_in_group1,
        contact1,
    ):
        """Ensure we can post if we are super user - even without membership."""
        payload = {
            "data": {
                "type": "platform_parameter_value_change_action",
                "attributes": {
                    "description": "The value 3",
                    "value": "3",
                    "date": "2023-05-02T13:17:00+00:00",
                },
                "relationships": {
                    "platform_parameter": {
                        "data": {
                            "id": str(parameter1_of_public_platform1_in_group1.id),
                            "type": "platform_parameter",
                        }
                    },
                    "contact": {
                        "data": {
                            "id": str(contact1.id),
                            "type": "contact",
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
        self.expect(resp.status_code).to_equal(201)

    @fixtures.use(
        [
            "super_user",
            "parameter1_of_public_platform1_in_group1",
            "contact1",
            "archived_public_platform1_in_group1",
        ]
    )
    def test_post_archived(
        self,
        super_user,
        parameter1_of_public_platform1_in_group1,
        contact1,
        archived_public_platform1_in_group1,
    ):
        """Ensure we can't post if the platform is already archived."""
        payload = {
            "data": {
                "type": "platform_parameter_value_change_action",
                "attributes": {
                    "description": "The value 3",
                    "value": "3",
                    "date": "2023-05-02T13:17:00+00:00",
                },
                "relationships": {
                    "platform_parameter": {
                        "data": {
                            "id": str(parameter1_of_public_platform1_in_group1.id),
                            "type": "platform_parameter",
                        }
                    },
                    "contact": {
                        "data": {
                            "id": str(contact1.id),
                            "type": "contact",
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
        self.expect(resp.status_code).to_equal(403)

    @fixtures.use(
        [
            "super_user",
            "parameter1_of_public_platform1_in_group1",
            "contact1",
        ]
    )
    def test_post_missing_date(
        self,
        super_user,
        parameter1_of_public_platform1_in_group1,
        contact1,
    ):
        """Ensure we can't post if we don't provide a date."""
        payload = {
            "data": {
                "type": "platform_parameter_value_change_action",
                "attributes": {
                    "description": "The value 3",
                    "value": "3",
                },
                "relationships": {
                    "platform_parameter": {
                        "data": {
                            "id": str(parameter1_of_public_platform1_in_group1.id),
                            "type": "platform_parameter",
                        }
                    },
                    "contact": {
                        "data": {
                            "id": str(contact1.id),
                            "type": "contact",
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
        self.expect(resp.status_code).to_equal(422)

    @fixtures.use(
        [
            "super_user",
            "parameter1_of_public_platform1_in_group1",
            "contact1",
        ]
    )
    def test_post_missing_value(
        self,
        super_user,
        parameter1_of_public_platform1_in_group1,
        contact1,
    ):
        """Ensure we can't post if we don't provide a value."""
        payload = {
            "data": {
                "type": "platform_parameter_value_change_action",
                "attributes": {
                    "description": "The value 3",
                    "date": "2023-05-02T13:17:00+00:00",
                },
                "relationships": {
                    "platform_parameter": {
                        "data": {
                            "id": str(parameter1_of_public_platform1_in_group1.id),
                            "type": "platform_parameter",
                        }
                    },
                    "contact": {
                        "data": {
                            "id": str(contact1.id),
                            "type": "contact",
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
        self.expect(resp.status_code).to_equal(422)

    @fixtures.use(
        [
            "super_user",
            "contact1",
        ]
    )
    def test_post_missing_platform_parameter(
        self,
        super_user,
        contact1,
    ):
        """Ensure we can't post if we don't provide a platform parameter."""
        payload = {
            "data": {
                "type": "platform_parameter_value_change_action",
                "attributes": {
                    "description": "The value 3",
                    "date": "2023-05-02T13:17:00+00:00",
                    "value": "3",
                },
                "relationships": {
                    "platform_parameter": {
                        "data": None,
                    },
                    "contact": {
                        "data": {
                            "id": str(contact1.id),
                            "type": "contact",
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
        self.expect(resp.status_code).to_equal(422)

    @fixtures.use(
        [
            "super_user",
            "parameter1_of_public_platform1_in_group1",
        ]
    )
    def test_post_missing_contact(
        self,
        super_user,
        parameter1_of_public_platform1_in_group1,
    ):
        """Ensure we can't post if we don't provide a contact."""
        payload = {
            "data": {
                "type": "platform_parameter_value_change_action",
                "attributes": {
                    "description": "The value 3",
                    "date": "2023-05-02T13:17:00+00:00",
                    "value": "3",
                },
                "relationships": {
                    "platform_parameter": {
                        "data": {
                            "id": str(parameter1_of_public_platform1_in_group1.id),
                            "type": "platform_parameter",
                        }
                    },
                    "contact": {
                        "data": None,
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

    @fixtures.use(["value1_of_parameter1_of_public_platform1_in_group1"])
    def test_patch_for_public_platform_no_user(
        self, value1_of_parameter1_of_public_platform1_in_group1
    ):
        """Ensure we can't patch without a user."""
        payload = {
            "data": {
                "type": "platform_parameter_value_change_action",
                "attributes": {"value": "42"},
            }
        }
        resp = self.client.patch(
            f"{self.url}/{value1_of_parameter1_of_public_platform1_in_group1.id}",
            data=json.dumps(payload),
            content_type="application/vnd.api+json",
        )
        self.expect(resp.status_code).to_equal(401)

    @fixtures.use(
        [
            "value1_of_parameter1_of_public_platform1_in_group1",
            "user1",
            "public_platform1_in_group1",
        ]
    )
    def test_patch_for_public_platform_member(
        self,
        value1_of_parameter1_of_public_platform1_in_group1,
        user1,
        public_platform1_in_group1,
    ):
        """Ensure a member can update the public platform with a new parameter value."""
        payload = {
            "data": {
                "type": "platform_parameter_value_change_action",
                "id": str(value1_of_parameter1_of_public_platform1_in_group1.id),
                "attributes": {"value": "42"},
            }
        }
        with self.run_requests_as(user1):
            with patch.object(idl, "get_all_permission_groups_for_a_user") as mock:
                mock.return_value = UserAccount(
                    id=user1.subject,
                    username=user1.subject,
                    administrated_permission_groups=[],
                    membered_permission_groups=public_platform1_in_group1.group_ids,
                )
                resp = self.client.patch(
                    f"{self.url}/{value1_of_parameter1_of_public_platform1_in_group1.id}",
                    data=json.dumps(payload),
                    content_type="application/vnd.api+json",
                )
        self.expect(resp.status_code).to_equal(200)
        self.expect(resp.json["data"]["attributes"]["value"]).to_equal("42")

        self.expect(
            resp.json["data"]["relationships"]["updated_by"]["data"]["id"]
        ).to_equal(str(user1.id))
        reloaded_platform = (
            db.session.query(Platform)
            .filter_by(id=public_platform1_in_group1.id)
            .first()
        )
        self.expect(reloaded_platform.update_description).to_equal(
            "update;platform parameter value change action"
        )
        # And ensure that we trigger the mqtt.
        mqtt.mqtt.publish.assert_called_once()
        call_args = mqtt.mqtt.publish.call_args[0]

        self.expect(call_args[0]).to_equal(
            "sms/patch-platform-parameter-value-change-action"
        )
        notification_data = json.loads(call_args[1])["data"]
        self.expect(notification_data["type"]).to_equal(
            "platform_parameter_value_change_action"
        )
        self.expect(notification_data["attributes"]["value"]).to_equal("42")
        self.expect(notification_data["attributes"]["description"]).to_equal(
            "The value 3"
        )

    @fixtures.use(
        [
            "value1_of_parameter1_of_public_platform1_in_group1",
            "user1",
            "public_platform1_in_group1",
        ]
    )
    def test_patch_for_public_platform_admin(
        self,
        value1_of_parameter1_of_public_platform1_in_group1,
        user1,
        public_platform1_in_group1,
    ):
        """Ensure an admin can update the public platform with a new parameter value."""
        payload = {
            "data": {
                "type": "platform_parameter_value_change_action",
                "id": str(value1_of_parameter1_of_public_platform1_in_group1.id),
                "attributes": {"value": "42"},
            }
        }
        with self.run_requests_as(user1):
            with patch.object(idl, "get_all_permission_groups_for_a_user") as mock:
                mock.return_value = UserAccount(
                    id=user1.subject,
                    username=user1.subject,
                    administrated_permission_groups=public_platform1_in_group1.group_ids,
                    membered_permission_groups=[],
                )
                resp = self.client.patch(
                    f"{self.url}/{value1_of_parameter1_of_public_platform1_in_group1.id}",
                    data=json.dumps(payload),
                    content_type="application/vnd.api+json",
                )
        self.expect(resp.status_code).to_equal(200)

    @fixtures.use(
        [
            "value1_of_parameter1_of_public_platform1_in_group1",
            "user1",
        ]
    )
    def test_patch_for_public_platform_no_member(
        self,
        value1_of_parameter1_of_public_platform1_in_group1,
        user1,
    ):
        """Ensure we can't patch if we are not even a member of the group."""
        payload = {
            "data": {
                "type": "platform_parameter_value_change_action",
                "id": str(value1_of_parameter1_of_public_platform1_in_group1.id),
                "attributes": {"value": "42"},
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
                    f"{self.url}/{value1_of_parameter1_of_public_platform1_in_group1.id}",
                    data=json.dumps(payload),
                    content_type="application/vnd.api+json",
                )
        self.expect(resp.status_code).to_equal(403)

    @fixtures.use(
        [
            "value1_of_parameter1_of_public_platform1_in_group1",
            "super_user",
        ]
    )
    def test_patch_for_public_platform_no_member_super_user(
        self,
        value1_of_parameter1_of_public_platform1_in_group1,
        super_user,
    ):
        """Ensure we can patch if we are super user, even if we aren't member of any group."""
        payload = {
            "data": {
                "type": "platform_parameter_value_change_action",
                "id": str(value1_of_parameter1_of_public_platform1_in_group1.id),
                "attributes": {"value": "42"},
            }
        }
        with self.run_requests_as(super_user):
            resp = self.client.patch(
                f"{self.url}/{value1_of_parameter1_of_public_platform1_in_group1.id}",
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.expect(resp.status_code).to_equal(200)

    @fixtures.use(["value1_of_parameter1_of_private_platform_of_user1", "user1"])
    def test_patch_for_private_platform_creator(
        self, value1_of_parameter1_of_private_platform_of_user1, user1
    ):
        """Ensure we can patch for a private platform if we are creator."""
        payload = {
            "data": {
                "type": "platform_parameter_value_change_action",
                "id": str(value1_of_parameter1_of_private_platform_of_user1.id),
                "attributes": {"value": "42"},
            }
        }
        with self.run_requests_as(user1):
            resp = self.client.patch(
                f"{self.url}/{value1_of_parameter1_of_private_platform_of_user1.id}",
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.expect(resp.status_code).to_equal(200)

    @fixtures.use(["value1_of_parameter1_of_private_platform_of_user1", "user2"])
    def test_patch_for_private_platform_different_user(
        self, value1_of_parameter1_of_private_platform_of_user1, user2
    ):
        """Ensure we can't patch for a private platform if we are not the creator."""
        payload = {
            "data": {
                "type": "platform_parameter_value_change_action",
                "id": str(value1_of_parameter1_of_private_platform_of_user1.id),
                "attributes": {"value": "42"},
            }
        }
        with self.run_requests_as(user2):
            resp = self.client.patch(
                f"{self.url}/{value1_of_parameter1_of_private_platform_of_user1.id}",
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.expect(resp.status_code).to_equal(403)

    @fixtures.use(["value1_of_parameter1_of_private_platform_of_user1", "super_user"])
    def test_patch_for_private_platform_super_user(
        self, value1_of_parameter1_of_private_platform_of_user1, super_user
    ):
        """Ensure we can patch for a private platform if we are super user."""
        payload = {
            "data": {
                "type": "platform_parameter_value_change_action",
                "id": str(value1_of_parameter1_of_private_platform_of_user1.id),
                "attributes": {"value": "42"},
            }
        }
        with self.run_requests_as(super_user):
            resp = self.client.patch(
                f"{self.url}/{value1_of_parameter1_of_private_platform_of_user1.id}",
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.expect(resp.status_code).to_equal(200)

    @fixtures.use(
        [
            "super_user",
            "value1_of_parameter1_of_public_platform1_in_group1",
            "archived_public_platform1_in_group1",
        ]
    )
    def test_patch_for_archived_platform_super_user(
        self,
        super_user,
        value1_of_parameter1_of_public_platform1_in_group1,
        archived_public_platform1_in_group1,
    ):
        """Ensure we can't patch for platforms that are already archived."""
        payload = {
            "data": {
                "type": "platform_parameter_value_change_action",
                "id": str(value1_of_parameter1_of_public_platform1_in_group1.id),
                "attributes": {"value": "42"},
            }
        }
        with self.run_requests_as(super_user):
            resp = self.client.patch(
                f"{self.url}/{value1_of_parameter1_of_public_platform1_in_group1.id}",
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.expect(resp.status_code).to_equal(403)

    @fixtures.use(
        [
            "super_user",
            "value1_of_parameter1_of_public_platform1_in_group1",
            "parameter1_of_public_platform2_in_group1",
            "archived_public_platform2_in_group1",
        ]
    )
    def test_patch_to_archived_platform_super_user(
        self,
        super_user,
        value1_of_parameter1_of_public_platform1_in_group1,
        parameter1_of_public_platform2_in_group1,
        archived_public_platform2_in_group1,
    ):
        """Ensure we can't patch to non editable platforms."""
        payload = {
            "data": {
                "type": "platform_parameter_value_change_action",
                "id": str(value1_of_parameter1_of_public_platform1_in_group1.id),
                "relationships": {
                    "platform_parameter": {
                        "data": {
                            "id": str(parameter1_of_public_platform2_in_group1.id),
                            "type": "platform_parameter",
                        }
                    }
                },
            }
        }
        with self.run_requests_as(super_user):
            resp = self.client.patch(
                f"{self.url}/{value1_of_parameter1_of_public_platform1_in_group1.id}",
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.expect(resp.status_code).to_equal(403)

    @fixtures.use(["value1_of_parameter1_of_public_platform1_in_group1"])
    def test_delete_for_public_platform_no_user(
        self, value1_of_parameter1_of_public_platform1_in_group1
    ):
        """Ensure we can't delete without a user."""
        resp = self.client.delete(
            f"{self.url}/{value1_of_parameter1_of_public_platform1_in_group1.id}"
        )
        self.expect(resp.status_code).to_equal(401)

    @fixtures.use(
        [
            "value1_of_parameter1_of_public_platform1_in_group1",
            "user1",
            "public_platform1_in_group1",
        ]
    )
    def test_delete_for_public_platform_member(
        self,
        value1_of_parameter1_of_public_platform1_in_group1,
        user1,
        public_platform1_in_group1,
    ):
        """Ensure we can delete if we are group member."""
        with self.run_requests_as(user1):
            with patch.object(idl, "get_all_permission_groups_for_a_user") as mock:
                mock.return_value = UserAccount(
                    id=user1.subject,
                    username=user1.subject,
                    administrated_permission_groups=[],
                    membered_permission_groups=public_platform1_in_group1.group_ids,
                )
                resp = self.client.delete(
                    f"{self.url}/{value1_of_parameter1_of_public_platform1_in_group1.id}"
                )
        self.expect(resp.status_code).to_equal(200)

        reloaded_platform = (
            db.session.query(Platform)
            .filter_by(id=public_platform1_in_group1.id)
            .first()
        )
        self.expect(reloaded_platform.update_description).to_equal(
            "delete;platform parameter value change action"
        )
        # And ensure that we trigger the mqtt.
        mqtt.mqtt.publish.assert_called_once()
        call_args = mqtt.mqtt.publish.call_args[0]

        self.expect(call_args[0]).to_equal(
            "sms/delete-platform-parameter-value-change-action"
        )
        self.expect(json.loads).of(call_args[1]).to_equal(
            {
                "data": {
                    "type": "platform_parameter_value_change_action",
                    "id": str(value1_of_parameter1_of_public_platform1_in_group1.id),
                }
            }
        )

    @fixtures.use(
        [
            "value1_of_parameter1_of_public_platform1_in_group1",
            "user1",
            "public_platform1_in_group1",
        ]
    )
    def test_delete_for_public_platform_admin(
        self,
        value1_of_parameter1_of_public_platform1_in_group1,
        user1,
        public_platform1_in_group1,
    ):
        """Ensure we can delete if we are admin."""
        with self.run_requests_as(user1):
            with patch.object(idl, "get_all_permission_groups_for_a_user") as mock:
                mock.return_value = UserAccount(
                    id=user1.subject,
                    username=user1.subject,
                    administrated_permission_groups=public_platform1_in_group1.group_ids,
                    membered_permission_groups=[],
                )
                resp = self.client.delete(
                    f"{self.url}/{value1_of_parameter1_of_public_platform1_in_group1.id}"
                )
        self.expect(resp.status_code).to_equal(200)

    @fixtures.use(
        [
            "value1_of_parameter1_of_public_platform1_in_group1",
            "user1",
        ]
    )
    def test_delete_for_public_platform_no_member(
        self,
        value1_of_parameter1_of_public_platform1_in_group1,
        user1,
    ):
        """Ensure we can't delete if we are not even group member."""
        with self.run_requests_as(user1):
            with patch.object(idl, "get_all_permission_groups_for_a_user") as mock:
                mock.return_value = UserAccount(
                    id=user1.subject,
                    username=user1.subject,
                    administrated_permission_groups=[],
                    membered_permission_groups=[],
                )
                resp = self.client.delete(
                    f"{self.url}/{value1_of_parameter1_of_public_platform1_in_group1.id}"
                )
        self.expect(resp.status_code).to_equal(403)

    @fixtures.use(
        [
            "value1_of_parameter1_of_public_platform1_in_group1",
            "super_user",
        ]
    )
    def test_delete_for_public_platform_no_member_super_user(
        self,
        value1_of_parameter1_of_public_platform1_in_group1,
        super_user,
    ):
        """Ensure we can delete if we are super user, even without group membership."""
        with self.run_requests_as(super_user):
            resp = self.client.delete(
                f"{self.url}/{value1_of_parameter1_of_public_platform1_in_group1.id}"
            )
        self.expect(resp.status_code).to_equal(200)

    @fixtures.use(["user1", "value1_of_parameter1_of_private_platform_of_user1"])
    def test_delete_for_private_platform_creator(
        self, user1, value1_of_parameter1_of_private_platform_of_user1
    ):
        """Ensure we can delete for a private platform if we are creator."""
        with self.run_requests_as(user1):
            resp = self.client.delete(
                f"{self.url}/{value1_of_parameter1_of_private_platform_of_user1.id}",
            )
        self.expect(resp.status_code).to_equal(200)

    @fixtures.use(["user2", "value1_of_parameter1_of_private_platform_of_user1"])
    def test_delete_for_private_platform_different_user(
        self, user2, value1_of_parameter1_of_private_platform_of_user1
    ):
        """Ensure we can't delete for a private platform if we aren't the creator."""
        with self.run_requests_as(user2):
            resp = self.client.delete(
                f"{self.url}/{value1_of_parameter1_of_private_platform_of_user1.id}",
            )
        self.expect(resp.status_code).to_equal(403)

    @fixtures.use(["super_user", "value1_of_parameter1_of_private_platform_of_user1"])
    def test_delete_for_private_platform_super_user(
        self, super_user, value1_of_parameter1_of_private_platform_of_user1
    ):
        """Ensure we can delete for a private platform if we are super user."""
        with self.run_requests_as(super_user):
            resp = self.client.delete(
                f"{self.url}/{value1_of_parameter1_of_private_platform_of_user1.id}",
            )
        self.expect(resp.status_code).to_equal(200)

    @fixtures.use(
        [
            "super_user",
            "value1_of_parameter1_of_public_platform1_in_group1",
            "archived_public_platform1_in_group1",
        ]
    )
    def test_delete_for_archived_platform_super_user(
        self,
        super_user,
        value1_of_parameter1_of_public_platform1_in_group1,
        archived_public_platform1_in_group1,
    ):
        """Ensure we can't delete for archived platforms."""
        with self.run_requests_as(super_user):
            resp = self.client.delete(
                f"{self.url}/{value1_of_parameter1_of_public_platform1_in_group1.id}",
            )
        self.expect(resp.status_code).to_equal(403)
