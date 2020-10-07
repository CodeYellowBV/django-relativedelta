import pytest


@pytest.fixture
def dummy_intervals(db):
    from testapp.models import Interval
    yield [
        Interval.objects.create(date='2020-03-06'),
        Interval.objects.create(date='2020-10-06'),
    ]
