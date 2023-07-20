# SPDX-FileCopyrightText: 2022 - 2023
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Resource classes for Configuration static location begin actions."""

from flask_rest_jsonapi import ResourceDetail
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.orm.exc import NoResultFound

from ...frj_csv_export.resource import ResourceList
from ..helpers.location_checks import StaticLocationActionValidator
from ..helpers.resource_mixin import (
    add_created_by_id,
    add_updated_by_id,
    decode_json_request_data,
)
from ..models import Configuration, ConfigurationStaticLocationBeginAction
from ..models.base_model import db
from ..permissions.common import DelegateToCanFunctions
from ..permissions.rules import filter_visible
from ..schemas.configuration_static_location_actions_schema import (
    ConfigurationStaticLocationBeginActionSchema,
)
from ..token_checker import token_required
from .base_resource import (
    check_if_object_not_found,
    query_configuration_set_update_description_and_update_pidinst,
    set_update_description_text_user_and_pidinst,
)


class ConfigurationStaticLocationBeginActionList(ResourceList):
    """List resource for Configuration static location begin actions (get, post)."""

    def before_create_object(self, data, *args, **kwargs):
        """Run some validations before we create the object."""
        data_with_relationships = decode_json_request_data()
        StaticLocationActionValidator().validate_create(data_with_relationships)
        add_created_by_id(data)

    def query(self, view_kwargs):
        """
        Query the Configuration static location begin actions from the database.

        Also handle optional pre-filters (for specific configuration, for example).
        """
        query_ = filter_visible(self.session.query(self.model))
        configuration_id = view_kwargs.get("configuration_id")

        if configuration_id is not None:
            try:
                self.session.query(Configuration).filter_by(id=configuration_id).one()
            except NoResultFound:
                raise ObjectNotFound(
                    {
                        "parameter": "id",
                    },
                    "Configuration: {} not found".format(configuration_id),
                )
            else:
                query_ = query_.filter(
                    ConfigurationStaticLocationBeginAction.configuration_id
                    == configuration_id
                )
        return query_

    def after_post(self, result):
        """
        Add update description to related platform.

        :param result:
        :return:
        """
        result_id = result[0]["data"]["relationships"]["configuration"]["data"]["id"]
        msg = "create;static location action"
        query_configuration_set_update_description_and_update_pidinst(msg, result_id)

        return result

    schema = ConfigurationStaticLocationBeginActionSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": ConfigurationStaticLocationBeginAction,
        "methods": {
            "query": query,
            "before_create_object": before_create_object,
        },
    }
    permission_classes = [DelegateToCanFunctions]


class ConfigurationStaticLocationBeginActionDetail(ResourceDetail):
    """Detail resource for Configuration static location begin actions (get, delete, patch)."""

    validator = StaticLocationActionValidator()

    def before_get(self, args, kwargs):
        """
        Return some checks before we return ob object.

        Currently we have the following checks:
        - Check if the object exists (return 404 otherwise)
        - Check that the user is allowed to see the object (401 or 405 otherwise)
        """
        check_if_object_not_found(self._data_layer.model, kwargs)

    def before_patch(self, args, kwargs, data=None):
        """Run some checks before we update an object."""
        data_with_relationships = decode_json_request_data()
        self.validator.validate_update(data_with_relationships, kwargs["id"])
        add_updated_by_id(data)

    def after_patch(self, result):
        """
        Add update description to related configuration.

        :param result:
        :return:
        """
        result_id = result["data"]["relationships"]["configuration"]["data"]["id"]
        msg = "update;static location action"
        query_configuration_set_update_description_and_update_pidinst(msg, result_id)
        return result

    def before_delete(self, args, kwargs):
        """Run some checks before we delete."""
        location_action = (
            db.session.query(ConfigurationStaticLocationBeginAction)
            .filter_by(id=kwargs["id"])
            .one_or_none()
        )
        if location_action is None:
            raise ObjectNotFound("Object not found!")
        self.tasks_after_delete = []

        configuration = location_action.get_parent()
        msg = "delete;static location action"

        def run_updates():
            """Set the update description & update external metadata for pidinst."""
            set_update_description_text_user_and_pidinst(configuration, msg)

        self.tasks_after_delete.append(run_updates)

    def after_delete(self, *args, **kwargs):
        """Run some hooks after deleting."""
        for task in self.tasks_after_delete:
            task()
        return super().after_delete(*args, **kwargs)

    schema = ConfigurationStaticLocationBeginActionSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": ConfigurationStaticLocationBeginAction,
    }
    permission_classes = [DelegateToCanFunctions]
