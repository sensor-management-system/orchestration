"""Module for the custom field relationship resource."""
from flask_rest_jsonapi import ResourceRelationship

from project.api.models.base_model import db
from project.api.models.customfield import Customfield
from project.api.schemas.customfield_schema import CustomfieldSchema
from project.api.token_checker import token_required


class CustomfieldRelationship(ResourceRelationship):
    """
    Detail resource for custom fields.

    Provides methods to work with relationships
    between customfields and other objects.
    """

    schema = CustomfieldSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": Customfield,
    }
