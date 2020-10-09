from flask_rest_jsonapi import ResourceList

from project.api.models.base_model import db
from project.api.models.contact import Contact
from project.api.schemas.contact_schema import ContactSchema
from project.api.token_checker import token_required


class ContactList(ResourceList):
    """
    provides get and post methods to retrieve
     a collection of Contacts or create one.
    """

    def query(self, view_kwargs):

        query_ = self.session.query(Contact)
        configuration_id = view_kwargs.get('configuration_id')
        platform_id = view_kwargs.get('platform_id')
        device_id = view_kwargs.get('device_id')

        if configuration_id is not None:
            try:
                self.session.query(Configuration).filter_by(id=configuration_id).one()
            except NoResultFound:
                raise ObjectNotFound(
                    {'parameter': 'id'},
                    "Configuration: {} not found".format(configuration_id)
                )
            else:
                query_ = query_.join(Contact.configurations).filter(
                    Configuration.id == configuration_id)

        if platform_id is not None:
            try:
                self.session.query(Platform).filter_by(id=platform_id).one()
            except NoResultFound:
                raise ObjectNotFound(
                    {'parameter': 'id'},
                    "Platform: {} not found".format(platform_id)
                )
            else:
                query_ = query_.join(Contact.platforms).filter(
                    Platform.id == platform_id)

        if device_id is not None:
            try:
                self.session.query(Device).filter_by(id=device_id).one()
            except NoResultFound:
                raise ObjectNotFound(
                    {'parameter': 'id'},
                    "Device: {} not found".format(platform_id)
                )
            else:
                query_ = query_.join(Contact.devices).filter(
                    Device.id == device_id)

        return query_

    schema = ContactSchema
    # decorators = (token_required,)
    data_layer = {'session': db.session,
                  'model': Contact}
