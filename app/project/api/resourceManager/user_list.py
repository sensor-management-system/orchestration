from ..models.base_model import db
from ..models.user import User
from ..schemas.user_schema import UserSchema
from ..token_checker import token_required
from ...frj_csv_export.resource import ResourceList


class UserList(ResourceList):
    """
    provides get and post methods to retrieve a
    collection of Events or create one.
    """

    schema = UserSchema
    decorators = (token_required,)
    data_layer = {"session": db.session, "model": User}
