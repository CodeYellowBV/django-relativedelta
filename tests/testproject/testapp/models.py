from django.db import models
from src.relativedeltafield import RelativeDeltaField

class Interval(models.Model):
	value=RelativeDeltaField(null=True, blank=True)
