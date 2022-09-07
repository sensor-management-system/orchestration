"""Resources for the usage statistics."""
from ...frj_csv_export.resource import ResourceList
from ..helpers.errors import MethodNotAllowed
from ..models import Configuration, Device, Platform, User
from ..models.base_model import db


class UsageStatistics(ResourceList):
    """Resource class to get usage statistics."""

    def get(self):
        """
        Return a response for the usage statistics.

        Currently those are mainly counts for the models, but
        we can extend those later.
        """
        models_to_query = {
            "devices": Device,
            "platforms": Platform,
            "configurations": Configuration,
            "users": User,
        }
        counts = {}
        for model_name, model in models_to_query.items():
            count = db.session.query(model).count()
            counts[model_name] = count

        return {
            "counts": counts,
        }

    def post(self):
        """Don't allow post requests."""
        raise MethodNotAllowed("endpoint is readonly")
