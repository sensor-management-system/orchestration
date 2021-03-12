from flask_rest_jsonapi import ResourceDetail, ResourceRelationship

from project.api.models.base_model import db
from project.api.models.unmount_actions import PlatformUnmountAction
from project.api.resourceManager.base_resource import (
    add_created_by_id,
    add_updated_by_id,
)
from project.api.schemas.unmount_actions_schema import PlatformUnmountActionSchema
from project.api.token_checker import token_required
from project.frj_csv_export.resource import ResourceList


class PlatformUnmountActionList(ResourceList):
    def before_create_object(self, data, *args, **kwargs):
        """Use jwt to add user id to dataset"""
        add_created_by_id(data)

    schema = PlatformUnmountActionSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": PlatformUnmountAction,
        "methods": {
            "before_create_object": before_create_object,
        },
    }


class PlatformUnmountActionDetail(ResourceDetail):
    def before_patch(self, args, kwargs, data):
        """Add Created by user id to the data"""
        add_updated_by_id(data)

    schema = PlatformUnmountActionSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": PlatformUnmountAction,
    }


class PlatformUnmountActionRelationship(ResourceRelationship):
    schema = PlatformUnmountActionSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": PlatformUnmountAction,
    }
