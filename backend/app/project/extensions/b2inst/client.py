# SPDX-FileCopyrightText: 2026
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Api client for the b2inst."""

import json
import typing
import urllib.request


class B2InstClient:
    """Client class to work with the b2inst."""

    def __init__(self, base_url, access_token):
        """Init the client with an access token."""
        self.base_url = base_url
        self.access_token = access_token

    def create_draft_record(self, data: dict):
        """Create a new draft record from the data.

        The data must look like this:

        {
            "metadata": {
                "Name": "Some device",
                "Manufacturer": [{"manufacturerName": "Coorp"}],
                "Owner": [{"ownerName": "GFZ"}],
                // more PIDINST fields
            },
            "access": {
                "record": "public",
                "files": "public"
            },
            "files": {
                "enabled": false
            }
        }
        """
        url = f"{self.base_url}/api/records?access_token={self.access_token}"
        request = urllib.request.Request(
            url,
            method="POST",
            data=json.dumps(data).encode(),
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(request) as resp:
            result = json.load(resp)
        return result

    def publish_record(self, record_id: str):
        """Publish the record.

        This will give the record a persistent identifier.
        """
        url = f"{self.base_url}/api/records/{record_id}/draft/actions/publish?access_token={self.access_token}"
        request = urllib.request.Request(
            url,
            method="POST",
        )
        with urllib.request.urlopen(request) as resp:
            result = json.load(resp)
        return result

    def create_new_draft(self, record_id: str):
        """Create a new draft for an existing record.

        Only the new draft can be modified.

        The workflow of creating new drafts for existing records
        will ensure that there is only one persistent identifier
        for the instrument, so the pid identifies the instrument
        itself (not the set of metadata that might change).
        """
        url = f"{self.base_url}/api/records/{record_id}/draft?access_token={self.access_token}"
        request = urllib.request.Request(
            url,
            method="POST",
        )
        with urllib.request.urlopen(request) as resp:
            result = json.load(resp)
        return result

    def create_new_version(self, record_id: str):
        """Create a new version for an existing record.

        This is another option to indicate changed metadata.
        This new version will have its own record id and a new
        persistent identifier.

        Both versions will be linked in the b2inst.

        Please note: This new version will identify the metadata
        set of the instrument. The identified instrument will have
        multiple metadata sets.
        """
        url = f"{self.base_url}/api/records/{record_id}/versions?access_token={self.access_token}"
        request = urllib.request.Request(
            url,
            method="POST",
        )
        with urllib.request.urlopen(request) as resp:
            result = json.load(resp)
        return result

    def update_draft(self, record_id: str, data: dict):
        """Change the metadata set for the draft.

        The data needs to have the same structure as
        for the creation of the create_record method.
        """
        url = f"{self.base_url}/api/records/{record_id}/draft?access_token={self.access_token}"
        request = urllib.request.Request(
            url,
            method="PUT",
            data=json.dumps(data).encode(),
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(request) as resp:
            result = json.load(resp)
        return result

    def add_communities(self, record_id: str, community_ids: typing.List[str]):
        """Add a community to a draft."""
        # You think the records/records look strange? I guess you are right.
        # The b2inst developer was informed about it.
        # Lets see if it changes.
        url = f"{self.base_url}/api/records/{record_id}/communities?access_token={self.access_token}"
        communities = [{"id": cid} for cid in community_ids]
        payload = {
            "communities": communities,
        }
        request = urllib.request.Request(
            url,
            method="POST",
            data=json.dumps(payload).encode(),
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(request) as resp:
            result = json.load(resp)
        return result

    def get_communities(self):
        """Return the list of communities."""
        url = f"{self.base_url}/api/communities"
        request = urllib.request.Request(
            url,
        )
        with urllib.request.urlopen(request) as resp:
            result = json.load(resp)
        return result

    def get_record_frontend_url(self, record_id: str):
        """Return the frontend url for a given record."""
        return f"{self.base_url}/records/{record_id}"

    def ping(self):
        """Check if the b2int is accessible."""
        url = f"{self.base_url}/api/ping"
        request = urllib.request.Request(
            url,
        )
        with urllib.request.urlopen(request) as resp:
            result = resp.read()
        return result
