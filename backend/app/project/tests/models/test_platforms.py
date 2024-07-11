# SPDX-FileCopyrightText: 2021 - 2023
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Tests for the platform model."""

from project.api.models.base_model import db
from project.api.models.platform import Platform
from project.api.schemas.platform_schema import PlatformSchema
from project.tests.base import BaseTestCase


class TestPlatformModel(BaseTestCase):
    """Test class for the platform model."""

    def test_add_platform_model(self):
        """Ensure we can add a platform model to the database."""
        platform = Platform(
            id=13,
            short_name="short_name test",
            description="description test",
            long_name="long_name test",
            manufacturer_name="manufacturer_name test",
            manufacturer_uri="http://cv.de/manufacturer_uri",
            model="model test",
            platform_type_uri="http://cv.de/platform_type_uri",
            platform_type_name="platform_type_name test",
            status_uri="http://cv.de/status_uri test",
            status_name="status_name test",
            website="http://website.de/platform",
            inventory_number="inventory_number test",
            serial_number="serial_number test",
            persistent_identifier="persistent_identifier_test",
            is_public=False,
            is_private=False,
            is_internal=True,
        )
        PlatformSchema().dump(platform)
        db.session.add(platform)
        db.session.commit()

        p = db.session.query(Platform).filter_by(id=platform.id).one()
        self.assertIn(p.persistent_identifier, "persistent_identifier_test")

    def test_text_search_fields(self):
        """Ensure the most important fields are in the fields for full text search."""
        text_fields = Platform.text_search_fields()
        self.assertTrue("short_name" in text_fields)
        self.assertFalse("created_by_id" in text_fields)
