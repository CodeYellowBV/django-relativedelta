from django.db import models
from relativedeltafield import RelativeDeltaField

class Interval(models.Model):
	value=RelativeDeltaField()
