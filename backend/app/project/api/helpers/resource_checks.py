# SPDX-FileCopyrightText: 2022
# - Luca Johannes Nendel <luca-johannes.nendel@ufz.de>
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Some validator classes for several resources."""

from sqlalchemy import or_

from ... import db
from ..models import ConfigurationDynamicLocationBeginAction
from .errors import ConflictError


class DevicePropertyValidator:
    """Validator for device properties."""

    def validate_property_dynamic_location_action_deletion(self, existing_property_id):
        """
        Validate that we can delete the device property.

        Raises a ConflictError if it is not possible.

        Current checks:
        - checks if the device property isn't referenced inside a dynamic_location_action
        """
        dynamic_location_property_usages = self._get_dynamic_location_property_usage(
            existing_property_id
        )
        for _usage in dynamic_location_property_usages:
            raise ConflictError(self._build_error_message_orphan())

    def _get_dynamic_location_property_usage(self, existing_property_id):
        """Return the query to find the dynamic locations that refer to the property."""
        dynamic_location_actions = db.session.query(
            ConfigurationDynamicLocationBeginAction
        ).filter(
            or_(
                ConfigurationDynamicLocationBeginAction.x_property_id
                == existing_property_id,
                ConfigurationDynamicLocationBeginAction.y_property_id
                == existing_property_id,
                ConfigurationDynamicLocationBeginAction.z_property_id
                == existing_property_id,
            )
        )

        return dynamic_location_actions

    def _build_error_message_orphan(self):
        """Build the error message if the device property can't be deleted."""
        return (
            "There is still a dynamic location action that uses this measured variable."
        )
