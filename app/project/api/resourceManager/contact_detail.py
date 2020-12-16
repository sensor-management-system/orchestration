from flask_rest_jsonapi import ResourceDetail
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.orm.exc import NoResultFound

from project.api.models.base_model import db
from project.api.models.contact import Contact
from project.api.schemas.contact_schema import ContactSchema


class ContactDetail(ResourceDetail):
    """
     provides get, patch and delete methods to retrieve details
     of an object, update an object and delete a Contact
    """

    def before_get_object(self, view_kwargs):
        if view_kwargs.get('id') is not None:
            try:
                _ = self.session.query(Contact).filter_by(
                    id=view_kwargs['id']).one()
            except NoResultFound:
                raise ObjectNotFound({'parameter': 'contact_id'},
                                     "Contact: {} not found".format(view_kwargs['id']))

    schema = ContactSchema
    # decorators = (token_required,)
    data_layer = {'session': db.session,
                  'model': Contact,
                  'methods': {'before_get_object': before_get_object}
                  }
