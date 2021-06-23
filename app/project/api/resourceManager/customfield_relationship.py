"""Module for the custom field relationship resource."""
from flask_rest_jsonapi import ResourceRelationship

from ..models.base_model import db
from ..models.customfield import CustomField
from ..schemas.customfield_schema import CustomFieldSchema
from ..token_checker import token_required


class CustomFieldRelationship(ResourceRelationship):
    """
    Relationship resource for custom fields.

    Provides methods to work with relationships
    between customfields and other objects.
    """

    schema = CustomFieldSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": CustomField,
    }
