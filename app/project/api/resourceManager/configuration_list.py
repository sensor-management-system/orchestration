from sqlalchemy import or_

from .base_resource import add_contact_to_object
from ..datalayers.esalchemy import EsSqlalchemyDataLayer
from ..helpers.resource_mixin import add_created_by_id
from ..models.base_model import db
from ..models.configuration import Configuration
from ..schemas.configuration_schema import ConfigurationSchema
from ..token_checker import token_required, current_user_or_none
from ...frj_csv_export.resource import ResourceList


class ConfigurationList(ResourceList):
    """
    provides get and post methods to retrieve
    a collection of Devices or create one.
    """

    def after_get_collection(self, collection, qs, view_kwargs):
        """Take the intersection between requested collection and
        what the user allowed querying.

        :param collection:
        :param qs:
        :param view_kwargs:
        :return:
        """

        query = db.session.query(self.model)
        current_user = current_user_or_none(optional=True)
        if current_user is None:
            query = query.filter_by(is_public=True)
        else:
            if not current_user.is_superuser:
                query = query.filter(or_(self.model.is_public, self.model.is_internal,))

        allowed_collection = query.all()

        return set(collection).intersection(allowed_collection)

    def after_get(self, result):
        result.update({"meta": {"count": len(result["data"])}})
        return result

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
        add_created_by_id(data)

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
        "methods": {
            "before_create_object": before_create_object,
            "after_get_collection": after_get_collection,
        },
    }
