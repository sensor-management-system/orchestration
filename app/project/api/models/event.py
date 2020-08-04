from sqlalchemy.sql import func

from project.api.models.base_model import db


class Event(db.Model):
    """
    Event class
    """

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=func.now())
    device_id = db.Column(db.Integer, db.ForeignKey("device.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", backref=db.backref("events"))
