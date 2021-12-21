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


def before_mount_action(data):
    """

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
        raise ConflictError("Private device can't be used in a configuration.")

    beginn_date_as_string = data["attributes"]["begin_date"]
    beginn_date = dateutil.parser.parse(beginn_date_as_string).isoformat()

    if last_mount_action and not last_unmount_action:
        raise ConflictError(
            f"Device is mounted on {last_mount_action.configuration.label} since \
            {last_mount_action.begin_date} and has no unmount date."
        )

    elif last_mount_action and last_unmount_action:
        if last_mount_action.begin_date > last_unmount_action.end_date:
            raise ConflictError(
                f"Device still Mounted on {last_mount_action.configuration.label}"
            )

        if beginn_date < last_unmount_action.end_date.isoformat():
            raise ConflictError(
                f"Device still Mounted on {last_mount_action.configuration.label} till: \
                        {last_unmount_action.end_date}"
            )
