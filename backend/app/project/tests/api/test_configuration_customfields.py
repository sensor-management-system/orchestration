# SPDX-FileCopyrightText: 2022 - 2024
# - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Tests for the configuration custom field endpoints."""

import json

from project import base_url
from project.api.models import Configuration, ConfigurationCustomField, Contact, User
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
    "customfield1_of_public_configuration1_in_group1", scope=lambda: db.session
)
@fixtures.use(["public_configuration1_in_group1"])
def create_customfield1_of_public_configuration1_in_group1(
    public_configuration1_in_group1,
):
    """Create an customfield for the public configuration."""
    result = ConfigurationCustomField(
        configuration=public_configuration1_in_group1,
        key="https://gfz-potsdam.de",
        value="GFZ",
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


class TestConfigurationCustomFieldServices(BaseTestCase):
    """Test configuration customfields."""

    url = base_url + "/configuration-customfields"

    def test_post_configuration_customfield_api(self):
        """Ensure that we can add a custom field."""
        # First we need to make sure that we have a configuration
        configuration = Configuration(
            label="Very new configuration",
            is_public=True,
            is_internal=False,
        )
        db.session.add(configuration)
        db.session.commit()

        # Now as it is saved we can be sure that has an id
        self.assertTrue(configuration.id is not None)

        count_customfields = (
            db.session.query(ConfigurationCustomField)
            .filter_by(
                configuration_id=configuration.id,
            )
            .count()
        )
        # However, this new configuration for sure has no customfields
        self.assertEqual(count_customfields, 0)

        # Now we can write the request to add a customfield
        payload = {
            "data": {
                "type": "configuration_customfield",
                "attributes": {
                    "value": "https://www.gfz-potsdam.de",
                    "key": "GFZ Homepage",
                    "description": "The GFZ homepage",
                },
                "relationships": {
                    "configuration": {
                        "data": {"type": "configuration", "id": str(configuration.id)}
                    }
                },
            }
        }
        with self.client:
            url_post = base_url + "/configuration-customfields"
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
            db.session.query(ConfigurationCustomField).filter_by(
                configuration_id=configuration.id,
            )
        )
        # We now have one customfield
        self.assertEqual(len(customfields), 1)

        # And it is as we specified it
        customfield = customfields[0]
        self.assertEqual(customfield.value, "https://www.gfz-potsdam.de")
        self.assertEqual(customfield.key, "GFZ Homepage")
        self.assertEqual(customfield.description, "The GFZ homepage")
        self.assertEqual(customfield.configuration_id, configuration.id)
        self.assertEqual(
            str(customfield.configuration_id), response.get_json()["data"]["id"]
        )

        reloaded_configuration = (
            db.session.query(Configuration).filter_by(id=configuration.id).first()
        )
        self.assertEqual(
            reloaded_configuration.update_description, "create;custom field"
        )

    def test_post_configuration_customfield_api_missing_key(self):
        """Ensure that we don't add a customfield with missing key."""
        configuration = Configuration(
            label="Very new configuration",
            is_public=True,
            is_internal=False,
        )
        db.session.add(configuration)
        db.session.commit()

        # Now we can write the request to add a customfield
        payload = {
            "data": {
                "type": "configuration_customfield",
                "attributes": {
                    "key": None,
                    "value": "GFZ Homepage",
                },
                "relationships": {
                    "configuration": {
                        "data": {"type": "configuration", "id": str(configuration.id)}
                    }
                },
            }
        }
        with self.client:
            url_post = base_url + "/configuration-customfields"
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
            db.session.query(ConfigurationCustomField)
            .filter_by(
                configuration_id=configuration.id,
            )
            .count()
        )
        self.assertEqual(count_customfields, 0)

    def test_post_configuration_customfield_api_missing_configuration(self):
        """Ensure that we don't add a customfield with missing configuration."""
        count_customfields_before = db.session.query(ConfigurationCustomField).count()
        payload = {
            "data": {
                "type": "configuration_customfield",
                "attributes": {
                    "key": "GFZ!",
                    "value": "GFZ Homepage",
                },
                "relationships": {
                    "configuration": {"data": {"type": "configuration", "id": None}}
                },
            }
        }
        with self.client:
            url_post = base_url + "/configuration-customfields"
            response = self.client.post(
                url_post,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
                headers=create_token(),
            )
        # it will not work, as we miss an important part (the configuration)
        self.assertEqual(response.status_code, 422)
        self.assertNotEqual(response.status_code, 200)
        count_customfields_after = db.session.query(ConfigurationCustomField).count()
        self.assertEqual(count_customfields_before, count_customfields_after)

    def test_get_configuration_customfields_api(self):
        """Ensure that we can get a list of configuration customfields."""
        configuration1 = Configuration(
            label="Just a configuration",
            is_public=True,
            is_internal=False,
        )
        configuration2 = Configuration(
            label="Another configuration",
            is_public=True,
            is_internal=False,
        )

        db.session.add(configuration1)
        db.session.add(configuration2)
        db.session.commit()

        customfield1 = ConfigurationCustomField(
            key="GFZ",
            value="https://www.gfz-potsdam.de",
            description="The GFZ homepage",
            configuration=configuration1,
        )
        customfield2 = ConfigurationCustomField(
            key="UFZ",
            value="https://www.ufz.de",
            configuration=configuration1,
        )
        customfield3 = ConfigurationCustomField(
            key="PIK",
            value="https://www.pik-potsdam.de",
            configuration=configuration2,
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
                base_url + "/configuration-customfields",
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
                    # and we want to check the link for the configuration as well
                    configuration_link = customfield["relationships"]["configuration"][
                        "links"
                    ]["related"]
                    resp_configuration = self.client.get(
                        configuration_link,
                        content_type="application/vnd.api+json",
                    )
                    self.assertEqual(resp_configuration.status_code, 200)
                    self.assertEqual(
                        resp_configuration.get_json()["data"]["id"],
                        str(customfield1.configuration_id),
                    )
                    self.assertEqual(
                        resp_configuration.get_json()["data"]["attributes"]["label"],
                        customfield1.configuration.label,
                    )

            self.assertTrue(customfield1_data is not None)

            # Now we tested the get request for the list response
            # It is time to check the detail one as well
            response = self.client.get(
                base_url + "/configuration-customfields/" + str(customfield1.id),
                content_type="application/vnd.api+json",
            )
            self.assertEqual(response.status_code, 200)
            # I already tested the response for this customfield
            self.assertEqual(response.get_json()["data"], customfield1_data)

            # And now we want to make sure that we already filter the customfields
            # with a given configuration id
            response = self.client.get(
                base_url
                + "/configurations/"
                + str(configuration1.id)
                + "/configuration-customfields",
                content_type="application/vnd.api+json",
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.get_json()["data"]), 2)
            response = self.client.get(
                base_url
                + "/configurations/"
                + str(configuration2.id)
                + "/configuration-customfields",
                content_type="application/vnd.api+json",
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.get_json()["data"]), 1)

    def test_get_configuration_customfields_filter_configuration_id(self):
        """Ensure that we can get filter by configuration_id."""
        configuration1 = Configuration(
            label="Just a configuration",
            is_public=True,
            is_internal=False,
        )
        configuration2 = Configuration(
            label="Another configuration",
            is_public=True,
            is_internal=False,
        )

        db.session.add(configuration1)
        db.session.add(configuration2)
        db.session.commit()

        customfield1 = ConfigurationCustomField(
            key="GFZ",
            value="https://www.gfz-potsdam.de",
            description="The GFZ homepage",
            configuration=configuration1,
        )
        customfield2 = ConfigurationCustomField(
            key="UFZ",
            value="https://www.ufz.de",
            configuration=configuration1,
        )
        customfield3 = ConfigurationCustomField(
            key="PIK",
            value="https://www.pik-potsdam.de",
            configuration=configuration2,
        )

        db.session.add(customfield1)
        db.session.add(customfield2)
        db.session.add(customfield3)
        db.session.commit()

        with self.client:
            response = self.client.get(
                base_url
                + f"/configuration-customfields?filter[configuration_id]={configuration1.id}",
                content_type="application/vnd.api+json",
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.get_json()["data"]), 2)
            response = self.client.get(
                base_url
                + f"/configuration-customfields?filter[configuration_id]={configuration2.id}",
                content_type="application/vnd.api+json",
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.get_json()["data"]), 1)

            response = self.client.get(
                base_url
                + f"/configuration-customfields?filter[configuration_id]={configuration2.id + 999}",
                content_type="application/vnd.api+json",
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.get_json()["data"]), 0)

    def test_patch_configuration_customfield_api_configuration(self):
        """Ensure that we can update a customfield by changing the configuration."""
        configuration1 = Configuration(
            label="Just a configuration",
            is_public=True,
            is_internal=False,
        )
        configuration2 = Configuration(
            label="Another configuration",
            is_public=True,
            is_internal=False,
        )

        db.session.add(configuration1)
        db.session.add(configuration2)
        db.session.commit()

        customfield1 = ConfigurationCustomField(
            key="GFZ",
            value="https://www.gfz-potsdam.de",
            configuration=configuration1,
        )
        db.session.add(customfield1)
        db.session.commit()

        payload = {
            "data": {
                "type": "configuration_customfield",
                "id": str(customfield1.id),
                "attributes": {
                    "key": "UFZ",
                    "value": "https://www.ufz.de",
                },
                "relationships": {
                    "configuration": {
                        "data": {"type": "configuration", "id": str(configuration2.id)}
                    }
                },
            }
        }
        with self.client:
            url_patch = base_url + "/configuration-customfields/" + str(customfield1.id)
            response = self.client.patch(
                url_patch,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
                headers=create_token(),
            )

        self.assertEqual(response.status_code, 200)

        customfield_reloaded = (
            db.session.query(ConfigurationCustomField)
            .filter_by(id=customfield1.id)
            .one()
        )
        self.assertEqual(customfield_reloaded.value, "https://www.ufz.de")
        self.assertEqual(customfield_reloaded.key, "UFZ")
        self.assertEqual(customfield_reloaded.configuration_id, configuration2.id)

    def test_patch_configuration_customfield_api_value(self):
        """Ensure that we can update a customfield by changing key & value."""
        configuration = Configuration(
            label="Just a configuration",
            is_public=True,
            is_internal=False,
        )

        db.session.add(configuration)
        db.session.commit()

        customfield1 = ConfigurationCustomField(
            key="GFZ",
            value="https://www.gfz-potsdam.de",
            configuration=configuration,
        )
        db.session.add(customfield1)
        db.session.commit()

        payload = {
            "data": {
                "type": "configuration_customfield",
                "id": str(customfield1.id),
                "attributes": {
                    "key": "UFZ",
                    "value": "https://www.ufz.de",
                },
            }
        }
        with self.client:
            url_patch = base_url + "/configuration-customfields/" + str(customfield1.id)
            response = self.client.patch(
                url_patch,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
                headers=create_token(),
            )

        self.assertEqual(response.status_code, 200)

        customfield_reloaded = (
            db.session.query(ConfigurationCustomField)
            .filter_by(id=customfield1.id)
            .one()
        )
        self.assertEqual(customfield_reloaded.value, "https://www.ufz.de")
        self.assertEqual(customfield_reloaded.key, "UFZ")

        reloaded_configuration = (
            db.session.query(Configuration).filter_by(id=configuration.id).first()
        )
        self.assertEqual(
            reloaded_configuration.update_description, "update;custom field"
        )

    def test_http_response_not_found(self):
        """Make sure that the backend responds with 404 HTTP-Code if a resource was not found."""
        url = f"{self.url}/{fake.random_int()}"
        _ = super().http_code_404_when_resource_not_found(url)

    @fixtures.use(["super_user", "public_configuration1_in_group1"])
    def test_post_triggers_mqtt_notification(
        self, super_user, public_configuration1_in_group1
    ):
        """Ensure that we can post a customfield and publish the notification via mqtt."""
        payload = {
            "data": {
                "type": "configuration_customfield",
                "attributes": {
                    "key": "GFZ",
                    "value": "https://gfz-potsdam.de",
                },
                "relationships": {
                    "configuration": {
                        "data": {
                            "type": "configuration",
                            "id": str(public_configuration1_in_group1.id),
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

        self.expect(call_args[0]).to_equal("sms/post-configuration-customfield")
        notification_data = json.loads(call_args[1])["data"]
        self.expect(notification_data["type"]).to_equal("configuration_customfield")
        self.expect(notification_data["attributes"]["key"]).to_equal("GFZ")
        self.expect(str).of(notification_data["id"]).to_match(r"\d+")

    @fixtures.use(["super_user", "customfield1_of_public_configuration1_in_group1"])
    def test_patch_triggers_mqtt_notification(
        self, super_user, customfield1_of_public_configuration1_in_group1
    ):
        """Ensure that we can patch a customfield and publish the notification via mqtt."""
        with self.run_requests_as(super_user):
            resp = self.client.patch(
                f"{self.url}/{customfield1_of_public_configuration1_in_group1.id}",
                data=json.dumps(
                    {
                        "data": {
                            "type": "configuration_customfield",
                            "id": str(
                                customfield1_of_public_configuration1_in_group1.id
                            ),
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

        self.expect(call_args[0]).to_equal("sms/patch-configuration-customfield")
        notification_data = json.loads(call_args[1])["data"]
        self.expect(notification_data["type"]).to_equal("configuration_customfield")
        self.expect(notification_data["attributes"]["value"]).to_equal("website")
        self.expect(notification_data["attributes"]["key"]).to_equal(
            customfield1_of_public_configuration1_in_group1.key
        )

    @fixtures.use(["super_user", "customfield1_of_public_configuration1_in_group1"])
    def test_delete_triggers_mqtt_notification(
        self,
        super_user,
        customfield1_of_public_configuration1_in_group1,
    ):
        """Ensure that we can delete a customfield and publish the notification via mqtt."""
        with self.run_requests_as(super_user):
            resp = self.client.delete(
                f"{self.url}/{customfield1_of_public_configuration1_in_group1.id}",
            )
        self.expect(resp.status_code).to_equal(200)
        # And ensure that we trigger the mqtt.
        mqtt.mqtt.publish.assert_called_once()
        call_args = mqtt.mqtt.publish.call_args[0]

        self.expect(call_args[0]).to_equal("sms/delete-configuration-customfield")
        self.expect(json.loads).of(call_args[1]).to_equal(
            {
                "data": {
                    "type": "configuration_customfield",
                    "id": str(customfield1_of_public_configuration1_in_group1.id),
                }
            }
        )
