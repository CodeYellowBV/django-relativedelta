from django.test import TestCase

from .testapp.models import Interval

from datetime import timedelta
from dateutils import relativedelta

class RelativeDeltaFieldTest(TestCase):
	def setUp(self):
		Interval.objects.all().delete()


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
		self.assertEqual(1, obj.value.years)
		self.assertEqual(3, obj.value.months)
		self.assertEqual(4, obj.value.days)
		self.assertEqual(18, obj.value.hours)
		self.assertEqual(11, obj.value.minutes)
		self.assertEqual(50, obj.value.seconds)
		self.assertEqual(100010, obj.value.microseconds)


	def test_string_input(self):
		obj = Interval(value='P1Y3M4.5DT5H70.5M80.10001S')
		obj.full_clean()

		self.assertIsInstance(obj.value, relativedelta)

		# Check that the values are normalized
		self.assertEqual(1, obj.value.years)
		self.assertEqual(3, obj.value.months)
		self.assertEqual(4, obj.value.days)
		self.assertEqual(18, obj.value.hours)
		self.assertEqual(11, obj.value.minutes)
		self.assertEqual(50, obj.value.seconds)
		self.assertEqual(100010, obj.value.microseconds)


	def test_timedelta_input(self):
		td = timedelta(days=4.5,hours=5,minutes=70.5,seconds=80.100005,microseconds=5)
		obj = Interval(value=td)
		obj.full_clean()

		self.assertIsInstance(obj.value, relativedelta)

		# Check that the values are normalized
		self.assertEqual(0, obj.value.years)
		self.assertEqual(0, obj.value.months)
		self.assertEqual(4, obj.value.days)
		self.assertEqual(18, obj.value.hours)
		self.assertEqual(11, obj.value.minutes)
		self.assertEqual(50, obj.value.seconds)
		self.assertEqual(100010, obj.value.microseconds)


	def test_filtering_works(self):
		obj1 = Interval(value='P1Y3M4.5DT5H70.5M80.10001S')
		obj1.save()

		obj2 = Interval(value='P12D')
		obj2.save()

		q = Interval.objects.filter(value__gt='P1Y')
		self.assertEqual(1, q.count())

		q = Interval.objects.filter(value__lt='P2Y')
		self.assertEqual(2, q.count())
