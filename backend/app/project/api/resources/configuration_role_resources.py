# SPDX-FileCopyrightText: 2022 - 2023
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Resources for configuration contact roles."""

from flask_rest_jsonapi import ResourceDetail, ResourceList
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.exc import NoResultFound

from ..models import Configuration
from ..models.base_model import db
from ..models.contact_role import ConfigurationContactRole
from ..permissions.common import DelegateToCanFunctions
from ..permissions.rules import filter_visible
from ..schemas.role import ConfigurationRoleSchema
from ..token_checker import token_required
from .base_resource import (
    check_if_object_not_found,
    query_configuration_set_update_description_and_update_pidinst,
    set_update_description_text_user_and_pidinst,
)


class ConfigurationRoleList(ResourceList):
    """
    List resource for configuration contact roles.

    Provides get and post methods to retrieve
    a collection of Configuration Role or create one.
    """

    def query(self, view_kwargs):
        """Query the entries from the database."""
        query_ = filter_visible(self.session.query(self.model))
        configuration_id = view_kwargs.get("configuration_id")

        if configuration_id is not None:
            try:
                self.session.query(Configuration).filter_by(id=configuration_id).one()
            except NoResultFound:
                raise ObjectNotFound(
                    {"parameter": "id"},
                    "Configuration: {} not found".format(configuration_id),
                )
            query_ = query_.filter(
                ConfigurationContactRole.configuration_id == configuration_id
            )
        return query_

    def after_post(self, result):
        """
        Add update description to related platform.

        :param result:
        :return:
        """
        result_id = result[0]["data"]["relationships"]["configuration"]["data"]["id"]
        msg = "create;contact"
        query_configuration_set_update_description_and_update_pidinst(msg, result_id)

        return result

    schema = ConfigurationRoleSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": ConfigurationContactRole,
        "methods": {"query": query},
    }
    permission_classes = [DelegateToCanFunctions]


class ConfigurationRoleDetail(ResourceDetail):
    """
    Detail resource for configuration contact roles.

    Provides get, patch and delete methods to retrieve details
    of an object, update an object and delete a Configuration Role.
    """

    def before_get(self, args, kwargs):
        """
        Return 404 Responses if role not found.

        Also check if we are allowed to see the entry.
        """
        check_if_object_not_found(self._data_layer.model, kwargs)

    def after_patch(self, result):
        """
        Add update description to related configuration.

        :param result:
        :return:
        """
        result_id = result["data"]["relationships"]["configuration"]["data"]["id"]
        msg = "update;contact"
        query_configuration_set_update_description_and_update_pidinst(msg, result_id)
        return result

    def before_delete(self, args, kwargs):
        """Check that we are allowed to delete."""
        contact_role = (
            db.session.query(ConfigurationContactRole)
            .filter_by(id=kwargs["id"])
            .one_or_none()
        )
        if contact_role is None:
            raise ObjectNotFound("Object not found!")
        self.tasks_after_delete = []

        configuration = contact_role.get_parent()
        msg = "delete;contact"

        def run_updates():
            """Set the update description & update external metadata for pidinst."""
            set_update_description_text_user_and_pidinst(configuration, msg)

        self.tasks_after_delete.append(run_updates)

    def after_delete(self, *args, **kwargs):
        """Run some hooks after deleting."""
        for task in self.tasks_after_delete:
            task()
        return super().after_delete(*args, **kwargs)

    schema = ConfigurationRoleSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": ConfigurationContactRole,
    }
    permission_classes = [DelegateToCanFunctions]
