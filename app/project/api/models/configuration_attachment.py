

from project.api.models.base_model import db


class ConfigurationAttachment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(256), nullable=True)
    url = db.Column(db.String(1024), nullable=False)
    configuration_id = db.Column(
        db.Integer, db.ForeignKey("configuration.id"), nullable=False
    )
