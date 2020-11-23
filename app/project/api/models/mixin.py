from datetime import datetime

import sqlalchemy
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.sql import func

from project.api.models.base_model import db
from project.api.token_checker import current_user_id

from project.api.search import add_to_index, remove_from_index, query_index


def _current_user_id_or_none():
    try:
        return current_user_id()
    except BaseException:
        return None


class AuditMixin:
    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=datetime.now)

    @declared_attr
    def created_by_id(self):
        return db.Column(
            db.Integer,
            db.ForeignKey(
                "user.id", name="fk_%s_created_by_id" % self.__name__, use_alter=True
            ),
            # nullable=False,
            default=_current_user_id_or_none,
        )

    @declared_attr
    def created_by(self):
        return db.relationship(
            "User",
            primaryjoin="User.id == %s.created_by_id" % self.__name__,
            remote_side="User.id",
        )

    @declared_attr
    def updated_by_id(self):
        return db.Column(
            db.Integer,
            db.ForeignKey(
                "user.id", name="fk_%s_updated_by_id" % self.__name__, use_alter=True
            ),
            # nullable=False,
            default=_current_user_id_or_none,
            onupdate=_current_user_id_or_none,
        )

    @declared_attr
    def updated_by(self):
        return db.relationship(
            "User",
            primaryjoin="User.id == %s.updated_by_id" % self.__name__,
            remote_side="User.id",
        )


class SearchableMixin:
    @classmethod
    def search(cls, query, page, per_page):
        ids, total = query_index(cls.__tablename__, query, page, per_page)
        if total == 0 or not ids:
            return cls.query.filter(sqlalchemy.sql.false()), total
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        return (
            cls.query.filter(cls.id.in_(ids)).order_by(db.case(when, value=cls.id)),
            total,
        )

    @classmethod
    def before_commit(cls, session):
        session._changes = {
            "add": list(session.new),
            "update": list(session.dirty),
            "delete": list(session.deleted),
        }

    @classmethod
    def after_commit(cls, session):
        for obj in session._changes["add"]:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes["update"]:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes["delete"]:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)


db.event.listen(db.session, "before_commit", SearchableMixin.before_commit)
db.event.listen(db.session, "after_commit", SearchableMixin.after_commit)
