# SPDX-FileCopyrightText: 2022
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Tests for the download endpoints for uploaded attachments."""

from unittest.mock import patch

from project import base_url
from project.api.models import (
    Configuration,
    ConfigurationAttachment,
    Contact,
    Device,
    DeviceAttachment,
    Platform,
    PlatformAttachment,
    User,
)
from project.api.models.base_model import db
from project.tests.base import BaseTestCase, fake
from project.views import download_files


class TestDeviceAttachmentDownloads(BaseTestCase):
    """Test case to download device attachment contents."""

    url = base_url + "/device-attachments"

    def test_get_not_found(self):
        """Ensure that we return 404 for non existing attachments."""
        url = f"{self.url}/123456789/file/somefile.txt"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_get_internal_no_user(self):
        """Ensure that we require a user for internal devices."""
        device = Device(
            short_name="a new device",
            manufacturer_name=fake.pystr(),
            is_public=False,
            is_private=False,
            is_internal=True,
        )
        attachment = DeviceAttachment(
            device=device, label="gfz", url="https://www.gfz-potsdam.de"
        )
        db.session.add_all([device, attachment])
        db.session.commit()

        url = f"{self.url}/{attachment.id}/file/somefile.txt"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_get_redirect_for_normal_attachment(self):
        """Ensure that we can redirect for attachments that don't have an internal url."""
        device = Device(
            short_name="a new device",
            manufacturer_name=fake.pystr(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        attachment = DeviceAttachment(
            device=device, label="gfz", url="https://www.gfz-potsdam.de"
        )
        db.session.add_all([device, attachment])
        db.session.commit()

        url = f"{self.url}/{attachment.id}/file/somefile.txt"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_get_content_public_no_user(self):
        """Get the content for a public device."""
        device = Device(
            short_name="a new device",
            manufacturer_name=fake.pystr(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        attachment = DeviceAttachment(
            device=device,
            label="gfz",
            # url will not be used.
            url="http://localhost/.../file.txt",
            internal_url="http://minio:8080/.../file.txt",
        )
        db.session.add_all([device, attachment])
        db.session.commit()

        url = f"{self.url}/{attachment.id}/file/somefile.txt"
        with patch.object(download_files, "build_response") as build_response_mock:
            with patch.object(
                download_files, "get_content_type"
            ) as get_content_type_mock:
                build_response_mock.return_value = "some text"
                get_content_type_mock.return_value = "plain/text"

                response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "plain/text")
        self.assertEqual(response.text, "some text")

    def test_get_content_internal_with_user(self):
        """Get the content for an internal device with a given user."""
        contact = Contact(
            given_name="Max", family_name="Powers", email="max.powers@nuclear.capital"
        )
        user = User(contact=contact, subject=contact.email)
        device = Device(
            short_name="a new device",
            manufacturer_name=fake.pystr(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        attachment = DeviceAttachment(
            device=device,
            label="gfz",
            # url will not be used.
            url="http://localhost/.../file.txt",
            internal_url="http://minio:8080/.../file.txt",
        )
        db.session.add_all([device, attachment, contact, user])
        db.session.commit()

        url = f"{self.url}/{attachment.id}/file/somefile.txt"
        with patch.object(download_files, "build_response") as build_response_mock:
            with patch.object(
                download_files, "get_content_type"
            ) as get_content_type_mock:
                build_response_mock.return_value = "some text"
                get_content_type_mock.return_value = "plain/text"

                with self.run_requests_as(user):
                    response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "plain/text")
        self.assertEqual(response.text, "some text")


class TestPlatformAttachmentDownloads(BaseTestCase):
    """Test case to download platform attachment contents."""

    url = base_url + "/platform-attachments"

    def test_get_not_found(self):
        """Ensure that we return 404 for non existing attachments."""
        url = f"{self.url}/123456789/file/somefile.txt"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_get_internal_no_user(self):
        """Ensure that we require a user for internal platform."""
        platform = Platform(
            short_name="a new platform",
            manufacturer_name=fake.pystr(),
            is_public=False,
            is_private=False,
            is_internal=True,
        )
        attachment = PlatformAttachment(
            platform=platform, label="gfz", url="https://www.gfz-potsdam.de"
        )
        db.session.add_all([platform, attachment])
        db.session.commit()

        url = f"{self.url}/{attachment.id}/file/somefile.txt"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_get_redirect_for_normal_attachment(self):
        """Ensure that we can redirect for attachments that don't have an internal url."""
        platform = Platform(
            short_name="a new platform",
            manufacturer_name=fake.pystr(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        attachment = PlatformAttachment(
            platform=platform, label="gfz", url="https://www.gfz-potsdam.de"
        )
        db.session.add_all([platform, attachment])
        db.session.commit()

        url = f"{self.url}/{attachment.id}/file/somefile.txt"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_get_content_public_no_user(self):
        """Get the content for a public platform."""
        platform = Platform(
            short_name="a new platform",
            manufacturer_name=fake.pystr(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        attachment = PlatformAttachment(
            platform=platform,
            label="gfz",
            # url will not be used.
            url="http://localhost/.../file.txt",
            internal_url="http://minio:8080/.../file.txt",
        )
        db.session.add_all([platform, attachment])
        db.session.commit()

        url = f"{self.url}/{attachment.id}/file/somefile.txt"
        with patch.object(download_files, "build_response") as build_response_mock:
            with patch.object(
                download_files, "get_content_type"
            ) as get_content_type_mock:
                build_response_mock.return_value = "some text"
                get_content_type_mock.return_value = "plain/text"

                response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "plain/text")
        self.assertEqual(response.text, "some text")

    def test_get_content_internal_with_user(self):
        """Get the content for an internal platform with a given user."""
        contact = Contact(
            given_name="Max", family_name="Powers", email="max.powers@nuclear.capital"
        )
        user = User(contact=contact, subject=contact.email)
        platform = Platform(
            short_name="a new platform",
            manufacturer_name=fake.pystr(),
            is_public=True,
            is_private=False,
            is_internal=False,
        )
        attachment = PlatformAttachment(
            platform=platform,
            label="gfz",
            # url will not be used.
            url="http://localhost/.../file.txt",
            internal_url="http://minio:8080/.../file.txt",
        )
        db.session.add_all([platform, attachment, contact, user])
        db.session.commit()

        url = f"{self.url}/{attachment.id}/file/somefile.txt"
        with patch.object(download_files, "build_response") as build_response_mock:
            with patch.object(
                download_files, "get_content_type"
            ) as get_content_type_mock:
                build_response_mock.return_value = "some text"
                get_content_type_mock.return_value = "plain/text"

                with self.run_requests_as(user):
                    response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "plain/text")
        self.assertEqual(response.text, "some text")


class TestConfigurationAttachmentDownloads(BaseTestCase):
    """Test case to download configuration attachment contents."""

    url = base_url + "/configuration-attachments"

    def test_get_not_found(self):
        """Ensure that we return 404 for non existing attachments."""
        url = f"{self.url}/123456789/file/somefile.txt"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_get_internal_no_user(self):
        """Ensure that we require a user for internal configuration."""
        configuration = Configuration(
            label="a new configuration",
            is_public=False,
            is_internal=True,
        )
        attachment = ConfigurationAttachment(
            configuration=configuration, label="gfz", url="https://www.gfz-potsdam.de"
        )
        db.session.add_all([configuration, attachment])
        db.session.commit()

        url = f"{self.url}/{attachment.id}/file/somefile.txt"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_get_redirect_for_normal_attachment(self):
        """Ensure that we can redirect for attachments that don't have an internal url."""
        configuration = Configuration(
            label="a new configuration",
            is_public=True,
            is_internal=False,
        )
        attachment = ConfigurationAttachment(
            configuration=configuration, label="gfz", url="https://www.gfz-potsdam.de"
        )
        db.session.add_all([configuration, attachment])
        db.session.commit()

        url = f"{self.url}/{attachment.id}/file/somefile.txt"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_get_content_public_no_user(self):
        """Get the content for a public configuration."""
        configuration = Configuration(
            label="a new configuration",
            is_public=True,
            is_internal=False,
        )
        attachment = ConfigurationAttachment(
            configuration=configuration,
            label="gfz",
            # url will not be used.
            url="http://localhost/.../file.txt",
            internal_url="http://minio:8080/.../file.txt",
        )
        db.session.add_all([configuration, attachment])
        db.session.commit()

        url = f"{self.url}/{attachment.id}/file/somefile.txt"
        with patch.object(download_files, "build_response") as build_response_mock:
            with patch.object(
                download_files, "get_content_type"
            ) as get_content_type_mock:
                build_response_mock.return_value = "some text"
                get_content_type_mock.return_value = "plain/text"

                response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "plain/text")
        self.assertEqual(response.text, "some text")

    def test_get_content_internal_with_user(self):
        """Get the content for an internal configuration with a given user."""
        contact = Contact(
            given_name="Max", family_name="Powers", email="max.powers@nuclear.capital"
        )
        user = User(contact=contact, subject=contact.email)
        configuration = Configuration(
            label="a new configuration",
            is_public=True,
            is_internal=False,
        )
        attachment = ConfigurationAttachment(
            configuration=configuration,
            label="gfz",
            # url will not be used.
            url="http://localhost/.../file.txt",
            internal_url="http://minio:8080/.../file.txt",
        )
        db.session.add_all([configuration, attachment, contact, user])
        db.session.commit()

        url = f"{self.url}/{attachment.id}/file/somefile.txt"
        with patch.object(download_files, "build_response") as build_response_mock:
            with patch.object(
                download_files, "get_content_type"
            ) as get_content_type_mock:
                build_response_mock.return_value = "some text"
                get_content_type_mock.return_value = "plain/text"

                with self.run_requests_as(user):
                    response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "plain/text")
        self.assertEqual(response.text, "some text")
