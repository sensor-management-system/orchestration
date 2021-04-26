from .base_model import db
from .mixin import AuditMixin


class ConfigurationPlatform(db.Model, AuditMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    offset_x = db.Column(db.Float(), nullable=True)
    offset_y = db.Column(db.Float(), nullable=True)
    offset_z = db.Column(db.Float(), nullable=True)

    configuration_id = db.Column(
        db.Integer, db.ForeignKey("configuration.id"), nullable=False
    )
    configuration = db.relationship(
        "Configuration",
        backref=db.backref("configuration_platforms", cascade="all, delete-orphan"),
        cascade="all",
    )
    platform_id = db.Column(db.Integer, db.ForeignKey("platform.id"), nullable=False)
    platform = db.relationship(
        "Platform",
        backref=db.backref("configuration_platform", cascade="all"),
        foreign_keys=[platform_id],
    )
    parent_platform_id = db.Column(
        db.Integer, db.ForeignKey("platform.id"), nullable=True
    )
    parent_platform = db.relationship(
        "Platform",
        backref=db.backref("inner_configuration_platform", cascade="all"),
        foreign_keys=[parent_platform_id],
    )
