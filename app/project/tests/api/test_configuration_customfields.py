"""Tests for the configuration custom field endpoints."""

import json

from project import base_url
from project.api.models.base_model import db
from project.api.models.configuration import Configuration
from project.api.models.configuration_customfield import \
    ConfigurationCustomField
from project.tests.base import (BaseTestCase, create_token, fake,
                                query_result_to_list)


class TestConfigurationCustomFieldServices(BaseTestCase):
    """Test configuration customfields."""

    url = base_url + "/configuration_customfields"

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
