from flask_rest_jsonapi import ResourceList


class Ping(ResourceList):
    def get(self):
        response = {
            'status': 'success',
            'message': 'Hello Sensor!'
        }
        return response
