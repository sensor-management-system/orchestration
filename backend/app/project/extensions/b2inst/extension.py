# SPDX-FileCopyrightText: 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Extension to handle pids & pidinst via b2inst."""

import logging

from flask import current_app

from ...api.helpers.errors import BadRequestError
from ...api.models import Configuration, Device, Platform
from ...api.models.base_model import db
from . import client, mappers


class B2Inst:
    """Flask extension to handle pidinst metadata."""

    def __init__(self, app=None):
        """Init the object."""
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Init with the app."""
        app.teardown_appcontext(self.teardown)

    def teardown(self, exception):
        """Cleanup."""
        pass

    @property
    def url(self):
        """Return the base url for the b2inst service."""
        return current_app.config["B2INST_URL"]

    @property
    def token(self):
        """Return the token for the b2inst service."""
        return current_app.config["B2INST_TOKEN"]

    @property
    def community(self):
        """Return the community name that we want to use in the b2inst."""
        return current_app.config["B2INST_COMMUNITY"]

    @property
    def base_landing_page(self):
        """Return the base url for the landing page."""
        return current_app.config["SMS_FRONTEND_URL"]

    @property
    def schema_version(self):
        """Return the schema version that we want to use for pidinst."""
        return "1.0"

    @property
    def b2inst_client(self):
        """Return the b2inst client that we use for running our requests."""
        return client.B2InstClient(base_url=self.url, access_token=self.token)

    def create_pid(self, instrument):
        """Create a pid & store it in the instrument."""
        community_id = self._find_community_id(self.community)

        mapper_lookup = {
            Device: mappers.B2InstDeviceMapper,
            Platform: mappers.B2InstPlatformMapper,
            Configuration: mappers.B2InstConfigurationMapper,
        }
        mapper = mapper_lookup[type(instrument)]()
        try:
            draft_data = mapper.to_draft_post(
                instrument,
                base_landing_page=self.base_landing_page,
                schema_version=self.schema_version,
            )
            draft = self.b2inst_client.create_draft_record(draft_data.dict())
            draft_id = draft["id"]
            instrument.b2inst_record_id = draft_id

            if community_id:
                self.b2inst_client.add_communities(
                    draft_id, community_ids=[community_id]
                )
            record_data = self.b2inst_client.publish_record(draft_id)
            persistent_identifier = record_data["metadata"]["Identifier"][
                "identifierValue"
            ]
            return persistent_identifier
        except Exception as err:
            logging.error("Creation of the b2inst record failed")
            logging.error({"exception": err, "instrument": instrument})
            raise BadRequestError(str(err))

    def update_external_metadata(self, instrument, run_async=True):
        """Update the metadata for the instrument in b2inst."""
        # We need to extract it as the instrument may not be anymore in
        # the db session when we run the task function.
        type_ = type(instrument)
        id_ = instrument.id

        def task():
            # Reload the instrument.
            instrument = db.session.query(type_).filter_by(id=id_).first()

            record_id = instrument.b2inst_record_id
            mapper_lookup = {
                Device: mappers.B2InstDeviceMapper,
                Platform: mappers.B2InstPlatformMapper,
                Configuration: mappers.B2InstConfigurationMapper,
            }
            mapper = mapper_lookup[type(instrument)]()
            draft_data = mapper.to_draft_post(
                instrument,
                base_landing_page=self.base_landing_page,
                schema_version=self.schema_version,
            )
            try:
                self.b2inst_client.create_new_draft(record_id)
                self.b2inst_client.update_draft(record_id, draft_data.dict())
                self.b2inst_client.publish_record(record_id)
            except Exception as err:
                logging.error("Update of the b2inst record failed")
                logging.error(
                    {"exception": err, "record_id": record_id, "data": draft_data}
                )
                # If we run it in async mode, then raising the exception
                # will not affect the request.
                # However, we will see it in the logs of the system, so
                # it still makes sense to call that.
                raise err

        if run_async:
            from ... import executor

            executor.submit(task)
        else:
            task()

    def _find_community_id(self, community_name):
        """Find the commonity id for a given community name."""
        response = self.b2inst_client.get_communities()
        hits = response["hits"]["hits"]
        for c in hits:
            if c["metadata"]["title"] == community_name:
                return c["id"]
        return None

    def check_availability(self):
        """Raise an exception if the service is not avaiable."""
        self.b2inst_client.ping()

    def has_external_metadata(self, instrument):
        """Return true if the instrument has external metadata that may need updates."""
        return getattr(instrument, "b2inst_record_id", None) is not None

    def get_record_frontend_url(self, record_id):
        """Return the frontend record url (to show it to the user)."""
        return self.b2inst_client.get_record_frontend_url(record_id)
