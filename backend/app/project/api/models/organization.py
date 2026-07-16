# SPDX-FileCopyrightText: 2026
# - Nils Brinckmann <nils.brinckmann@gfz.de>
# - GFZ - Helmholtz Centre for Geosciences (GFZ, https://www.gfz.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Model for organizations."""

from ..es_utils import ElasticSearchIndexTypes, settings_with_ngrams
from .base_model import db
from .mixin import SearchableMixin


class Organization(db.Model, SearchableMixin):
    """Model class for organizations."""

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(256), nullable=False)
    ror = db.Column(db.String(256), nullable=True)
    abbreviation = db.Column(db.String(8), nullable=True)

    def to_search_entry(self):
        """Return a dict structure to put into the search index."""
        return {
            "name": self.name,
            "ror": self.ror,
            "abbreviation": self.abbreviation,
        }

    @staticmethod
    def get_search_index_properties():
        """Set the types for the fields in the search index."""
        type_keyword_and_full_searchable = (
            ElasticSearchIndexTypes.keyword_and_full_searchable(
                analyzer="ngram_analyzer"
            )
        )
        return {
            "name": type_keyword_and_full_searchable,
            "ror": type_keyword_and_full_searchable,
            "abbreviation": type_keyword_and_full_searchable,
        }

    @classmethod
    def get_search_index_definition(cls):
        """Create the settings for the search index."""
        return {
            "aliases": {},
            "mappings": {
                "properties": cls.get_search_index_properties(),
            },
            "settings": settings_with_ngrams(
                analyzer_name="ngram_analyzer",
                filter_name="ngram_filter",
                min_ngram=1,
                max_ngram=10,
                max_ngram_diff=10,
            ),
        }
