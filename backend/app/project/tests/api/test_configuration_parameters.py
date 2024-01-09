# SPDX-FileCopyrightText: 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Tests for the configuration parameter endpoints."""

import datetime
import json
from unittest.mock import patch

import pytz

from project import base_url
from project.api.models import (
    Configuration,
    ConfigurationParameter,
    ConfigurationParameterValueChangeAction,
    Contact,
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
    """
    Create a second contact for the tests.

    Different from contact1 to support multiple users.
    """
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
    """Create another normal user to use it in the tests."""
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


@fixtures.register("public_configuration1_in_group1", scope=lambda: db.session)
def create_public_configuration1_in_group1():
    """Create a public configuration that uses group 1 for permission management."""
    result = Configuration(
        label="public configuration1",
        is_internal=False,
        is_public=True,
        cfg_permission_group="1",
    )
    db.session.add(result)
    db.session.commit()
    return result


@fixtures.register(
    "parameter1_of_public_configuration1_in_group1", scope=lambda: db.session
)
@fixtures.use(["public_configuration1_in_group1"])
def create_parameter1_of_public_configuration1_in_group1(
    public_configuration1_in_group1,
):
    """Create a parameter on public_configuration1."""
    result = ConfigurationParameter(
        configuration=public_configuration1_in_group1,
        label="specialvalue",
        description="some value",
        unit_name="count",
        unit_uri="http://foo/count",
    )
    db.session.add(result)
    db.session.commit()
    return result


@fixtures.register("archived_public_configuration1_in_group1", scope=lambda: db.session)
@fixtures.use(["public_configuration1_in_group1"])
def create_archvied_public_configuration1_in_group1(public_configuration1_in_group1):
    """Create an archived public configuration that uses group 1 for permission management."""
    public_configuration1_in_group1.archived = True
    db.session.add(public_configuration1_in_group1)
    db.session.commit()
    return public_configuration1_in_group1


@fixtures.register("archived_public_configuration2_in_group1", scope=lambda: db.session)
@fixtures.use(["public_configuration2_in_group1"])
def create_archvied_public_configuration2_in_group1(public_configuration2_in_group1):
    """Create another archived public configuration that uses group 1 for permission management."""
    public_configuration2_in_group1.archived = True
    db.session.add(public_configuration2_in_group1)
    db.session.commit()
    return public_configuration2_in_group1


@fixtures.register("public_configuration2_in_group1", scope=lambda: db.session)
def create_public_configuration2_in_group1():
    """Create another public configuration that uses group 1 for permission management."""
    result = Configuration(
        label="public configuration2",
        is_internal=False,
        is_public=True,
        cfg_permission_group="1",
    )
    db.session.add(result)
    db.session.commit()
    return result


@fixtures.register("internal_configuration1_in_group1", scope=lambda: db.session)
def create_internal_configuration1_in_group1():
    """Create an internal configuration that uses group 1 for permission management."""
    result = Configuration(
        label="internal configuration1",
        is_internal=True,
        is_public=False,
        cfg_permission_group="1",
    )
    db.session.add(result)
    db.session.commit()
    return result


class TestConfigurationParameterServices(BaseTestCase):
    """Test the urls to interact with the configuration parameters."""

    url = base_url + "/configuration-parameters"

    def test_get_list_empty(self):
        """Ensure that we query the url and get an empty list if there are no data."""
        resp = self.client.get(self.url)
        self.expect(resp.status_code).to_equal(200)

    @fixtures.use(
        [
            "public_configuration1_in_group1",
            "parameter1_of_public_configuration1_in_group1",
        ]
    )
    def test_get_list_for_public_configuration_no_user(
        self,
        public_configuration1_in_group1,
        parameter1_of_public_configuration1_in_group1,
    ):
        """Ensure we get public configurations without user."""
        resp = self.client.get(self.url)
        self.expect(resp.status_code).to_equal(200)
        self.expect(resp.json["data"]).to_have_length(1)

        self.expect(resp.json["data"][0]["id"]).to_equal(
            str(parameter1_of_public_configuration1_in_group1.id)
        )
        self.expect(resp.json["data"][0]["type"]).to_equal("configuration_parameter")
        self.expect(resp.json["data"][0]["attributes"]["label"]).to_equal(
            "specialvalue"
        )
        self.expect(resp.json["data"][0]["attributes"]["description"]).to_equal(
            "some value"
        )
        self.expect(resp.json["data"][0]["attributes"]["unit_name"]).to_equal("count")
        self.expect(resp.json["data"][0]["attributes"]["unit_uri"]).to_equal(
            "http://foo/count"
        )
        self.expect(
            resp.json["data"][0]["attributes"]["created_at"]
        ).to_be_a_datetime_string()
        self.expect(
            resp.json["data"][0]["attributes"]["updated_at"]
        ).to_be_a_datetime_string()

        self.expect(
            resp.json["data"][0]["relationships"]["configuration"]["data"]["id"]
        ).to_equal(
            str(public_configuration1_in_group1.id),
        )
        self.expect(
            resp.json["data"][0]["relationships"]["configuration"]["data"]["type"]
        ).to_equal("configuration")
        self.expect(
            resp.json["data"][0]["relationships"][
                "configuration_parameter_value_change_actions"
            ]["data"]
        ).to_have_length(0),

    @fixtures.use(["internal_configuration1_in_group1"])
    def test_get_list_for_internal_configuration_no_user(
        self, internal_configuration1_in_group1
    ):
        """Ensure we don't include data for internal configurations if we don't have a user."""
        parameter = ConfigurationParameter(
            configuration=internal_configuration1_in_group1,
            label="specialvalue",
            description="some value",
            unit_name="count",
            unit_uri="http://foo/count",
        )
        db.session.add(parameter)
        db.session.commit()

        resp = self.client.get(self.url)
        self.expect(resp.status_code).to_equal(200)
        self.expect(resp.json["data"]).to_have_length(0)

    @fixtures.use(["user1", "internal_configuration1_in_group1"])
    def test_get_list_for_internal_configuration_with_user(
        self, user1, internal_configuration1_in_group1
    ):
        """Ensure we include data for internal configurations when we have a user."""
        parameter = ConfigurationParameter(
            configuration=internal_configuration1_in_group1,
            label="specialvalue",
            description="some value",
            unit_name="count",
            unit_uri="http://foo/count",
        )
        db.session.add(parameter)
        db.session.commit()

        with self.run_requests_as(user1):
            resp = self.client.get(self.url)
        self.expect(resp.status_code).to_equal(200)
        self.expect(resp.json["data"]).to_have_length(1)

    def test_get_one_non_existing(self):
        """Ensure that we get an 404 for a non existing parameter."""
        resp = self.client.get(self.url + "/12345678901234")
        self.expect(resp.status_code).to_equal(404)

    @fixtures.use(["public_configuration1_in_group1"])
    def test_get_one_for_public_configuration_no_user(
        self, public_configuration1_in_group1
    ):
        """Ensure we get parameters of public configurations even without user."""
        parameter = ConfigurationParameter(
            configuration=public_configuration1_in_group1,
            label="specialvalue",
            description="some value",
            unit_name="count",
            unit_uri="http://foo/count",
        )
        db.session.add(parameter)
        db.session.commit()

        resp = self.client.get(f"{self.url}/{parameter.id}")
        self.expect(resp.status_code).to_equal(200)

        self.expect(resp.json["data"]["id"]).to_equal(str(parameter.id))
        self.expect(resp.json["data"]["type"]).to_equal("configuration_parameter")
        self.expect(resp.json["data"]["attributes"]["label"]).to_equal("specialvalue")
        self.expect(resp.json["data"]["attributes"]["description"]).to_equal(
            "some value"
        )
        self.expect(resp.json["data"]["attributes"]["unit_name"]).to_equal("count")
        self.expect(resp.json["data"]["attributes"]["unit_uri"]).to_equal(
            "http://foo/count"
        )
        self.expect(
            resp.json["data"]["attributes"]["created_at"]
        ).to_be_a_datetime_string()
        self.expect(
            resp.json["data"]["attributes"]["updated_at"]
        ).to_be_a_datetime_string()

        self.expect(
            resp.json["data"]["relationships"]["configuration"]["data"]["id"]
        ).to_equal(
            str(public_configuration1_in_group1.id),
        )
        self.expect(
            resp.json["data"]["relationships"]["configuration"]["data"]["type"]
        ).to_equal("configuration")
        self.expect(
            resp.json["data"]["relationships"][
                "configuration_parameter_value_change_actions"
            ]["data"]
        ).to_have_length(0)

    @fixtures.use(["internal_configuration1_in_group1"])
    def test_get_one_for_internal_configuration_no_user(
        self, internal_configuration1_in_group1
    ):
        """Ensure we get an 401 for an internal configuration without a user."""
        parameter = ConfigurationParameter(
            configuration=internal_configuration1_in_group1,
            label="specialvalue",
            description="some value",
            unit_name="count",
            unit_uri="http://foo/count",
        )
        db.session.add(parameter)
        db.session.commit()

        resp = self.client.get(f"{self.url}/{parameter.id}")
        self.expect(resp.status_code).to_equal(401)

    @fixtures.use(["user1", "internal_configuration1_in_group1"])
    def test_get_one_for_internal_configuration_with_user(
        self, user1, internal_configuration1_in_group1
    ):
        """Ensure we can access data for internal configurations when we have a user."""
        parameter = ConfigurationParameter(
            configuration=internal_configuration1_in_group1,
            label="specialvalue",
            description="some value",
            unit_name="count",
            unit_uri="http://foo/count",
        )
        db.session.add(parameter)
        db.session.commit()

        with self.run_requests_as(user1):
            resp = self.client.get(f"{self.url}/{parameter.id}")
        self.expect(resp.status_code).to_equal(200)

    @fixtures.use(
        ["public_configuration1_in_group1", "public_configuration2_in_group1"]
    )
    def test_get_list_prefiltered_by_configuration(
        self, public_configuration1_in_group1, public_configuration2_in_group1
    ):
        """Ensure we get can prefilter by configuration."""
        parameter1 = ConfigurationParameter(
            configuration=public_configuration1_in_group1,
            label="specialvalue",
            description="some value",
            unit_name="count",
            unit_uri="http://foo/count",
        )
        parameter2 = ConfigurationParameter(
            configuration=public_configuration2_in_group1,
            label="othervalue",
            description="some value",
            unit_name="meter",
            unit_uri="http://foo/meter",
        )
        db.session.add_all([parameter1, parameter2])
        db.session.commit()

        resp1 = self.client.get(
            f"{base_url}/configurations/{public_configuration1_in_group1.id}/configuration-parameters"
        )
        self.expect(resp1.status_code).to_equal(200)
        self.expect(resp1.json["data"]).to_have_length(1)
        self.expect(resp1.json["data"][0]["id"]).to_equal(str(parameter1.id))

        resp2 = self.client.get(
            f"{base_url}/configurations/{public_configuration2_in_group1.id}/configuration-parameters"
        )
        self.expect(resp2.status_code).to_equal(200)
        self.expect(resp2.json["data"]).to_have_length(1)
        self.expect(resp2.json["data"][0]["id"]).to_equal(str(parameter2.id))

    @fixtures.use(["public_configuration1_in_group1"])
    def test_get_list_prefiltered_invalid_configuration_id(
        self, public_configuration1_in_group1
    ):
        """Ensure we get an 404 if the configuration id doesn't exist."""
        parameter = ConfigurationParameter(
            configuration=public_configuration1_in_group1,
            label="specialvalue",
            description="some value",
            unit_name="count",
            unit_uri="http://foo/count",
        )
        db.session.add(parameter)
        db.session.commit()

        resp = self.client.get(
            f"{base_url}/configurations/{public_configuration1_in_group1.id+12345}/configuration-parameters"
        )
        self.expect(resp.status_code).to_equal(404)

    @fixtures.use(
        ["public_configuration1_in_group1", "public_configuration2_in_group1"]
    )
    def test_get_list_prefiltered_by_configuration_id(
        self, public_configuration1_in_group1, public_configuration2_in_group1
    ):
        """Ensure we get can prefilter by filter[configuration_id]."""
        parameter1 = ConfigurationParameter(
            configuration=public_configuration1_in_group1,
            label="specialvalue",
            description="some value",
            unit_name="count",
            unit_uri="http://foo/count",
        )
        parameter2 = ConfigurationParameter(
            configuration=public_configuration2_in_group1,
            label="othervalue",
            description="some value",
            unit_name="meter",
            unit_uri="http://foo/meter",
        )
        db.session.add_all([parameter1, parameter2])
        db.session.commit()

        resp1 = self.client.get(
            f"{base_url}/configuration-parameters?filter[configuration_id]={public_configuration1_in_group1.id}"
        )
        self.expect(resp1.status_code).to_equal(200)
        self.expect(resp1.json["data"]).to_have_length(1)
        self.expect(resp1.json["data"][0]["id"]).to_equal(str(parameter1.id))

        resp2 = self.client.get(
            f"{base_url}/configuration-parameters?filter[configuration_id]={public_configuration2_in_group1.id}"
        )
        self.expect(resp2.status_code).to_equal(200)
        self.expect(resp2.json["data"]).to_have_length(1)
        self.expect(resp2.json["data"][0]["id"]).to_equal(str(parameter2.id))

        resp3 = self.client.get(
            f"{base_url}/configuration-parameters?filter[configuration_id]={public_configuration2_in_group1.id + 9999}"
        )
        self.expect(resp3.status_code).to_equal(200)
        self.expect(resp3.json["data"]).to_have_length(0)

    @fixtures.use(["public_configuration1_in_group1"])
    def test_post_no_user(self, public_configuration1_in_group1):
        """Ensure we can't post if we don't have a user."""
        payload = {
            "data": {
                "type": "configuration_parameter",
                "attributes": {
                    "label": "specialvalue",
                    "description": "some description",
                    "unit_uri": "http://foo/count",
                    "unit_name": "count",
                },
                "relationships": {
                    "configuration": {
                        "data": {
                            "id": str(public_configuration1_in_group1.id),
                            "type": "configuration",
                        }
                    }
                },
            }
        }

        resp = self.client.post(self.url, data=json.dumps(payload))
        self.expect(resp.status_code).to_equal(401)

    @fixtures.use(["user1", "public_configuration1_in_group1"])
    def test_post_member(self, user1, public_configuration1_in_group1):
        """Ensure we can post if we are a member of one of the groups."""
        payload = {
            "data": {
                "type": "configuration_parameter",
                "attributes": {
                    "label": "specialvalue",
                    "description": "some description",
                    "unit_uri": "http://foo/count",
                    "unit_name": "count",
                },
                "relationships": {
                    "configuration": {
                        "data": {
                            "id": str(public_configuration1_in_group1.id),
                            "type": "configuration",
                        }
                    }
                },
            }
        }

        with self.run_requests_as(user1):
            with patch.object(idl, "get_all_permission_groups_for_a_user") as mock:
                mock.return_value = UserAccount(
                    id=user1.subject,
                    username=user1.subject,
                    administrated_permission_groups=[],
                    membered_permission_groups=[
                        public_configuration1_in_group1.cfg_permission_group
                    ],
                )
                resp = self.client.post(
                    self.url,
                    data=json.dumps(payload),
                    content_type="application/vnd.api+json",
                )
        self.expect(resp.status_code).to_equal(201)
        # Test some basic fields.
        self.expect(resp.json["data"]["attributes"]["label"]).to_equal("specialvalue")
        self.expect(resp.json["data"]["attributes"]["description"]).to_equal(
            "some description"
        )
        self.expect(resp.json["data"]["attributes"]["unit_uri"]).to_equal(
            "http://foo/count"
        )
        self.expect(resp.json["data"]["attributes"]["unit_name"]).to_equal("count")

        # And ensure that we set the created by id.
        self.expect(
            resp.json["data"]["relationships"]["created_by"]["data"]["id"]
        ).to_equal(str(user1.id))

        # And we also want to make sure that the configuration has an updated
        # update description.

        reloaded_configuration = (
            db.session.query(Configuration)
            .filter_by(id=public_configuration1_in_group1.id)
            .first()
        )
        self.expect(reloaded_configuration.update_description).to_equal(
            "create;configuration parameter"
        )

    @fixtures.use(["user1", "public_configuration1_in_group1"])
    def test_post_admin(self, user1, public_configuration1_in_group1):
        """Ensure we can post if we are a admin of one of the groups."""
        payload = {
            "data": {
                "type": "configuration_parameter",
                "attributes": {
                    "label": "specialvalue",
                    "description": "some description",
                    "unit_uri": "http://foo/count",
                    "unit_name": "count",
                },
                "relationships": {
                    "configuration": {
                        "data": {
                            "id": str(public_configuration1_in_group1.id),
                            "type": "configuration",
                        }
                    }
                },
            }
        }

        with self.run_requests_as(user1):
            with patch.object(idl, "get_all_permission_groups_for_a_user") as mock:
                mock.return_value = UserAccount(
                    id=user1.subject,
                    username=user1.subject,
                    administrated_permission_groups=[
                        public_configuration1_in_group1.cfg_permission_group
                    ],
                    membered_permission_groups=[],
                )
                resp = self.client.post(
                    self.url,
                    data=json.dumps(payload),
                    content_type="application/vnd.api+json",
                )
        self.expect(resp.status_code).to_equal(201)

    @fixtures.use(["user1", "public_configuration1_in_group1"])
    def test_post_not_in_group(self, user1, public_configuration1_in_group1):
        """Ensure we can't post if we are a not even member of one of the groups."""
        payload = {
            "data": {
                "type": "configuration_parameter",
                "attributes": {
                    "label": "specialvalue",
                    "description": "some description",
                    "unit_uri": "http://foo/count",
                    "unit_name": "count",
                },
                "relationships": {
                    "configuration": {
                        "data": {
                            "id": str(public_configuration1_in_group1.id),
                            "type": "configuration",
                        }
                    }
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

    @fixtures.use(["super_user", "public_configuration1_in_group1"])
    def test_post_not_in_group_super_user(
        self, super_user, public_configuration1_in_group1
    ):
        """Ensure we can post if we are a super user."""
        payload = {
            "data": {
                "type": "configuration_parameter",
                "attributes": {
                    "label": "specialvalue",
                    "description": "some description",
                    "unit_uri": "http://foo/count",
                    "unit_name": "count",
                },
                "relationships": {
                    "configuration": {
                        "data": {
                            "id": str(public_configuration1_in_group1.id),
                            "type": "configuration",
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

    @fixtures.use(["super_user", "archived_public_configuration1_in_group1"])
    def test_post_archived(self, super_user, archived_public_configuration1_in_group1):
        """Ensure not even super users can post for archived configurations."""
        payload = {
            "data": {
                "type": "configuration_parameter",
                "attributes": {
                    "label": "specialvalue",
                    "description": "some description",
                    "unit_uri": "http://foo/count",
                    "unit_name": "count",
                },
                "relationships": {
                    "configuration": {
                        "data": {
                            "id": str(archived_public_configuration1_in_group1.id),
                            "type": "configuration",
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
        self.expect(resp.status_code).to_equal(403)

    @fixtures.use(["super_user", "public_configuration1_in_group1"])
    def test_post_missing_label(self, super_user, public_configuration1_in_group1):
        """Ensure we can't post if we don't provide a label."""
        payload = {
            "data": {
                "type": "configuration_parameter",
                "attributes": {
                    "label": None,
                    "description": "some description",
                    "unit_uri": "http://foo/count",
                    "unit_name": "count",
                },
                "relationships": {
                    "configuration": {
                        "data": {
                            "id": str(public_configuration1_in_group1.id),
                            "type": "configuration",
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
        self.expect(resp.status_code).to_equal(422)

    @fixtures.use(["super_user"])
    def test_post_missing_configuration(self, super_user):
        """Ensure we can't post if we don't provide a configuration."""
        payload = {
            "data": {
                "type": "configuration_parameter",
                "attributes": {
                    "label": "specialvalue",
                    "description": "some description",
                    "unit_uri": "http://foo/count",
                    "unit_name": "count",
                },
                "relationships": {
                    "configuration": {
                        "data": None,
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
        self.expect(resp.status_code).to_equal(422)

    @fixtures.use(["super_user", "public_configuration1_in_group1"])
    def test_post_missing_attributes(self, super_user, public_configuration1_in_group1):
        """Ensure we can post if don't include non required attributes."""
        payload = {
            "data": {
                "type": "configuration_parameter",
                "attributes": {
                    "label": "specialvalue",
                },
                "relationships": {
                    "configuration": {
                        "data": {
                            "id": str(public_configuration1_in_group1.id),
                            "type": "configuration",
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

    @fixtures.use(["parameter1_of_public_configuration1_in_group1"])
    def test_patch_for_public_configuration_no_user(
        self, parameter1_of_public_configuration1_in_group1
    ):
        """Ensure we can't patch without a user."""
        payload = {
            "data": {
                "type": "configuration_parameter",
                "attributes": {
                    "label": "super specialvalue",
                },
            }
        }

        resp = self.client.patch(
            f"{self.url}/{parameter1_of_public_configuration1_in_group1.id}",
            data=json.dumps(payload),
            content_type="application/vnd.api+json",
        )
        self.expect(resp.status_code).to_equal(401)

    @fixtures.use(
        [
            "user1",
            "parameter1_of_public_configuration1_in_group1",
            "public_configuration1_in_group1",
        ]
    )
    def test_patch_for_public_configuration_member(
        self,
        user1,
        parameter1_of_public_configuration1_in_group1,
        public_configuration1_in_group1,
    ):
        """Ensure we can patch if we are a member."""
        payload = {
            "data": {
                "id": str(parameter1_of_public_configuration1_in_group1.id),
                "type": "configuration_parameter",
                "attributes": {
                    "label": "super specialvalue",
                },
            }
        }

        with self.run_requests_as(user1):
            with patch.object(idl, "get_all_permission_groups_for_a_user") as mock:
                mock.return_value = UserAccount(
                    id=user1.subject,
                    username=user1.subject,
                    administrated_permission_groups=[],
                    membered_permission_groups=[
                        public_configuration1_in_group1.cfg_permission_group
                    ],
                )
                resp = self.client.patch(
                    f"{self.url}/{parameter1_of_public_configuration1_in_group1.id}",
                    data=json.dumps(payload),
                    content_type="application/vnd.api+json",
                )
        self.expect(resp.status_code).to_equal(200)
        self.expect(resp.json["data"]["attributes"]["label"]).to_equal(
            "super specialvalue"
        )
        # Also check that we set the updated by value.
        self.expect(
            resp.json["data"]["relationships"]["updated_by"]["data"]["id"]
        ).to_equal(str(user1.id))

        # and we check that the configuration has a changed update description

        reloaded_configuration = (
            db.session.query(Configuration)
            .filter_by(id=public_configuration1_in_group1.id)
            .first()
        )
        self.expect(reloaded_configuration.update_description).to_equal(
            "update;configuration parameter"
        )

    @fixtures.use(
        [
            "user1",
            "parameter1_of_public_configuration1_in_group1",
            "public_configuration1_in_group1",
        ]
    )
    def test_patch_for_public_configuration_admin(
        self,
        user1,
        parameter1_of_public_configuration1_in_group1,
        public_configuration1_in_group1,
    ):
        """Ensure we can patch if we are an admin of the group."""
        payload = {
            "data": {
                "id": str(parameter1_of_public_configuration1_in_group1.id),
                "type": "configuration_parameter",
                "attributes": {
                    "label": "super specialvalue",
                },
            }
        }

        with self.run_requests_as(user1):
            with patch.object(idl, "get_all_permission_groups_for_a_user") as mock:
                mock.return_value = UserAccount(
                    id=user1.subject,
                    username=user1.subject,
                    administrated_permission_groups=[
                        public_configuration1_in_group1.cfg_permission_group
                    ],
                    membered_permission_groups=[],
                )
                resp = self.client.patch(
                    f"{self.url}/{parameter1_of_public_configuration1_in_group1.id}",
                    data=json.dumps(payload),
                    content_type="application/vnd.api+json",
                )
        self.expect(resp.status_code).to_equal(200)

    @fixtures.use(
        [
            "user1",
            "parameter1_of_public_configuration1_in_group1",
            "public_configuration1_in_group1",
        ]
    )
    def test_patch_for_public_configuration_no_member(
        self,
        user1,
        parameter1_of_public_configuration1_in_group1,
        public_configuration1_in_group1,
    ):
        """Ensure we can't patch if we are not even an member of the group."""
        payload = {
            "data": {
                "id": str(parameter1_of_public_configuration1_in_group1.id),
                "type": "configuration_parameter",
                "attributes": {
                    "label": "super specialvalue",
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
                    f"{self.url}/{parameter1_of_public_configuration1_in_group1.id}",
                    data=json.dumps(payload),
                    content_type="application/vnd.api+json",
                )
        self.expect(resp.status_code).to_equal(403)

    @fixtures.use(
        [
            "super_user",
            "parameter1_of_public_configuration1_in_group1",
            "public_configuration1_in_group1",
        ]
    )
    def test_patch_for_public_configuration_no_member_super_user(
        self,
        super_user,
        parameter1_of_public_configuration1_in_group1,
        public_configuration1_in_group1,
    ):
        """Ensure we can patch if we are super user."""
        payload = {
            "data": {
                "id": str(parameter1_of_public_configuration1_in_group1.id),
                "type": "configuration_parameter",
                "attributes": {
                    "label": "super specialvalue",
                },
            }
        }

        with self.run_requests_as(super_user):
            resp = self.client.patch(
                f"{self.url}/{parameter1_of_public_configuration1_in_group1.id}",
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.expect(resp.status_code).to_equal(200)

    @fixtures.use(
        [
            "super_user",
            "parameter1_of_public_configuration1_in_group1",
            "archived_public_configuration1_in_group1",
        ]
    )
    def test_patch_for_archived_configuration_super_user(
        self,
        super_user,
        parameter1_of_public_configuration1_in_group1,
        archived_public_configuration1_in_group1,
    ):
        """Ensure we can't patch for archived configurations."""
        payload = {
            "data": {
                "id": str(parameter1_of_public_configuration1_in_group1.id),
                "type": "configuration_parameter",
                "attributes": {
                    "label": "super specialvalue",
                },
            }
        }

        with self.run_requests_as(super_user):
            resp = self.client.patch(
                f"{self.url}/{parameter1_of_public_configuration1_in_group1.id}",
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.expect(resp.status_code).to_equal(403)

    @fixtures.use(
        [
            "super_user",
            "parameter1_of_public_configuration1_in_group1",
            "archived_public_configuration2_in_group1",
        ]
    )
    def test_patch_to_archived_configuration_super_user(
        self,
        super_user,
        parameter1_of_public_configuration1_in_group1,
        archived_public_configuration2_in_group1,
    ):
        """Ensure we can't patch to non editable configurations."""
        payload = {
            "data": {
                "id": str(parameter1_of_public_configuration1_in_group1.id),
                "type": "configuration_parameter",
                "attributes": {
                    "label": "super specialvalue",
                },
                "relationships": {
                    "configuration": {
                        "data": {
                            "id": str(archived_public_configuration2_in_group1.id),
                            "type": "configuration",
                        }
                    }
                },
            }
        }

        with self.run_requests_as(super_user):
            resp = self.client.patch(
                f"{self.url}/{parameter1_of_public_configuration1_in_group1.id}",
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.expect(resp.status_code).to_equal(403)

    @fixtures.use(["parameter1_of_public_configuration1_in_group1"])
    def test_delete_for_public_configuration_no_user(
        self, parameter1_of_public_configuration1_in_group1
    ):
        """Ensure we can't delete without a user."""
        resp = self.client.delete(
            f"{self.url}/{parameter1_of_public_configuration1_in_group1.id}",
        )
        self.expect(resp.status_code).to_equal(401)

    @fixtures.use(
        [
            "user1",
            "parameter1_of_public_configuration1_in_group1",
            "public_configuration1_in_group1",
        ]
    )
    def test_delete_for_public_configuration_member(
        self,
        user1,
        parameter1_of_public_configuration1_in_group1,
        public_configuration1_in_group1,
    ):
        """Ensure we can delete if we are a member."""
        with self.run_requests_as(user1):
            with patch.object(idl, "get_all_permission_groups_for_a_user") as mock:
                mock.return_value = UserAccount(
                    id=user1.subject,
                    username=user1.subject,
                    administrated_permission_groups=[],
                    membered_permission_groups=[
                        public_configuration1_in_group1.cfg_permission_group
                    ],
                )
                resp = self.client.delete(
                    f"{self.url}/{parameter1_of_public_configuration1_in_group1.id}",
                )
        self.expect(resp.status_code).to_equal(200)
        # We check that the configuration has a changed update description

        reloaded_configuration = (
            db.session.query(Configuration)
            .filter_by(id=public_configuration1_in_group1.id)
            .first()
        )
        self.expect(reloaded_configuration.update_description).to_equal(
            "delete;configuration parameter"
        )

    @fixtures.use(
        [
            "user1",
            "parameter1_of_public_configuration1_in_group1",
            "public_configuration1_in_group1",
        ]
    )
    def test_delete_for_public_configuration_admin(
        self,
        user1,
        parameter1_of_public_configuration1_in_group1,
        public_configuration1_in_group1,
    ):
        """Ensure we can delete if we are an admin of the group."""
        with self.run_requests_as(user1):
            with patch.object(idl, "get_all_permission_groups_for_a_user") as mock:
                mock.return_value = UserAccount(
                    id=user1.subject,
                    username=user1.subject,
                    administrated_permission_groups=[
                        public_configuration1_in_group1.cfg_permission_group
                    ],
                    membered_permission_groups=[],
                )
                resp = self.client.delete(
                    f"{self.url}/{parameter1_of_public_configuration1_in_group1.id}",
                )
        self.expect(resp.status_code).to_equal(200)

    @fixtures.use(
        [
            "user1",
            "parameter1_of_public_configuration1_in_group1",
            "public_configuration1_in_group1",
        ]
    )
    def test_delete_for_public_configuration_no_member(
        self,
        user1,
        parameter1_of_public_configuration1_in_group1,
        public_configuration1_in_group1,
    ):
        """Ensure we can't delete if we are not even an member of the group."""
        with self.run_requests_as(user1):
            with patch.object(idl, "get_all_permission_groups_for_a_user") as mock:
                mock.return_value = UserAccount(
                    id=user1.subject,
                    username=user1.subject,
                    administrated_permission_groups=[],
                    membered_permission_groups=[],
                )
                resp = self.client.delete(
                    f"{self.url}/{parameter1_of_public_configuration1_in_group1.id}",
                )
        self.expect(resp.status_code).to_equal(403)

    @fixtures.use(
        [
            "super_user",
            "parameter1_of_public_configuration1_in_group1",
            "public_configuration1_in_group1",
        ]
    )
    def test_delete_for_public_configuration_no_member_super_user(
        self,
        super_user,
        parameter1_of_public_configuration1_in_group1,
        public_configuration1_in_group1,
    ):
        """Ensure we can delete if we are super user."""
        with self.run_requests_as(super_user):
            resp = self.client.delete(
                f"{self.url}/{parameter1_of_public_configuration1_in_group1.id}",
            )
        self.expect(resp.status_code).to_equal(200)

    @fixtures.use(
        [
            "super_user",
            "parameter1_of_public_configuration1_in_group1",
            "archived_public_configuration1_in_group1",
        ]
    )
    def test_delete_for_archived_configuration_super_user(
        self,
        super_user,
        parameter1_of_public_configuration1_in_group1,
        archived_public_configuration1_in_group1,
    ):
        """Ensure we can't delete for archived configurations."""
        with self.run_requests_as(super_user):
            resp = self.client.delete(
                f"{self.url}/{parameter1_of_public_configuration1_in_group1.id}",
            )
        self.expect(resp.status_code).to_equal(403)

    @fixtures.use(["parameter1_of_public_configuration1_in_group1", "contact1"])
    def test_include_parameter_value_change_actions(
        self, parameter1_of_public_configuration1_in_group1, contact1
    ):
        """Ensure we can include the value change actions in the payload."""
        value1 = ConfigurationParameterValueChangeAction(
            configuration_parameter=parameter1_of_public_configuration1_in_group1,
            contact=contact1,
            date=datetime.datetime(2023, 5, 2, 15, 30, 00, tzinfo=pytz.utc),
            value="3",
        )
        value2 = ConfigurationParameterValueChangeAction(
            configuration_parameter=parameter1_of_public_configuration1_in_group1,
            contact=contact1,
            date=datetime.datetime(2023, 5, 2, 19, 30, 00, tzinfo=pytz.utc),
            value="42",
        )
        db.session.add_all([value1, value2])

        resp = self.client.get(
            "".join(
                [
                    self.url,
                    "/",
                    str(parameter1_of_public_configuration1_in_group1.id),
                    "?",
                    "include=configuration_parameter_value_change_actions",
                ]
            ),
        )
        self.expect(resp.status_code).to_equal(200)
        values = [x["attributes"]["value"] for x in resp.json["included"]]
        self.expect(values).to_have_length(2)
        self.expect(values).to_include_all_of(["3", "42"])

    @fixtures.use(
        [
            "super_user",
            "parameter1_of_public_configuration1_in_group1",
            "public_configuration1_in_group1",
        ]
    )
    def test_delete_for_public_configuration_with_action(
        self,
        super_user,
        parameter1_of_public_configuration1_in_group1,
        public_configuration1_in_group1,
    ):
        """Ensure we can't delete if we have a value chance action."""
        value1 = ConfigurationParameterValueChangeAction(
            configuration_parameter=parameter1_of_public_configuration1_in_group1,
            contact=super_user.contact,
            date=datetime.datetime(2023, 5, 2, 15, 30, 00, tzinfo=pytz.utc),
            value="3",
        )
        db.session.add(value1)
        db.session.commit()

        with self.run_requests_as(super_user):
            resp = self.client.delete(
                f"{self.url}/{parameter1_of_public_configuration1_in_group1.id}",
            )
        self.expect(resp.status_code).to_equal(409)
