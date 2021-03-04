from flask_rest_jsonapi import ResourceDetail, ResourceRelationship

from project.api.models.base_model import db
from project.frj_csv_export.resource import ResourceList
from project.api.resourceManager.base_resource import add_created_by_id
from project.api.resourceManager.base_resource import add_updated_by_id

from project.api.models.mount_actions import PlatformMountAction
from project.api.schemas.mount_actions_schema import PlatformMountActionSchema


class PlatformMountActionList(ResourceList):
    def before_create_object(self, data, *args, **kwargs):
        """Use jwt to add user id to dataset"""
        add_created_by_id(data)

    schema = PlatformMountActionSchema
    data_layer = {
        "session": db.session,
        "model": PlatformMountAction,
        "methods": {
            "before_create_object": before_create_object,
        },
    }


class PlatformMountActionDetail(ResourceDetail):
    def before_patch(self, args, kwargs, data):
        """Add Created by user id to the data"""
        add_updated_by_id(data)

    schema = PlatformMountActionSchema
    data_layer = {
        "session": db.session,
        "model": PlatformMountAction,
    }


class PlatformMountActionRelationship(ResourceRelationship):
    schema = PlatformMountActionSchema
    data_layer = {
        "session": db.session,
        "model": PlatformMountAction,
    }
