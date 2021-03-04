from flask_rest_jsonapi import ResourceDetail, ResourceRelationship

from project.api.models.base_model import db
from project.api.models.generic_actions import GenericConfigurationAction
from project.api.resourceManager.base_resource import (
    add_created_by_id,
    add_updated_by_id,
)
from project.api.schemas.generic_actions_schema import GenericConfigurationActionSchema
from project.frj_csv_export.resource import ResourceList


class GenericConfigurationActionList(ResourceList):
    def before_create_object(self, data, *args, **kwargs):
        """Use jwt to add user id to dataset"""
        add_created_by_id(data)

    schema = GenericConfigurationActionSchema
    data_layer = {
        "session": db.session,
        "model": GenericConfigurationAction,
        "methods": {
            "before_create_object": before_create_object,
        },
    }


class GenericConfigurationActionDetail(ResourceDetail):
    def before_patch(self, args, kwargs, data):
        """Add Created by user id to the data"""
        add_updated_by_id(data)

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
