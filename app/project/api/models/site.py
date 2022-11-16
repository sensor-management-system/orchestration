"""Site model."""
from geoalchemy2 import Geometry
from sqlalchemy.ext.mutable import MutableList

from ..es_utils import ElasticSearchIndexTypes, settings_with_ngrams
from ..helpers.errors import ConflictError
from ..helpers.geometry import geometry_to_wkt
from ..models.mixin import (
    ArchivableMixin,
    AuditMixin,
    BeforeCommitValidatableMixin,
    SearchableMixin,
)
from .base_model import db


class Site(
    db.Model, AuditMixin, ArchivableMixin, BeforeCommitValidatableMixin, SearchableMixin
):
    """Model class for sites (areas of interest)."""

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    label = db.Column(db.String(256), nullable=True)
    geometry = db.Column(Geometry("POLYGON"), nullable=True)
    description = db.Column(db.Text, nullable=True)
    epsg_code = db.Column(db.String(256), default="4326")
    is_internal = db.Column(db.Boolean, default=False)
    is_public = db.Column(db.Boolean, default=False)
    group_ids = db.Column(MutableList.as_mutable(db.ARRAY(db.String)), nullable=True)
    # And for the address
    street = db.Column(db.String(256), nullable=True)
    street_number = db.Column(db.String(256), nullable=True)
    city = db.Column(db.String(256), nullable=True)
    zip_code = db.Column(db.String(256), nullable=True)
    country = db.Column(db.String(256), nullable=True)
    building = db.Column(db.String(256), nullable=True)
    room = db.Column(db.String(256), nullable=True)
    update_description = db.Column(db.String(256), nullable=True)
    # SiteContactRoles have a backref to the sites, so there is no need
    # to put it here explicitly.
    # Configurations also have the backrefs.

    def validate(self):
        """
        Validate the model.

        Check that we don't have multiple visibility values.
        """
        super().validate()
        if self.is_internal and self.is_public:
            raise ConflictError("The site can't be both internal and public")
        if not any([self.is_internal, self.is_public]):
            raise ConflictError("There must be a visibility set for the site.")

    def to_search_entry(self):
        """
        Return the configuration as dict for full text search.

        All the fields here will be searchable and can be used as
        filters in our full text search.
        """
        return {
            "label": self.label,
            # https://www.elastic.co/guide/en/elasticsearch/reference/current/geo-shape.html#geo-polygon
            "geometry": geometry_to_wkt(self.geometry),
            "description": self.description,
            "epsg_code": self.epsg_code,
            "is_internal": self.is_internal,
            "is_public": self.is_public,
            "created_by_id": self.created_by_id,
            "group_ids": self.group_ids,
            "archived": self.archived,
            "street": self.street,
            "street_number": self.street_number,
            "city": self.city,
            "zip_code": self.zip_code,
            "country": self.country,
            "building": self.building,
            "room": self.room,
            "site_contact_roles": [
                scr.to_search_entry() for scr in self.site_contact_roles
            ],
            # For the moment we don't include the configurations as it would
            # require us to keep all the data up to date (not only for
            # every change in the configuration, but also for changes in
            # mounts, locations, maybe even in devices, etc.)
        }

    @staticmethod
    def get_search_index_definition():
        """
        Return the index configuration for the elasticsearch.

        Describes which fields will be searchable by some text (with stemmer, etc)
        and via keyword (raw equality checks).
        """
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
            "aliases": {},
            "mappings": {
                "properties": {
                    "label": type_keyword_and_full_searchable,
                    # https://www.elastic.co/guide/en/elasticsearch/reference/current/geo-shape.html#geo-polygon
                    "geometry": {"type": "geo_shape"},
                    "description": type_text_full_searchable,
                    "epsg_code": type_keyword,
                    "is_internal": {
                        "type": "boolean",
                    },
                    "is_public": {
                        "type": "boolean",
                    },
                    "created_by_id": {
                        "type": "integer",
                    },
                    "group_ids": type_keyword,
                    "archived": {
                        "type": "boolean",
                    },
                    "street": type_keyword_and_full_searchable,
                    "street_number": type_keyword_and_full_searchable,
                    "city": type_keyword_and_full_searchable,
                    "zip_code": type_keyword_and_full_searchable,
                    "country": type_keyword_and_full_searchable,
                    "building": type_keyword_and_full_searchable,
                    "room": type_keyword_and_full_searchable,
                    "site_contact_roles": {
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
                    # As mentioned we don't include the data for the
                    # configurations here.
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
