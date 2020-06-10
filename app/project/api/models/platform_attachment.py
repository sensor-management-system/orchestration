from project.api.models.base_model import db


class PlatformAttachment(db.Model):
    """
    Platform Attachment class
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    label = db.Column(db.String(256))
    url = db.Column(db.String(1024), nullable=False)
    platform_id = db.Column(db.Integer, db.ForeignKey('platform.id'))
