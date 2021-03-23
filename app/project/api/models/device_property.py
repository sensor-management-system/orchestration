"""Model for device properties."""


from ..models.device import Device
from .base_model import db


class DeviceProperty(db.Model):
    """DeviceProperty class."""

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
    resolution = db.Column(db.Float(), nullable=True)
    resolution_unit_uri = db.Column(db.String(256), nullable=True)
    resolution_unit_name = db.Column(db.String(256), nullable=True)
    device_id = db.Column(db.Integer, db.ForeignKey("device.id"), nullable=False)
    device = db.relationship(Device, uselist=False, foreign_keys=[device_id])

    def to_search_entry(self):
        """Convert the model to a dict to store it in the full text search."""
        # to be included in devices
        return {
            "label": self.label,
            "unit_name": self.unit_name,
            "unit_uri": self.unit_uri,
            "compartment_name": self.compartment_name,
            "compartment_uri": self.compartment_uri,
            "property_name": self.property_name,
            "property_uri": self.property_uri,
            "sample_medium_name": self.sampling_media_name,
            "sample_medium_uri": self.sampling_media_uri,
            "resolution_unit_name": self.resolution_unit_name,
            "resolution_unit_uri": self.resolution_unit_uri,
        }
