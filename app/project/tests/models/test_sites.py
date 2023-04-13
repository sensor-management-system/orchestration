# SPDX-FileCopyrightText: 2022
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Test classes for the sites."""

from project.api.helpers.errors import ConflictError
from project.api.models import Site
from project.api.models.base_model import db
from project.tests.base import BaseTestCase


class TestPostGIS(BaseTestCase):
    """Test case for postgis."""

    def test_postgis_is_installed(self):
        """Ensure that we installed postgis."""
        # If the query succeeds, we have a version of postgis installed.
        # If it raises an exception, we don't have it properly setup.
        query = "select postgis_version()"
        with db.session.connection() as con:
            resp = con.execute(query)
            res = resp.fetchall()
        self.assertTrue(len(res) > 0)


class TestSites(BaseTestCase):
    """Test case for the model itself."""

    def test_dont_allow_internal_and_public_both_false(self):
        """Ensure that we raise exceptions if both are false."""
        site = Site(is_internal=False, is_public=False)
        db.session.add(site)

        with self.assertRaises(ConflictError):
            db.session.commit()

    def test_dont_allow_internal_and_public_both_true(self):
        """Ensure that we raise exceptions if both are true."""
        site = Site(is_internal=True, is_public=True)
        db.session.add(site)

        with self.assertRaises(ConflictError):
            db.session.commit()

    def test_allow_internal(self):
        """Ensure we can save it if it is just internal."""
        site = Site(is_internal=True, is_public=False)
        db.session.add(site)
        db.session.commit()

    def test_allow_public(self):
        """Ensure we can save it if it is just internal."""
        site = Site(is_internal=False, is_public=True)
        db.session.add(site)
        db.session.commit()

    def test_allow_public_to_internal(self):
        """Ensure we can switch to internal."""
        site = Site(is_internal=False, is_public=True)
        db.session.add(site)
        db.session.commit()

        site.is_internal = True
        site.is_public = False
        db.session.add(site)
        db.session.commit()

    def test_allow_internal_to_public(self):
        """Ensure we can switch to internal."""
        site = Site(is_internal=True, is_public=False)
        db.session.add(site)
        db.session.commit()

        site.is_internal = False
        site.is_public = True
        db.session.add(site)
        db.session.commit()
