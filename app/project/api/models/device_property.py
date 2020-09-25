from project.api.models.base_model import db
from project.api.models.device import Device


class DeviceProperty(db.Model):
    """
    DeviceProperty class
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    measuring_range_min = db.Column(db.Float(), nullable=True)
    measuring_range_max = db.Column(db.Float(), nullable=True)
    failure_value = db.Column(db.Float(), nullable=True)
    accuracy = db.Column(db.Float(), nullable=True)
    label = db.Column(db.String(256), nullable=True)
    unit_uri = db.Column(db.String(256), nullable=True)  # CV
    unit_name = db.Column(db.String(256), nullable=True)  # CV
    compartment_uri = db.Column(db.String(256), nullable=True)  # vermutlich CV
    compartment_name = db.Column(db.String(256), nullable=True)  # vermutlich CV
    property_uri = db.Column(db.String(256), nullable=True)  # vermutlich CV
    property_name = db.Column(db.String(256), nullable=True)  # vermutlich CV
    # vermutlich CV, z.B. Atmosphere, Pedosphere
    sampling_media_uri = db.Column(db.String(256), nullable=True)
    sampling_media_name = db.Column(db.String(256), nullable=True)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'), nullable=False)
    device = db.relationship(
        Device, uselist=False, foreign_keys=[device_id]
    )
