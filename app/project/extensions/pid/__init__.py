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
            return repr(e)
        except requests.exceptions.HTTPError as e:
            return repr(e)
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

    def create_a_new_pid(self, source_object_url: string) -> string:
        """
        Create a new PID.

        :param source_object_url: the url for the source object.
        :return str: the pid of the object.
        """

        json_data = json.dumps([{"type": "URL", "parsed_data": source_object_url}])
        header = {"Content-Type": "application/json", "Accept": "application/json"}
        try:
            response = requests.post(
                url=self.pid_service_url,
                data=json_data,
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

    def update_existing_pid(self, source_object_url, updated_url):
        """
        Update an existing PID.
        :param updated_url:
        :param source_object_url: The API Service URL with the PID.
        :return:
        """
        json_data = json.dumps([{"type": "URL", "parsed_data": updated_url}])
        header = {"Content-Type": "application/json", "Accept": "application/json"}
        try:
            response = requests.put(
                url=self.pid_service_url + "/" + source_object_url,
                data=json_data,
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

    def delete_a_pid(self, source_object_url):
        """
        Delete a PID.
        :param source_object_url: The API Service URL with the PID.
        :return:
        """
        header = {"Content-Type": "application/json", "Accept": "application/json"}
        try:
            response = requests.delete(
                url=self.pid_service_url + "/" + source_object_url,
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
