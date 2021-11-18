"""Module for the custom field detail resource."""
from flask_rest_jsonapi import ResourceDetail

from .base_resource import check_if_object_not_found
from ..models.base_model import db
from ..models.customfield import CustomField
from ..schemas.customfield_schema import CustomFieldSchema
from ..token_checker import token_required


class CustomFieldDetail(ResourceDetail):
    """
    Detail resource for custom fields.

    Provides get, patch & delete methods to retrieve
    a custom field, update it or to delete it.
    """

    def before_get(self, args, kwargs):
        """Return 404 Responses if CustomField not found"""
        check_if_object_not_found(self._data_layer.model, kwargs)

    schema = CustomFieldSchema
    decorators = (token_required,)
    data_layer = {
        "session": db.session,
        "model": CustomField,
    }
