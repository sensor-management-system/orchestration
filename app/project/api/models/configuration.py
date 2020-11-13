import collections
from sqlalchemy.ext.hybrid import hybrid_property

from project.api.models.base_model import db
from project.api.models.mixin import AuditMixin

ConfigurationsTuple = collections.namedtuple(
    "ConfigurationsTuple", ["configuration_devices", "configuration_platforms"]
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
    resolution = db.Column(db.Float(), nullable=True)
    resolution_unit_uri = db.Column(db.String(256), nullable=True)
    resolutionUnitName = db.Column(db.String(256), nullable=True)

    longitude_src_device_property_id = db.Column(
        db.Integer, db.ForeignKey("device_property.id"), nullable=True
    )
    src_longitude = db.relationship(
        "DeviceProperty", uselist=False, foreign_keys=[longitude_src_device_property_id]
    )

    latitude_src_device_property_id = db.Column(
        db.Integer, db.ForeignKey("device_property.id"), nullable=True
    )
    src_latitude = db.relationship(
        "DeviceProperty", uselist=False, foreign_keys=[latitude_src_device_property_id]
    )

    elevation_src_device_property_id = db.Column(
        db.Integer, db.ForeignKey("device_property.id"), nullable=True
    )
    src_elevation = db.relationship(
        "DeviceProperty", uselist=False, foreign_keys=[elevation_src_device_property_id]
    )

    @hybrid_property
    def hierarchy(self):
        return ConfigurationsTuple(
            configuration_devices=self.configuration_devices,
            configuration_platforms=self.configuration_platforms,
        )

    @hierarchy.setter
    def hierarchy(self, value):
        new_configuration_devices = value.configuration_devices
        new_configuration_platforms = value.configuration_platforms

        current_configuration_device_by_device_id = {}

        for device_configuration in self.configuration_devices:
            current_configuration_device_by_device_id[
                device_configuration.device_id
            ] = device_configuration

        current_configuration_platform_by_platform_id = {}

        for platform_configuration in self.configuration_platforms:
            current_configuration_platform_by_platform_id[
                platform_configuration.platform_id
            ] = platform_configuration

        for new_cd in new_configuration_devices:
            device_id = new_cd.device_id
            old_configuration_device = current_configuration_device_by_device_id.get(
                device_id, None
            )
            if old_configuration_device is not None:
                new_cd.id = old_configuration_device.id
                new_cd.created_at = old_configuration_device.created_at
                new_cd.created_by = old_configuration_device.created_by
            new_cd.configuration = self

        for new_cp in new_configuration_platforms:
            platform_id = new_cp.platform_id
            old_configuration_platform = current_configuration_platform_by_platform_id.get(
                platform_id, None
            )
            if old_configuration_platform is not None:
                new_cp.id = old_configuration_platform.id
                new_cp.created_at = old_configuration_platform.created_at
                new_cp.created_by = old_configuration_platform.created_by
            new_cp.configuration = self

        self.configuration_devices = new_configuration_devices
        self.configuration_platforms = new_configuration_platforms
