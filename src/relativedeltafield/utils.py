""" .. currentmodule:: relativedelta.utils"""

import re
import typing
from datetime import timedelta

from dateutil.relativedelta import relativedelta

# This is not quite ISO8601, as it allows the SQL/Postgres extension
# of allowing a minus sign in the values, and you can mix weeks with
# other units (which ISO doesn't allow).
iso8601_duration_re: re.Pattern = re.compile(
    r'P'
    r'(?:(?P<years>-?\d+(?:\.\d+)?)Y)?'
    r'(?:(?P<months>-?\d+(?:\.\d+)?)M)?'
    r'(?:(?P<weeks>-?\d+(?:\.\d+)?)W)?'
    r'(?:(?P<days>-?\d+(?:\.\d+)?)D)?'
    r'(?:T'
    r'(?:(?P<hours>-?\d+(?:\.\d+)?)H)?'
    r'(?:(?P<minutes>-?\d+(?:\.\d+)?)M)?'
    r'(?:(?P<seconds>-?\d+(?:\.\d+)?)S)?'
    r')?'
    r'$'
)

# This is the comma-separated internal value to be used for databases non supporting the interval type natively
iso8601_csv_re: re.Pattern = re.compile(
    r"^(?P<years>^[-\d]\d{4})/(?P<months>[-\d]\d{2})/(?P<days>[-\d]\d{2}) "
    r"(?P<hours>[-\d]\d{2}):(?P<minutes>[-\d]\d{2}):(?P<seconds>[-\d]\d{2})\."
    r"(?P<microseconds>[-\d]\d{6})$"
)


# Parse ISO8601 timespec
def parse_relativedelta(
    value: typing.Optional[typing.Union[relativedelta, timedelta, str]]
) -> typing.Union[relativedelta, typing.NoReturn]:
    """Parses a relative delta, time delta or string into ISO08601

    Raises:

        ValueError: IS the value is not an ISO08601 spec
    """
    if value is None or value == '':
        return None

    if isinstance(value, timedelta):
        microseconds = value.seconds % 1 * 1e6 + value.microseconds
        seconds = int(value.seconds)
        return relativedelta(days=value.days, seconds=seconds, microseconds=microseconds)

    if isinstance(value, relativedelta):
        return value.normalized()

    if isinstance(value, str):
        try:
            m = iso8601_duration_re.match(value) or iso8601_csv_re.match(value)
            if m:
                args = {}
                for k, v in m.groupdict().items():
                    if v is None:
                        args[k] = 0
                    elif '.' in v:
                        args[k] = float(v)
                    else:
                        args[k] = int(v)
                return relativedelta(**args).normalized() if m else None
        except Exception:  # pylint: disable=broad-except
            pass
    raise ValueError('Not a valid (extended) ISO8601 interval specification')


def relativedelta_as_csv(self) -> str:
    """TODO: Docstring"""
    return '%05d/%03d/%03d %03d:%03d:%03d.%07d' % (
        self.years,
        self.months,
        self.days,
        self.hours,
        self.minutes,
        self.seconds,
        self.microseconds
    )


def format_relativedelta(relativedelta_: relativedelta) -> str:
    """Format ISO8601 timespec"""
    result_big: str = ''
    # TODO: We could always include all components, but that's kind of
    # ugly, since one second would be formatted as 'P0Y0M0W0DT0M1S'
    if relativedelta_.years:
        result_big += f'{relativedelta_.years}Y'

    if relativedelta_.months:
        result_big += f'{relativedelta_.months}M'

    if relativedelta_.days:
        result_big += f'{relativedelta_.days}D'

    result_small: str = ''
    if relativedelta_.hours:
        result_small += f'{relativedelta_.hours}H'

    if relativedelta_.minutes:
        result_small += f'{relativedelta_.minutes}M'

    # Microseconds is allowed here as a convenience, the user may have
    # used normalized(), which can result in microseconds
    if relativedelta_.seconds:
        seconds: float = relativedelta_.seconds
        if relativedelta_.microseconds:
            seconds += relativedelta_.microseconds / 1000000.0
        result_small += f'{seconds}S'

    if len(result_small) > 0:
        return f'P{result_big}T{result_small}'

    if len(result_big) == 0:
        return 'P0D'  # Doesn't matter much what field is zero, but just 'P' is invalid syntax, and so is ''

    return f'P{result_big}'
