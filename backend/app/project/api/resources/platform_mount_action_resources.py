# SPDX-FileCopyrightText: 2022 - 2023
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Resource classes for platform mount actions."""

from flask_rest_jsonapi import ResourceDetail, ResourceList
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.orm.exc import NoResultFound

from ..helpers.mounting_checks import PlatformMountActionValidator
from ..helpers.resource_mixin import (
    add_created_by_id,
    add_updated_by_id,
    decode_json_request_data,
)
from ..models.base_model import db
from ..models.configuration import Configuration
from ..models.mount_actions import PlatformMountAction
from ..models.platform import Platform
from ..permissions.common import DelegateToCanFunctions
from ..permissions.rules import filter_visible
from ..resources.base_resource import (
    check_if_object_not_found,
    query_configuration_set_update_description_and_update_pidinst,
    set_update_description_text_user_and_pidinst,
)
from ..schemas.mount_actions_schema import PlatformMountActionSchema
from ..token_checker import token_required


class PlatformMountActionList(ResourceList):
    """List resource for platform mount actions (get, post)."""

    validator = PlatformMountActionValidator()

    def before_post(self, args, kwargs, data=None):
        """Run some checks before creating it."""
        data_with_relationships = decode_json_request_data()
        self.validator.validate_create(data_with_relationships)

    def before_create_object(self, data, *args, **kwargs):
        """Add the created by info."""
        add_created_by_id(data)

    def query(self, view_kwargs):
        """
        Query the actions from the database.

        Also handle optional pre-filters (for specific configurations, for example).
        """
        query_ = filter_visible(self.session.query(self.model))
        configuration_id = view_kwargs.get("configuration_id")
        platform_id = view_kwargs.get("platform_id")
        parent_platform_id = view_kwargs.get("parent_platform_id")
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
                    PlatformMountAction.configuration_id == configuration_id
                )
        if platform_id is not None:
            try:
                self.session.query(Platform).filter_by(id=platform_id).one()
            except NoResultFound:
                raise ObjectNotFound(
                    {
                        "parameter": "id",
                    },
                    "Platform: {} not found".format(platform_id),
                )
            else:
                query_ = query_.filter(PlatformMountAction.platform_id == platform_id)
        if parent_platform_id is not None:
            try:
                self.session.query(Platform).filter_by(id=parent_platform_id).one()
            except NoResultFound:
                raise ObjectNotFound(
                    {
                        "parameter": "id",
                    },
                    "Parent platform: {} not found".format(parent_platform_id),
                )
            else:
                query_ = query_.filter(
                    PlatformMountAction.parent_platform_id == parent_platform_id
                )
        return query_

    def after_post(self, result):
        """
        Add update description to related platform.

        :param result:
        :return:
        """
        result_id = result[0]["data"]["relationships"]["configuration"]["data"]["id"]
        msg = "create;platform mount action"
        query_configuration_set_update_description_and_update_pidinst(msg, result_id)

        return result

    schema = PlatformMountActionSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": PlatformMountAction,
        "methods": {
            "before_create_object": before_create_object,
            "query": query,
        },
    }
    permission_classes = [DelegateToCanFunctions]


class PlatformMountActionDetail(ResourceDetail):
    """Detail resource for platform mount actions (get, delete, patch)."""

    validator = PlatformMountActionValidator()

    def before_get(self, args, kwargs):
        """Return 404 Responses if PlatformMountAction not found."""
        check_if_object_not_found(self._data_layer.model, kwargs)

    def before_patch(self, args, kwargs, data):
        """Do checks if wanted time-interval is available or not & some additional checks."""
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
        msg = "update;platform mount action"
        query_configuration_set_update_description_and_update_pidinst(msg, result_id)
        return result

    def before_delete(self, args, kwargs):
        """Do some checks for possible orphans."""
        self.validator.validate_delete(kwargs["id"])
        mount_action = (
            db.session.query(PlatformMountAction)
            .filter_by(id=kwargs["id"])
            .one_or_none()
        )
        if mount_action is None:
            raise ObjectNotFound("Object not found!")
        self.tasks_after_delete = []
        configuration = mount_action.configuration
        msg = "delete;platform mount action"

        def run_updates():
            """Set the update description & update external metadata for pidinst."""
            set_update_description_text_user_and_pidinst(configuration, msg)

        self.tasks_after_delete.append(run_updates)

    def after_delete(self, *args, **kwargs):
        """Run some hooks after deleting."""
        for task in self.tasks_after_delete:
            task()
        return super().after_delete(*args, **kwargs)

    schema = PlatformMountActionSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": PlatformMountAction,
    }
    permission_classes = [DelegateToCanFunctions]
