from project.api.ping import Ping


def Create_endpoints(api):

    api.route(Ping, 'test_connection', '/ping')