from flask_rest_jsonapi import ResourceRelationship

from project.api.models.baseModel import db
from project.api.models.platform import Platform
from project.api.schemas.platformSchema import PlatformSchema


class PlatformRelationship(ResourceRelationship):
    schema = PlatformSchema
    data_layer = {'session': db.session,
                  'model': Platform}
