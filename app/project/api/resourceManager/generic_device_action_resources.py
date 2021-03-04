from flask_rest_jsonapi import ResourceDetail, ResourceRelationship

from project.api.models.base_model import db
from project.api.models.generic_actions import GenericDeviceAction
from project.api.resourceManager.base_resource import (
    add_created_by_id,
    add_updated_by_id,
)
from project.api.schemas.generic_actions_schema import GenericDeviceActionSchema
from project.api.token_checker import token_required
from project.frj_csv_export.resource import ResourceList


class GenericDeviceActionList(ResourceList):
    def before_create_object(self, data, *args, **kwargs):
        """Use jwt to add user id to dataset"""
        add_created_by_id(data)

    schema = GenericDeviceActionSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": GenericDeviceAction,
        "methods": {
            "before_create_object": before_create_object,
        },
    }


class GenericDeviceActionDetail(ResourceDetail):
    def before_patch(self, args, kwargs, data):
        """Add Created by user id to the data"""
        add_updated_by_id(data)

    schema = GenericDeviceActionSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": GenericDeviceAction,
    }


class GenericDeviceActionRelationship(ResourceRelationship):
    schema = GenericDeviceActionSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": GenericDeviceAction,
    }
