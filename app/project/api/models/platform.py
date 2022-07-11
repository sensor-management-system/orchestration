"""Model for platforms."""

from ..es_utils import ElasticSearchIndexTypes, settings_with_ngrams
from ..models.mixin import (
    ArchivableMixin,
    AuditMixin,
    IndirectSearchableMixin,
    PermissionMixin,
    SearchableMixin,
)
from .base_model import db


class Platform(
    db.Model,
    AuditMixin,
    ArchivableMixin,
    SearchableMixin,
    IndirectSearchableMixin,
    PermissionMixin,
):
    """Platform class."""

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.Text, nullable=True)
    short_name = db.Column(db.String(256), nullable=False)
    long_name = db.Column(db.String(256), nullable=True)
    manufacturer_uri = db.Column(db.String(256), nullable=True)
    manufacturer_name = db.Column(db.String(256), nullable=False)
    model = db.Column(db.String(256), nullable=True)
    platform_type_uri = db.Column(db.String(256), nullable=True)
    platform_type_name = db.Column(db.String(256), nullable=True)
    status_uri = db.Column(db.String(256), nullable=True)
    status_name = db.Column(db.String(256), nullable=True)
    website = db.Column(db.String(1024), nullable=True)
    inventory_number = db.Column(db.String(256), nullable=True)
    serial_number = db.Column(db.String(256), nullable=True)
    persistent_identifier = db.Column(db.String(256), nullable=True, unique=True)
    update_description = db.Column(db.String(256), nullable=True)
    # The type of the identifier depends on the provider being used to register the instrument PID.
    # In the case of ePIC, the value of identifierType would be "Handle".
    identifier_type = db.Column(db.String(256), nullable=True)
    # The value of SchemaVersion is defined to be equal to the version number for each release version of the schema.
    schema_version = db.Column(db.String(256), nullable=True)
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
            "archived": self.archived,
            "website": self.website,
            "inventory_number": self.inventory_number,
            "serial_number": self.serial_number,
            "persistent_identifier": self.persistent_identifier,
            "attachments": [a.to_search_entry() for a in self.platform_attachments],
            "platform_contact_roles": [
                pcr.to_search_entry() for pcr in self.platform_contact_roles
            ],
            "generic_actions": [
                g.to_search_entry() for g in self.generic_platform_actions
            ],
            "software_update_actions": [
                s.to_search_entry() for s in self.platform_software_update_actions
            ],
            "is_internal": self.is_internal,
            "is_public": self.is_public,
            "is_private": self.is_private,
            "created_by_id": self.created_by_id,
            "group_ids": self.group_ids,
        }

    def get_parent_search_entities(self):
        """Get the parents where this here is included in the search index."""
        # This here should only affect configurations - as their search
        # index entry includes the platform.
        result = []
        # We only need to check the platform mount actions for associated
        # configurations - as there should be no unmount before an earlier
        # mount action.
        for action in self.platform_mount_actions:
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
            # Search the description just via text (and not via keyword).
            # We want this to be full searchable, but we don't need to
            # provide any suggestions for.
            "description": type_text_full_searchable,
            # Long & Short name via both text & keyword.
            "long_name": type_keyword_and_full_searchable,
            "short_name": type_keyword_and_full_searchable,
            # Names for Manufacturer, Status & Type searchable via both.
            "manufacturer_name": type_keyword_and_full_searchable,
            # Uris just via keyword (for filtering).
            "manufacturer_uri": type_keyword,
            "model": type_keyword_and_full_searchable,
            "platform_type_name": type_keyword_and_full_searchable,
            "platform_type_uri": type_keyword,
            "status_name": type_keyword_and_full_searchable,
            "status_uri": type_keyword,
            # Website just via text, as we won't search exactly the same website.
            "website": type_text_full_searchable,
            # Inventory, serial number & pid, allow search via both text and keyword.
            "inventory_number": type_keyword_and_full_searchable,
            "serial_number": type_keyword_and_full_searchable,
            "persistent_identifier": type_keyword_and_full_searchable,
            "archived": {
                "type": "boolean",
            },
            "is_internal": {
                "type": "boolean",
            },
            "is_public": {
                "type": "boolean",
            },
            "is_private": {
                "type": "boolean",
            },
            "created_by_id": {
                "type": "integer",
            },
            "group_ids": type_keyword,
            "attachments": {
                "type": "nested",
                "properties": {
                    # Allow search via text & keyword
                    "label": type_keyword_and_full_searchable,
                    # But don't allow search for the very same url (unlikely to be needed).
                    "url": type_text_full_searchable,
                },
            },
            "platform_contact_roles": {
                "type": "nested",
                "properties": {
                    "role_name": type_keyword_and_full_searchable,
                    "role_uri": type_keyword,
                    "contact": {
                        "type": "nested",
                        "properties": Contact.get_search_index_properties(),
                    },
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
                analyzer_name="ngram_analyzer",
                filter_name="ngram_filter",
                min_ngram=3,
                max_ngram=10,
                max_ngram_diff=10,
            ),
        }
