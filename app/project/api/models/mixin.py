import collections
import itertools
from datetime import datetime

import sqlalchemy
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.sql import func

from project.api.models.base_model import db
from project.api.search import (
    add_to_index,
    create_index,
    query_index,
    remove_from_index,
    remove_index,
)


class AuditMixin:
    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=None, onupdate=datetime.now)

    @declared_attr
    def created_by_id(self):
        return db.Column(
            db.Integer,
            db.ForeignKey(
                "user.id", name="fk_%s_created_by_id" % self.__name__, use_alter=True
            ),
            # nullable=False,
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
        )

    @declared_attr
    def updated_by(self):
        return db.relationship(
            "User",
            primaryjoin="User.id == %s.updated_by_id" % self.__name__,
            remote_side="User.id",
        )


class SearchableMixin:
    """Mixin to make a model searchable via full text search."""

    @classmethod
    def search(cls, query, page, per_page):
        """Search the model with a given query and pagination settings."""
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
        """Prepare the commit stage."""
        # First we create a list with all the new, updated or
        # deleted elements
        # This is also what is suggested to do here as well
        # https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xvi-full-text-search
        # However, in contrast do the idea there, we need also to query
        # the search entries now, as we are not allowed to run
        # any further sql in the after_commit stage.
        # And still - we don't have the new ids before the commit
        # nor can we be sure that all the elements are committed correctly,
        # so we still need to handle most of the logic in the after_commit
        # method
        session._changes = {
            "add": list(session.new),
            "update": list(session.dirty),
            "delete": list(session.deleted),
        }
        # And we want to store the payload here as well
        session._search_add = []

        for obj in itertools.chain(session._changes["add"], session._changes["update"]):
            if isinstance(obj, SearchableMixin):
                session._search_add.append(
                    SearchModelWithEntry(model=obj, entry=obj.to_search_entry())
                )

    @classmethod
    def after_commit(cls, session):
        """Update the search after the sqlalchemy commit."""
        ids_to_add = collections.defaultdict(set)
        for obj in itertools.chain(session._changes["add"], session._changes["update"]):
            if isinstance(obj, SearchableMixin):
                ids_to_add[obj.__tablename__].add(obj.id)
        for search_model_with_entry in session._search_add:
            model = search_model_with_entry.model
            if model.id in ids_to_add[model.__tablename__]:
                add_to_index(model.__tablename__, model, search_model_with_entry.entry)

        for obj in session._changes["delete"]:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)

        session._changes = None
        session._search_add = None

    @classmethod
    def reindex(cls):
        """Recreate the index for the model."""
        remove_index(cls.__tablename__)
        idx_definition = cls.get_search_index_definition()
        create_index(cls.__tablename__, idx_definition)

        for obj in cls.query:
            entry = obj.to_search_entry()
            add_to_index(cls.__tablename__, obj, entry)


db.event.listen(db.session, "before_commit", SearchableMixin.before_commit)
db.event.listen(db.session, "after_commit", SearchableMixin.after_commit)

SearchModelWithEntry = collections.namedtuple(
    "SearchModelWithEntry", ["model", "entry"]
)
