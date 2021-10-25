"""Model for the devices."""


from ..models.mixin import AuditMixin, SearchableMixin, IndirectSearchableMixin
from .base_model import db

from ..es_utils import settings_with_ngrams, ElasticSearchIndexTypes


class Device(db.Model, AuditMixin, SearchableMixin, IndirectSearchableMixin):
    """Device class."""

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.Text, nullable=True)
    short_name = db.Column(db.String(256), nullable=False)
    long_name = db.Column(db.String(256), nullable=True)
    serial_number = db.Column(db.String(256), nullable=True)
    manufacturer_uri = db.Column(db.String(256), nullable=True)
    manufacturer_name = db.Column(db.String(256), nullable=True)
    dual_use = db.Column(db.Boolean, default=False)
    model = db.Column(db.String(256), nullable=True)
    inventory_number = db.Column(db.String(256), nullable=True)
    persistent_identifier = db.Column(db.String(256), nullable=True, unique=True)
    website = db.Column(db.String(1024), nullable=True)
    device_type_uri = db.Column(db.String(256), nullable=True)
    device_type_name = db.Column(db.String(256), nullable=True)
    status_uri = db.Column(db.String(256), nullable=True)
    status_name = db.Column(db.String(256), nullable=True)
    customfields = db.relationship(
        "CustomField", cascade="save-update, merge, delete, delete-orphan"
    )
    device_properties = db.relationship(
        "DeviceProperty", cascade="save-update, merge, delete, delete-orphan"
    )
    events = db.relationship(
        "Event", cascade="save-update, merge, delete, delete-orphan"
    )

    device_attachments = db.relationship(
        "DeviceAttachment", cascade="save-update, merge, delete, delete-orphan"
    )

    def to_search_entry(self):
        """Convert the model to an dict to store in the full text search."""
        return {
            "short_name": self.short_name,
            "long_name": self.long_name,
            "description": self.description,
            "serial_number": self.serial_number,
            "manufacturer_name": self.manufacturer_name,
            "manufacturer_uri": self.manufacturer_uri,
            "dual_use": self.dual_use,
            "model": self.model,
            "inventory_number": self.inventory_number,
            "persistent_identifier": self.persistent_identifier,
            "website": self.website,
            "device_type_name": self.device_type_name,
            "device_type_uri": self.device_type_uri,
            "status_name": self.status_name,
            "status_uri": self.status_uri,
            "attachments": [a.to_search_entry() for a in self.device_attachments],
            "contacts": [c.to_search_entry() for c in self.contacts],
            "properties": [p.to_search_entry() for p in self.device_properties],
            "customfields": [c.to_search_entry() for c in self.customfields],
            "generic_actions": [
                g.to_search_entry() for g in self.generic_device_actions
            ],
            "software_update_actions": [
                s.to_search_entry() for s in self.device_software_update_actions
            ],
        }

    def get_parent_search_entities(self):
        """Get the parents where this here is included in the search index."""
        # This here should only affect configurations - as their search
        # index entry includes the device.
        result = []
        # We only need to check the device mount actions for associated
        # configurations - as there should be no unmount before an earlier
        # mount action.
        for action in self.device_mount_actions:
            result.append(action.configuration)
        return result

    @staticmethod
    def get_search_index_properties():
        """Get the properties for the index configuration."""
        from ..models.contact import Contact

        type_keyword = ElasticSearchIndexTypes.keyword()
        type_text_full_searchable = ElasticSearchIndexTypes.text_full_searchable(
            analyzer="ngram_analyzer"
        )
        type_keyword_and_full_searchable = (
            ElasticSearchIndexTypes.keyword_and_full_searchable(
                analyzer="ngram_analyzer"
            )
        )

        return {
            # We won't check the very equal description, so using text right away is fine.
            "description": type_text_full_searchable,
            # We may filter by long_name (keyword), but we also want to search all of its parts.
            "long_name": type_keyword_and_full_searchable,
            # Same for short_name.
            "short_name": type_keyword_and_full_searchable,
            # Serial number is more likely to be searched as keyword, but text search may be
            # fine here as well.
            "serial_number": type_keyword_and_full_searchable,
            # We may need keyword search, but mostly we will search via text.
            "manufacturer_name": type_keyword_and_full_searchable,
            # Manufacturer uri (as all uris), should be keyword only.
            "manufacturer_uri": type_keyword,
            # dual use is a boolean
            "dual_use": {"type": "boolean"},
            # Model should be both keyword & text.
            "model": type_keyword_and_full_searchable,
            # Inventory number is the same as serial number.
            "inventory_number": type_keyword_and_full_searchable,
            # As we may search for parts of it, we need text,
            # otherwise keyword would be the way to go
            "persistent_identifier": type_keyword_and_full_searchable,
            # We won't search for the very same website.
            "website": type_text_full_searchable,
            # Both search types for the device type name.
            "device_type_name": type_keyword_and_full_searchable,
            # Just keyword search for the device type uri.
            "device_type_uri": type_keyword,
            # Both for the status name.
            "status_name": type_keyword_and_full_searchable,
            # Just keyword for status uri.
            "status_uri": type_keyword,
            "attachments": {
                "type": "nested",
                "properties": {
                    # The label should be searchable via text & via keyword
                    "label": type_keyword_and_full_searchable,
                    # But for the url we will not search by keyword.
                    "url": type_text_full_searchable,
                },
            },
            "contacts": {
                "type": "nested",
                "properties": Contact.get_search_index_properties(),
            },
            "customfields": {
                "type": "nested",
                "properties": {
                    # The key should use keyword behaviour by default
                    # but should also searchable as text.
                    "key": type_keyword_and_full_searchable,
                    # The same for the value.
                    "value": type_keyword_and_full_searchable,
                },
            },
            "properties": {
                "type": "nested",
                "properties": {
                    # All the "normal" text fields searchable via text & keyword.
                    "label": type_keyword_and_full_searchable,
                    "unit_name": type_keyword_and_full_searchable,
                    # And all the uris only via keyword.
                    "unit_uri": type_keyword,
                    "compartment_name": type_keyword_and_full_searchable,
                    "compartment_uri": type_keyword,
                    "property_name": type_keyword_and_full_searchable,
                    "property_uri": type_keyword,
                    "sample_medium_name": type_keyword_and_full_searchable,
                    "sample_medium_uri": type_keyword,
                    "resolution_unit_name": type_keyword_and_full_searchable,
                    "resolution_unit_uri": type_keyword,
                },
            },
            "generic_actions": {
                "type": "nested",
                "properties": {
                    "action_type_uri": type_keyword,
                    "action_type_name": type_keyword_and_full_searchable,
                    "description": type_text_full_searchable,
                },
            },
            "software_update_actions": {
                "type": "nested",
                "properties": {
                    "software_type_name": type_keyword_and_full_searchable,
                    "software_type_uri": type_keyword,
                    "description": type_text_full_searchable,
                    "version": type_keyword_and_full_searchable,
                    "repository_url": type_text_full_searchable,
                },
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
            "settings": settings_with_ngrams(
                analyzer_name='ngram_analyzer',
                filter_name='ngram_filter',
                min_ngram=3,
                max_ngram=10,
                max_ngram_diff=10,
            ),
        }
