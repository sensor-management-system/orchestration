from flask_rest_jsonapi import ResourceDetail, ResourceRelationship

from project.api.models.base_model import db
from project.api.models.software_update_actions import DeviceSoftwareUpdateAction
from project.api.schemas.software_update_action_schema import DeviceSoftwareUpdateActionSchema
from project.frj_csv_export.resource import ResourceList

from project.api.resourceManager.base_resource import add_created_by_id, add_contact_to_object
from project.api.token_checker import token_required
from project.api.resourceManager.base_resource import add_updated_by_id


class DeviceSoftwareUpdateActionList(ResourceList):
    def before_create_object(self, data, *args, **kwargs):
        """Use jwt to add user id to dataset"""
        add_created_by_id(data)

    schema = DeviceSoftwareUpdateActionSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": DeviceSoftwareUpdateAction,
        "methods": {
            "before_create_object": before_create_object,
        },
    }


class DeviceSoftwareUpdateActionDetail(ResourceDetail):
    def before_patch(self, args, kwargs, data):
        """Add Created by user id to the data"""
        add_updated_by_id(data)

    schema = DeviceSoftwareUpdateActionSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": DeviceSoftwareUpdateAction,
    }


class DeviceSoftwareUpdateActionRelationship(ResourceRelationship):
    schema = DeviceSoftwareUpdateActionSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": DeviceSoftwareUpdateAction,
    }
