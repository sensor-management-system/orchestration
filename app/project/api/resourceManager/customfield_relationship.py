"""Module for the custom field relationship resource."""
from flask_rest_jsonapi import ResourceRelationship

from project.api.models.base_model import db
from project.api.models.customfield import CustomField
from project.api.schemas.customfield_schema import CustomFieldSchema
from project.api.token_checker import token_required


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
