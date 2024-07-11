# SPDX-FileCopyrightText: 2022
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

from flask_rest_jsonapi import ResourceList


class Ping(ResourceList):
    """
    This class allow client to ping the API.
    """

    def get(self):
        """Using GET method to ping API
        :return: response
        """
        response = {"status": "success", "message": "Pong"}
        return response
