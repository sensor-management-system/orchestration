# SPDX-FileCopyrightText: 2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Model for manufacturer models."""

from ..es_utils import ElasticSearchIndexTypes, settings_with_ngrams
from .base_model import db
from .mixin import SearchableMixin


class ManufacturerModel(db.Model, SearchableMixin):
    """Combination of manufacturer name and model."""

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    manufacturer_name = db.Column(db.String(256), nullable=False)
    model = db.Column(db.String(256), nullable=False)
    # The external system fields are there to point to different
    # sensor system that want to use the export control information
    # check from the SMS (GIPP for example).
    # The url is there so that we can link to that application
    # (as we don't list their devices within the SMS).
    external_system_name = db.Column(db.String(256), nullable=True)
    external_system_url = db.Column(db.String(256), nullable=True)

    def to_search_entry(self):
        """Convert the model to a dict to store in the full text search."""
        export_control = {}
        if self.export_control:
            export_control[
                "export_control_classification_number"
            ] = self.export_control.export_control_classification_number
            export_control[
                "customs_tariff_number"
            ] = self.export_control.customs_tariff_number
            export_control["dual_use"] = self.export_control.dual_use

        return {
            "manufacturer_name": self.manufacturer_name,
            "model": self.model,
            "external_system_name": self.external_system_name,
            "export_control": export_control,
        }

    @staticmethod
    def get_search_index_properties():
        """Get the properties for the index."""
        type_keyword_and_full_searchable = (
            ElasticSearchIndexTypes.keyword_and_full_searchable(
                analyzer="ngram_analyzer"
            )
        )
        return {
            "manufacturer_name": type_keyword_and_full_searchable,
            "model": type_keyword_and_full_searchable,
            "external_system_name": type_keyword_and_full_searchable,
            "export_control": {
                "type": "nested",
                "properties": {
                    "export_control_classification_number": type_keyword_and_full_searchable,
                    "customs_tariff_number": type_keyword_and_full_searchable,
                    "dual_use": {"type": "boolean"},
                },
            },
        }

    @classmethod
    def get_search_index_definition(cls):
        """Return the index configuration."""
        return {
            "aliases": {},
            "mappings": {"properties": cls.get_search_index_properties()},
            "settings": settings_with_ngrams(
                analyzer_name="ngram_analyzer",
                filter_name="ngram_filter",
                min_ngram=1,
                max_ngram=10,
                max_ngram_diff=10,
            ),
        }
