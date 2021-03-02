"""Module for the custom field detail resource."""
from flask_rest_jsonapi import ResourceDetail

from project.api.models.base_model import db
from project.api.models.customfield import CustomField
from project.api.schemas.customfield_schema import CustomFieldSchema
from project.api.token_checker import token_required


class CustomFieldDetail(ResourceDetail):
    """
    Detail resource for custom fields.

    Provides get, patch & delete methods to retrieve
    a custom field, update it or to delete it.
    """

    schema = CustomFieldSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": CustomField,
    }
