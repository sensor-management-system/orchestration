from flask_jwt_extended import jwt_required, get_jwt_identity, current_user
from sqlalchemy import or_

from .base_resource import add_contact_to_object
from ..datalayers.esalchemy import EsSqlalchemyDataLayer
from ..models.base_model import db
from ..models.configuration import Configuration
from ..schemas.configuration_schema import ConfigurationSchema
from ..token_checker import token_required
from ...frj_csv_export.resource import ResourceList


class ConfigurationList(ResourceList):
    """
    provides get and post methods to retrieve
    a collection of Devices or create one.
    """

    @jwt_required(optional=True)
    def get_collection(self, qs, view_kwargs, filters=None):
        """Retrieve a collection of objects through sqlalchemy with permissions

        :param QueryStringManager qs: a querystring manager to retrieve information from url
        :param dict view_kwargs: kwargs from the resource view
        :param dict filters: A dictionary of key/value filters to apply to the eventual query
        :return tuple: the number of object and the list of objects
        """

        self._data_layer.before_get_collection(qs, view_kwargs)
        query = self._data_layer.query(view_kwargs)
        if get_jwt_identity() is None:
            query = query.filter_by(is_public=True)
        else:
            if not current_user.is_superuser:
                query = query.filter(
                    or_(
                        self._data_layer.model.is_public,
                        self._data_layer.model.is_internal,
                    )
                )
        if filters:
            query = query.filter_by(**filters)
        if qs.filters:
            query = self._data_layer.filter_query(
                query, qs.filters, self._data_layer.model
            )
        if qs.sorting:
            query = self._data_layer.sort_query(query, qs.sorting)
        object_count = query.count()
        if getattr(self, "eagerload_includes", True):
            query = self._data_layer.eagerload_includes(query, qs)
        query = self._data_layer.paginate_query(query, qs.pagination)
        collection = query.all()
        collection = self._data_layer.after_get_collection(collection, qs, view_kwargs)
        return object_count, collection

    def before_create_object(self, data, *args, **kwargs):
        """
        Use jwt to add user id to dataset
        :param data:
        :param args:
        :param kwargs:
        :return:
        """
        if not any([data.get("is_public"), data.get("is_internal")]):
            data["is_internal"] = True
            data["is_public"] = False

    def after_post(self, result):
        """
        Automatically add the created user to object contacts
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
        "methods": {"before_create_object": before_create_object,},
    }
