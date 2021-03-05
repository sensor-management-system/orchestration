"""Model for platforms."""

from safrs import SAFRSBase

from project.api.models.base_model import db
from project.api.models.mixin import AuditMixin, SearchableMixin


class Platform(db.Model, AuditMixin, SearchableMixin, SAFRSBase):
    """Platform class."""

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.Text, nullable=True)
    short_name = db.Column(db.String(256), nullable=False)
    long_name = db.Column(db.String(256), nullable=True)
    manufacturer_uri = db.Column(db.String(256), nullable=True)
    manufacturer_name = db.Column(db.String(256), nullable=True)
    model = db.Column(db.String(256), nullable=True)
    platform_type_uri = db.Column(db.String(256), nullable=True)
    platform_type_name = db.Column(db.String(256), nullable=True)
    status_uri = db.Column(db.String(256), nullable=True)
    status_name = db.Column(db.String(256), nullable=True)
    website = db.Column(db.String(1024), nullable=True)
    inventory_number = db.Column(db.String(256), nullable=True)
    serial_number = db.Column(db.String(256), nullable=True)
    persistent_identifier = db.Column(db.String(256), nullable=True, unique=True)
    platform_attachments = db.relationship(
        "PlatformAttachment", cascade="save-update, merge, delete, delete-orphan"
    )

    def to_search_entry(self):
        """Convert the model to a dict to store it in a full text search."""
        return {
            "short_name": self.short_name,
            "long_name": self.long_name,
            "description": self.description,
            "manufacturer_name": self.manufacturer_name,
            "manufacturer_uri": self.manufacturer_uri,
            "model": self.model,
            "platform_type_name": self.platform_type_name,
            "status_name": self.status_name,
            "website": self.website,
            "inventory_number": self.inventory_number,
            "serial_number": self.serial_number,
            "persistent_identifier": self.persistent_identifier,
            "attachments": [a.to_search_entry() for a in self.platform_attachments],
            "contacts": [c.to_search_entry() for c in self.contacts],
        }

    @staticmethod
    def get_search_index_properties():
        """Get the properties for the index configuration."""
        from project.api.models.contact import Contact

        return {
            # Search the description just via text (and not via keyword).
            "description": {"type": "text"},
            # Long & Short name via both text & keyword.
            "long_name": {"type": "keyword", "fields": {"text": {"type": "text"}}},
            "short_name": {"type": "keyword", "fields": {"text": {"type": "text"}}},
            # Names for Manufacturer, Status & Type searchable via both.
            "manufacturer_name": {
                "type": "keyword",
                "fields": {"text": {"type": "text"}},
            },
            # Uris just via keyword (for filtering).
            "manufacturer_uri": {"type": "keyword"},
            "model": {"type": "keyword", "fields": {"text": {"type": "text"}}},
            "platform_type_name": {
                "type": "keyword",
                "fields": {"text": {"type": "text"}},
            },
            "platform_type_uri": {"type": "keyword"},
            "status_name": {
                "type": "keyword",
                "fields": {"text": {"type": "text"}},
            },
            "status_uri": {"type": "keyword"},
            # Website just via text, as we won't search exactly the same website.
            "website": {"type": "text"},
            # Inventory, serrial number & pid, allow search via both text and keyword.
            "inventory_number": {
                "type": "keyword",
                "fields": {"text": {"type": "text"}},
            },
            "serial_number": {
                "type": "keyword",
                "fields": {"text": {"type": "text"}},
            },
            "persistent_identifier": {
                "type": "keyword",
                "fields": {"text": {"type": "text"}},
            },
            "attachments": {
                "type": "nested",
                "properties": {
                    # Allow search via text & keyword
                    "label": {
                        "type": "keyword",
                        "fields": {"text": {"type": "text"}},
                    },
                    # But don't allow search for the very same url (unlikely to be needed).
                    "url": {"type": "text"},
                },
            },
            "contacts": {
                "type": "nested",
                "properties": Contact.get_search_index_properties(),
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
