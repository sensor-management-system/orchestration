import collections
from sqlalchemy.ext.hybrid import hybrid_property

from project.api.models.base_model import db
from project.api.models.device_property import DeviceProperty
from project.api.models.mixin import AuditMixin

ConfigurationsTuple = collections.namedtuple(
    "ConfigurationsTuple", ["configurations_device", "configurations_platform"]
)


class Configuration(db.Model, AuditMixin):
    """
    Configuration class
    """

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    start_date = db.Column(db.DateTime, nullable=True)
    end_date = db.Column(db.DateTime, nullable=True)
    location_type = db.Column(db.String(256), nullable=False)
    longitude = db.Column(db.Float(), nullable=True)
    latitude = db.Column(db.Float(), nullable=True)
    elevation = db.Column(db.Float(), nullable=True)
    project_uri = db.Column(db.String(256), nullable=True)
    project_name = db.Column(db.String(256), nullable=True)
    label = db.Column(db.String(256), nullable=True)
    status = db.Column(db.String(256), nullable=True, default="draft")

    longitude_src_device_property_id = db.Column(
        db.Integer, db.ForeignKey('device_property.id'), nullable=True
    )
    longitude_src_device_property = db.relationship(
        DeviceProperty, uselist=False, foreign_keys=[longitude_src_device_property_id]
    )

    latitude_src_device_property_id = db.Column(
        db.Integer, db.ForeignKey('device_property.id'), nullable=True
    )
    latitude_src_device_property = db.relationship(
        DeviceProperty, uselist=False, foreign_keys=[latitude_src_device_property_id]
    )

    elevation_src_device_property_id = db.Column(
        db.Integer, db.ForeignKey('device_property.id'), nullable=True
    )
    elevation_src_device_property = db.relationship(
        DeviceProperty, uselist=False, foreign_keys=[elevation_src_device_property_id]
    )

    @hybrid_property
    def hierarchy(self):
        return ConfigurationsTuple(
            configurations_device=self.configuration_device,
            configurations_platform=self.configuration_platform,
        )

    @hierarchy.setter
    def hierarchy(self, value):
        configuration_device = value.configurations_device
        configuration_platform = value.configurations_platform

        current_configuration_device_by_device_id = {}
        current_configuration_platform_by_platform_id = {}

        for device_configuration in self.configuration_device:
            current_configuration_device_by_device_id[
                device_configuration.device_id
            ] = device_configuration

        for platform_configuration in self.configuration_platform:
            current_configuration_platform_by_platform_id[
                platform_configuration.platform_id
            ] = platform_configuration

        for device_configuration in configuration_device:
            device_configuration.configuration = self
            if (
                    device_configuration.device_id
                    in current_configuration_device_by_device_id.keys()
            ):
                device_configuration.id = current_configuration_device_by_device_id[
                    configuration_device.device_id
                ].id

        for platform_configuration in configuration_platform:
            platform_configuration.configuration = self
            if (
                    platform_configuration.platform_id
                    in current_configuration_platform_by_platform_id.keys()
            ):
                platform_configuration.id = current_configuration_platform_by_platform_id[
                    platform_configuration.platform_id
                ].id
        self.configuration_device = configuration_device
        self.configuration_platform = configuration_platform
