from flask_rest_jsonapi import ResourceRelationship

from ..auth.permission_utils import (
    check_parent_group_before_change_a_relationship,
)
from ..models.base_model import db
from ..models.contact import Contact
from ..schemas.contact_schema import ContactSchema
from ..token_checker import token_required


class ContactRelationship(ResourceRelationship):
    """
    provides get, post, patch and delete methods to get relationships,
    create relationships, update relationships and delete
    relationships between Contact and other objects.
    """

    def before_post(self, args, kwargs, json_data=None):
        check_parent_group_before_change_a_relationship(
            "contacts/", self._data_layer.model
        )

    def before_patch(self, args, kwargs, json_data=None):
        check_parent_group_before_change_a_relationship(
            "contacts/", self._data_layer.model
        )

    def before_delete(self, args, kwargs, json_data=None):
        check_parent_group_before_change_a_relationship(
            "contacts/", self._data_layer.model
        )

    schema = ContactSchema
    decorators = (token_required,)
    data_layer = {"session": db.session, "model": Contact}
