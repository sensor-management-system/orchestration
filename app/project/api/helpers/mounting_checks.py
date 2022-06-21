"""Check functions to ensure consistency for mounts."""

#import dateutil.parser
#from sqlalchemy import and_
#
#from ... import db
#from ..models import Device, DeviceMountAction, Platform, PlatformMountAction
#from .date_time_range import DateTimeRange
#from .errors import ConflictError


def assert_object_is_free_to_be_mounted(data):
    """
    Check if the object is not attached to any configuration before attempting to mount it.

    - Mounting between m1 and u1 will through an exception that this object is mounted
      till x1_2 datetime.
    - Mounting in a date after m2 will als raise an exception that the object is mounted
        on a configuration and has no unmount date.
    - Also trying to Mount a Private Object through an exception.

    ---------m1---------------u1------------m2------------------>

    :param data: the incoming request data
    """
    #current_id = data.get("id")
    #begin_date_as_string = data["attributes"]["begin_date"]
    #begin_date = dateutil.parser.parse(begin_date_as_string).replace(tzinfo=None)
    #end_date_as_string = data["attributes"].get("end_date")
    #if end_date_as_string:
    #    end_date = dateutil.parser.parse(end_date_as_string).replace(tzinfo=None)
    #else:
    #    end_date = None
    #if "device" in data["relationships"]:

    #    object_id = data["relationships"]["device"]["data"]["id"]
    #    object_ = db.session.query(Device).filter_by(id=object_id).one_or_none()
    #    existing_mounts = db.session.query(DeviceMountAction).filter(
    #        and_(
    #            DeviceMountAction.id != current_id,
    #            DeviceMountAction.device_id == object_id,
    #        )
    #    )
    #else:
    #    object_id = data["relationships"]["platform"]["data"]["id"]
    #    object_ = db.session.query(Platform).filter_by(id=object_id).one_or_none()
    #    existing_mounts = db.session.query(PlatformMountAction).filter(
    #        and_(
    #            PlatformMountAction.id != current_id,
    #            PlatformMountAction.platform_id == object_id,
    #        )
    #    )
    #if object_.is_private:
    #    raise ConflictError("Private object can't be used in a configuration.")

    #try:
    #    new_planned_range = DateTimeRange(begin_date, end_date)
    #    for mount_action in existing_mounts:
    #        existing_range = DateTimeRange(
    #            mount_action.begin_date, mount_action.end_date
    #        )
    #        if new_planned_range.overlaps_with(existing_range):
    #            raise ConflictError(
    #                f"Object is blocked due to  usage in {mount_action.configuration.label} since \
    #                        {mount_action.begin_date}"
    #            )
    #except ValueError as e:
    #    raise ConflictError(str(e))

    # TODO: We decided to remove this temporarly.
    # So, once we want to re-introduce it, we are going to do that.
    pass
