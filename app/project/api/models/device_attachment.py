from project.api.models.base_model import db


class DeviceAttachment(db.Model):
    """
    Attachment class
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    label = db.Column(db.String(256))
    url = db.Column(db.String(1024), nullable=False)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'))
