# import dateutil.parser

from sqlalchemy import desc

# from .errors import ConflictError
from ..models import (
    # Device,
    DeviceMountAction,
    DeviceUnmountAction,
    # Platform,
    PlatformUnmountAction,
    PlatformMountAction,
)
from ... import db


def assert_object_is_free_to_be_mounted(data):
    """
    Methode to check if the object is not attached to any configuration before attempting to
    mount it.

    - Mounting between m1 and u1 will through an exception that this object is mounted till x1_2 datetime.
    - Mounting ina date after m2 will als raise an exception that the object is mounted
        on a configuration and has no unmount date.
    - Also trying to Mount a Private Object through an exception.

    ---------m1---------------u1------------m2------------------>

    :TODO: Find a suitable solution for Mounting Overlap

    :param data: the incoming request data
    """
    # if "device" in data["relationships"]:
    #
    #     object_id = data["relationships"]["device"]["data"]["id"]
    #     object_ = db.session.query(Device).filter_by(id=object_id).one_or_none()
    #     (
    #         first_mount_action,
    #         last_mount_action,
    #         last_unmount_action,
    #     ) = device_mount_and_unmount_dates(object_id)
    # else:
    #     object_id = data["relationships"]["platform"]["data"]["id"]
    #     object_ = db.session.query(Platform).filter_by(id=object_id).one_or_none()
    #     (
    #         first_mount_action,
    #         last_mount_action,
    #         last_unmount_action,
    #     ) = platform_mount_and_unmount_dates(object_id)
    # if object_.is_private:
    #     raise ConflictError("Private object can't be used in a configuration.")
    #
    # begin_date_as_string = data["attributes"]["begin_date"]
    # begin_date = dateutil.parser.parse(begin_date_as_string).replace(tzinfo=None)
    # # 1- Begin date is before the first mounted begin date and there is no end date
    # # ------mx----------m1--------------->
    # # TODO: make it possible if user set unmount date before first mount begin
    # if first_mount_action and (begin_date <= first_mount_action.begin_date):
    #     raise ConflictError(
    #         f"Object will be mounted on {first_mount_action.configuration.label} on \
    #                 {first_mount_action.begin_date}"
    #     )
    # # 2- Begin date is after last mounted begin date and there is no end date
    # # --------m1----------------------->
    # if (last_mount_action and not last_unmount_action) and (
    #         begin_date >= last_mount_action.begin_date
    # ):
    #     raise ConflictError(
    #         f"Object is mounted on {last_mount_action.configuration.label} since \
    #         {last_mount_action.begin_date} and has no unmount date."
    #     )
    # # 3- Begin date is between mount and unmount date.
    # # --------m1-----mx------u1------------>
    # elif last_mount_action and last_unmount_action:
    #     if last_mount_action.begin_date <= begin_date <= last_unmount_action.end_date:
    #         raise ConflictError(
    #             f"Object still Mounted on {last_mount_action.configuration.label} till: \
    #                     {last_unmount_action.end_date}"
    #         )
    #     # 4- Begin date is between unmount and mount date.
    #     # --------m1------u1----mx------m2------->
    #     # TODO: make it possible if the user accept to set unmount date before the last beginn date.
    #     elif last_unmount_action.end_date <= begin_date <= last_mount_action.begin_date:
    #         raise ConflictError(
    #             f"Object will be mounted on {last_mount_action.configuration.label} at: \
    #                     {last_mount_action.begin_date}"
    #         )

    # outsource mount & unmount logic to another branch.
    pass


def device_mount_and_unmount_dates(object_id):
    last_mount_action = (
        db.session.query(DeviceMountAction)
        .filter_by(device_id=object_id)
        .order_by(desc(DeviceMountAction.begin_date))
        .first()
    )
    first_mount_action = (
        db.session.query(DeviceMountAction)
        .filter_by(device_id=object_id)
        .order_by(DeviceMountAction.begin_date)
        .first()
    )
    last_unmount_action = (
        db.session.query(DeviceUnmountAction)
        .filter_by(device_id=object_id)
        .order_by(desc(DeviceUnmountAction.end_date))
        .first()
    )
    return first_mount_action, last_mount_action, last_unmount_action


def platform_mount_and_unmount_dates(object_id):
    last_mount_action = (
        db.session.query(PlatformMountAction)
        .filter_by(platform_id=object_id)
        .order_by(desc(PlatformMountAction.begin_date))
        .first()
    )
    first_mount_action = (
        db.session.query(PlatformMountAction)
        .filter_by(platform_id=object_id)
        .order_by(PlatformMountAction.begin_date)
        .first()
    )
    last_unmount_action = (
        db.session.query(PlatformUnmountAction)
        .filter_by(platform_id=object_id)
        .order_by(desc(PlatformUnmountAction.end_date))
        .first()
    )
    return first_mount_action, last_mount_action, last_unmount_action
