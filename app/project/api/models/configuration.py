from project.api.models.base_model import db
from project.api.models.device_property import DeviceProperty
from project.api.models.mixin import AuditMixin


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
