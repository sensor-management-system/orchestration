from flask_rest_jsonapi import ResourceDetail, ResourceRelationship

from project.api.models.base_model import db
from project.api.models.generic_actions import GenericConfigurationAction
from project.api.schemas.generic_actions_schema import GenericConfigurationActionSchema
from project.frj_csv_export.resource import ResourceList


class GenericConfigurationActionList(ResourceList):
    schema = GenericConfigurationActionSchema
    data_layer = {
        "session": db.session,
        "model": GenericConfigurationAction,
    }


class GenericConfigurationActionDetail(ResourceDetail):
    schema = GenericConfigurationActionSchema
    data_layer = {
        "session": db.session,
        "model": GenericConfigurationAction,
    }


class GenericConfigurationActionRelationship(ResourceRelationship):
    schema = GenericConfigurationActionSchema
    data_layer = {
        "session": db.session,
        "model": GenericConfigurationAction,
    }
