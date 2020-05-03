from flask_rest_jsonapi import ResourceList
from project.api.models.baseModel import db
from project.api.models.platform import Platform
from project.api.schemas.platformSchema import PlatformSchema


class PlatformList(ResourceList):
    schema = PlatformSchema
    data_layer = {'session': db.session,
                  'model': Platform}
