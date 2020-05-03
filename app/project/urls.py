from project.api.deviceDetail import DeviceDetail
from project.api.deviceList import DeviceList
from project.api.deviceRelationship import DeviceRelationship
from project.api.ping import Ping
from project.api.platformDetail import PlatformDetail
from project.api.platformList import PlatformList
from project.api.platformRelationship import PlatformRelationship


def Create_endpoints(api):
    api.route(Ping, 'test_connection', '/ping')

    # Platform
    api.route(PlatformList, 'platform_list', '/platforms')
    api.route(PlatformDetail, 'platform_detail', '/platforms/<int:id>',
              '/devices/<int:device_id>/platform')
    api.route(PlatformRelationship, 'platform_devices',
              '/platforms/<int:id>/relationships/devices')

    # Device
    api.route(DeviceList, 'devices_list', '/devices',
              '/platforms/<int:id>/devices')
    api.route(DeviceDetail, 'devices_detail', '/devices/<int:id>')
    api.route(DeviceRelationship, 'device_platform',
              '/devices/<int:id>/relationships/platform')
