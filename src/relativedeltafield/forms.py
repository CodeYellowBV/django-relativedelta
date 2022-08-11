""" .. currentmodule:: relativedelta.forms"""

from dateutil.relativedelta import relativedelta

from django import forms  # pylint: disable=import-error
from django.core.exceptions import ValidationError
from relativedeltafield.utils import format_relativedelta, parse_relativedelta


class RelativeDeltaFormField(forms.CharField):
    """Field for use in Django forms for relative time deltas"""

    def prepare_value(self, value: str) -> relativedelta:
        """Coerce the value into ISO ISO8601 format"""
        try:
            return format_relativedelta(value)

        except Exception:  # pylint: disable=W0703
            return value

    def to_python(self, value: str) -> relativedelta:
        """Coerce the value into a python relativedelta object"""
        return parse_relativedelta(value)

    def clean(self, value: str) -> relativedelta:
        """Validate the data

        Raises:

            ValidationError: when the value can not be coerced into ISO8601

        """
        try:
            return parse_relativedelta(value)

        except Exception as exc:
            raise ValidationError(
                'Not a valid (extended) ISO8601 interval specification',
                code='format'
            ) from exc
