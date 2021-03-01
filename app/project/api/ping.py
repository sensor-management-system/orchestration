from flask_rest_jsonapi import ResourceList


class Ping(ResourceList):
    """
    This class allow client to ping the API.
    """

    def get(self):
        """Using GET method to ping API
        :return: response
        """
        response = {"status": "success", "message": "Hello Sensor!"}
        return response
