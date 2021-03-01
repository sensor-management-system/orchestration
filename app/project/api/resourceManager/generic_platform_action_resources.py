from flask_rest_jsonapi import ResourceDetail, ResourceRelationship

from project.api.models.base_model import db
from project.api.models.generic_actions import GenericPlatformAction
from project.api.schemas.generic_actions_schema import GenericPlatformActionSchema
from project.frj_csv_export.resource import ResourceList


class GenericPlatformActionList(ResourceList):
    schema = GenericPlatformActionSchema
    data_layer = {
        "session": db.session,
        "model": GenericPlatformAction,
    }


class GenericPlatformActionDetail(ResourceDetail):
    schema = GenericPlatformActionSchema
    data_layer = {
        "session": db.session,
        "model": GenericPlatformAction,
    }


class GenericPlatformActionRelationship(ResourceRelationship):
    schema = GenericPlatformActionSchema
    data_layer = {
        "session": db.session,
        "model": GenericPlatformAction,
    }
