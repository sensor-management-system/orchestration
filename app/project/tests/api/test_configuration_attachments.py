"""Tests for the configuration attachment endpoints."""

import json

from project import base_url
from project.api.models.base_model import db
from project.api.models.configuration import Configuration
from project.api.models.configuration_attachment import ConfigurationAttachment
from project.tests.base import BaseTestCase, create_token, fake, query_result_to_list


class TestConfigurationAttachmentServices(BaseTestCase):
    """Test configuration attachments."""

    url = base_url + "/configuration-attachments"

    def test_post_configuration_attachment_api(self):
        """Ensure that we can add a configuration attachment."""
        # First we need to make sure that we have a configuration
        configuration = Configuration(
            label="Very new configuration",
            is_public=False,
            is_internal=True,
        )
        db.session.add(configuration)
        db.session.commit()

        # Now as it is saved we can be sure that has an id
        self.assertTrue(configuration.id is not None)

        count_configuration_attachments = (
            db.session.query(ConfigurationAttachment)
            .filter_by(
                configuration_id=configuration.id,
            )
            .count()
        )
        # However, this new configuration for sure has no attachments
        self.assertEqual(count_configuration_attachments, 0)

        # Now we can write the request to add a configuration attachment
        payload = {
            "data": {
                "type": "configuration_attachment",
                "attributes": {
                    "url": "https://www.gfz-potsdam.de",
                    "label": "GFZ Homepage",
                },
                "relationships": {
                    "configuration": {
                        "data": {"type": "configuration", "id": str(configuration.id)}
                    }
                },
            }
        }
        with self.client:
            url_post = base_url + "/configuration-attachments"
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
        configuration_attachments = query_result_to_list(
            db.session.query(ConfigurationAttachment).filter_by(
                configuration_id=configuration.id,
            )
        )
        # We now have one attachment
        self.assertEqual(len(configuration_attachments), 1)

        # And it is as we specified it
        configuration_attachment = configuration_attachments[0]
        self.assertEqual(configuration_attachment.url, "https://www.gfz-potsdam.de")
        self.assertEqual(configuration_attachment.label, "GFZ Homepage")
        self.assertEqual(configuration_attachment.configuration_id, configuration.id)
        self.assertEqual(
            str(configuration_attachment.configuration_id),
            response.get_json()["data"]["id"],
        )
        msg = "create;attachment"
        self.assertEqual(msg, configuration_attachment.configuration.update_description)

    def test_post_configuration_attachment_api_missing_url(self):
        """Ensure that we don't add a configuration attachment with missing url."""
        configuration = Configuration(
            label="Very new configuration",
            is_public=False,
            is_internal=True,
        )
        db.session.add(configuration)
        db.session.commit()

        # Now we can write the request to add a configuration attachment
        payload = {
            "data": {
                "type": "configuration_attachment",
                "attributes": {
                    "url": None,
                    "label": "GFZ Homepage",
                },
                "relationships": {
                    "configuration": {
                        "data": {"type": "configuration", "id": str(configuration.id)}
                    }
                },
            }
        }
        with self.client:
            url_post = base_url + "/configuration-attachments"
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
            db.session.query(ConfigurationAttachment)
            .filter_by(
                configuration_id=configuration.id,
            )
            .count()
        )
        self.assertEqual(count_attachments, 0)

    def test_post_configuration_attachment_api_missing_configuration(self):
        """Ensure that we don't add a configuration attachment with missing configuration."""
        count_configuration_attachments_before = db.session.query(
            ConfigurationAttachment
        ).count()
        payload = {
            "data": {
                "type": "configuration_attachment",
                "attributes": {
                    "url": "GFZ",
                    "label": "GFZ Homepage",
                },
                "relationships": {
                    "configuration": {"data": {"type": "configuration", "id": None}}
                },
            }
        }
        with self.client:
            url_post = base_url + "/configuration-attachments"
            response = self.client.post(
                url_post,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
                headers=create_token(),
            )
        # it will not work, as we miss an important part (the configuration)
        self.assertEqual(response.status_code, 422)
        count_configuration_attachments_after = db.session.query(
            ConfigurationAttachment
        ).count()
        self.assertEqual(
            count_configuration_attachments_before,
            count_configuration_attachments_after,
        )

    def test_get_configuration_attachment_api(self):
        """Ensure that we can get a list of configuration attachments."""
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

        configuration_attachment1 = ConfigurationAttachment(
            label="GFZ",
            url="https://www.gfz-potsdam.de",
            configuration=configuration1,
        )
        configuration_attachment2 = ConfigurationAttachment(
            label="UFZ",
            url="https://www.ufz.de",
            configuration=configuration1,
        )
        configuration_attachment3 = ConfigurationAttachment(
            label="PIK",
            url="https://www.pik-potsdam.de",
            configuration=configuration2,
        )

        db.session.add(configuration_attachment1)
        db.session.add(configuration_attachment2)
        db.session.add(configuration_attachment3)
        db.session.commit()

        all_configuration_attachments = [
            configuration_attachment1,
            configuration_attachment2,
            configuration_attachment3,
        ]

        with self.client:
            response = self.client.get(
                base_url + "/configuration-attachments",
                content_type="application/vnd.api+json",
            )
            self.assertEqual(response.status_code, 200)
            payload = response.get_json()

            self.assertEqual(len(payload["data"]), 3)

            configuration_attachment1_data = None
            for attachment in payload["data"]:
                attachment["id"] in [str(da.id) for da in all_configuration_attachments]
                attachment["attributes"]["url"] in [
                    da.url for da in all_configuration_attachments
                ]
                attachment["attributes"]["label"] in [
                    da.label for da in all_configuration_attachments
                ]

                if attachment["id"] == str(configuration_attachment1.id):
                    configuration_attachment1_data = attachment
                    self.assertEqual(
                        attachment["attributes"]["url"], configuration_attachment1.url
                    )
                    self.assertEqual(
                        attachment["attributes"]["label"],
                        configuration_attachment1.label,
                    )
                    # and we want to check the link for the configuration as well
                    configuration_link = attachment["relationships"]["configuration"][
                        "links"
                    ]["related"]
                    resp_configuration = self.client.get(
                        configuration_link,
                        content_type="application/vnd.api+json",
                    )
                    self.assertEqual(resp_configuration.status_code, 200)
                    self.assertEqual(
                        resp_configuration.get_json()["data"]["id"],
                        str(configuration_attachment1.configuration_id),
                    )
                    self.assertEqual(
                        resp_configuration.get_json()["data"]["attributes"]["label"],
                        configuration_attachment1.configuration.label,
                    )

            self.assertTrue(configuration_attachment1_data is not None)

            # Now we tested the get request for the list response
            # It is time to check the detail one as well
            response = self.client.get(
                base_url
                + "/configuration-attachments/"
                + str(configuration_attachment1.id),
                content_type="application/vnd.api+json",
            )
            self.assertEqual(response.status_code, 200)
            # I already tested the response for this attachment
            self.assertEqual(
                response.get_json()["data"], configuration_attachment1_data
            )

            # And now we want to make sure that we already filter the configuration attachments
            # with a given configuration id
            response = self.client.get(
                base_url
                + "/configurations/"
                + str(configuration1.id)
                + "/configuration-attachments",
                content_type="application/vnd.api+json",
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.get_json()["data"]), 2)
            response = self.client.get(
                base_url
                + "/configurations/"
                + str(configuration2.id)
                + "/configuration-attachments",
                content_type="application/vnd.api+json",
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.get_json()["data"]), 1)

    def test_patch_configuration_attachment_api(self):
        """Ensure that we can update a configuration attachment."""
        configuration1 = Configuration(
            label="Just a configuration",
            is_public=False,
            is_internal=True,
        )
        configuration2 = Configuration(
            label="Another configuration",
            is_public=False,
            is_internal=True,
        )

        db.session.add(configuration1)
        db.session.add(configuration2)
        db.session.commit()

        configuration_attachment1 = ConfigurationAttachment(
            label="GFZ",
            url="https://www.gfz-potsdam.de",
            configuration=configuration1,
        )
        db.session.add(configuration_attachment1)
        db.session.commit()

        payload = {
            "data": {
                "type": "configuration_attachment",
                "id": str(configuration_attachment1.id),
                "attributes": {
                    "label": "UFZ",
                    "url": "https://www.ufz.de",
                },
                "relationships": {
                    "configuration": {
                        "data": {"type": "configuration", "id": str(configuration2.id)}
                    }
                },
            }
        }
        with self.client:
            url_patch = (
                base_url
                + "/configuration-attachments/"
                + str(configuration_attachment1.id)
            )
            response = self.client.patch(
                url_patch,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
                headers=create_token(),
            )

        self.assertEqual(response.status_code, 200)

        configuration_attachment_reloaded = (
            db.session.query(ConfigurationAttachment)
            .filter_by(id=configuration_attachment1.id)
            .one()
        )
        self.assertEqual(configuration_attachment_reloaded.url, "https://www.ufz.de")
        self.assertEqual(configuration_attachment_reloaded.label, "UFZ")
        self.assertEqual(
            configuration_attachment_reloaded.configuration_id, configuration2.id
        )
        msg = "update;attachment"
        self.assertEqual(
            msg, configuration_attachment_reloaded.configuration.update_description
        )

    def test_http_response_not_found(self):
        """Make sure that the backend responds with 404 HTTP-Code if a resource was not found."""
        url = f"{self.url}/{fake.random_int()}"
        _ = super().http_code_404_when_resource_not_found(url)

    def test_post_configuration_attachment_with_no_label(self):
        """Ensure that we can not add a configuration attachment without a label."""
        configuration = Configuration(
            label="anew configuration",
            is_public=True,
            is_internal=False,
        )
        db.session.add(configuration)
        db.session.commit()
        self.assertTrue(configuration.id is not None)

        count_configuration_attachments = (
            db.session.query(ConfigurationAttachment)
            .filter_by(
                configuration_id=configuration.id,
            )
            .count()
        )
        self.assertEqual(count_configuration_attachments, 0)

        payload = {
            "data": {
                "type": "configuration_attachment",
                "attributes": {
                    "url": "https://www.ufz.de",
                    "label": None,
                },
                "relationships": {
                    "configuration": {
                        "data": {"type": "configuration", "id": str(configuration.id)}
                    }
                },
            }
        }
        with self.client:
            url_post = base_url + "/configuration-attachments"
            response = self.client.post(
                url_post,
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
                headers=create_token(),
            )
        self.assertEqual(response.status_code, 422)
