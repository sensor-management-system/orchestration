from flask_rest_jsonapi import ResourceRelationship

from project.api.models.base_model import db
from project.api.schemas.customfield_schema import CustomFieldSchema
from project.api.models.customfield import CustomField


class CustomFieldRelationship(ResourceRelationship):
    """
    provides get, post, patch and delete methods to get relationships,
    create relationships, update relationships and delete
    relationships between Customfield and other objects.
    """
    schema = CustomFieldSchema
    data_layer = {'session': db.session,
                  'model': CustomField}
