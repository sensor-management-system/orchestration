# SPDX-FileCopyrightText: 2021
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Utility functions to work with elasticsearch content."""


def settings_with_ngrams(
    analyzer_name: str,
    filter_name: str,
    min_ngram: int = 3,
    max_ngram: int = 3,
    max_ngram_diff: int = 1,
):
    """
    Return a settings section for our elasticseach indices.

    Also include a custom ngram analyzer.
    """
    settings = {
        "index": {
            "number_of_shards": "1",
            "max_ngram_diff": max_ngram_diff,
        },
        "analysis": {
            "filter": {
                filter_name: {
                    "type": "ngram",
                    "min_gram": min_ngram,
                    "max_gram": max_ngram,
                },
            },
            "analyzer": {
                analyzer_name: {
                    "filter": [
                        "lowercase",
                        filter_name,
                    ],
                    "type": "custom",
                    "tokenizer": "uax_url_email",

                },
            },
        },
    }
    return settings


class ElasticSearchIndexTypes:
    """Class to collect factory method to create the index types easier."""

    @staticmethod
    def keyword():
        """Return the definition for a keyword index type."""
        return {"type": "keyword"}

    @staticmethod
    def text_full_searchable(analyzer: str):
        """
        Return the definition for searchable text.

        The text will be searchable in various ways.
        Standard is with the search_as_you_type tupe,
        but it also allows text with a custom analyzer (ngrams for example)
        to support various forms of substring queries.
        """
        return {
            "type": "search_as_you_type",
            "fields": {
                "text_analyzer": {
                    "type": "text",
                    "analyzer": analyzer,
                    "search_analyzer": "standard",
                }
            },
        }

    @staticmethod
    def keyword_and_full_searchable(analyzer: str):
        """Return a keyword type that can also be used for full text search."""
        return {
            "type": "keyword",
            "fields": {
                "text": {
                    "type": "search_as_you_type",
                },
                "text_analyzer": {
                    "type": "text",
                    "analyzer": analyzer,
                    "search_analyzer": "standard",
                },
            },
        }
