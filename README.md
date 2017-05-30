# django-relativedelta

A Django field for the [`dateutils.relativedelta`](https://labix.org/python-dateutil#head-ba5ffd4df8111d1b83fc194b97ebecf837add454) class,
which conveniently maps to the [PostgresQL `INTERVAL` type](https://www.postgresql.org/docs/current/static/datatype-datetime.html#DATATYPE-INTERVAL-INPUT).

The standard [Django `DurationField`](https://docs.djangoproject.com/en/1.10/ref/models/fields/#durationfield)
maps to [Python's `datetime.timedelta`](https://docs.python.org/3/library/datetime.html#datetime.timedelta), which
has support for days and weeks, but not for years and months.  And if you try to read an `INTERVAL` that contains
months anyway, information is lost because each month gets converted to 30 days.

You should use this package when you need to store payment intervals
(which tend to be monthly or quarterly), publication intervals (which
can be weekly but also monthly) and so on, or when you simply don't
know what the intervals are going to be and want to offer some
flexibility.

If you want to use more advanced recurring dates, you should consider
using [django-recurrence](https://github.com/django-recurrence/django-recurrence)
instead.  This maps to the [`dateutils.rrule`](https://labix.org/python-dateutil#head-ba5ffd4df8111d1b83fc194b97ebecf837add454)
class, but it doesn't use native database field types, so you can't
perform arithmetic on them within the database.

## Limitations

Because this field is backed by an `INTERVAL` column, it neither
supports the relative `microseconds`, `weekday`, `leapdays`, `yearday`
and `nlyearday` arguments, nor the absolute arguments `year`, `month`,
`day`, `hour`, `second` and `microsecond`.

It does support fractional specifications, so a floating-point
`seconds` field allows for specifying microseconds with some loss of
precision due to the floating-point representation.

Databases other than PostgreSQL are not supported.
