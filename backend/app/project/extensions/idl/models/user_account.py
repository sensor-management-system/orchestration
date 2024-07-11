# SPDX-FileCopyrightText: 2022
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: EUPL-1.2

from dataclasses import dataclass
from typing import Any, Callable, List, Type, TypeVar, cast

from flask import current_app

T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def remove_prefix_from_ufz_idl(x: Any) -> str:
    """
    Remove the Prefix from uri due to idl implementation on ufz.
    This should be only temporary solution for this Problem!

    >> s = "/idl/permission-groups/dpvm-9"
    >> remove_prefix_from_ufz_idl(s)
    >>  "dpvm-9"

    :param string x: uir
    :return:
    """
    assert isinstance(x, str)
    return x.split("/")[-1]


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class UserAccount:
    id: str
    username: str
    administrated_permission_groups: List[str]
    membered_permission_groups: List[str]

    @staticmethod
    def from_dict(obj: Any) -> "UserAccount":
        assert isinstance(obj, dict)
        id = from_str(obj.get("id"))
        username = from_str(obj.get("userName"))
        if current_app.config["INSTITUTE"] == "ufz":
            administrated_permission_groups = from_list(
                remove_prefix_from_ufz_idl, obj.get("administratedPermissionGroups")
            )
            membered_permission_groups = from_list(
                remove_prefix_from_ufz_idl, obj.get("memberedPermissionGroups")
            )
        else:
            administrated_permission_groups = from_list(
                from_str, obj.get("administratedPermissionGroups")
            )
            membered_permission_groups = from_list(
                from_str, obj.get("memberedPermissionGroups")
            )
        return UserAccount(
            id, username, administrated_permission_groups, membered_permission_groups
        )


def idl_from_dict(s: dict) -> UserAccount:
    return UserAccount.from_dict(s)
