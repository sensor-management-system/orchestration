from flask_rest_jsonapi import ResourceList
from project.api.models.base_model import db
from project.api.models.platform import Platform
from project.api.schemas.platform_schema import PlatformSchema
from project.api.token_checker import token_required

from flask import request

class PlatformList(ResourceList):
    """
    PlatformList class for creating a platformSchema
    only POST and GET method allowed
    """

    def query(self, view_kwargs):
        """Extension to query platforms via elasticsearch."""
        query = self.session.query(Platform)

        rargs = request.args
        if rargs.get('q') is not None:
            page = rargs.get('page[number]', 1)
            per_page = rargs.get('page[size]', 20)
            query, _total = Platform.search(rargs['q'], page, per_page)
        return query


    schema = PlatformSchema
    # decorators = (token_required,)
    data_layer = {'session': db.session,
                  'model': Platform,
                  'methods': {
                      'query': query,
                    }
                  }
