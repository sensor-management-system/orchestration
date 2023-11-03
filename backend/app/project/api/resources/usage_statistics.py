# SPDX-FileCopyrightText: 2022 - 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Resources for the usage statistics."""
from flask import request
from flask_rest_jsonapi import ResourceList

from ..helpers.errors import MethodNotAllowed
from ..models import (
    Configuration,
    ConfigurationAttachment,
    Contact,
    DatastreamLink,
    Device,
    DeviceAttachment,
    Platform,
    PlatformAttachment,
    Site,
    SiteAttachment,
    User,
)
from ..models.base_model import db


class UsageStatistics(ResourceList):
    """Resource class to get usage statistics."""

    def get(self):
        """
        Return a response for the usage statistics.

        Currently those are mainly counts for the models, but
        we can extend those later.
        """
        true_values = ["true"]
        extended = request.args.get("extended") in true_values

        models_to_query = {
            "devices": Device,
            "platforms": Platform,
            "configurations": Configuration,
            "sites": Site,
        }
        counts = {}
        for model_name, model in models_to_query.items():
            count = db.session.query(model).count()
            counts[model_name] = count

        # For users we only want to know the active ones
        counts["users"] = db.session.query(User).filter(User.active).count()

        if extended:
            counts["device_pids"] = (
                db.session.query(Device)
                .filter(Device.persistent_identifier.is_not(None))
                .count()
            )
            counts["platform_pids"] = (
                db.session.query(Platform)
                .filter(Platform.persistent_identifier.is_not(None))
                .count()
            )
            counts["configuration_pids"] = (
                db.session.query(Configuration)
                .filter(Configuration.persistent_identifier.is_not(None))
                .count()
            )
            counts["pids"] = (
                counts["device_pids"]
                + counts["platform_pids"]
                + counts["configuration_pids"]
            )

            counts["organizations"] = (
                db.session.query(User)
                .join(User.contact)
                .filter(User.active)
                .filter(Contact.organization.is_not(None))
                .filter(Contact.organization != "")
                .distinct(Contact.organization)
                .count()
            )
            counts["uploads"] = (
                db.session.query(DeviceAttachment)
                .filter(DeviceAttachment.internal_url.is_not(None))
                .filter(DeviceAttachment.internal_url != "")
                .count()
                + db.session.query(PlatformAttachment)
                .filter(PlatformAttachment.internal_url.is_not(None))
                .filter(PlatformAttachment.internal_url != "")
                .count()
                + db.session.query(ConfigurationAttachment)
                .filter(ConfigurationAttachment.internal_url.is_not(None))
                .filter(ConfigurationAttachment.internal_url != "")
                .count()
                + db.session.query(SiteAttachment)
                .filter(SiteAttachment.internal_url.is_not(None))
                .filter(SiteAttachment.internal_url != "")
                .count()
            )
            counts["orcids"] = (
                db.session.query(Contact)
                .filter(Contact.orcid.is_not(None))
                .filter(Contact.orcid != "")
                .count()
            )
            counts["datastreams"] = db.session.query(DatastreamLink).count()
        return {
            "counts": counts,
        }

    def post(self):
        """Don't allow post requests."""
        raise MethodNotAllowed("endpoint is readonly")
