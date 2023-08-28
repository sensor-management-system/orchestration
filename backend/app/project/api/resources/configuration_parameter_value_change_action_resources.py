# SPDX-FileCopyrightText:  2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Module for the configuration parameter value change action resource classes."""

from flask_rest_jsonapi import ResourceDetail, ResourceList
from flask_rest_jsonapi.exceptions import ObjectNotFound

from ..helpers.resource_mixin import add_created_by_id, add_updated_by_id
from ..models import (
    Configuration,
    ConfigurationParameter,
    ConfigurationParameterValueChangeAction,
)
from ..models.base_model import db
from ..permissions.common import DelegateToCanFunctions
from ..permissions.rules import filter_visible
from ..schemas.configuration_parameter_value_change_action_schema import (
    ConfigurationParameterValueChangeActionSchema,
)
from ..token_checker import token_required
from .base_resource import (
    check_if_object_not_found,
    query_configuration_set_update_description_and_update_pidinst,
    set_update_description_text_user_and_pidinst,
)


class ConfigurationParameterValueChangeActionList(ResourceList):
    """Resource class for the configuratin parameter value change action list."""

    def query(self, kwargs):
        """Return the possibly filtered query."""
        query_ = filter_visible(self.session.query(self.model))
        configuration_id = kwargs.get("configuration_id")
        if configuration_id is not None:
            configuration = (
                self.session.query(Configuration).filter_by(id=configuration_id).first()
            )
            if not configuration:
                raise ObjectNotFound(
                    {
                        "parameter": "id",
                    },
                    "Configuration: {} not found".format(configuration_id),
                )
            query_ = query_.filter(
                ConfigurationParameter.configuration_id == configuration_id
            )
        return query_

    def before_create_object(self, data, *args, **kwargs):
        """Run some hooks before creating the object."""
        add_created_by_id(data)

    def after_post(self, result):
        """Run some hooks after posting the data."""
        configuration_parameter_id = result[0]["data"]["relationships"][
            "configuration_parameter"
        ]["data"]["id"]
        configuration_parameter = (
            db.session.query(ConfigurationParameter)
            .filter_by(id=configuration_parameter_id)
            .first()
        )
        if configuration_parameter:
            configuration_id = configuration_parameter.configuration_id
            msg = "create;configuration parameter value change action"
            query_configuration_set_update_description_and_update_pidinst(
                msg, configuration_id
            )
        return result

    schema = ConfigurationParameterValueChangeActionSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": ConfigurationParameterValueChangeAction,
        "methods": {
            "query": query,
            "before_create_object": before_create_object,
        },
    }
    permission_classes = [DelegateToCanFunctions]


class ConfigurationParameterValueChangeActionDetail(ResourceDetail):
    """Resouce class for the configuration parameter value change action details."""

    def before_get(self, args, kwargs):
        """Run some hooks before getting the data."""
        check_if_object_not_found(self._data_layer.model, kwargs)

    def before_patch(self, args, kwargs, data):
        """Run some hooks before patching the data."""
        add_updated_by_id(data)

    def after_patch(self, result):
        """Run some hooks after patching the data."""
        configuration_parameter_id = result["data"]["relationships"][
            "configuration_parameter"
        ]["data"]["id"]
        configuration_parameter = (
            db.session.query(ConfigurationParameter)
            .filter_by(id=configuration_parameter_id)
            .first()
        )
        if configuration_parameter:
            configuration_id = configuration_parameter.configuration_id
            msg = "update;configuration parameter value change action"
            query_configuration_set_update_description_and_update_pidinst(
                msg, configuration_id
            )
        return result

    def before_delete(self, args, kwargs):
        """Run some hooks before deleting the data."""
        value_change_action = (
            db.session.query(ConfigurationParameterValueChangeAction)
            .filter_by(id=kwargs["id"])
            .one_or_none()
        )
        if value_change_action is None:
            raise ObjectNotFound("Object not found!")
        msg = "delete;configuration parameter value change action"
        configuration_parameter = value_change_action.configuration_parameter
        set_update_description_text_user_and_pidinst(
            configuration_parameter.configuration, msg
        )

    schema = ConfigurationParameterValueChangeActionSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": ConfigurationParameterValueChangeAction,
    }
    permission_classes = [DelegateToCanFunctions]
