from django.contrib import admin

from testapp.models import Interval, IntervalWithChoice


@admin.register(Interval)
class IntervalAdmin(admin.ModelAdmin):
	list_display = ['value']
	list_filter = ['value']


@admin.register(IntervalWithChoice)
class IntervalWithChoiceAdmin(admin.ModelAdmin):
	list_display = ['value']
	list_filter = ['value']
