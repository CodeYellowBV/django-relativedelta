from dateutil.relativedelta import relativedelta
from django import forms
from django.test import TestCase
from testapp.models import Interval, IntervalWithChoice

IntervalForm = forms.modelform_factory(model=IntervalWithChoice, fields=forms.ALL_FIELDS)


class RelativeDeltaFormFieldTest(TestCase):
	def setUp(self):
		self.obj = Interval.objects.create(value=relativedelta(years=1))

	def test_unbound_form_rendering(self):
		form = IntervalForm()

		self.assertHTMLEqual(
			str(form['value']),
			'''
				<select name="value" id="id_value">
					<option value="" selected>---------</option>
					<option value="P1M">1 month</option>
					<option value="P3M">3 months</option>
					<option value="P6M">6 months</option>
				</select>
			'''
		)

	def test_bound_form_rendering(self):
		self.obj = Interval.objects.create(value=relativedelta(months=3))
		form = IntervalForm(instance=self.obj)

		self.assertHTMLEqual(
			str(form['value']),
			'''
				<select name="value" id="id_value">
					<option value="">---------</option>
					<option value="P1M">1 month</option>
					<option selected value="P3M">3 months</option>
					<option value="P6M">6 months</option>
				</select>
			'''
		)

	def test_form_submission_string_choice(self):
		self.obj = IntervalWithChoice.objects.create(value=relativedelta(months=1))
		data = {'value': 'P3M'}
		form = IntervalForm(data, instance=self.obj)
		self.assertTrue(form.is_valid())
		form.save()

		self.obj.refresh_from_db()
		self.assertEqual(self.obj.value, relativedelta(months=3))

	def test_form_submission_relativedelta_choice(self):
		self.obj = IntervalWithChoice.objects.create(value=relativedelta(months=1))
		data = {'value': 'P6M'}
		form = IntervalForm(data, instance=self.obj)
		self.assertTrue(form.is_valid())
		form.save()

		self.obj.refresh_from_db()
		self.assertEqual(self.obj.value, relativedelta(months=6))

	def test_form_submission_empty(self):
		self.obj = IntervalWithChoice.objects.create(value=relativedelta(months=1))
		data = {'value': ''}
		form = IntervalForm(data, instance=self.obj)
		self.assertTrue(form.is_valid())
		form.save()

		self.obj.refresh_from_db()
		self.assertIsNone(self.obj.value)
