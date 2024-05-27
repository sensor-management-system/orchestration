# SPDX-FileCopyrightText: 2022
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Precondition classes for sites."""

from ...api.helpers.errors import ConflictError
from ...api.models import Configuration
from ...api.models.base_model import db
from .base import Precondition


class AllConfigurationsForSiteAreAlreadyArchived(Precondition):
    """
    Checks the configurations of a site.

    This checks if all linked configurations are already archived.
    """

    def __init__(self):
        """Init the object."""

        def object_rule(object):
            """Return a conflict error if there is a configuration is not archved."""
            configurations = db.session.query(Configuration).filter_by(
                site_id=object.id
            )
            for configuration in configurations:
                if not configuration.archived:
                    return ConflictError(
                        f"Configuration {configuration.id} is not archvived."
                    )

        super().__init__(object_rule)
