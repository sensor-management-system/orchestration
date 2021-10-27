"""Class and helpers for the configurations."""

import collections

from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import validates

from .base_model import db
from .mixin import AuditMixin, SearchableMixin
from ..helpers.errors import ConflictError

from ..es_utils import settings_with_ngrams, ElasticSearchIndexTypes

ConfigurationsTuple = collections.namedtuple(
    "ConfigurationsTuple", ["configuration_devices", "configuration_platforms"]
)


class Configuration(db.Model, AuditMixin, SearchableMixin):
    """Data model for the configurations."""

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    start_date = db.Column(db.DateTime, nullable=True)
    end_date = db.Column(db.DateTime, nullable=True)
    location_type = db.Column(db.String(256), nullable=True)
    longitude = db.Column(db.Float(), nullable=True)
    latitude = db.Column(db.Float(), nullable=True)
    elevation = db.Column(db.Float(), nullable=True)
    project_uri = db.Column(db.String(256), nullable=True)
    project_name = db.Column(db.String(256), nullable=True)
    label = db.Column(db.String(256), nullable=True)
    status = db.Column(db.String(256), nullable=True, default="draft")

    longitude_src_device_property_id = db.Column(
        db.Integer, db.ForeignKey("device_property.id"), nullable=True
    )
    src_longitude = db.relationship(
        "DeviceProperty", uselist=False, foreign_keys=[longitude_src_device_property_id]
    )

    latitude_src_device_property_id = db.Column(
        db.Integer, db.ForeignKey("device_property.id"), nullable=True
    )
    src_latitude = db.relationship(
        "DeviceProperty", uselist=False, foreign_keys=[latitude_src_device_property_id]
    )

    elevation_src_device_property_id = db.Column(
        db.Integer, db.ForeignKey("device_property.id"), nullable=True
    )
    src_elevation = db.relationship(
        "DeviceProperty", uselist=False, foreign_keys=[elevation_src_device_property_id]
    )
    configuration_attachments = db.relationship(
        "ConfigurationAttachment", cascade="save-update, merge, delete, delete-orphan"
    )
    groups_ids = db.Column(MutableList.as_mutable(db.ARRAY(db.Integer)), nullable=True)
    is_internal = db.Column(db.Boolean, default=False)
    is_public = db.Column(db.Boolean, default=False)

    @validates("is_internal")
    def validate_internal(self, key, is_internal):
        if is_internal and bool(self.is_public):
            raise ConflictError(
                "Please make sure that this object is not public at first."
            )
        return is_internal

    @validates("is_public")
    def validate_public(self, key, is_public):

        if is_public and bool(self.is_internal):
            raise ConflictError(
                "Please make sure that this object is not internal at first."
            )
        return is_public

    @hybrid_property
    def hierarchy(self):
        """
        Return a tuple with that the hierarchy can be build.

        The tuple contains the data with the links to the used
        devices and platforms. It also includes how the
        devices and platforms are used in the configuration (offsets,
        calibration dates) and how the hiearchy is structured (
        on which device is a platform, and what are those parent
        platforms).

        With the data here a real tree can be build.
        """
        return ConfigurationsTuple(
            configuration_devices=self.configuration_devices,
            configuration_platforms=self.configuration_platforms,
        )

    @hierarchy.setter
    def hierarchy(self, value):
        new_configuration_devices = value.configuration_devices
        new_configuration_platforms = value.configuration_platforms

        current_configuration_device_by_device_id = {}

        for device_configuration in self.configuration_devices:
            current_configuration_device_by_device_id[
                device_configuration.device_id
            ] = device_configuration

        current_configuration_platform_by_platform_id = {}

        for platform_configuration in self.configuration_platforms:
            current_configuration_platform_by_platform_id[
                platform_configuration.platform_id
            ] = platform_configuration

        for new_cd in new_configuration_devices:
            device_id = new_cd.device_id
            old_configuration_device = current_configuration_device_by_device_id.get(
                device_id, None
            )
            if old_configuration_device is not None:
                new_cd.id = old_configuration_device.id
                new_cd.created_at = old_configuration_device.created_at
                new_cd.created_by = old_configuration_device.created_by
            new_cd.configuration = self

        for new_cp in new_configuration_platforms:
            platform_id = new_cp.platform_id
            old_configuration_platform = (
                current_configuration_platform_by_platform_id.get(platform_id, None)
            )
            if old_configuration_platform is not None:
                new_cp.id = old_configuration_platform.id
                new_cp.created_at = old_configuration_platform.created_at
                new_cp.created_by = old_configuration_platform.created_by
            new_cp.configuration = self

        self.configuration_devices = new_configuration_devices
        self.configuration_platforms = new_configuration_platforms

    def to_search_entry(self):
        """
        Return the configuration as dict for full text search.

        All the fields here will be searchable and can be used as
        filters in our full text search.
        """
        platforms = []
        for configuration_platform in self.configuration_platforms:
            if configuration_platform.platform is not None:
                platforms.append(configuration_platform.platform)
        devices = []
        firmware_versions = []
        for configuration_device in self.configuration_devices:
            if configuration_device.device is not None:
                devices.append(configuration_device.device)
            if configuration_device.firmware_version is not None:
                firmware_versions.append(configuration_device.firmware_version)

        # TODO: With the change for the mount & unmount Actions
        # this here must be improved.
        # Also we need to update the configurations in case that
        # we have a change in the platform or device

        return {
            "label": self.label,
            "status": self.status,
            "location_type": self.location_type,
            "project_uri": self.project_uri,
            "project_name": self.project_name,
            "platforms": [p.to_search_entry() for p in platforms],
            "devices": [d.to_search_entry() for d in devices],
            "contacts": [c.to_search_entry() for c in self.contacts],
            "firmware_versions": firmware_versions,
            "attachments": [
                a.to_search_entry() for a in self.configuration_attachments
            ],
            "generic_actions": [
                g.to_search_entry() for g in self.generic_configuration_actions
            ],
            "static_location_begin_actions": [
                s.to_search_entry()
                for s in self.configuration_static_location_begin_actions
            ],
            "static_location_end_actions": [
                s.to_search_entry()
                for s in self.configuration_static_location_end_actions
            ],
            "dynamic_location_begin_actions": [
                d.to_search_entry()
                for d in self.configuration_dynamic_location_begin_actions
            ],
            "dynamic_location_end_actions": [
                d.to_search_entry()
                for d in self.configuration_dynamic_location_end_actions
            ],
            "platform_mount_actions": [
                p.to_search_entry() for p in self.platform_mount_actions
            ],
            "device_mount_actions": [
                d.to_search_entry() for d in self.device_mount_actions
            ],
            "platform_unmount_actions": [
                p.to_search_entry() for p in self.platform_unmount_actions
            ],
            "device_unmount_actions": [
                d.to_search_entry() for d in self.device_unmount_actions
            ],
            "is_internal": self.is_internal,
            "is_public": self.is_public,
            "created_by_id": self.created_by_id,
            # start & end dates?
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
                    "created_by_id": {
                        "type": "integer",
                    },
                    "label": type_keyword_and_full_searchable,
                    "status": type_keyword_and_full_searchable,
                    "location_type": type_keyword_and_full_searchable,
                    "project_name": type_keyword_and_full_searchable,
                    # The uri just for an keyword filter.
                    "project_uri": type_keyword,
                    "platforms": {
                        "type": "nested",
                        "properties": Platform.get_search_index_properties(),
                    },
                    "devices": {
                        "type": "nested",
                        "properties": Device.get_search_index_properties(),
                    },
                    "contacts": {
                        "type": "nested",
                        "properties": Contact.get_search_index_properties(),
                    },
                    "firmware_versions": type_keyword_and_full_searchable,
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
                    "static_location_begin_actions": {
                        "type": "nested",
                        "properties": {
                            "description": type_text_full_searchable,
                        },
                    },
                    "static_location_end_actions": {
                        "type": "nested",
                        "properties": {
                            "description": type_text_full_searchable,
                        },
                    },
                    "dynamic_location_begin_actions": {
                        "type": "nested",
                        "properties": {
                            "description": type_text_full_searchable,
                        },
                    },
                    "dynamic_location_end_actions": {
                        "type": "nested",
                        "properties": {
                            "description": type_text_full_searchable,
                        },
                    },
                    "platform_mount_actions": {
                        "type": "nested",
                        "properties": {
                            "description": type_text_full_searchable,
                            "platform": {
                                "type": "nested",
                                "properties": Platform.get_search_index_properties(),
                            },
                        },
                    },
                    "device_mount_actions": {
                        "type": "nested",
                        "properties": {
                            "description": type_text_full_searchable,
                            "device": {
                                "type": "nested",
                                "properties": Device.get_search_index_properties(),
                            },
                        },
                    },
                    "platform_unmount_actions": {
                        "type": "nested",
                        "properties": {"description": type_text_full_searchable},
                    },
                    "device_unmount_actions": {
                        "type": "nested",
                        "properties": {"description": type_text_full_searchable},
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
