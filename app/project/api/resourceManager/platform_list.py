from flask_rest_jsonapi import ResourceList
from project.api.models.base_model import db
from project.api.models.platform import Platform
from project.api.schemas.platform_schema import PlatformSchema
from project.api.token_checker import token_required


class PlatformList(ResourceList):
    """
    PlatformList class for creating a platformSchema
    only POST and GET method allowed
    """

    schema = PlatformSchema
    decorators = (token_required,)
    data_layer = {'session': db.session,
                  'model': Platform
                  }
