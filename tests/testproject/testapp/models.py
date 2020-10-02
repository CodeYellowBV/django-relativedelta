import datetime

from django.db import models
from relativedeltafield import RelativeDeltaField


class Interval(models.Model):
    value = RelativeDeltaField(null=True, blank=True)
    date = models.DateField(default=datetime.date(2020, 10, 21))
