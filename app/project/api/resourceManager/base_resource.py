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
        class_name = obj.capitalize()  # Contact
        object_id = obj + '_id'  # contact_id
        # to import a module dynamically
        module = __import__("project.api.models." + obj)
        object_class = getattr(module, class_name)
        instance = object_class()
        try:
            object_ = self.session.query(instance).filter_by(
                id=view_kwargs[object_id]).one()
        except NoResultFound:
            raise ObjectNotFound({'parameter': object_id},
                                 "{}: {} not found".format(
                                     instance, view_kwargs[object_id]))
        else:
            if object_.device is not None:
                view_kwargs['id'] = object_.device.id
            else:
                view_kwargs['id'] = None
