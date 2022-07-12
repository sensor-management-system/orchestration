"""Extension for the PID."""
import json
import string

import requests
from flask import current_app
from requests.auth import HTTPBasicAuth

from ...api.helpers.errors import ConflictError, ServiceIsUnreachableError


class Pid:
    """Flask extension for the PID services."""

    def __init__(self, app=None):
        """Init the object."""
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Init the extension with the app object."""
        app.teardown_appcontext(self.teardown)

    def teardown(self, exception):
        """Cleanup on teardown of the app."""
        pass

    @property
    def pid_service_url(self):
        """The service url and prefix."""
        return current_app.config["PID_SERVICE_URL"]

    @property
    def pid_service_user(self):
        """The pid service username."""
        return current_app.config["PID_SERVICE_USER"]

    @property
    def pid_service_password(self):
        """The pid service password."""
        return current_app.config["PID_SERVICE_PASSWORD"]

    @property
    def pid_suffix(self):
        """Get sms suffix."""
        return current_app.config["PID_SUFFIX"]

    @property
    def pid_prefix(self):
        """Get sms prefix."""
        return current_app.config["PID_PREFIX"]

    def list_pids(self):
        """
        Retrieve the list of pids at once.

        :return: a list of all pids.
        """
        header = {"Accept": "application/json"}
        try:
            response = requests.get(
                self.pid_service_url,
                auth=HTTPBasicAuth(self.pid_service_user, self.pid_service_password),
                verify=False,
                headers=header,
            )
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            raise ServiceIsUnreachableError(repr(e))
        except requests.exceptions.HTTPError as e:
            raise ConflictError(repr(e))
        return response.json()

    def search_after_a_pid(self, term):
        """
        search for a PID by using a term.

        :return: a dict.
        """
        header = {"Accept": "application/json"}
        response = requests.get(
            self.pid_service_url,
            auth=HTTPBasicAuth(self.pid_service_user, self.pid_service_password),
            verify=False,
            headers=header,
            params={"URL": term},
        )
        return response.json()

    def list(self, limit=0, page=None):
        """
        Retrieve the list of pids at once.

        :param limit: the maximum number of items to return. The default is 1000.
        As a special case, if you specify limit=0, all items will be returned,
        without limit.
        :param page: When using limit parameter the returned data are displayed on multiple pages.
        the number of the page to return. I.e., if you specify limit=100&page=3, items 201 through 300
        will be returned
        :return: a list of all pids.
        """
        header = {"Accept": "application/json"}
        try:
            response = requests.get(
                self.pid_service_url,
                auth=HTTPBasicAuth(self.pid_service_user, self.pid_service_password),
                verify=False,
                headers=header,
                params={"limit": limit, "page": page},
            )
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            raise ServiceIsUnreachableError(repr(e))
        except requests.exceptions.HTTPError as e:
            raise ConflictError(repr(e))
        return response.json()

    def get(self, object_pid):
        """
        Retrieve the information at once for a PID.

        :example response.json:
        [
                {
                    "idx": 1,
                    "type": "URL",
                    "parsed_data": "https://localhost.localdomain/devices/4/basic",
                    "data": "aHR0cHM6Ly9sb2NhbGhvc3QubG9jYWxkb21haW4vZGV2aWNlcy80L2Jhc2lj",
                    "timestamp": "2022-07-25T12:27:12Z",
                    "ttl_type": 0,
                    "ttl": 86400,
                    "refs": [],
                    "privs": "rwr-"
                },
                {
                    "idx": 2,
                    "type": "LandingPage",
                    "parsed_data": "https://localhost.localdomain/devices/4/basic",
                    "data": "aHR0cHM6Ly9sb2NhbGhvc3QubG9jYWxkb21haW4vZGV2aWNlcy80L2Jhc2lj",
                    "timestamp": "2022-07-25T12:27:12Z",
                    "ttl_type": 0,
                    "ttl": 86400,
                    "refs": [],
                    "privs": "rwr-"
                },
                {
                    "idx": 3,
                    "type": "Identifier",
                    "parsed_data": "4",
                    "data": "NA==",
                    "timestamp": "2022-07-25T12:27:12Z",
                    "ttl_type": 0,
                    "ttl": 86400,
                    "refs": [],
                    "privs": "rwr-"
                },
                {
                    "idx": 4,
                    "type": "IdentifierType",
                    "parsed_data": "handler",
                    "data": "aGFuZGxlcg==",
                    "timestamp": "2022-07-25T12:27:12Z",
                    "ttl_type": 0,
                    "ttl": 86400,
                    "refs": [],
                    "privs": "rwr-"
                },
                {
                    "idx": 5,
                    "type": "SchemaVersion",
                    "parsed_data": "1.0",
                    "data": "MS4w",
                    "timestamp": "2022-07-25T12:27:12Z",
                    "ttl_type": 0,
                    "ttl": 86400,
                    "refs": [],
                    "privs": "rwr-"
                },
                {
                    "idx": 6,
                    "type": "Name",
                    "parsed_data": "TID1",
                    "data": "VElEMQ==",
                    "timestamp": "2022-07-25T12:27:12Z",
                    "ttl_type": 0,
                    "ttl": 86400,
                    "refs": [],
                    "privs": "rwr-"
                },
                {
                    "idx": 7,
                    "type": "Owner",
                    "parsed_data": "kotyba.alhaj-taha@ufz.de",
                    "data": "a290eWJhLmFsaGFqLXRhaGFAdWZ6LmRl",
                    "timestamp": "2022-07-25T12:27:12Z",
                    "ttl_type": 0,
                    "ttl": 86400,
                    "refs": [],
                    "privs": "rwr-"
                },
                {
                    "idx": 8,
                    "type": "OwnerName",
                    "parsed_data": "Kotyba Alhaj Taha",
                    "data": "S290eWJhIEFsaGFqIFRhaGE=",
                    "timestamp": "2022-07-25T12:27:12Z",
                    "ttl_type": 0,
                    "ttl": 86400,
                    "refs": [],
                    "privs": "rwr-"
                },
                {
                    "idx": 9,
                    "type": "Manufacturer",
                    "parsed_data": "https://localhost.localdomain/cv/api/v1/manufacturers/22/",
                    "data": "aHR0cHM6Ly9sb2NhbGhvc3QubG9jYWxkb21haW4vY3YvYXBpL3YxL21hbnVm\nYWN0dXJlcnMvMjIv",
                    "timestamp": "2022-07-25T12:27:12Z",
                    "ttl_type": 0,
                    "ttl": 86400,
                    "refs": [],
                    "privs": "rwr-"
                },
                {
                    "idx": 10,
                    "type": "ManufacturerName",
                    "parsed_data": "Ackermann KG",
                    "data": "QWNrZXJtYW5uIEtH",
                    "timestamp": "2022-07-25T12:27:12Z",
                    "ttl_type": 0,
                    "ttl": 86400,
                    "refs": [],
                    "privs": "rwr-"
                },
                {
                    "idx": 100,
                    "type": "HS_ADMIN",
                    "parsed_data": {
                        "adminId": "21.T11998/USER53",
                        "adminIdIndex": 300,
                        "perms": {
                            "add_handle": true,
                            "delete_handle": true,
                            "add_derived_prefix": false,
                            "delete_derived_prefix": false,
                            "modify_value": true,
                            "remove_value": true,
                            "add_value": true,
                            "modify_admin": true,
                            "remove_admin": true,
                            "add_admin": true,
                            "read_value": true,
                            "list_handles": false
                        }
                    },
                    "data": "B/MAAAAQMjEuVDExOTk4L1VTRVI1MwAAASw=",
                    "timestamp": "2022-07-25T12:27:12Z",
                    "ttl_type": 0,
                    "ttl": 86400,
                    "refs": [],
                    "privs": "rwr-"
                }
            ]
        :param object_pid: The pid
        :return: pid description.
        """
        header = {"Content-Type": "application/json", "Accept": "application/json"}
        try:
            response = requests.get(
                url=self.pid_service_url + object_pid,
                auth=HTTPBasicAuth(self.pid_service_user, self.pid_service_password),
                verify=False,
                headers=header,
            )

            response.raise_for_status()
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            raise ServiceIsUnreachableError(repr(e))
        except requests.exceptions.HTTPError as e:
            raise ConflictError(repr(e))
        return response

    def search(self, term=None, limit=0):
        """
        search for a PID by using a term.

        :param limit: the limit of results
        :param term: a string to Search and get the PID of an object with the selected url.
        :return: a list of match pids.
        """
        header = {"Accept": "application/json"}
        response = requests.get(
            self.pid_service_url,
            auth=HTTPBasicAuth(self.pid_service_user, self.pid_service_password),
            verify=False,
            headers=header,
            params={"URL": f"*{term}*", "limit": limit},
        )
        return response.json()

    def create(self, instrument_data) -> string:
        """
        Create a new PID.

        :param instrument_data: the url for the source object.
        :return str: the pid of the object.
        """

        header = {"Content-Type": "application/json", "Accept": "application/json"}
        try:
            response = requests.post(
                url=self.pid_service_url,
                json=instrument_data,
                auth=HTTPBasicAuth(self.pid_service_user, self.pid_service_password),
                verify=False,
                headers=header,
                params={"prefix": self.pid_suffix, "suffix": self.pid_prefix},
            )
            response.raise_for_status()
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            raise ServiceIsUnreachableError(repr(e))
        except requests.exceptions.HTTPError as e:
            raise ConflictError(repr(e))
        epic_pid = response.json()["epic-pid"]
        return epic_pid

    def update(self, source_object_pid, instrument_data):
        """
        Update an existing PID.

        :param instrument_data: data to update
        :param source_object_pid: The PID.
        :return:
        """
        header = {"Content-Type": "application/json", "Accept": "application/json"}
        try:
            response = requests.put(
                url=self.pid_service_url + source_object_pid,
                json=instrument_data,
                auth=HTTPBasicAuth(self.pid_service_user, self.pid_service_password),
                verify=False,
                headers=header,
            )
            response.raise_for_status()
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            raise ServiceIsUnreachableError(repr(e))
        except requests.exceptions.HTTPError as e:
            raise ConflictError(repr(e))
        return response.status_code  # 204

    def delete(self, object_pid):
        """
        Delete a PID.

        :param object_pid: the PID.
        :return:
        """
        header = {"Content-Type": "application/json", "Accept": "application/json"}
        try:
            response = requests.delete(
                url=self.pid_service_url + object_pid,
                auth=HTTPBasicAuth(self.pid_service_user, self.pid_service_password),
                verify=False,
                headers=header,
            )
            response.raise_for_status()
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            raise ServiceIsUnreachableError(repr(e))
        except requests.exceptions.HTTPError as e:
            raise ConflictError(repr(e))
        return response.status_code  # 204
