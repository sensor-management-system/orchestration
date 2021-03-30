from .base_model import db


class DeviceAttachment(db.Model):
    """
    Attachment class
    """

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    label = db.Column(db.String(256), nullable=True)
    url = db.Column(db.String(1024), nullable=False)
    device_id = db.Column(db.Integer, db.ForeignKey("device.id"), nullable=False)
    device = db.relationship("Device")

    def to_search_entry(self):
        # to be included in the devices
        return {"label": self.label, "url": self.url}
