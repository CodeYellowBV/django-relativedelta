from dateutil.relativedelta import relativedelta
from django.db import models
from relativedeltafield import RelativeDeltaField


class Interval(models.Model):
	value=RelativeDeltaField(null=True, blank=True)


class IntervalWithChoice(models.Model):
	CHOICES = [
		(relativedelta(months=1), '1 month'),
		('P3M', '3 months'),
		(relativedelta(months=6), '6 months'),
	]
	value=RelativeDeltaField(null=True, blank=True, choices=CHOICES)
