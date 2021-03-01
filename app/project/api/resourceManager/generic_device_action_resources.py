from flask_rest_jsonapi import ResourceDetail, ResourceRelationship

from project.api.models.base_model import db
from project.api.models.generic_actions import GenericDeviceAction
from project.api.schemas.generic_actions_schema import GenericDeviceActionSchema
from project.frj_csv_export.resource import ResourceList


class GenericDeviceActionList(ResourceList):
    schema = GenericDeviceActionSchema
    data_layer = {
        "session": db.session,
        "model": GenericDeviceAction,
    }


class GenericDeviceActionDetail(ResourceDetail):
    schema = GenericDeviceActionSchema
    data_layer = {
        "session": db.session,
        "model": GenericDeviceAction,
    }


class GenericDeviceActionRelationship(ResourceRelationship):
    schema = GenericDeviceActionSchema
    data_layer = {
        "session": db.session,
        "model": GenericDeviceAction,
    }
