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
    def after_get_collection(self, collection, qs, view_kwargs):
        """Take the intersection between requested collection and
        what the user allowed querying.

        :param collection:
        :param qs:
        :param view_kwargs:
        :return:
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

        allowed_collection = query.all()

        return set(collection).intersection(allowed_collection)

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
