"""PID resources.."""
from flask import g, request
from flask_rest_jsonapi import ResourceDetail

from ..helpers.errors import (
    BadRequestError,
    UnauthorizedError,
)
from ...extensions.instances import pid
from ...frj_csv_export.resource import ResourceList


class PidList(ResourceList):
    def get(self, *args, **kwargs):
        """List Pids, or search PIDS for a term in url."""
        if not g.user:
            raise UnauthorizedError("Authentication required.")
        limit = request.args["limit"] if "limit" in request.args.keys() else None
        page = request.args["page"] if "page" in request.args.keys() else None
        if "term" in request.args:
            term = request.args["term"]
            response = pid.search_after_a_pid(term, limit)
        else:
            response = pid.list_pids(limit, page)
        return response

    def post(self, *args, **kwargs):
        """Create a new PID"""
        if not g.user:
            raise UnauthorizedError("Authentication required.")
        if "url" not in request.args.keys():
            raise BadRequestError("No url.")
        url = request.args["url"]
        persistent_identifier = pid.create_a_new_pid(url)
        response = {"pid": persistent_identifier}
        return response


class PidDetail(ResourceDetail):
    def get(self, *args, **kwargs):
        """GEt PID information."""
        if not g.user:
            raise UnauthorizedError("Authentication required.")
        if "pid" not in kwargs.keys():
            raise BadRequestError("No pid.")
        source_object_pid = kwargs["pid"]
        response = pid.get_a_pid(source_object_pid)
        return response

    def patch(self, *args, **kwargs):
        """Update PID."""
        if not g.user:
            raise UnauthorizedError("Authentication required.")
        if "pid" not in kwargs.keys() or "url" not in request.args.keys():
            raise BadRequestError("No pid or url.")
        source_object_pid = kwargs["pid"]
        updated_url = request.args["url"]
        return pid.update_existing_pid(source_object_pid, updated_url)

    def delete(self, *args, **kwargs):
        """Delete a PID."""
        if not g.user:
            raise UnauthorizedError("Authentication required.")
        if "pid" not in kwargs.keys():
            raise BadRequestError("No pid.")
        source_object_pid = kwargs["pid"]
        return pid.delete_a_pid(source_object_pid)
