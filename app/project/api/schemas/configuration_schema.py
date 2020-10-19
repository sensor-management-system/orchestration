from marshmallow_jsonapi import fields
from marshmallow_jsonapi.flask import Schema, Relationship

from project.api.schemas.contact_schema import ContactSchema
from project.api.schemas.device_property_schema import DevicePropertySchema

from project.api.serializer.configuration_hierarchy_field import ConfigurationHierarchyField


class ConfigurationSchema(Schema):
    """
    This class create a schema for a configuration

    """

    class Meta:
        type_ = "configuration"
        self_view = "configuration_detail"
        self_view_kwargs = {"id": "<id>"}

    id = fields.Integer(as_string=True, dump_only=True)
    start_date = fields.DateTime()
    end_date = fields.DateTime()
    location_type = fields.String(required=True)
    longitude = fields.Float()
    latitude = fields.Float()
    elevation = fields.Float()
    project_uri = fields.String()
    project_name = fields.String()
    label = fields.String()
    status = fields.String(default="draft")
    hierarchy = ConfigurationHierarchyField(allow_none=True)

    longitude_src_device_property = Relationship(
        self_view_kwargs={"id": "<id>"},
        related_view="device_property_detail",
        related_view_kwargs={"id": "<longitude_src_device_property_id>"},
        type_="device_property",
    )

    latitude_src_device_property = Relationship(
        self_view_kwargs={"id": "<id>"},
        related_view="device_property_detail",
        related_view_kwargs={"id": "<latitude_src_device_property_id>"},
        type_="device_property",
    )

    elevation_src_device_property = Relationship(
        self_view_kwargs={"id": "<id>"},
        related_view="device_property_detail",
        related_view_kwargs={"id": "<elevation_src_device_property_id>"},
        type_="device_property",
    )

    contacts = Relationship(
        attribute="contacts",
        self_view_kwargs={"id": "<id>"},
        related_view="contact_list",
        related_view_kwargs={"filter": '[{"name":"configurations","op":"any","val":'
                                       '{"name": "id","op": "eq","val": <id>}'
                                       '}]'
                             },
        many=True,
        schema="ContactSchema",
        type_="contact",
        id_field="id",
    )
