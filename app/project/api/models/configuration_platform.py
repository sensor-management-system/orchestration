from project.api.models.base_model import db
from project.api.models.configuration import Configuration
from project.api.models.mixin import AuditMixin
from project.api.models.platform import Platform


class ConfigurationPlatform(db.Model, AuditMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    offset_x = db.Column(db.Float(), nullable=True)
    offset_y = db.Column(db.Float(), nullable=True)
    offset_z = db.Column(db.Float(), nullable=True)

    configuration_id = db.Column(
        db.Integer, db.ForeignKey("configuration.id"), nullable=False
    )
    configuration = db.relationship(
        "Configuration", backref=db.backref("configuration_platform"), cascade="all"
    )
    platform_id = db.Column(db.Integer, db.ForeignKey("platform.id"), nullable=False)
    platform = db.relationship(
        "Platform",
        backref=db.backref("configuration_platform"),
        foreign_keys=[platform_id],
        cascade="all",
    )
    parent_platform_id = db.Column(
        db.Integer, db.ForeignKey("platform.id"), nullable=True
    )
    parent_platform = db.relationship(
        "Platform",
        backref=db.backref("inner_configuration_platform"),
        foreign_keys=[parent_platform_id],
        cascade="all",
    )
