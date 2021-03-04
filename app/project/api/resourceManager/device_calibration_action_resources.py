from flask_rest_jsonapi import ResourceDetail, ResourceRelationship

from project.api.models.base_model import db
from project.api.models.calibration_actions import DeviceCalibrationAction
from project.api.resourceManager.base_resource import (
    add_created_by_id,
    add_updated_by_id,
)
from project.api.schemas.calibration_actions_schema import DeviceCalibrationActionSchema
from project.frj_csv_export.resource import ResourceList


class DeviceCalibrationActionList(ResourceList):
    def before_create_object(self, data, *args, **kwargs):
        """Use jwt to add user id to dataset"""
        add_created_by_id(data)

    schema = DeviceCalibrationActionSchema
    data_layer = {
        "session": db.session,
        "model": DeviceCalibrationAction,
        "methods": {
            "before_create_object": before_create_object,
        },
    }


class DeviceCalibrationActionDetail(ResourceDetail):
    def before_patch(self, args, kwargs, data):
        """Add Created by user id to the data"""
        add_updated_by_id(data)

    schema = DeviceCalibrationActionSchema
    data_layer = {
        "session": db.session,
        "model": DeviceCalibrationAction,
    }


class DeviceCalibrationActionRelationship(ResourceRelationship):
    schema = DeviceCalibrationActionSchema
    data_layer = {
        "session": db.session,
        "model": DeviceCalibrationAction,
    }
