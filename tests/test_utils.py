from datetime import timedelta
from unittest import TestCase

from dateutil.relativedelta import relativedelta

from relativedeltafield.utils import parse_relativedelta, relativedelta_as_csv


class ParseRelativedeltaTest(TestCase):
    def assertStrictEqual(self, a, b):
        self.assertEqual(a, b)
        self.assertEqual(type(a), type(b))

    def test_simple_parse_timedelta(self):
        self.assertStrictEqual(relativedelta(microseconds=300000.0), parse_relativedelta(timedelta(seconds=0.3)))
        self.assertStrictEqual(relativedelta(
            seconds=2, microseconds=300000.0), parse_relativedelta(timedelta(seconds=2.3))
        )
        self.assertStrictEqual(
            relativedelta(days=11, hours=18, minutes=11, seconds=50, microseconds=100010),
            parse_relativedelta(timedelta(weeks=1, days=4.5, hours=5, minutes=70.5, seconds=80.100005, microseconds=5))
        )

    def test_normalize_timedelta(self):
        self.assertStrictEqual(
            relativedelta(seconds=21, microseconds=600000.0),
            parse_relativedelta(timedelta(seconds=2.3, microseconds=19.3e6))
        )

    def test_parse_iso8601csv(self):
        """Test parsing the internal comma-separated-value representation"""
        self.assertStrictEqual(
            relativedelta(years=1925, months=9, days=-14, hours=-12, minutes=27, seconds=54, microseconds=-123456),
            parse_relativedelta('01925/009/-14 -12:027:054.-123456')
        )


class CSVFormatTest(TestCase):
    def test_csv_conversions(self):
        self.assertEqual(
            relativedelta_as_csv(relativedelta(years=1925, months=9, days=-4,
                                               hours=-12, minutes=27, seconds=54,
                                               microseconds=-123456)),
            '01925/009/-04 -12:027:054.-123456')
        self.assertEqual(
            parse_relativedelta('01925/009/-04 -12:027:054.-123456'),
            relativedelta(years=1925, months=9, days=-4,
                          hours=-12, minutes=27, seconds=54,
                          microseconds=-123456)
        )
        self.assertEqual(
            relativedelta_as_csv(relativedelta(years=-1925, months=9, days=-4,
                                               hours=-12, minutes=27, seconds=-54,
                                               microseconds=123456)),
            '-1925/009/-04 -12:027:-54.0123456')
        self.assertEqual(
            parse_relativedelta('-1925/009/-04 -12:027:-54.0123456'),
            relativedelta(years=-1925, months=9, days=-4,
                          hours=-12, minutes=27, seconds=-54,
                          microseconds=123456)
        )
