"""Module for the custom field detail resource."""
from flask_rest_jsonapi import ResourceDetail

from project.api.models.base_model import db
from project.api.models.customfield import Customfield
from project.api.schemas.customfield_schema import CustomfieldSchema
from project.api.token_checker import token_required


class CustomfieldDetail(ResourceDetail):
    """
    Detail resource for custom fields.

    Provides get, patch & delete methods to retrieve
    a custom field, update it or to delete it.
    """

    schema = CustomfieldSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": Customfield,
    }
