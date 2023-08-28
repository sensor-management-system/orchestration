# SPDX-FileCopyrightText: 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Test classes for the generic configuration action attachments."""
import datetime
import json
from unittest.mock import patch

import pytz

from project import base_url
from project.api.models import (
    Configuration,
    ConfigurationAttachment,
    Contact,
    GenericConfigurationAction,
    GenericConfigurationActionAttachment,
    User,
)
from project.api.models.base_model import db
from project.extensions.idl.models.user_account import UserAccount
from project.extensions.instances import idl
from project.tests.base import BaseTestCase


class TestGenericConfigurationActionAttachments(BaseTestCase):
    """Test class for the generic configuration action attachments."""

    url = base_url + "/generic-configuration-action-attachments"

    def test_patch_to_non_editable_configuration(self):
        """Ensure we can't update to a configuration we can't edit."""
        configuration1 = Configuration(
            label="configuration1",
            is_public=False,
            is_internal=True,
            cfg_permission_group="1",
        )
        configuration2 = Configuration(
            label="configuration2",
            is_public=False,
            is_internal=True,
            cfg_permission_group="2",
        )
        contact = Contact(
            given_name="first",
            family_name="contact",
            email="first.contact@localhost",
        )
        action1 = GenericConfigurationAction(
            configuration=configuration1,
            contact=contact,
            begin_date=datetime.datetime(2022, 12, 24, 0, 0, 0, tzinfo=pytz.utc),
            action_type_name="Something",
            action_type_uri="something",
        )
        action2 = GenericConfigurationAction(
            configuration=configuration2,
            contact=contact,
            begin_date=datetime.datetime(2022, 12, 24, 0, 0, 0, tzinfo=pytz.utc),
            action_type_name="Something",
            action_type_uri="something",
        )
        attachment1 = ConfigurationAttachment(
            configuration=configuration1,
            url="https://gfz-potsdam.de",
            label="GFZ",
        )
        attachment2 = ConfigurationAttachment(
            configuration=configuration2,
            url="https://gfz-potsdam.de",
            label="GFZ",
        )
        action_attachment = GenericConfigurationActionAttachment(
            action=action1,
            attachment=attachment1,
        )
        user = User(
            subject=contact.email,
            contact=contact,
        )
        db.session.add_all(
            [
                configuration1,
                configuration2,
                contact,
                user,
                action1,
                action2,
                attachment1,
                attachment2,
                action_attachment,
            ]
        )
        db.session.commit()

        payload = {
            "data": {
                "type": "generic_configuration_action_attachment",
                "id": action_attachment.id,
                "attributes": {},
                "relationships": {
                    # We try to switch here to another configuration for
                    # which we have no edit permissions.
                    "action": {
                        "data": {
                            "type": "generic_configuration_action",
                            "id": action2.id,
                        }
                    },
                    "attachment": {
                        "data": {
                            "type": "configuration_attachment",
                            "id": attachment2.id,
                        }
                    },
                },
            }
        }

        with self.run_requests_as(user):
            with patch.object(idl, "get_all_permission_groups_for_a_user") as mock:
                mock.return_value = UserAccount(
                    id="123",
                    username=user.subject,
                    administrated_permission_groups=[],
                    membered_permission_groups=[configuration1.cfg_permission_group],
                )
                with self.client:
                    response = self.client.patch(
                        f"{self.url}/{action_attachment.id}",
                        data=json.dumps(payload),
                        content_type="application/vnd.api+json",
                    )
        self.assertEqual(response.status_code, 403)
