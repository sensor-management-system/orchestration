"""Some shortcuts for the views."""

from ..api.helpers.errors import NotFoundError
from ..api.models.base_model import db


def get_object_or_404(model, ident):
    """Mimiks the django get_object_or_404 shortcut function."""
    object = db.session.query(model).get(ident)
    if not object:
        raise NotFoundError("Object not found!")
    return object
