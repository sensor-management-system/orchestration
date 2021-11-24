import requests
from flask import current_app

from project.api.helpers.errors import ServiceIsUnreachableError, ConflictError
from project.api.models.idl_user import idl_from_dict


class Idl:
    def get_all_permission_groups(self, user_subject):
        """
        Returns a list of groups or Projects for a user-subject that are fetched from the IDL service.

        :param user_subject: the subject coming from the user jwt.
        :return: list
        """
        sms_idl_token = current_app.config["SMS_IDL_TOKEN"]
        access_headers = {
            "Authorization": "Bearer {}".format(sms_idl_token),
            "Accept": "application/json",
        }
        idl_url = current_app.config["IDL_URL"]
        params = {"page": 1, "itemsPerPage": 100, "username_is": user_subject}
        try:
            response = requests.get(
                idl_url, headers=access_headers, params=params, timeout=5
            )
            response.raise_for_status()

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            raise ServiceIsUnreachableError(repr(e))
        except requests.exceptions.HTTPError as e:
            raise ConflictError(repr(e))
        json_obj = response.json()
        # Checking for an empty list
        if not json_obj:
            return []
        result = idl_from_dict(json_obj[0])
        return result
