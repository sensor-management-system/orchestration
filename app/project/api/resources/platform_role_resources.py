# SPDX-FileCopyrightText: 2022 - 2023
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Platform contact role resources."""

from flask_rest_jsonapi import ResourceDetail
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.exc import NoResultFound

from ...frj_csv_export.resource import ResourceList
from ..models import Platform
from ..models.base_model import db
from ..models.contact_role import PlatformContactRole
from ..permissions.common import DelegateToCanFunctions
from ..permissions.rules import filter_visible
from ..schemas.role import PlatformRoleSchema
from ..token_checker import token_required
from .base_resource import (
    check_if_object_not_found,
    query_platform_set_update_description_and_update_pidinst,
    set_update_description_text_user_and_pidinst,
)


class PlatformRoleList(ResourceList):
    """
    List resource for platform contact roles.

    Provides get and post methods to retrieve
    a collection of Platform Role or create one.
    """

    def query(self, view_kwargs):
        """
        Query the entries from the database.

        Handle also cases to get all the platform attachments
        for a specific platform.
        """
        query_ = filter_visible(self.session.query(self.model))
        platform_id = view_kwargs.get("platform_id")

        if platform_id is not None:
            try:
                self.session.query(Platform).filter_by(id=platform_id).one()
            except NoResultFound:
                raise ObjectNotFound(
                    {"parameter": "id"}, "Platform: {} not found".format(platform_id)
                )
            query_ = query_.filter(PlatformContactRole.platform_id == platform_id)
        return query_

    def after_post(self, result):
        """
        Add update description to related platform.

        :param result:
        :return:
        """
        result_id = result[0]["data"]["relationships"]["platform"]["data"]["id"]
        msg = "create;contact"
        query_platform_set_update_description_and_update_pidinst(msg, result_id)

        return result

    schema = PlatformRoleSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": PlatformContactRole,
        "methods": {"query": query},
    }
    permission_classes = [DelegateToCanFunctions]


class PlatformRoleDetail(ResourceDetail):
    """
    Detail resource for platform contact roles.

    Provides get, patch and delete methods to retrieve details
    of an object, update an object and delete a Platform Role
    """

    def before_get(self, args, kwargs):
        """Return 404 Responses if role not found."""
        check_if_object_not_found(self._data_layer.model, kwargs)

    def after_patch(self, result):
        """
        Add update description to related device.

        :param result:
        :return:
        """
        result_id = result["data"]["relationships"]["platform"]["data"]["id"]
        msg = "update;contact"
        query_platform_set_update_description_and_update_pidinst(msg, result_id)
        return result

    def before_delete(self, args, kwargs):
        """Update the platforms update description."""
        contact_role = (
            db.session.query(PlatformContactRole)
            .filter_by(id=kwargs["id"])
            .one_or_none()
        )
        if contact_role is None:
            raise ObjectNotFound("Object not found!")

        self.tasks_after_delete = []
        platform = contact_role.get_parent()
        msg = "delete;contact"

        def run_updates():
            """Set the update description & update external metadata for pidinst."""
            set_update_description_text_user_and_pidinst(platform, msg)

        self.tasks_after_delete.append(run_updates)

    def after_delete(self, *args, **kwargs):
        """Run some hooks after deleting."""
        for task in self.tasks_after_delete:
            task()
        return super().after_delete(*args, **kwargs)

    schema = PlatformRoleSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": PlatformContactRole,
    }
    permission_classes = [DelegateToCanFunctions]
