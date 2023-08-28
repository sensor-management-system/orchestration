# SPDX-FileCopyrightText: 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Test class for the uploads."""

import io
from functools import wraps
from unittest.mock import patch

from flask import current_app

from project import base_url
from project.api.models import Contact, User
from project.api.models.base_model import db
from project.tests.base import BaseTestCase
from project.views.upload_files import minio


def overwrite_config(**config_kwargs):
    """Wrap a function to allow us to overwrite config values for the scope of the function."""

    def inner(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            old_config = dict(current_app.config)
            current_app.config.update(config_kwargs)
            try:
                return f(*args, **kwargs)
            finally:
                current_app.config.update(old_config)

        return wrapper

    return inner


class TestUpload(BaseTestCase):
    """Test class for the upload view."""

    upload_url = base_url + "/upload"

    def test_upload_no_user(self):
        """Ensure we can't upload without user."""
        resp = self.client.post(self.upload_url, data={})
        self.assertEqual(resp.status_code, 401)

    def test_no_files(self):
        """Ensure we return a 400 response if we don't have a file."""
        contact = Contact(
            given_name="first", family_name="contact", email="first.contact@localhost"
        )
        user = User(contact=contact, subject=contact.email)
        db.session.add_all([contact, user])
        db.session.commit()

        with self.run_requests_as(user):
            resp = self.client.post(self.upload_url, data={})
        self.assertEqual(resp.status_code, 400)

    @overwrite_config(ALLOWED_MIME_TYPES=["text/plain"])
    def test_not_allowed_mimetype(self):
        """Ensure we reject not allowed mimetypes."""
        contact = Contact(
            given_name="first", family_name="contact", email="first.contact@localhost"
        )
        user = User(contact=contact, subject=contact.email)
        db.session.add_all([contact, user])
        db.session.commit()

        data = {
            # Here it is an octet-stream, which we don't support.
            "file": (io.BytesIO(b"begin print(a) end"), "some text.qbasic"),
        }
        with self.run_requests_as(user):
            resp = self.client.post(
                self.upload_url, data=data, content_type="multipart/form-data"
            )
        self.assertEqual(resp.status_code, 415)

    @overwrite_config(ALLOWED_MIME_TYPES=["text/csv"])
    def test_allowed_mimetype(self):
        """Ensure we can ask minio to upload supported files."""
        contact = Contact(
            given_name="first", family_name="contact", email="first.contact@localhost"
        )
        user = User(contact=contact, subject=contact.email)
        db.session.add_all([contact, user])
        db.session.commit()

        data = {
            "file": (io.BytesIO(b"field1,field2,field3"), "data.csv"),
        }
        with self.run_requests_as(user):
            with patch.object(minio, "upload_object") as upload_object:
                upload_object.return_value = "Ok"
                resp = self.client.post(
                    self.upload_url, data=data, content_type="multipart/form-data"
                )
                upload_object.assert_called_once()
        self.assertEqual(resp.status_code, 201)

    @overwrite_config(ALLOWED_MIME_TYPES=["text/csv"])
    def test_allowed_mimetype_with_additional_encoding(self):
        """Ensure we support files also if we have additional encoding values in the mimetype."""
        contact = Contact(
            given_name="first", family_name="contact", email="first.contact@localhost"
        )
        user = User(contact=contact, subject=contact.email)
        db.session.add_all([contact, user])
        db.session.commit()

        data = {
            "file": (
                io.BytesIO(b"field1,field2,field3"),
                "data.csv",
                "text/csv; charset=utf-8",
            ),
        }
        with self.run_requests_as(user):
            with patch.object(minio, "upload_object") as upload_object:
                upload_object.return_value = "Ok"
                resp = self.client.post(
                    self.upload_url, data=data, content_type="multipart/form-data"
                )
                upload_object.assert_called_once()
        self.assertEqual(resp.status_code, 201)
