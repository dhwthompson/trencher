from django.test import TestCase
from datetime import date

from .dates import date_name

class DateNameTestCase(TestCase):

    def test_today(self):
        today = date(2020, 6, 1)
        self.assertEqual(date_name(date(2020, 6, 1), today=today), "Today")

    def test_tomorrow(self):
        today = date(2020, 6, 1)
        self.assertEqual(date_name(date(2020, 6, 2), today=today), "Tomorrow")

    def test_later_in_the_week(self):
        today = date(2020, 6, 1)
        self.assertEqual(date_name(date(2020, 6, 7), today=today), "Sunday")

    def test_earlier_in_the_week(self):
        # Dates in the past should always be explicit
        today = date(2020, 6, 4)
        self.assertEqual(date_name(date(2020, 6, 2), today=today), "Tuesday 2 Jun")

    def test_within_a_week(self):
        # Next week, but less than a week away
        today = date(2020, 6, 4)
        self.assertEqual(date_name(date(2020, 6, 8), today=today), "Monday")

    def test_a_week_away(self):
        today = date(2020, 6, 4)
        self.assertEqual(date_name(date(2020, 6, 11), today=today), "Thursday 11 Jun")

