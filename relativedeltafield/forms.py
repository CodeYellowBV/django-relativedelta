from dateutil.relativedelta import relativedelta
from django.forms import Field

from relativedeltafield.utils import format_relativedelta


class RelativeDeltaField(Field):
	def prepare_value(self, value):
		if isinstance(value, relativedelta):
			return format_relativedelta(value)
		return value
