# SPDX-FileCopyrightText: 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Extension to handle pids & pidinst via b2inst."""

import json
import logging

import requests
from flask import current_app

from ...api.helpers.errors import BadRequestError
from ...api.models import Configuration, Device, Platform
from ...api.models.base_model import db
from . import mappers, schemas


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
                community=community_id,
                # Open access just specifies if associated files are
                # visible for the public or not.
                # We don't store files in b2inst, so we don't care.
                # (And the metadata that we send are always public).
                open_access=True,
                base_landing_page=self.base_landing_page,
                schema_version=self.schema_version,
            )
            draft = self._create_draft(draft_data)
            draft_id = draft["id"]
            instrument.b2inst_record_id = draft_id

            self._publish_draft(draft_id)

            record_data = self._get_record_data(draft_id)
            persistent_identifier_with_prefix = record_data["metadata"]["ePIC_PID"]
            persistent_identifier = persistent_identifier_with_prefix.replace(
                "http://hdl.handle.net/", ""
            )
            return persistent_identifier
        except requests.HTTPError as e:
            try:
                raise BadRequestError(e.response.json()["message"])
            except (requests.JSONDecodeError, KeyError):
                raise e

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
            community_id = self._find_community_id(self.community)

            mapper_lookup = {
                Device: mappers.B2InstDeviceMapper,
                Platform: mappers.B2InstPlatformMapper,
                Configuration: mappers.B2InstConfigurationMapper,
            }
            mapper = mapper_lookup[type(instrument)]()
            draft_data = mapper.to_draft_post(
                instrument,
                community=community_id,
                open_access=True,
                base_landing_page=self.base_landing_page,
                schema_version=self.schema_version,
            )
            response_existing_entry = requests.get(
                f"{self.url}/api/records/{record_id}?access_token={self.token}"
            )
            response_existing_entry.raise_for_status()
            existing_entry = response_existing_entry.json()["metadata"]
            patch = mappers.B2InstDraftMapper().to_json_patch(
                draft_data, existing_entry
            )

            url = f"{self.url}/api/records/{record_id}?access_token={self.token}"
            response = requests.patch(
                url,
                data=json.dumps(patch),
                headers={"Content-Type": "application/json-patch+json"},
            )
            if not response.ok:
                logging.error("Update of the b2inst record failed")
                logging.error({"response": response.text, "url": url, "payload": patch})
            # If we run it in async mode, then raising the exception
            # will not affect the request.
            # However, we will see it in the logs of the system, so
            # it still makes sense to call that.
            response.raise_for_status()

        if run_async:
            from ... import executor

            executor.submit(task)
        else:
            task()

    def _get_communities(self):
        """Return the list of communities."""
        url = f"{self.url}/api/communities"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()["hits"]["hits"]

    def _find_community_id(self, community_name):
        """Find the commonity id for a given community name."""
        for c in self._get_communities():
            if c["name"] == community_name:
                return c["id"]
        return None

    def _create_draft(self, draft: schemas.B2InstDraftPost):
        """Create a draft record."""
        url = f"{self.url}/api/records/?access_token={self.token}"
        payload = draft.dict()
        response = requests.post(url, json=payload)
        if not response.ok:
            logging.error("Creation of the b2inst draft failed")
            logging.error({"response": response.text, "url": url, "payload": payload})
        response.raise_for_status()
        return response.json()

    def _publish_draft(self, draft_id):
        """Publish the draft."""
        payload = [
            {
                "op": "add",
                "path": "/publication_state",
                "value": "submitted",
            }
        ]
        url = f"{self.url}/api/records/{draft_id}/draft?access_token={self.token}"

        response = requests.patch(
            url,
            data=json.dumps(payload),
            headers={"Content-Type": "application/json-patch+json"},
        )
        if not response.ok:
            logging.error("Publishing the b2inst draft failed")
            logging.error({"response": response.text, "url": url, "payload": payload})
        response.raise_for_status()

    def _get_record_data(self, record_id):
        """Return the data for the record in the b2inst."""
        url = f"{self.url}/api/records/{record_id}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def check_availability(self):
        """Raise an exception if the service is not avaiable."""
        url = f"{self.url}/api"
        response = requests.get(url)
        response.raise_for_status()

    def has_external_metadata(self, instrument):
        """Return true if the instrument has external metadata that may need updates."""
        return getattr(instrument, "b2inst_record_id", None) is not None

    def get_record_frontend_url(self, record_id):
        """Return the frontend record url (to show it to the user)."""
        return f"{self.url}/records/{record_id}"
