from flask import request

from .permission_utils import (
    check_for_permissions,
    check_patch_permission,
    check_deletion_permission,
    check_permissions_for_related_objects,
)

protected_views = [
    "api.device_detail",
    "api.device_list",
    "api.platform_detail",
    "api.platform_list",
]
related_objects_protected_views = [
    "api.device_mount_action_list",
    "api.device_mount_action_detail",
    "api.platform_mount_action_list",
    "api.platform_mount_action_detail",
]


def permission_manager(view, view_args, view_kwargs, *args, **kwargs):
    """The function used to check permissions

    :param callable view: the view
    :param list view_args: view args
    :param dict view_kwargs: view kwargs
    :param list args: decorator args
    :param dict kwargs: decorator kwargs
    """

    if view_args[0].view in protected_views:
        method = request.method
        if method == "GET":
            if "id" in view_kwargs:
                kwargs["id"] = view_kwargs["id"]
                check_for_permissions(view_args[0].data_layer["model"], kwargs)
        elif method == "PATCH":
            check_patch_permission(view_kwargs, view_args[0].data_layer["model"])
        elif method == "DELETE":
            check_deletion_permission(view_kwargs, view_args[0].data_layer["model"])

    elif view_args[0].view in related_objects_protected_views:

        method = request.method
        if method == "GET":
            if "id" in view_kwargs:
                kwargs["id"] = view_kwargs["id"]
                check_permissions_for_related_objects(
                    view_args[0].data_layer["model"], kwargs["id"]
                )
    #     elif method == "PATCH":
    #         check_patch_permission_for_related_objects(
    #             view_kwargs, view_args[0].data_layer["model"]
    #         )
    #     elif method == "DELETE":
    #         check_deletion_permission_for_related_objects(
    #             view_kwargs, view_args[0].data_layer["model"]
    #         )
