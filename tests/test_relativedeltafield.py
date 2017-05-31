from django.test import TestCase

from .testapp.models import Interval

from dateutils import relativedelta

class RelativeDeltaFieldTest(TestCase):
	def test_basic_value_survives_db_roundtrip(self):
		input_value = relativedelta(years=2,months=3,days=4,hours=5,minutes=52,seconds=30,microseconds=5)
		obj = Interval(value=input_value)
		obj.save()

		obj.refresh_from_db()
		self.assertEqual(input_value, obj.value)


	def test_none_value_also_survives_db_roundtrip(self):
		obj = Interval(value=None)
		obj.save()

		obj.refresh_from_db()
		self.assertIsNone(obj.value)


	def test_value_is_normalized_on_full_clean(self):
		input_value = relativedelta(years=1,months=3,days=4.5,hours=5,minutes=70.5,seconds=80.100005,microseconds=5)
		obj = Interval(value=input_value)
		obj.full_clean()

		self.assertNotEqual(input_value, obj.value)
		self.assertEqual(input_value.normalized(), obj.value)

		# Quick sanity check to ensure the input isn't mutated
		self.assertEqual(4.5, input_value.days)

		# Check that the values are normalized
		self.assertEqual(4, obj.value.days)
		self.assertEqual(18, obj.value.hours)
		self.assertEqual(11, obj.value.minutes)
		self.assertEqual(50, obj.value.seconds)
		self.assertEqual(100010, obj.value.microseconds)
