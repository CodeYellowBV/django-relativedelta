from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _

from datetime import timedelta

from relativedeltafield import forms
from relativedeltafield.utils import parse_relativedelta, format_relativedelta


class RelativeDeltaField(models.Field):
	"""Stores dateutil.relativedelta.relativedelta objects.

	Uses INTERVAL on PostgreSQL.
	"""
	empty_strings_allowed = False
	default_error_messages = {
		'invalid': _("'%(value)s' value has an invalid format. It must be in "
					 "ISO8601 interval format.")
	}
	description = _("RelativeDelta")

	def db_type(self, connection):
		if connection.settings_dict['ENGINE'] in (
		'django.db.backends.postgresql_psycopg2', 'django.db.backends.postgresql',
		'django.contrib.gis.db.backends.postgis'):
			return 'interval'
		else:
			raise ValueError(_('RelativeDeltaField only supports PostgreSQL for storage'))

	def to_python(self, value):
		if value is None:
			return value
		elif isinstance(value, relativedelta):
			return value.normalized()
		elif isinstance(value, timedelta):
			return (relativedelta() + value).normalized()

		try:
			return parse_relativedelta(value)
		except (ValueError, TypeError):
			raise ValidationError(
				self.error_messages['invalid'],
				code='invalid',
				params={'value': value},
			)

	def get_db_prep_value(self, value, connection, prepared=False):
		if value is None:
			return value
		else:
			return format_relativedelta(self.to_python(value))

	# This is a bit of a mindfuck.  We have to cast the output field
	# as text to bypass the standard deserialisation of PsycoPg2 to
	# datetime.timedelta, which loses information.  We then parse it
	# ourselves in convert_relativedeltafield_value().
	#
	# We make it easier for ourselves by doing some formatting here,
	# so that we don't need to rely on weird detection logic for the
	# current value of IntervalStyle (PsycoPg2 actually gets this
	# wrong; it only checks / sets DateStyle, but not IntervalStyle)
	#
	# We can't simply replace or remove PsycoPg2's parser, because
	# that would mess with any existing Django DurationFields, since
	# Django assumes PsycoPg2 returns pre-parsed datetime.timedeltas.
	def select_format(self, compiler, sql, params):
		fmt = 'to_char(%s, \'PYYYY"Y"MM"M"DD"DT"HH24"H"MI"M"SS.US"S"\')' % sql
		return fmt, params

	def get_db_converters(self, connection):
		return [self.convert_relativedeltafield_value]

	def convert_relativedeltafield_value(self, value, expression, connection, context):
		if value is not None:
			return parse_relativedelta(value)

	def value_to_string(self, obj):
		val = self.value_from_object(obj)
		return '' if val is None else format_relativedelta(val)

	def formfield(self, **kwargs):
		defaults = {'form_class': forms.RelativeDeltaField}
		defaults.update(kwargs)
		return super().formfield(**defaults)
