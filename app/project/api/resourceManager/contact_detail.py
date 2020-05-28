from project.api.models.base_model import db
from project.api.models.contact import Contact
from project.api.resourceManager.base_resource import BaseResourceDetail
from project.api.schemas.contact_schema import ContactSchema


class ContactDetail(BaseResourceDetail):
    """
     provides get, patch and delete methods to retrieve details
     of an object, update an object and delete a Contact
    """

    def before_get_object(self, view_kwargs):
        """

        :param view_kwargs:
        :return:
        """

        super().query_an_object(kwargs=view_kwargs, o=Contact)

    schema = ContactSchema
    data_layer = {'session': db.session,
                  'model': Contact,
                  'methods': {'before_create_object': before_get_object}}
