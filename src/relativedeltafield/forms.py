from django import forms
from django.core.exceptions import ValidationError

from relativedeltafield.utils import parse_relativedelta, format_relativedelta


class RelativeDeltaFormField(forms.CharField):

    def prepare_value(self, value):
        try:
            return format_relativedelta(value)
        except Exception:
            return value

    def to_python(self, value):
        return parse_relativedelta(value)

    def clean(self, value):
        try:
            return parse_relativedelta(value)
        except Exception:
            raise ValidationError('Not a valid (extended) ISO8601 interval specification', code='format')
