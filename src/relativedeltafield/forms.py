import relativedeltafield
from dateutil.relativedelta import relativedelta
from django import forms


class RelativeDeltaChoiceField(forms.TypedChoiceField):
	def _set_choices(self, value):
		value = [(self.prepare_value(val), label) for val, label in value]
		super()._set_choices(value)
	choices = property(forms.TypedChoiceField._get_choices, _set_choices)

	def to_python(self, value):
		if value in self.empty_values:
			return None
		return relativedeltafield.parse_relativedelta(value)

	def prepare_value(self, value):
		if isinstance(value, relativedelta):
			return relativedeltafield.format_relativedelta(value)
		return super().prepare_value(value)

	def valid_value(self, value):
		value = self.prepare_value(value)
		return super().valid_value(value)
