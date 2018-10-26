import re

from dateutil.relativedelta import relativedelta


# This is not quite ISO8601, as it allows the SQL/Postgres extension
# of allowing a minus sign in the values, and you can mix weeks with
# other units (which ISO doesn't allow).
iso8601_duration_re = re.compile(
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

# Parse ISO8601 timespec
def parse_relativedelta(str):
	m = iso8601_duration_re.match(str)
	if m:
		args = {}
		for k, v in m.groupdict().items():
			if v is  None:
				args[k] = 0
			elif '.' in v:
				args[k] = float(v)
			else:
				args[k] = int(v)
		return relativedelta(**args).normalized() if m else None

	raise ValueError('Not a valid (extended) ISO8601 interval specification')


# Format ISO8601 timespec
def format_relativedelta(relativedelta):
	result_big = ''
	# TODO: We could always include all components, but that's kind of
	# ugly, since one second would be formatted as 'P0Y0M0W0DT0M1S'
	if relativedelta.years:
		result_big += '{}Y'.format(relativedelta.years)
	if relativedelta.months:
		result_big += '{}M'.format(relativedelta.months)
	if relativedelta.days:
		result_big += '{}D'.format(relativedelta.days)

	result_small = ''
	if relativedelta.hours:
		result_small += '{}H'.format(relativedelta.hours)
	if relativedelta.minutes:
		result_small += '{}M'.format(relativedelta.minutes)
	# Microseconds is allowed here as a convenience, the user may have
	# used normalized(), which can result in microseconds
	if relativedelta.seconds:
		seconds = relativedelta.seconds
		if relativedelta.microseconds:
			seconds += relativedelta.microseconds / 1000000.0
		result_small += '{}S'.format(seconds)

	if len(result_small) > 0:
		return 'P{}T{}'.format(result_big, result_small)
	elif len(result_big) == 0:
		return 'P0D' # Doesn't matter much what field is zero, but just 'P' is invalid syntax, and so is ''
	else:
		return 'P{}'.format(result_big)
