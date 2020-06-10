from project.api.models.base_model import db


class DeviceProperties(db.Model):
    """
    Properties class
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    measuring_range_min = db.Column(db.Float())
    measuring_range_max = db.Column(db.Float())
    failure_value = db.Column(db.Float())
    accuracy = db.Column(db.Float())
    label = db.Column(db.String(256))
    unit_uri = db.Column(db.String(256))  # CV
    unit_name = db.Column(db.String(256))  # CV
    Compartment_uri = db.Column(db.String(256))  # vermutlich CV
    Compartment_name = db.Column(db.String(256))  # vermutlich CV
    property_uri = db.Column(db.String(256))  # vermutlich CV
    property_name = db.Column(db.String(256))  # vermutlich CV
    # vermutlich CV, z.B. Atmosphere, Pedosphere
    sampling_media_uri = db.Column(db.String(256))
    sampling_media_name = db.Column(db.String(256))
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'))
