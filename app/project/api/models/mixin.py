import collections
import itertools
from datetime import datetime

import sqlalchemy
from sqlalchemy.ext.declarative import declared_attr

from ..search import (
    add_to_index,
    create_index,
    query_index,
    remove_from_index,
    remove_index,
)
from .base_model import db


class AuditMixin:
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # define 'updated at' to be populated with datetime.utcnow()
    updated_at = db.Column(db.DateTime, default=None, onupdate=datetime.utcnow)

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
        )

    @declared_attr
    def updated_by(self):
        return db.relationship(
            "User",
            primaryjoin="User.id == %s.updated_by_id" % self.__name__,
            remote_side="User.id",
        )


class IndirectSearchableMixin:
    """
    Mixin for chose elements that should only be indirect searchable.

    An example: The device properties that are part of the devices.
    We will only search directly for devices - but the full text
    index should contain up to date information about the device
    properties as well.

    This is what this IndirectSearchableMixin should be used for.
    """

    def get_parent_search_entities(self):
        """
        Return the list of "parent" search entities.

        As an example for a device property I want to
        have the device - as the device property will be
        included in the full text search index entry for the
        device.
        However for contacts, we want to have them included in
        multiple entries (devices, platforms, configurations), so
        we need to handle a list of those entries.

        Please also note: We only have a very small set of
        full searchable entities for the moment (devices, platforms,
        configurations & contacts).
        """
        return []


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
            if isinstance(obj, IndirectSearchableMixin):
                for parent_obj in obj.get_parent_search_entities():
                    if isinstance(parent_obj, SearchableMixin):
                        session._search_add.append(
                            SearchModelWithEntry(
                                model=parent_obj, entry=parent_obj.to_search_entry()
                            )
                        )
        for obj in session._changes["delete"]:
            if isinstance(obj, IndirectSearchableMixin):
                for parent_obj in obj.get_parent_search_entities():
                    if isinstance(parent_obj, SearchableMixin):
                        session._search_add.append(
                            SearchModelWithEntry(
                                model=parent_obj, entry=parent_obj.to_search_entry()
                            )
                        )

    @classmethod
    def after_commit(cls, session):
        """Update the search after the sqlalchemy commit."""
        ids_to_add = collections.defaultdict(set)

        # We are going to collect all the ids for which we need to add or update
        # the search index.
        # Adding & Updating is here the very same command, so we can handle
        # all of them in one run.

        # When we go through all of the changes to add & to update
        # then we can take all the direct searchable entities, as well
        # as all parents of the indirect ones.
        for search_model_with_entry in session._search_add:
            obj = search_model_with_entry.model
            ids_to_add[obj.__tablename__].add(obj.id)
        # For those indirect ones we also want to check the deleted ones
        # So that we know that the parents must be updated as well.
        # However, if the ones that we want to update get deleted themselves
        # it really doesn't make any more sense to update them in the search
        # index. We can ignore them right away.
        for obj in session._changes["delete"]:
            if isinstance(obj, SearchableMixin):
                ids_to_add[obj.__tablename__].discard(obj.id)

        ids_processed = collections.defaultdict(set)
        # So, now we have all of those that we want to update,
        # we can start adding them to the search index.
        for search_model_with_entry in session._search_add:
            model = search_model_with_entry.model
            if model.id in ids_to_add[model.__tablename__]:
                if not model.id in ids_processed[model.__tablename__]:
                    add_to_index(
                        model.__tablename__, model, search_model_with_entry.entry
                    )
                    ids_processed[model.__tablename__].add(model.id)

        # And then, we can delete old entries if necessary.
        for obj in session._changes["delete"]:
            if isinstance(obj, SearchableMixin):
                if obj.id not in ids_processed[obj.__tablename__]:
                    remove_from_index(obj.__tablename__, obj)
                    ids_processed[obj.__tablename__].add(obj.id)

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
