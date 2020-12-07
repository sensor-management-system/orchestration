from project.api.models.base_model import db


class PlatformAttachment(db.Model):
    """
    Platform Attachment class
    """

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    label = db.Column(db.String(256), nullable=True)
    url = db.Column(db.String(1024), nullable=False)
    platform_id = db.Column(db.Integer, db.ForeignKey("platform.id"), nullable=False)

    def to_search_entry(self):
        # to be included in the platform
        return {"label": self.label, "url": self.url}
