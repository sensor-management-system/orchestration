from project.api.models.base_model import db


class CustomField(db.Model):
    """
    Custom Field class
    """

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    key = db.Column(db.String(256), nullable=False)
    value = db.Column(db.String(1024), nullable=True)
    device_id = db.Column(db.Integer, db.ForeignKey("device.id"), nullable=False)

    def to_search_entry(self):
        return {
            "key": self.key,
            "value": self.value,
        }
