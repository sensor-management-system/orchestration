# SPDX-FileCopyrightText: 2020 - 2023
# - Martin Abbrent <martin.abbrent@ufz.de>
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Model for contacts & reference tables."""

from ..es_utils import ElasticSearchIndexTypes, settings_with_ngrams
from ..models.mixin import AuditMixin, IndirectSearchableMixin, SearchableMixin
from .base_model import db

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


class Contact(db.Model, AuditMixin, SearchableMixin, IndirectSearchableMixin):
    """Contact class."""

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    given_name = db.Column(db.String(256), nullable=False)
    family_name = db.Column(db.String(256), nullable=False)
    website = db.Column(db.String(1024), nullable=True)
    email = db.Column(db.String(256), nullable=False, unique=True)
    active = db.Column(db.Boolean, default=True)
    organization = db.Column(db.String(1024), nullable=True)
    orcid = db.Column(db.String(32), nullable=True, unique=True)
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
            "organization": self.organization,
            "orcid": self.orcid,
            "created_by_id": self.created_by_id,
        }

    @staticmethod
    def get_search_index_properties():
        """Get the properties for the index configuration."""
        type_text_full_searchable = ElasticSearchIndexTypes.text_full_searchable(
            analyzer="ngram_analyzer"
        )
        type_keyword_and_full_searchable = (
            ElasticSearchIndexTypes.keyword_and_full_searchable(
                analyzer="ngram_analyzer"
            )
        )
        return {
            "given_name": type_keyword_and_full_searchable,
            "family_name": type_keyword_and_full_searchable,
            # Not necessary to allow exact search for the personal website.
            "website": type_text_full_searchable,
            "organization": type_keyword_and_full_searchable,
            "email": type_keyword_and_full_searchable,
            "orcid": type_keyword_and_full_searchable,
            "created_by_id": {
                "type": "integer",
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

    def get_parent_search_entities(self):
        """Return a list with all the devices, platforms & configurations."""
        # We collect here all the devices, platforms & configurations with that
        # the contact is associated.
        # So that we can update their search index information once we
        # update the contact here (so we have contact information in the
        # search index for a device).
        # We don't refer to the contact roles, as they are part of the index
        # for the device/platform/configuration.
        result = []
        # TODO: Check if this contact_device_roles name stays to refer back
        # to the DeviceContactRole model
        for device_contact_role in self.contact_device_roles:
            device = device_contact_role.device
            result.append(device)
        # TODO: Again check the backref
        for platform_contact_role in self.contact_platform_roles:
            platform = platform_contact_role.platform
            result.append(platform)
        # TODO: Again check the backref
        for configuration_contact_role in self.contact_configuration_roles:
            configuration = configuration_contact_role.configuration
            result.append(configuration)

        return result
