from marshmallow_jsonapi.flask import Relationship


def set_device_relationship_schema(object_type):
    device = Relationship(attribute='device',
                          self_view='device_' + object_type,
                          self_view_kwargs={'id': '<id>'},
                          related_view='devices_detail',
                          related_view_kwargs={'id': '<id>'},
                          schema='DeviceSchema',
                          type_='device')
    return device


def set_platform_relationship_schema(object_type):
    platform = Relationship(attribute='platform',
                            self_view='platform_' + object_type,
                            self_view_kwargs={'id': '<id>'},
                            related_view='platform_detail',
                            related_view_kwargs={'id': '<id>'},
                            schema='PlatformSchema',
                            type_='platform')
    return platform
