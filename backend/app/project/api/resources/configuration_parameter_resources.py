# SPDX-FileCopyrightText:  2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Module for the configuration parameter resource classes."""

from flask_rest_jsonapi import ResourceDetail, ResourceList
from flask_rest_jsonapi.exceptions import ObjectNotFound

from ..helpers.errors import DeletionError
from ..helpers.resource_mixin import add_created_by_id, add_updated_by_id
from ..models import Configuration, ConfigurationParameter
from ..models.base_model import db
from ..permissions.common import DelegateToCanFunctions
from ..permissions.rules import filter_visible
from ..schemas.configuration_parameter_schema import ConfigurationParameterSchema
from ..token_checker import token_required
from .base_resource import (
    check_if_object_not_found,
    query_configuration_set_update_description_and_update_pidinst,
    set_update_description_text_user_and_pidinst,
)


class ConfigurationParameterList(ResourceList):
    """Resource class for the configuration parameter list."""

    def query(self, view_kwargs):
        """Return the possibly filtered query."""
        query_ = filter_visible(self.session.query(self.model))
        configuration_id = view_kwargs.get("configuration_id")
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
        result_id = result[0]["data"]["relationships"]["configuration"]["data"]["id"]
        msg = "create;configuration parameter"
        query_configuration_set_update_description_and_update_pidinst(msg, result_id)

        return result

    schema = ConfigurationParameterSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": ConfigurationParameter,
        "methods": {
            "query": query,
            "before_create_object": before_create_object,
        },
    }
    permission_classes = [DelegateToCanFunctions]


class ConfigurationParameterDetail(ResourceDetail):
    """Resource class for the configuration parameter details."""

    def before_get(self, args, kwargs):
        """Run some hooks before getting the object."""
        check_if_object_not_found(self._data_layer.model, kwargs)

    def before_patch(self, args, kwargs, data):
        """Run some hooks before patching the data."""
        add_updated_by_id(data)

    def after_patch(self, result):
        """Run some hooks after patching the data."""
        result_id = result["data"]["relationships"]["configuration"]["data"]["id"]
        msg = "update;configuration parameter"
        query_configuration_set_update_description_and_update_pidinst(msg, result_id)
        return result

    def before_delete(self, args, kwargs):
        """Run some hooks before deleting the data."""
        configuration_paramater = (
            db.session.query(ConfigurationParameter)
            .filter_by(id=kwargs["id"])
            .one_or_none()
        )
        if configuration_paramater is None:
            raise ObjectNotFound("Object not found!")
        if configuration_paramater.configuration_parameter_value_change_actions:
            raise DeletionError("There are values associated to the parameter.")
        msg = "delete;configuration parameter"
        set_update_description_text_user_and_pidinst(
            configuration_paramater.configuration, msg
        )

    schema = ConfigurationParameterSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": ConfigurationParameter,
    }
    permission_classes = [DelegateToCanFunctions]
