from project.frj_monkey_patching.resource import ResourceList
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.orm.exc import NoResultFound

from project.api.models.base_model import db
from project.api.models.configuration import Configuration
from project.api.models.contact import Contact
from project.api.models.device import Device
from project.api.models.platform import Platform
from project.api.schemas.contact_schema import ContactSchema
from project.api.datalayers.esalchemy import EsSqlalchemyDataLayer
from project.api.token_checker import token_required


class ContactList(ResourceList):
    """
    provides get and post methods to retrieve
     a collection of Contacts or create one.
    """

    def query(self, view_kwargs):

        query_ = self.session.query(Contact)
        configuration_id = view_kwargs.get("configuration_id")
        platform_id = view_kwargs.get("platform_id")
        device_id = view_kwargs.get("device_id")

        if configuration_id is not None:
            try:
                self.session.query(Configuration).filter_by(id=configuration_id).one()
            except NoResultFound:
                raise ObjectNotFound(
                    {"parameter": "id"},
                    "Configuration: {} not found".format(configuration_id),
                )
            else:
                query_ = query_.join(Contact.configurations).filter(
                    Configuration.id == configuration_id
                )

        if platform_id is not None:
            try:
                self.session.query(Platform).filter_by(id=platform_id).one()
            except NoResultFound:
                raise ObjectNotFound(
                    {"parameter": "id"}, "Platform: {} not found".format(platform_id)
                )
            else:
                query_ = query_.join(Contact.platforms).filter(
                    Platform.id == platform_id
                )

        if device_id is not None:
            try:
                self.session.query(Device).filter_by(id=device_id).one()
            except NoResultFound:
                raise ObjectNotFound(
                    {"parameter": "id"}, "Device: {} not found".format(platform_id)
                )
            else:
                query_ = query_.join(Contact.devices).filter(Device.id == device_id)

        return query_

    schema = ContactSchema
    # decorators = (token_required,)
    data_layer = {
        "class": EsSqlalchemyDataLayer,
        "session": db.session,
        "model": Contact,
        "methods": {
            "query": query,
        },
    }
