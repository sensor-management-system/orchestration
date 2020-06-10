from project.api.models.base_model import db
from project.api.token_checker import token_required
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.sql import func


@token_required
def _current_user_id_or_none(current_user):
    user_name = current_user['sub'].split('@')[0]
    return user_name


class Platform(db.Model):
    """
    Platform class
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.Text)
    short_name = db.Column(db.String(256))
    long_name = db.Column(db.String(256))
    manufacturer_uri = db.Column(db.String(256))
    manufacturer_name = db.Column(db.String(256))
    model = db.Column(db.String(256))
    platform_type_uri = db.Column(db.String(256))
    platform_type_name = db.Column(db.String(256))
    status_uri = db.Column(db.String(256))
    status_name = db.Column(db.String(256))
    website = db.Column(db.String(1024))
    created_at = db.Column(db.DateTime(timezone=True),
                           default=func.now())
    modified_at = db.Column(db.DateTime(timezone=True),
                            onupdate=func.now())
    inventory_number = db.Column(db.String(256))
    serial_number = db.Column(db.String(256))
    persistent_identifier = db.Column(db.String(256))
    platform_attachment = db.relationship("PlatformAttachment",
                                          cascade="save-update, merge, "
                                                  "delete, delete-orphan")

    @declared_attr
    def created_by(cls):
        return db.Column(db.Integer,
                         db.ForeignKey('user.id',
                                       name='fk_%s_created_by'
                                            % cls.__name__,
                                       use_alter=True),
                         # nullable=False,
                         default=_current_user_id_or_none
                         )

    # created_by_id = db.Column(db.Integer(),
    #                          db.ForeignKey('user.id'),
    #                          default=_current_user_id_or_none)
    # created_by = db.relationship('User', backref=db.backref('platforms',
    #                                                        lazy=True))
    # modified_by_id = db.Column(id.Integer, db.ForeignKey('user.id'))
    # modified_by = db.relationship('User', backref=db.backref('platforms',
    #                                                         lazy=True))
