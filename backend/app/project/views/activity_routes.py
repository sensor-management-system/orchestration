# SPDX-FileCopyrightText: 2024
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Tobias Kuhnert <tobias.kuhnert@ufz.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Routes to access information about the activities."""

import dateutil.parser
from flask import Blueprint, request
from sqlalchemy import func, text
from sqlalchemy.sql import select

from ..api.helpers.errors import BadRequestError
from ..api.models import ActivityLog
from ..api.models.base_model import db
from ..config import env
from .utils import handle_json_api_errors

activity_routes = Blueprint(
    "activity_routes", __name__, url_prefix=env("URL_PREFIX", "/rdm/svm-api/v1")
)


@activity_routes.route("/controller/global-activities", methods=["GET"])
@handle_json_api_errors
def global_activity():
    """Return the json with contributions per day.

    The result will look like
    {
        "2024-07-04": 3,
        "2024-07-05": 7,
        "2024-07-08": 1
    }

    So it is a summary per day.
    """
    if "earliest" not in request.args.keys():
        raise BadRequestError("Need an 'earliest' parameter for temporal boundary")
    if "latest" not in request.args.keys():
        raise BadRequestError("Need an 'latest' parameter for temporal boundary")
    earliest_str = request.args["earliest"]
    latest_str = request.args["latest"]

    try:
        earliest = dateutil.parser.parse(earliest_str)
        latest = dateutil.parser.parse(latest_str)
    except dateutil.parser.ParserError:
        raise BadRequestError("Parameters must be ISO 8601")

    # Executes the following query:

    # with cte_days as (
    #     select to_char(created_at, 'YYYY-MM-DD') as day
    #     from activity_log
    #     where created_at >= :earliest
    #     and created_at <= :latest
    # )
    # select
    #     day,
    #     count(*) as count
    # from cte_days
    # group by day

    # It first filters the activities by the time interval that we gave.
    # Then we convert the date-time of creation to a date.
    # And third we group by that date & count how many entries we have per day.

    cte_days = (
        select([func.to_char(ActivityLog.created_at, "YYYY-MM-DD").label("day")])
        .where(ActivityLog.created_at >= text(":earliest"))
        .where(ActivityLog.created_at <= text(":latest"))
        .cte("cte_days")
    )

    query = select([cte_days.c.day, func.count().label("count")]).group_by(
        cte_days.c.day
    )

    # Execute the query
    query_result = db.session.execute(query, {"earliest": earliest, "latest": latest})

    data = []
    for row in query_result.fetchall():
        data.append({"date": row["day"], "count": row["count"]})
    return {"data": data}
    query_result = db.session.execute(
        text(query), {"earliest": earliest, "latest": latest}
    )
    data = []
    for row in query_result.fetchall():
        data.append({"date": row["day"], "count": row["count"]})
    return {"data": data}
