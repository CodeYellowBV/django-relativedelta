from django.contrib import admin

from testapp.models import Interval, IntervalWithChoices


@admin.register(Interval)
class IntervalAdmin(admin.ModelAdmin):
    list_display = ['value']
    list_filter = ['value']
