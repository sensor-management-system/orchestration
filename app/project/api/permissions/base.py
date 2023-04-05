# SPDX-FileCopyrightText: 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Some base classes based on handling in the django rest framework."""

# From https://github.com/encode/django-rest-framework/blob/master/rest_framework/permissions.py

from flask import request
from marshmallow.exceptions import ValidationError


class OperationHolderMixin:
    """Mixin to combine permission classes."""

    def __and__(self, other):
        """Combine both entries so that both must be valid."""
        return OperandHolder(AND, self, other)

    def __or__(self, other):
        """Combine both entries so that only one must be valid."""
        return OperandHolder(OR, self, other)

    def __rand__(self, other):
        """Combine both entries so that both must be valid."""
        return OperandHolder(AND, other, self)

    def __ror__(self, other):
        """Combine both entries so that only one must be valid."""
        return OperandHolder(OR, other, self)

    def __invert__(self):
        """Invert one permission class check."""
        return SingleOperandHolder(NOT, self)


class SingleOperandHolder(OperationHolderMixin):
    """Class to transform one permission class."""

    def __init__(self, operator_class, op1_class):
        """Init the object."""
        self.operator_class = operator_class
        self.op1_class = op1_class

    def __call__(self, *args, **kwargs):
        """Run the operator on the one permission class."""
        op1 = self.op1_class(*args, **kwargs)
        return self.operator_class(op1)


class OperandHolder(OperationHolderMixin):
    """Class to transform/combine two permission classes."""

    def __init__(self, operator_class, op1_class, op2_class):
        """Init the object."""
        self.operator_class = operator_class
        self.op1_class = op1_class
        self.op2_class = op2_class

    def __call__(self, *args, **kwargs):
        """Combine both permission classes."""
        op1 = self.op1_class(*args, **kwargs)
        op2 = self.op2_class(*args, **kwargs)
        return self.operator_class(op1, op2)


class AND:
    """Logic to combine two permission classes with AND logic."""

    def __init__(self, op1, op2):
        """Init the object."""
        self.op1 = op1
        self.op2 = op2

    def has_permission(self, view, view_args, view_kwargs, *args, **kwargs):
        """Return true if both permission classes apply successfully."""
        return self.op1.has_permission(
            view, view_args, view_kwargs, *args, **kwargs
        ) and self.op2.has_permission(view, view_args, view_kwargs, *args, **kwargs)

    def has_object_permission(self, view, view_args, view_kwargs, obj, *args, **kwargs):
        """Retrn true if both permission classes apply for the object."""
        return self.op1.has_object_permission(
            view, view_args, view_kwargs, obj, *args, **kwargs
        ) and self.op2.has_object_permission(
            view, view_args, view_kwargs, obj, *args, **kwargs
        )


class OR:
    """Logic to combine two permission classes with OR logic."""

    def __init__(self, op1, op2):
        """Init the object."""
        self.op1 = op1
        self.op2 = op2

    def has_permission(self, view, view_args, view_kwargs, *args, **kwargs):
        """Return true of one of the permission classes apply successfully."""
        return self.op1.has_permission(
            view, view_args, view_kwargs, *args, **kwargs
        ) or self.op2.has_permission(view, view_args, view_kwargs, *args, **kwargs)

    def has_object_permission(self, view, view_args, view_kwargs, obj, *args, **kwargs):
        """Return true of one of the permission classes apply for the object."""
        return self.op1.has_object_permission(
            view, view_args, view_kwargs, obj, *args, **kwargs
        ) or self.op2.has_object_permission(
            view, view_args, view_kwargs, obj, *args, **kwargs
        )


class NOT:
    """Logic to invert one permission class."""

    def __init__(self, op1):
        """Init the object."""
        self.op1 = op1

    def has_permission(self, view, view_args, view_kwargs, *args, **kwargs):
        """Return true if the inner permission class doesn't apply."""
        return not self.op1.has_permission(
            view, view_args, view_kwargs, *args, **kwargs
        )

    def has_object_permission(self, view, view_args, view_kwargs, obj, *args, **kwargs):
        """Return true if the inner permission class doesn't apply."""
        return not self.op1.has_object_permission(
            view, view_args, view_kwargs, obj, *args, **kwargs
        )


class BasePermissionMetaclass(OperationHolderMixin, type):
    """Base meta class for the permissions."""

    pass


class BasePermission(metaclass=BasePermissionMetaclass):
    """Base class for the permissions."""

    def has_permission(self, view, view_args, view_kwargs, *args, **kwargs):
        """Return always true."""
        return True

    def has_object_permission(self, view, view_args, view_kwargs, obj, *args, **kwargs):
        """Return always true."""
        return True


class ModelPermission(BasePermission):
    """Base class for checks on the object permissions."""

    id_attribute = "id"

    def has_permission(self, view, view_args, view_kwargs, *args, **kwargs):
        """Return true if we have the permissions on the object."""
        if request.method == "POST":
            try:
                data = view_args[0].schema().load(request.json)
                return self.has_create_permission(
                    view, view_args, view_kwargs, data, *args, **kwargs
                )
            except ValidationError:
                # this will be handled by other parts of the application.
                # So we don't care here.
                return True
        if not view_kwargs.get(self.id_attribute):
            # This handler doesn't apply here as it is not about one single entry.
            return True
        resource = view_args[0]
        data_layer = resource.data_layer
        obj = (
            data_layer["session"]
            .query(data_layer["model"])
            .filter_by(**view_kwargs)
            .first()
        )
        if obj:
            return self.has_object_permission(
                view, view_args, view_kwargs, obj, *args, **kwargs
            )
        # Not found, so we can't apply this permission set.
        # The other logic may handle that.
        return True
