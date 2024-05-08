#!/usr/bin/env python3

"""Publish SMS data on zenodo."""

import os
import pathlib

import requests


class Env:
    def str(self, key, default=None):
        return os.getenv(key, default)

    def int(self, key, default=None):
        if key in os.environ.keys():
            return int(os.environ[key])
        return default


class ZenodoApi:
    def __init__(self, base_url, access_token):
        self.base_url = base_url
        self.access_token = access_token

    def get_depositions(self):
        url = f"{self.base_url}/api/deposit/depositions"
        response = requests.get(url, params={"access_token": self.access_token})
        response.raise_for_status()
        return response.json()

    def create_deposition(self):
        url = f"{self.base_url}/api/deposit/depositions"
        response = requests.post(url, params={"access_token": self.access_token}, json={})
        response.raise_for_status()
        return response.json()

    def get_optional_deposition(self, id_):
        url = f"{self.base_url}/api/deposit/depositions/{id_}"
        response = requests.get(url, params={"access_token": self.access_token})
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json()

    def upload_file(self, file, bucket_url):
        path = pathlib.Path(file)
        filename = path.name

        with path.open("rb") as fp:
            response = requests.put(
                f"{bucket_url}/{filename}",
                data=fp,
                params={"access_token": self.access_token}
            )
            response.raise_for_status()
            return response.json()

    def update_metadata(self, id_, metadata):

        url = f"{self.base_url}/api/deposit/depositions/{id_}"
        data = {
            "metadata": metadata
        }
        response = requests.put(url, params={"access_token": self.access_token}, json=data)
        response.raise_for_status()
        return response.json()

    def publish_deposition(self, id_):

        url = f"{self.base_url}/api/deposit/depositions/{id_}/actions/publish"
        response = requests.post(url, params={"access_token": self.access_token})
        response.raise_for_status()
        return response.json()



def main():
    env = Env()
    zenodo_url = env.str("ZENODO_URL", "https://sandbox.zenodo.org")
    zenodo_access_token = env.str("ZENODO_ACCESS_TOKEN")
    version = env.str("VERSION", "1.15.0")

    zenodo_api = ZenodoApi(base_url=zenodo_url, access_token=zenodo_access_token)

    deposition = zenodo_api.create_deposition()
    deposition_id = deposition["id"]
    files_to_upload = [
        "./README.md",
    ]
    for file in files_to_upload:
        upload_info = zenodo_api.upload_file(file, deposition["links"]["bucket"])

    metadata = {
        "title": "Sensor Management System",
        "upload_type": "software",
        "description": "The Sensor Management System is a tool to manage sensors.",
        "creators": [{
            "name": "Nils Brinckmann",
            "affiliation": "Helmholtz Centre Potsdam - German Research Centre for Geosciences GFZ",
        }],
        "version": version,
    }
    update_metadata_response = zenodo_api.update_metadata(deposition_id, metadata)
    publish_response = zenodo_api.publish_deposition(deposition_id)

    print(publish_response)

if __name__ == "__main__":
    main()
