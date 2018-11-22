import numbers
from decimal import Decimal

from .base import Field


class NumericField(Field):
    def serialize(self, value):
        if not isinstance(value, numbers.Number):
            if value:
                raise ValueError("Value must be numeric.")
        return value

    def deserialize(self, value):
        if value is None:
            return value
        try:
            if self.label == 'Estimate':
                return round(Decimal(value), 6)
            else:
                return int(value)
        except ValueError:
            pass
        try:
            return float(value)
        except ValueError:
            pass

        # If we've made it this far, somehow Taskwarrior has
        # a non-numeric value stored in this field; this shouldn't
        # happen, but it's probably inappropriate to blow up.
        return value
