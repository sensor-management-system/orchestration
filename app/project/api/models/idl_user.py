from dataclasses import dataclass
from typing import List, Any, Callable, TypeVar, Type, cast

T = TypeVar("T")


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class IdlUser:
    id: int
    username: str
    administrated_permissions_groups: List[int]
    membered_permissions_groups: List[int]

    @staticmethod
    def from_dict(obj: Any) -> "IdlUser":
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        username = from_str(obj.get("username"))
        administrated_permissions_groups = from_list(
            from_int, obj.get("administratedPermissionsGroups")
        )
        membered_permissions_groups = from_list(
            from_int, obj.get("memberedPermissionsGroups")
        )
        return IdlUser(
            id, username, administrated_permissions_groups, membered_permissions_groups
        )


def idl_from_dict(s: dict) -> IdlUser:
    return IdlUser.from_dict(s)
