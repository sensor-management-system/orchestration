# SPDX-FileCopyrightText: 2022
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Extension for the IDL (for permission groups)."""

import operator
from typing import List, Optional

import requests
from cachetools import TTLCache, cachedmethod
from flask import current_app

from ...api.helpers.errors import ConflictError, ServiceIsUnreachableError
from .models import permission_group, user_account


class Idl:
    """Flask extension for the institute decoupling layer to handle permission groups."""

    def __init__(self, app=None):
        """Init the object."""
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Init the extension with the app object."""
        app.teardown_appcontext(self.teardown)
        # And create caches.
        self.cache_user_account = TTLCache(
            # Here we need quite a lot of entries.
            maxsize=5000,
            ttl=app.config.get("IDL_CACHING_SECONDS", 600),
        )
        self.cache_permission_groups = TTLCache(
            # Here we only save one single entry (a list of all events).
            maxsize=1,
            ttl=app.config.get("IDL_CACHING_SECONDS", 600),
        )

    def teardown(self, exception):
        """Cleanup on teardown of the app."""
        pass

    @property
    def base_url(self):
        """Get the base url to work with the external idl service."""
        return current_app.config["IDL_URL"]

    @property
    def token(self):
        """Get the token to work with the external idl service."""
        return current_app.config["SMS_IDL_TOKEN"]

    @cachedmethod(operator.attrgetter("cache_user_account"))
    def get_all_permission_groups_for_a_user(
        self, user_subject
    ) -> Optional[user_account.UserAccount]:
        """
        Return an object with the users data.

        Those include the lists of administrated_permission_groups and
        membered_permission_groups.
        """
        url = f"{self.base_url}/user-accounts"
        params = {
            "page": 1,
            # We only need the exact entry
            "itemsPerPage": 1,
            "userName_is": user_subject,
        }
        json_obj = self.make_request_to_idl(url, params)
        # Checking for an empty list
        if not json_obj:
            return None
        result = user_account.idl_from_dict(json_obj[0])
        return result

    def make_request_to_idl(self, url, params):
        """
        Make a request to the IDL.

        :param url: IDL url
        :param params:
        :return:
        """
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/json",
        }
        try:
            response = requests.get(url, headers=headers, params=params, timeout=5)
            response.raise_for_status()

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            raise ServiceIsUnreachableError(repr(e))
        except requests.exceptions.HTTPError as e:
            raise ConflictError(repr(e))
        json_obj = response.json()
        return json_obj

    @cachedmethod(operator.attrgetter("cache_permission_groups"))
    def get_permission_groups(self) -> List[permission_group.PermissionGroup]:
        """
        Return a list of groups fetched from the IDL service.

        :return: list
        """
        url = f"{self.base_url}/permission-groups"
        # TODO: Deactivate pagination
        params = {"page": 1, "itemsPerPage": 100}
        json_obj = self.make_request_to_idl(url, params)
        if not json_obj:
            return []
        result = permission_group.permission_groups_from_list_of_dicts(json_obj)
        return result
