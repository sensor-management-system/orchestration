from flask_rest_jsonapi import ResourceDetail
from project.api.models.base_model import db
from project.api.models.platform import Platform
from project.api.schemas.platform_schema import PlatformSchema


class PlatformDetail(ResourceDetail):
    """
     provides get, patch and delete methods to retrieve details
     of an object, update an object and delete an Event
    """

    schema = PlatformSchema
    # decorators = (token_required,)
    data_layer = {'session': db.session,
                  'model': Platform,
                 }
