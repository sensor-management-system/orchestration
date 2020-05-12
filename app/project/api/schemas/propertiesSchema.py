from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Schema, Relationship


class PropertiesSchema(Schema):
    """
    This class create a schema for a properties.
    Every attribute in the schema going to expose through the api.
    It uses library called marshmallow-jsonapi that fit
    the JSONAPI 1.0 specification and provides Flask integration.

    """

    class Meta:
        type_ = 'properties'
        self_view = 'properties_detail'
        self_view_kwargs = {'id': '<id>'}

    id = fields.Integer(as_string=True, dump_only=True)
    accuracy = fields.Str(allow_none=True)
    label = fields.Str(allow_none=True)
    unit = fields.Str(allow_none=True)
    Compartment = fields.Str(required=True)
    measuringRangeMin = fields.Float(as_string=True, required=True)
    measuringRangeMax = fields.Float(as_string=True, required=True)
    failureValue = fields.Float(as_string=True, required=True)
    Variable = fields.Str(required=True)
    model = fields.Str(required=True)
    inventoryNumber = fields.Integer()
    src = fields.Str(allow_none=True)
    SamplingMedia = fields.Date(allow_none=True)
    persistentIdentifier = fields.Integer()

    device = Relationship(attribute='properties',
                          self_view='properties_events',
                          self_view_kwargs={'id': '<id>'},
                          related_view='properties_detail',
                          related_view_kwargs={'id': '<id>'},
                          schema='PropertiesSchema',
                          type_='properties')
