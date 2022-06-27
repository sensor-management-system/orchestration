from dataclasses import dataclass
from typing import Any, Callable, List, Type, TypeVar, cast

T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class_dict(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class PermissionGroup:
    """
    Permission group class.

    Compared to the IDL specific class, we only handle
    those attributes here that we want to return to
    a client for the SMS (to shhow a list of groups).
    So a list of permission groups will not contain the
    membership information.
    """

    id: str
    name: str
    description: str

    @staticmethod
    def from_dict(obj: dict) -> "PermissionGroup":
        assert isinstance(obj, dict)
        id = from_str(obj.get("id"))
        name = from_str(obj.get("name"))
        description = from_str(obj.get("description"))
        return PermissionGroup(
            id,
            name,
            description,
        )

    def to_dict(self) -> dict:
        """
        Follow the JSON:API style guid to serialize the dictionary.

        :return:
        """
        attributes: dict = {
            "name": from_str(self.name),
            "description": from_str(self.description),
        }
        result: dict = {
            "id": from_str(self.id),
            "type": "permission_group",
            "attributes": attributes,
        }
        return result


def permission_groups_from_list_of_dicts(s: List) -> List[PermissionGroup]:
    return from_list(PermissionGroup.from_dict, s)


def permission_groups_to_list_of_jsonapi_dicts(x: List[PermissionGroup]) -> List:
    return from_list(lambda x: to_class_dict(PermissionGroup, x), x)
