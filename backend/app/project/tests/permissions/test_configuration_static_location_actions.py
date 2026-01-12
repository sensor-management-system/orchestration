# SPDX-FileCopyrightText: 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Test classes for the static locations."""
import datetime
import json

from project import base_url
from project.api.models import (
    Configuration,
    ConfigurationStaticLocationBeginAction,
    Contact,
    PermissionGroup,
    PermissionGroupMembership,
    User,
)
from project.api.models.base_model import db
from project.tests.base import BaseTestCase


class TestConfigurationStaticLocation(BaseTestCase):
    """Test class for the static locations."""

    url = base_url + "/static-location-actions"

    def setUp(self):
        """Set stuff up for the tests."""
        super().setUp()
        normal_contact = Contact(
            given_name="normal", family_name="user", email="normal.user@localhost"
        )
        self.normal_user = User(subject=normal_contact.email, contact=normal_contact)
        self.permission_group = PermissionGroup(name="test", entitlement="test")
        self.other_group = PermissionGroup(name="other", entitlement="other")
        self.membership = PermissionGroupMembership(
            permission_group=self.permission_group, user=self.normal_user
        )
        db.session.add_all(
            [
                normal_contact,
                self.normal_user,
                self.permission_group,
                self.other_group,
                self.membership,
            ]
        )
        db.session.commit()

    def test_patch_to_non_editable_configuration(self):
        """Ensure we can't update to a configuration we can't edit."""
        configuration1 = Configuration(
            label="config1",
            is_public=False,
            is_internal=True,
        )
        configuration2 = Configuration(
            label="config2",
            is_public=False,
            is_internal=True,
            cfg_permission_group=str(self.other_group.id),
        )
        contact = Contact(
            given_name="first",
            family_name="contact",
            email="first.contact@localhost",
        )
        location = ConfigurationStaticLocationBeginAction(
            configuration=configuration1,
            begin_date=datetime.datetime(
                2022, 12, 1, 0, 0, 0, tzinfo=datetime.timezone.utc
            ),
            begin_contact=contact,
        )
        db.session.add_all([configuration1, configuration2, contact, location])
        db.session.commit()

        payload = {
            "data": {
                "type": "configuration_static_location_action",
                "id": location.id,
                "attributes": {},
                "relationships": {
                    # We try to switch here to another configuration for
                    # which we have no edit permissions.
                    "configuration": {
                        "data": {
                            "type": "configuration",
                            "id": configuration2.id,
                        }
                    },
                },
            }
        }

        with self.run_requests_as(self.normal_user):
            response = self.client.patch(
                f"{self.url}/{location.id}",
                data=json.dumps(payload),
                content_type="application/vnd.api+json",
            )
        self.assertEqual(response.status_code, 403)
