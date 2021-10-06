import collections
import itertools
from datetime import datetime

import sqlalchemy
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import validates

from .base_model import db
from ..helpers.errors import ConflictError
from ..search import (
    add_to_index,
    create_index,
    query_index,
    remove_from_index,
    remove_index,
)


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
    """
    Mixin to make a model searchable via full text search.

    The whole lgoic here may be a little complex, so lets explain.

    We want to create entries in a full text search index (elasticsearch)
    to be ahle to search for eny of the texts associated with our
    data set.

    We currently search explicitly for only some of our entities.
    This are - at the time of wriging - contacts, configurations,
    platforms and devices.

    For the contacts it is relativly easy:
    - We only want the name (given & family name), as well as
      the email address.
    - We don't want to search contacts by filtering for which devices
      they are resposible. So we don't need more included data.

    For the devices it is way more complex:
    - We want all of the attributes of a device itself to be searchable
      (short name, long name, serial numbers, descriptions, manufacturer, ...).
    - We also want to search for customfields (key-value pairs) as we
      may want to add another kind of identifier there.
    - For this additional fields we want to include them in the search index
      entry for the device. However as they are seperate entities that
      are also added, updated or removed seperatly from the device itself,
      we need to update our device entry for every change on the customfields.
    - We tag those customfields with IndirectSearchableMixin to know, that
      we have assoicated (parent) entities that must be updated on a change.
    - This effects also the device properties, device attachments and the
      device specific actions.
    - One thing we are not itnerested here are the device mount & unmount
      actiosn. Those are specific for the configuration and should only be
      included there.
    - But one other thing that we want to incluide are the contacts of a device.
      This way we would be able to search for a persons name and find the
      the associated devices (in case we don't remember the exact name of the
      device, but we know who is resposible).
      This will make us to update the device entry as well if we update a
      contact (contact is both direct & indirect searchable).
    - We don't need to include attachments a second time for the actions, they
      are already included in the attachments themselves (and adding them
      a second time will change the word statistics in the search index without
      giving more information.)
    - So all in all we will end with a data dict similar to this:
      {
        short_name: "abc",
        long_name": "Aaa Bbb Ccc",
        description: "Useful device",
        contacts: [
          {
            given_name: "max",
            family_name: "mustermann",
            // ...
          },
          // ...
        ],
        "properties": [
          {
            label: "property 1",
            // ...
          },
          // ...
        ],
        // attachments, generic_device_actions, device_software_update_actions, ..
      }
    - So we included all the information about the device in one dict/object.
      And with this view the term "parent" makes most sense. The parent
      of the customfield entry is the overall device data dict ifself.
    - Contacts can have more then one parent. They should be included
      in the devices, in the platforms and in the configurations.

    For the platforms this is very similar to the devices. THe omly difference
    is that there are fewer fields (no properties for example.)

    The basic sitation for the configruations is similar as well:
    - We have the main attributes (label, project).
    - We have associated attachments, generic actions and location actions.
    - The situation for mount & unmount actions is a bit more interesting.
      Basically we not only want to have the description of those actions
      included but also the associated platforms & devices. (And we want
      those texts in the search index to be update once a device or a
      platform is changed. As we only have the configurations then that
      are effected it is do-able, but it really starts to be complex...
      Sorry for that!).
    - However, with a change of the devices & platforms we must update
      the configuration again.

    So the SearchableMixin and IndirectSearchableMixin are a way to
    represent the information about all of this relationships - and
    to run the necessary synchronization work.
    """

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
            for searchable in cls.yield_searchables(obj):
                session._search_add.append(
                    SearchModelWithEntry(
                        model=searchable, entry=searchable.to_search_entry()
                    )
                )
        for obj in session._changes["delete"]:
            # We really don't want the direct searchables that are deleted
            # but we want every associated one
            # We really want to skip this level here and start with the
            # IndirectSearchables
            if isinstance(obj, IndirectSearchableMixin):
                for parent_obj in obj.get_parent_search_entities():
                    for searchable in cls.yield_searchables(parent_obj):
                        session._search_add.append(
                            SearchModelWithEntry(
                                model=searchable, entry=searchable.to_search_entry()
                            )
                        )

    @classmethod
    def yield_searchables(cls, obj):
        """Yield all searchables (direct & indirect over multiple levels)."""
        # Please note: Currently the SearchableMixin and IndirectSearchableMixin
        # classes doesn't give us an endless recursion here (we dont't have
        # circular dependencies). However this setting is fragile, so
        # be careful and add a set to check ids of already yielded entities
        # if ncessary.
        if isinstance(obj, SearchableMixin):
            yield obj
        if isinstance(obj, IndirectSearchableMixin):
            for parent in obj.get_parent_search_entities():
                yield from cls.yield_searchables(parent)

    @classmethod
    def after_commit(cls, session):
        """Update the search after the sqlalchemy commit."""
        ids_to_add = collections.defaultdict(set)

        # We are going to collect all the ids for which we need to add or update
        # the search index.
        # Adding & Updating is here the very same command, so we can handle
        # all of them in one run.
        for search_model_with_entry in session._search_add:
            obj = search_model_with_entry.model
            ids_to_add[obj.__tablename__].add(obj.id)
        # Because of the indirect searchable we can have the job
        # to update their parent entries, it can still be the case that
        # we want to delete the parent object. If so, it doesn't make any
        # sense to try to update the search index for those - we will just
        # delete them and are fine.
        for obj in session._changes["delete"]:
            if isinstance(obj, SearchableMixin):
                ids_to_add[obj.__tablename__].discard(obj.id)

        ids_processed = collections.defaultdict(set)
        # So, now we have all of those that we want to update,
        # we can start adding them to the search index.
        for search_model_with_entry in session._search_add:
            model = search_model_with_entry.model
            if model.id in ids_to_add[model.__tablename__]:
                if model.id not in ids_processed[model.__tablename__]:
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


class PermissionMixin:
    __abstract__ = True
    groups_ids = db.Column(MutableList.as_mutable(db.ARRAY(db.Integer)), nullable=True)
    is_private = db.Column(db.Boolean, default=False)
    is_internal = db.Column(db.Boolean, default=True)
    is_public = db.Column(db.Boolean, default=False)

    @validates('is_private')
    def validate_private(self, key, is_private):
        if (is_private and self.is_public) | (is_private and self.is_internal):
            raise ConflictError("failed permission validation")
        return is_private

    @validates('is_internal')
    def validate_internal(self, key, is_internal):
        if (is_internal and self.is_public) | (is_internal and self.is_private):
            raise ConflictError("failed permission validation")
        return is_internal

    @validates('is_public')
    def validate_public(self, key, is_public):
        if (is_public and self.is_private) | (is_public and self.is_internal):
            raise ConflictError("failed permission validation")
        return is_public
