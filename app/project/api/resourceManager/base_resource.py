from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.orm.exc import NoResultFound


class BaseResourceDetail():
    """
    Base Resource detail
    """

    def query_an_object(self, view_kwargs, obj):
        """

        :param kwargs:
        :return:
        """
        obj_class = obj.capitalize()
        obj_id = obj + '_id'
        module = __import__("project.api.models." + obj)
        the_class = getattr(module, obj_class)
        try:
            object_ = self.session.query(the_class).filter_by(
                id=view_kwargs[obj_id]).one()
        except NoResultFound:
            raise ObjectNotFound({'parameter': obj_id},
                                 "{}: {} not found".format(
                                     obj_class, view_kwargs[obj_id]))
        else:
            if object_.device is not None:
                view_kwargs['id'] = object_.device.id
            else:
                view_kwargs['id'] = None
