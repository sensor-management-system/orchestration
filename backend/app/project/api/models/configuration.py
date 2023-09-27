# SPDX-FileCopyrightText: 2020 - 2023
# - Martin Abbrent <martin.abbrent@ufz.de>
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

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
    project = db.Column(db.String(256), nullable=True)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(256), nullable=True, default="draft")
    cfg_permission_group = db.Column(db.String, nullable=True)
    is_internal = db.Column(db.Boolean, default=False)
    is_public = db.Column(db.Boolean, default=False)
    update_description = db.Column(db.String(256), nullable=True)
    b2inst_record_id = db.Column(db.String(256), nullable=True)
    persistent_identifier = db.Column(db.String(256), nullable=True, unique=True)
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
        return {
            "label": self.label,
            "description": self.description,
            "project": self.project,
            "status": self.status,
            "cfg_permission_group": self.cfg_permission_group,
            "updated_at": self.updated_at,
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
            "configuration_customfields": [
                a.to_search_entry() for a in self.configuration_customfields
            ],
            "configuration_parameters": [
                p.to_search_entry() for p in self.configuration_parameters
            ],
            "archived": self.archived,
            "is_internal": self.is_internal,
            "is_public": self.is_public,
            "created_by_id": self.created_by_id,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "site_id": self.site_id,
            "persistent_identifier": self.persistent_identifier,
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
                    "project": type_keyword_and_full_searchable,
                    "description": type_text_full_searchable,
                    "status": type_keyword_and_full_searchable,
                    "cfg_permission_group": type_keyword,
                    "start_date": {"type": "date"},
                    "end_date": {"type": "date"},
                    "updated_at": {
                        "type": "date",
                        "format": "strict_date_optional_time",
                    },
                    "platforms": {
                        "properties": Platform.get_search_index_properties(),
                    },
                    "devices": {
                        "properties": Device.get_search_index_properties(),
                    },
                    "configuration_contact_roles": {
                        "properties": {
                            "role_name": type_keyword_and_full_searchable,
                            "role_uri": type_keyword,
                            "contact": {
                                "properties": Contact.get_search_index_properties(),
                            },
                        },
                    },
                    "attachments": {
                        "properties": {
                            # Allow search via text & keyword
                            "label": type_keyword_and_full_searchable,
                            # But don't allow search for the very same url (unlikely to be needed).
                            "url": type_text_full_searchable,
                        },
                    },
                    "configuration_parameters": {
                        "properties": {
                            "label": type_keyword_and_full_searchable,
                            "description": type_keyword_and_full_searchable,
                            "unit_uri": type_keyword,
                            "unit_name": type_keyword_and_full_searchable,
                            "configuration_parameter_value_change_actions": {
                                "properties": {
                                    "value": type_keyword_and_full_searchable,
                                    "description": type_keyword_and_full_searchable,
                                },
                            },
                        },
                    },
                    "generic_actions": {
                        "properties": {
                            "action_type_uri": type_keyword,
                            "action_type_name": type_keyword_and_full_searchable,
                            "description": type_text_full_searchable,
                        },
                    },
                    "configuration_static_location_actions": {
                        "properties": {
                            "begin_description": type_text_full_searchable,
                            "end_description": type_text_full_searchable,
                            "label": type_keyword_and_full_searchable,
                        },
                    },
                    "configuration_dynamic_location_actions": {
                        "properties": {
                            "begin_description": type_text_full_searchable,
                            "end_description": type_text_full_searchable,
                            "label": type_keyword_and_full_searchable,
                        },
                    },
                    "platform_mount_actions": {
                        "properties": {
                            "begin_description": type_text_full_searchable,
                            "end_description": type_text_full_searchable,
                            "platform": {
                                "properties": Platform.get_search_index_properties(),
                            },
                        },
                    },
                    "device_mount_actions": {
                        "properties": {
                            "begin_description": type_text_full_searchable,
                            "end_description": type_text_full_searchable,
                            "device": {
                                "properties": Device.get_search_index_properties(),
                            },
                        },
                    },
                    "customfields": {
                        "properties": {
                            # The key should use keyword behaviour by default
                            # but should also searchable as text.
                            "key": type_keyword_and_full_searchable,
                            # The same for the value.
                            "value": type_keyword_and_full_searchable,
                        },
                    },
                    "site_id": {
                        "type": "integer",
                    },
                    "persistent_identifier": type_keyword_and_full_searchable,
                }
            },
            "settings": settings_with_ngrams(
                analyzer_name="ngram_analyzer",
                filter_name="ngram_filter",
                min_ngram=1,
                max_ngram=10,
                max_ngram_diff=10,
            ),
        }
