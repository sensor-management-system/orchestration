from datetime import datetime
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.sql import func

from project.api.models.base_model import db
from project.api.token_checker import current_user_id


def _current_user_id_or_none():
    try:
        return current_user_id()
    except BaseException:
        return None


class AuditMixin():
    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=datetime.now)

    @declared_attr
    def created_by_id(self):
        return db.Column(db.Integer,
                         db.ForeignKey('user.id', name='fk_%s_created_by_id' % self.__name__,
                                       use_alter=True),
                         # nullable=False,
                         default=_current_user_id_or_none
                         )

    @declared_attr
    def created_by(self):
        return db.relationship(
            'User',
            primaryjoin='User.id == %s.created_by_id' % self.__name__,
            remote_side='User.id'
        )

    @declared_attr
    def updated_by_id(self):
        return db.Column(db.Integer,
                         db.ForeignKey('user.id', name='fk_%s_updated_by_id' % self.__name__,
                                       use_alter=True),
                         # nullable=False,
                         default=_current_user_id_or_none,
                         onupdate=_current_user_id_or_none
                         )

    @declared_attr
    def updated_by(self):
        return db.relationship(
            'User',
            primaryjoin='User.id == %s.updated_by_id' % self.__name__,
            remote_side='User.id'
        )
