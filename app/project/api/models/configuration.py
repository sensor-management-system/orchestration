"""Class and helpers for the configurations."""

from ..es_utils import ElasticSearchIndexTypes, settings_with_ngrams
from ..helpers.errors import ConflictError
from .base_model import db
from .mixin import (
    ArchivableMixin,
    AuditMixin,
    BeforeCommitValidatableMixin,
    SearchableMixin,
)


class Configuration(
    db.Model, AuditMixin, ArchivableMixin, SearchableMixin, BeforeCommitValidatableMixin
):
    """Data model for the configurations."""

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    start_date = db.Column(db.DateTime(timezone=True), nullable=True)
    end_date = db.Column(db.DateTime(timezone=True), nullable=True)
    label = db.Column(db.String(256), nullable=True)
    status = db.Column(db.String(256), nullable=True, default="draft")
    cfg_permission_group = db.Column(db.String, nullable=True)
    is_internal = db.Column(db.Boolean, default=False)
    is_public = db.Column(db.Boolean, default=False)
    update_description = db.Column(db.String(256), nullable=True)
    configuration_attachments = db.relationship(
        "ConfigurationAttachment", cascade="save-update, merge, delete, delete-orphan"
    )
    site_id = db.Column(db.Integer, db.ForeignKey("site.id"), nullable=True)
    site = db.relationship("Site", backref="configurations")

    def validate(self):
        """
        Validate the model.

        Check that we don't have multiple visibility values.
        """
        super().validate()
        if self.is_internal and self.is_public:
            raise ConflictError("The configuration can't be both internal and public")

    def to_search_entry(self):
        """
        Return the configuration as dict for full text search.

        All the fields here will be searchable and can be used as
        filters in our full text search.
        """
        # TODO: With the change for the mount & unmount Actions
        # this here must be improved.
        # Also we need to update the configurations in case that
        # we have a change in the platform or device

        return {
            "label": self.label,
            "status": self.status,
            "cfg_permission_group": self.cfg_permission_group,
            "configuration_contact_roles": [
                ccr.to_search_entry() for ccr in self.configuration_contact_roles
            ],
            "attachments": [
                a.to_search_entry() for a in self.configuration_attachments
            ],
            "generic_actions": [
                g.to_search_entry() for g in self.generic_configuration_actions
            ],
            "configuration_static_location_actions": [
                s.to_search_entry()
                for s in self.configuration_static_location_begin_actions
            ],
            "configuration_dynamic_location_actions": [
                d.to_search_entry()
                for d in self.configuration_dynamic_location_begin_actions
            ],
            "platform_mount_actions": [
                p.to_search_entry() for p in self.platform_mount_actions
            ],
            "device_mount_actions": [
                d.to_search_entry() for d in self.device_mount_actions
            ],
            "archived": self.archived,
            "is_internal": self.is_internal,
            "is_public": self.is_public,
            "created_by_id": self.created_by_id,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "site_id": self.site_id,
        }

    @staticmethod
    def get_search_index_definition():
        """
        Return the index configuration for the elasticsearch.

        Describes which fields will be searchable by some text (with stemmer, etc)
        and via keyword (raw equality checks).
        """
        from ..models.contact import Contact
        from ..models.device import Device
        from ..models.platform import Platform

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
            "aliases": {},
            "mappings": {
                "properties": {
                    "is_internal": {
                        "type": "boolean",
                    },
                    "is_public": {
                        "type": "boolean",
                    },
                    "archived": {
                        "type": "boolean",
                    },
                    "created_by_id": {
                        "type": "integer",
                    },
                    "label": type_keyword_and_full_searchable,
                    "status": type_keyword_and_full_searchable,
                    "cfg_permission_group": type_keyword,
                    "start_date": {"type": "date"},
                    "end_date": {"type": "date"},
                    "platforms": {
                        "type": "nested",
                        "properties": Platform.get_search_index_properties(),
                    },
                    "devices": {
                        "type": "nested",
                        "properties": Device.get_search_index_properties(),
                    },
                    "configuration_contact_roles": {
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
                    "attachments": {
                        "type": "nested",
                        "properties": {
                            # Allow search via text & keyword
                            "label": type_keyword_and_full_searchable,
                            # But don't allow search for the very same url (unlikely to be needed).
                            "url": type_text_full_searchable,
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
                    "configuration_static_location_actions": {
                        "type": "nested",
                        "properties": {
                            "description": type_text_full_searchable,
                        },
                    },
                    "configuration_dynamic_location_actions": {
                        "type": "nested",
                        "properties": {
                            "description": type_text_full_searchable,
                        },
                    },
                    "platform_mount_actions": {
                        "type": "nested",
                        "properties": {
                            "begin_description": type_text_full_searchable,
                            "end_description": type_text_full_searchable,
                            "platform": {
                                "type": "nested",
                                "properties": Platform.get_search_index_properties(),
                            },
                        },
                    },
                    "device_mount_actions": {
                        "type": "nested",
                        "properties": {
                            "begin_description": type_text_full_searchable,
                            "end_description": type_text_full_searchable,
                            "device": {
                                "type": "nested",
                                "properties": Device.get_search_index_properties(),
                            },
                        },
                    },
                    "site_id": {
                        "type": "integer",
                    },
                }
            },
            "settings": settings_with_ngrams(
                analyzer_name="ngram_analyzer",
                filter_name="ngram_filter",
                min_ngram=3,
                max_ngram=10,
                max_ngram_diff=10,
            ),
        }
