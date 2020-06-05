from flask_rest_jsonapi import ResourceDetail
from project.api.models.base_model import db
from project.api.models.platform import Platform
from project.api.schemas.platform_schema import PlatformSchema
from project.api.token_checker import token_required


class PlatformDetail(ResourceDetail):
    """
     provides get, patch and delete methods to retrieve details
     of an object, update an object and delete an Event
    """

    @token_required
    def before_create_object(*args, **kwargs):
        """Make custom work here. View args and kwargs are provided as parameter
        """



    schema = PlatformSchema
    data_layer = {'session': db.session,
                  'model': Platform,
                  'methods': {'before_get_object': before_create_object}
                  }
