#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2024 - 2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Publish the SMS on zenodo."""

import json
import os
import pathlib
import sys

import requests


class Env:
    """Helper class to access the enviroment variables."""

    def str(self, key, default=None):
        """Return the env variable as  a string."""
        return os.getenv(key, default)

    def int(self, key, default=None):
        """Return the env variable as an integer."""
        if key in os.environ.keys():
            return int(os.environ[key])
        return default

    def bool(self, key, default=None):
        """Return the env variable as a boolean."""
        if key in os.environ.keys():
            value = os.environ[key]
            if value.lower() in ["true", "yes"]:
                return True
            if value.lower() in ["false", "no"]:
                return False
        return default


class ZenodoApi:
    """Helper class to work with the zenodo rest api."""

    def __init__(self, base_url, access_token):
        """Init the object with the base url and the access token."""
        self.base_url = base_url
        self.access_token = access_token

    def get_depositions(self):
        """Return the list of depositions that we can see with our token."""
        url = f"{self.base_url}/api/deposit/depositions"
        response = requests.get(url, params={"access_token": self.access_token})
        response.raise_for_status()
        return response.json()

    def create_deposition(self):
        """Create a new deposition."""
        url = f"{self.base_url}/api/deposit/depositions"
        response = requests.post(
            url, params={"access_token": self.access_token}, json={}
        )
        response.raise_for_status()
        return response.json()

    def get_optional_deposition(self, id_):
        """Return the deposition for the id or None if we can't find it."""
        url = f"{self.base_url}/api/deposit/depositions/{id_}"
        response = requests.get(url, params={"access_token": self.access_token})
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json()

    def upload_file(self, file, bucket_url):
        """Upload a file to the bucket."""
        path = pathlib.Path(file)
        filename = path.name

        with path.open("rb") as fp:
            response = requests.put(
                f"{bucket_url}/{filename}",
                data=fp,
                params={"access_token": self.access_token},
            )
            response.raise_for_status()
            return response.json()

    def update_metadata(self, id_, metadata):
        """Update the metadata for the deposition."""
        url = f"{self.base_url}/api/deposit/depositions/{id_}"
        data = {"metadata": metadata}
        response = requests.put(
            url, params={"access_token": self.access_token}, json=data
        )
        response.raise_for_status()
        return response.json()

    def publish_deposition(self, id_):
        """Publish the deposition."""
        url = f"{self.base_url}/api/deposit/depositions/{id_}/actions/publish"
        response = requests.post(url, params={"access_token": self.access_token})
        response.raise_for_status()
        return response.json()


class Handle:
    """Class to talk with a handle server."""

    def __init__(self, base_url, prefix, username, password):
        """Init the instance."""
        # base_url looks like this "https://rz-vm561.gfz-potsdam.de:8000/api/handles"
        self.base_url = base_url
        # prefix looks like this "20.500.14372"
        self.prefix = prefix
        self.username = username
        self.password = password

    def put(self, url, handle):
        """Set the handle entry to point to the url."""
        payload = {
            "handle": f"{self.prefix}/{handle}",
            "values": [
                {
                    "index": 1,
                    "type": "URL",
                    "data": {
                        "format": "string",
                        "value": url,
                    },
                },
                {
                    "index": 100,
                    "type": "HS_ADMIN",
                    "data": {
                        "format": "admin",
                        "value": {
                            "handle": f"0.NA./{self.prefix}",
                            "index": 200,
                            "permissions": "011111110011",
                        },
                    },
                },
            ],
        }
        url = f"{self.base_url}/{self.prefix}/{handle}"
        resp = requests.put(
            url,
            json=payload,
            auth=requests.auth.HTTPBasicAuth(self.username, self.password),
        )
        resp.raise_for_status()
        return resp.json()


def main():
    """Upload the sms data to zenodo and publish the information."""
    file_to_upload = sys.argv[1]
    env = Env()
    zenodo_url = env.str("ZENODO_URL")
    zenodo_access_token = env.str("ZENODO_ACCESS_TOKEN")
    version = env.str("VERSION")
    pid_prefix = env.str("PID_PREFIX")
    pid_service_password = env.str("PID_SERVICE_PASSWORD")
    pid_service_url = env.str("PID_SERVICE_URL")
    pid_service_user = env.str("PID_SERVICE_USER")
    only_draft = env.bool("ONLY_DRAFT", default=False)
    repository_url = env.str(
        "REPOSITORY_URL",
        default="https://codebase.helmholtz.cloud/hub-terra/sms/orchestration",
    )

    # If we have the pid service available we set the handle entry for SMM-Repository.
    # This way this will always point to our repo, even we move it.
    if all([pid_service_user, pid_service_password, pid_service_url, pid_prefix]):
        handle = Handle(
            base_url=pid_service_url,
            prefix=pid_prefix,
            username=pid_service_user,
            password=pid_service_password,
        )
        handle.put(repository_url, "SMS-Repository")
        repository_url = "https://hdl.handle.net/20.500.14372/SMS-Repository"

    zenodo_api = ZenodoApi(base_url=zenodo_url, access_token=zenodo_access_token)

    deposition = zenodo_api.create_deposition()
    deposition_id = deposition["id"]

    zenodo_api.upload_file(file_to_upload, deposition["links"]["bucket"])

    metadata_file = pathlib.Path(__file__).parent / "metadata.json"
    with metadata_file.open() as infile:
        metadata = json.load(infile)

    description_file = pathlib.Path(__file__).parent / "description.html"
    with description_file.open() as infile:
        description = infile.read()

    metadata.update(
        {
            "version": version,
            "description": description,
        }
    )
    metadata["custom"].update(
        {
            "code:codeRepository": repository_url,
        }
    )
    zenodo_api.update_metadata(deposition_id, metadata)

    print(f"{zenodo_url}/uploads/{deposition_id}")

    if not only_draft:
        zenodo_api.publish_deposition(deposition_id)
        print(f"{zenodo_url}/records/{deposition_id}")


if __name__ == "__main__":
    main()
