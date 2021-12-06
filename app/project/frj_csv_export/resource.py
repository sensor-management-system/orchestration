# -*- coding: utf-8 -*-

"""This module contains the logic of resource management
Modifications: Adopted form Custom content negotiation #171 ( miLibris /
flask-rest-jsonapi ) """
import json
from flask.wrappers import Response as FlaskResponse
from werkzeug.wrappers import Response
import pandas as pd
from cherrypicker import CherryPicker
from flask import request, url_for, make_response
from flask_rest_jsonapi.decorators import (
    check_method_requirements,
    jsonapi_exception_formatter,
)
from flask_rest_jsonapi.pagination import add_pagination_links
from flask_rest_jsonapi.querystring import QueryStringManager as QSManager
from flask_rest_jsonapi.resource import Resource as ResourceBase
from flask_rest_jsonapi.resource import ResourceMeta as ResourceMetaBase
from flask_rest_jsonapi.schema import compute_schema
from flask_rest_jsonapi.utils import JSONEncoder
from marshmallow import ValidationError
from marshmallow_jsonapi.exceptions import IncorrectTypeError
from marshmallow_jsonapi.fields import BaseRelationship
from six import with_metaclass

from .content import parse_json, render_csv, render_json
from .exceptions import InvalidAcceptType


def transform_to_series(objects, schema):
    """
    Convert list of dictionaries to a pandas DataFrame and returns a flat CSV file.
    :param schema: MarshmallowSchema for the object
    :param objects: a list of the objects
    :return: dataframe
    """
    # CherryPicker for restructuring the data into flat tables
    # use the to_search_entry() to get the mode as a dict
    list_of_flat_dicts = []
    for obj in objects:
        picker = CherryPicker(schema().nested_dict_serializer(obj))
        flat_dict = picker.flatten().get()
        list_of_flat_dicts.append(flat_dict)

    # json_normalize() works with lists of dictionaries (records) to convert the list
    # to a pandas DataFrame, and in addition can also handle nested dictionaries.
    df = pd.json_normalize(list_of_flat_dicts)
    return df


class Resource(ResourceBase):
    """Base resource class"""

    def __new__(cls, request_parsers=None, response_renderers=None):
        """Constructor of a resource instance"""
        if hasattr(cls, "_data_layer"):
            cls._data_layer.resource = cls

        return super(Resource, cls).__new__(cls)

    def __init__(self, request_parsers=None, response_renderers=None):
        # Start with default parsers, but accept user provided ones
        self.request_parsers = {
            "application/vnd.api+json": parse_json,
            "application/json": parse_json,
        }
        if request_parsers is not None:
            self.request_parsers.update(request_parsers)

        # Start with default renderers, but accept user provided ones
        self.response_renderers = {
            "application/vnd.api+json": render_json,
            "application/json": render_json,
            "text/html": render_json,
            "text/csv": render_csv,
        }
        if response_renderers is not None:
            self.response_renderers.update(response_renderers)

    def parse_request(self):
        return self.request_parsers[request.content_type](request)

    @jsonapi_exception_formatter
    def dispatch_request(self, *args, **kwargs):
        """Logic of how to handle a request"""
        method = getattr(self, request.method.lower(), None)
        if method is None and request.method == "HEAD":
            method = getattr(self, "get", None)
        assert method is not None, "Unimplemented method {}".format(request.method)

        # Choose a renderer based on the Accept header
        if len(request.accept_mimetypes) < 1:
            # If the request doesn't specify a mimetype, assume JSON API
            accept_type = "application/vnd.api+json"
        elif request.accept_mimetypes.best not in self.response_renderers:
            # Check if we support the response type
            raise InvalidAcceptType(
                "This endpoint only provides the following content types: {}".format(
                    ", ".join(self.response_renderers.keys())
                )
            )
        else:
            accept_type = request.accept_mimetypes.best
        renderer = self.response_renderers[accept_type]

        response = method(*args, **kwargs)
        return renderer(response)


class ResourceList(with_metaclass(ResourceMetaBase, Resource)):
    """Base class of a resource list manager"""

    @check_method_requirements
    def get(self, *args, **kwargs):
        """Retrieve a collection of objects"""
        self.before_get(args, kwargs)

        qs = QSManager(request.args, self.schema)

        parent_filter = self._get_parent_filter(request.url, kwargs)
        _, objects = self.get_collection(qs, kwargs, filters=parent_filter)
        objects_count = len(objects)
        if "HTTP_ACCEPT" in request.headers.environ:
            http_accept = request.headers.environ["HTTP_ACCEPT"]
            if http_accept == "text/csv":
                return transform_to_series(objects, self.schema)
        schema_kwargs = getattr(self, "get_schema_kwargs", dict())
        schema_kwargs.update({"many": True})

        self.before_marshmallow(args, kwargs)

        schema = compute_schema(self.schema, schema_kwargs, qs, qs.include)

        result = schema.dump(objects)

        view_kwargs = (
            request.view_args if getattr(self, "view_kwargs", None) is True else dict()
        )
        add_pagination_links(
            result, objects_count, qs, url_for(self.view, _external=True, **view_kwargs)
        )

        result.update({"meta": {"count": objects_count}})

        final_result = self.after_get(result)

        return final_result

    @check_method_requirements
    def post(self, *args, **kwargs):
        """Create an object"""
        qs = QSManager(request.args, self.schema)
        json_data = self.parse_request()

        self.before_marshmallow(args, kwargs)

        schema = compute_schema(
            self.schema, getattr(self, "post_schema_kwargs", dict()), qs, qs.include
        )

        try:
            data = schema.load(json_data, partial=True)
        except IncorrectTypeError as e:
            errors = e.messages
            for error in errors["errors"]:
                error["status"] = "409"
                error["title"] = "Incorrect type"
            return errors, 409
        except ValidationError as e:
            errors = e.messages
            for message in errors["errors"]:
                message["status"] = "422"
                message["title"] = "Validation error"
            return errors, 422

        self.before_post(args, kwargs, data=data)

        obj = self.create_object(data, kwargs)

        result = schema.dump(obj)

        if result["data"].get("links", {}).get("self"):
            final_result = (result, 201, {"Location": result["data"]["links"]["self"]})
        else:
            final_result = (result, 201)

        result = self.after_post(final_result)

        return result

    def _get_parent_filter(self, url, kwargs):
        """
        Returns a dictionary of filters that should be applied to ensure only resources
        belonging to the parent resource are returned
        """

        url_segments = url.split("/")
        parent_segment = url_segments[-3]
        parent_id = url_segments[-2]

        for key, value in self.schema._declared_fields.items():
            if isinstance(value, BaseRelationship):
                if value.type_ == parent_segment:
                    return {value.id_field: parent_id}

        return {}

    def before_get(self, args, kwargs):
        """Hook to make custom work before get method"""

    def after_get(self, result):
        """Hook to make custom work after get method"""
        return result

    def before_post(self, args, kwargs, data=None):
        """Hook to make custom work before post method"""

    def after_post(self, result):
        """Hook to make custom work after post method"""
        return result

    def before_marshmallow(self, args, kwargs):
        pass

    def get_collection(self, qs, kwargs, filters=None):
        return self._data_layer.get_collection(qs, kwargs, filters=filters)

    def create_object(self, data, kwargs):
        return self._data_layer.create_object(data, kwargs)
