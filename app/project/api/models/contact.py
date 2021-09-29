"""Model for contacts & reference tables."""

import itertools

from .base_model import db
from ..models.mixin import SearchableMixin, IndirectSearchableMixin

platform_contacts = db.Table(
    "platform_contacts",
    db.Column(
        "platform_id", db.Integer, db.ForeignKey("platform.id"), primary_key=True
    ),
    db.Column("contact_id", db.Integer, db.ForeignKey("contact.id"), primary_key=True),
)

device_contacts = db.Table(
    "device_contacts",
    db.Column("device_id", db.Integer, db.ForeignKey("device.id"), primary_key=True),
    db.Column("contact_id", db.Integer, db.ForeignKey("contact.id"), primary_key=True),
)

configuration_contacts = db.Table(
    "configuration_contacts",
    db.Column(
        "configuration_id",
        db.Integer,
        db.ForeignKey("configuration.id"),
        primary_key=True,
    ),
    db.Column("contact_id", db.Integer, db.ForeignKey("contact.id"), primary_key=True),
)


class Contact(db.Model, SearchableMixin, IndirectSearchableMixin):
    """Contact class."""

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    given_name = db.Column(db.String(256), nullable=False)
    family_name = db.Column(db.String(256), nullable=False)
    website = db.Column(db.String(1024), nullable=True)
    email = db.Column(db.String(256), nullable=False, unique=True)
    active = db.Column(db.Boolean, default=True)
    devices = db.relationship(
        "Device",
        secondary=device_contacts,
        lazy="subquery",
        backref=db.backref("contacts", lazy=True),
    )
    platforms = db.relationship(
        "Platform",
        secondary=platform_contacts,
        lazy="subquery",
        backref=db.backref("contacts", lazy=True),
    )
    configurations = db.relationship(
        "Configuration",
        secondary=configuration_contacts,
        lazy="subquery",
        backref=db.backref("contacts", lazy=True),
    )

    def to_search_entry(self):
        """Transform the model to an entry to store in the full text search."""
        # to be included in platforms, devices, etc.
        return {
            "given_name": self.given_name,
            "family_name": self.family_name,
            "website": self.website,
            "email": self.email,
        }

    @staticmethod
    def get_search_index_properties():
        """Get the properties for the index configuration."""
        return {
            "given_name": {
                "type": "keyword",
                "fields": {"text": {"type": "text"}},
            },
            "family_name": {
                "type": "keyword",
                "fields": {"text": {"type": "text"}},
            },
            # Not necessary to allow exact search for the personal website.
            "website": {"type": "text"},
            "email": {
                "type": "keyword",
                "fields": {"text": {"type": "text"}},
            },
        }

    @classmethod
    def get_search_index_definition(cls):
        """
        Return the index configuration for the elasticsearch.

        Describes which fields will be searchable by some text (with stemmer, etc)
        and via keyword (raw equality checks).
        """
        return {
            "aliases": {},
            "mappings": {"properties": cls.get_search_index_properties()},
            "settings": {"index": {"number_of_shards": "1"}},
        }

    def get_parent_search_entities(self):
        """Return a list with all the devices, platforms & configurations."""
        return list(itertools.chain(self.devices, self.platforms, self.configurations))
