# -*- coding: utf-8 -*-

"""This module contains the main class of the Api to initialize the Api,
plug default decorators for each resources
methods, speficy which blueprint to use, define the Api routes and plug
additional oauth manager and permission manager
- Modifications: Adopted form Custom content negotiation #171 ( miLibris /
flask-rest-jsonapi )
"""

from flask_rest_jsonapi import Api as APIBase


class Api(APIBase):
    """The main class of the Api"""

    def __init__(
        self,
        app=None,
        blueprint=None,
        decorators=None,
        request_parsers=None,
        response_renderers=None,
    ):
        """Initialize an instance of the Api

        :param app: the flask application
        :param blueprint: a flask blueprint
        :param tuple decorators: a tuple of decorators plugged to each resource methods
        """
        super().__init__(
            app=app,
            blueprint=blueprint,
            decorators=decorators,
        ),
        # Store any custom parsers and renderers, which will be passed to the resources
        self.request_parsers = request_parsers or {}
        self.response_renderers = response_renderers or {}

    def init_app(
        self,
        app=None,
        blueprint=None,
        additional_blueprints=None,
        request_parsers=None,
        response_renderers=None,
    ):
        """Update flask application with our api

        :param Application app: a flask application
        """
        if app is not None:
            self.app = app

        if blueprint is not None:
            self.blueprint = blueprint

        for resource in self.resources:
            self.route(
                resource["resource"],
                resource["view"],
                *resource["urls"],
                url_rule_options=resource["url_rule_options"],
            )

        if self.blueprint is not None:
            self.app.register_blueprint(self.blueprint)

        if additional_blueprints is not None:
            for blueprint in additional_blueprints:
                self.app.register_blueprint(blueprint)

        self.app.config.setdefault("PAGE_SIZE", 30)
        # Store any custom parsers and renderers, which will be passed to the resources
        self.request_parsers = request_parsers or {}
        self.response_renderers = response_renderers or {}

    def route(self, resource, view, *urls, **kwargs):
        """Create an api view.

        :param Resource resource: a resource class inherited from
        flask_rest_jsonapi.resource.Resource
        :param str view: the view name
        :param list urls: the urls of the view
        :param dict kwargs: additional options of the route
        """
        resource.view = view
        url_rule_options = kwargs.get("url_rule_options") or dict()

        view_func = resource.as_view(
            view,
            request_parsers=self.request_parsers,
            response_renderers=self.response_renderers,
        )
        if "blueprint" in kwargs:
            resource.view = ".".join([kwargs["blueprint"].name, resource.view])
            for url in urls:
                kwargs["blueprint"].add_url_rule(
                    url, view_func=view_func, **url_rule_options
                )
        elif self.blueprint is not None:
            resource.view = ".".join([self.blueprint.name, resource.view])
            for url in urls:
                self.blueprint.add_url_rule(
                    url, view_func=view_func, **url_rule_options
                )
        elif self.app is not None:
            for url in urls:
                self.app.add_url_rule(url, view_func=view_func, **url_rule_options)
        else:
            self.resources.append(
                {
                    "resource": resource,
                    "view": view,
                    "urls": urls,
                    "url_rule_options": url_rule_options,
                }
            )
        self.resource_registry.append(resource)
