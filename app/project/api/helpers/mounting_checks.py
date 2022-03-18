import dateutil.parser


from sqlalchemy import desc

from .errors import ConflictError
from ..models import (
    Device,
    DeviceMountAction,
    DeviceUnmountAction,
    Platform,
    PlatformUnmountAction,
    PlatformMountAction,
)
from ... import db


def assert_object_is_free_to_be_mounted(data):
    """
    Methode to check if the object is not attached to any configuration before attempting to
    mount it.

    - Mounting between x1_1 and x1_2 will through an exception that this object is mounted till x1_2 datetime.
    - Mounting ina date after x2_1 will als raise an exception that the object is mounted
        on a configuration and has no unmount date.
    - Also trying to Mount a Private Object through an exception.

    ---------x1_1---------------x1_2------------x2_1------------------>

    :TODO: Find a suitable solution for Mounting Overlap

    :param data: the incoming request data
    """
    if "device" in data["relationships"]:

        object_id = data["relationships"]["device"]["data"]["id"]

        object_ = db.session.query(Device).filter_by(id=object_id).one_or_none()
        last_mount_action = (
            db.session.query(DeviceMountAction)
            .filter_by(device_id=object_id)
            .order_by(desc(DeviceMountAction.begin_date))
            .first()
        )
        last_unmount_action = (
            db.session.query(DeviceUnmountAction)
            .filter_by(device_id=object_id)
            .order_by(desc(DeviceUnmountAction.end_date))
            .first()
        )
    else:
        object_id = data["relationships"]["platform"]["data"]["id"]
        object_ = db.session.query(Platform).filter_by(id=object_id).one_or_none()
        last_mount_action = (
            db.session.query(PlatformMountAction)
            .filter_by(platform_id=object_id)
            .order_by(desc(PlatformMountAction.begin_date))
            .first()
        )
        last_unmount_action = (
            db.session.query(PlatformUnmountAction)
            .filter_by(platform_id=object_id)
            .order_by(desc(PlatformUnmountAction.end_date))
            .first()
        )
    if object_.is_private:
        raise ConflictError("Private object can't be used in a configuration.")

    begin_date_as_string = data["attributes"]["begin_date"]
    beginn_date = dateutil.parser.parse(begin_date_as_string).replace(tzinfo=None)
    if last_mount_action and not last_unmount_action:
        raise ConflictError(
            f"Object is mounted on {last_mount_action.configuration.label} since \
            {last_mount_action.begin_date} and has no unmount date."
        )

    elif last_mount_action and last_unmount_action:
        if last_mount_action.begin_date > last_unmount_action.end_date:
            raise ConflictError(
                f"Object still Mounted on {last_mount_action.configuration.label}"
            )

        if beginn_date < last_unmount_action.end_date:
            raise ConflictError(
                f"Object still Mounted on {last_mount_action.configuration.label} till: \
                        {last_unmount_action.end_date}"
            )
