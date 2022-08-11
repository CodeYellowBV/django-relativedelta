from django.core.exceptions import ValidationError
from django.db import models
from relativedeltafield.utils import (format_relativedelta,
                                      parse_relativedelta,
                                      relativedelta_as_csv)

try:
    from django.utils.translation import gettext_lazy as _
except ImportError:
    from django.utils.translation import ugettext as _


class RelativeDeltaDescriptor:
    def __init__(self, field) -> None:
        self.field = field

    def __get__(self, obj, objtype=None):
        if obj is None:
            return None
        value = obj.__dict__.get(self.field.name)
        if value is None:
            return None
        try:
            return parse_relativedelta(value)
        except ValueError as e:
            raise ValidationError({self.field.name: e})

    def __set__(self, obj, value):
        obj.__dict__[self.field.name] = value


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
    descriptor_class = RelativeDeltaDescriptor

    def get_lookup(self, lookup_name):
        ret = super().get_lookup(lookup_name)
        return ret

    def db_type(self, connection):
        if connection.vendor == 'postgresql':
            return 'interval'
        else:
            return 'varchar(33)'

    def get_db_prep_save(self, value, connection):
        if value is None:
            return None
        if connection.vendor == 'postgresql':
            return super().get_db_prep_save(value, connection)
        else:
            if isinstance(value, str):  # we need to convert it to the non-postgres format
                return relativedelta_as_csv(parse_relativedelta(value))
            return relativedelta_as_csv(value)

    def to_python(self, value):
        if value is None:
            return value
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
            if connection.vendor == 'postgresql':
                return format_relativedelta(self.to_python(value))
            else:
                return relativedelta_as_csv(self.to_python(value))

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
        if compiler.connection.vendor == 'postgresql':
            fmt = 'to_char(%s, \'PYYYY"Y"MM"M"DD"DT"HH24"H"MI"M"SS.US"S"\')' % sql
        else:
            fmt = sql
        return fmt, params

    def from_db_value(self, value, expression, connection, context=None):
        if value is not None:
            return parse_relativedelta(value)

    def value_to_string(self, obj):
        val = self.value_from_object(obj)
        return '' if val is None else format_relativedelta(val)
