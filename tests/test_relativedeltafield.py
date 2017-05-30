from django.test import TestCase

from .testapp.models import Interval

from dateutils import relativedelta

class RelativeDeltaFieldTest(TestCase):
	def test_basic_value_survives_db_roundtrip(self):
		input_value = relativedelta(years=2,months=3,hours=5,minutes=52,seconds=30.00005)
		obj = Interval(value=input_value)
		obj.save()

		obj.refresh_from_db()
		self.assertEqual(input_value, obj.value)
