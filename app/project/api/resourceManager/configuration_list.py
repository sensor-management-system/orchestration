"""Configuration list resource."""

from sqlalchemy import or_

from ...frj_csv_export.resource import ResourceList
from ..datalayers.esalchemy import (
    EsSqlalchemyDataLayer,
    OrFilter,
    TermEqualsExactStringFilter,
)
from ..helpers.resource_mixin import add_created_by_id
from ..models.base_model import db
from ..models.configuration import Configuration
from ..schemas.configuration_schema import ConfigurationSchema
from ..token_checker import get_current_user_or_none_by_optional, token_required
from .base_resource import add_contact_to_object


class ConfigurationList(ResourceList):
    """
    Resource for the device list endpoint.

    Supports GET (list) & POST (create) methods.
    """

    def query(self, view_kwargs):
        """
        Filter for what the user is allowed to query.

        :param view_kwargs:
        :return: queryset or es filter
        """
        query = db.session.query(self.model)
        current_user = get_current_user_or_none_by_optional(optional=True)
        if current_user is None:
            query = query.filter_by(is_public=True)
        else:
            if not current_user.is_superuser:
                query = query.filter(
                    or_(
                        self.model.is_public,
                        self.model.is_internal,
                    )
                )
        return query

    def es_query(self, view_kwargs):
        """
        Return the elasticsearch filter for the query.

        Should return the same set as query, but using
        the elasticsearch fields.
        """
        current_user = get_current_user_or_none_by_optional(optional=True)
        if current_user is None:
            return TermEqualsExactStringFilter("is_public", True)
        if not current_user.is_superuser:
            return OrFilter(
                [
                    TermEqualsExactStringFilter("is_public", True),
                    TermEqualsExactStringFilter("is_internal", True),
                ]
            )
        return None

    def before_create_object(self, data, *args, **kwargs):
        """
        Set the visibility of the object (internal of nothing else is given).

        :param data: data of the request (as dict)
        :param args:
        :param kwargs:
        :return: None
        """
        # Will modify the data inplace.
        if not any([data.get("is_public"), data.get("is_internal")]):
            data["is_internal"] = True
            data["is_public"] = False
        add_created_by_id(data)

    def after_post(self, result):
        """
        Automatically add the created user to object contacts.

        :param result:
        :return:
        """
        result_id = result[0]["data"]["id"]
        d = db.session.query(Configuration).filter_by(id=result_id).first()
        add_contact_to_object(d)

        return result

    schema = ConfigurationSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": Configuration,
        "class": EsSqlalchemyDataLayer,
        "methods": {
            "before_create_object": before_create_object,
            "query": query,
            "es_query": es_query,
        },
    }
