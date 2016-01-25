import datetime
import unittest
import pytz
import holidays as holidaymodule
from ...rules.holidayrules import HolidayRule


class HolidayRuleTest(unittest.TestCase):
    def setUp(self):
        self.pst = pytz.timezone('US/Pacific')
        self.utc = pytz.timezone('UTC')
        self.holidays = [
            datetime.date(2015, 12, 25),
            datetime.date(2016, 12, 25),
            datetime.date(2017, 12, 25)
        ]

    def test_repr(self):
        holiday = HolidayRule(self.holidays, tz=self.utc)

        self.assertEqual(
            str(holiday)[:12],
            "<HolidayRule"
        )

    def test_next_before_holiday(self):
        dt = self.utc.localize(datetime.datetime(2016, 1, 23, 12, 43, 0))
        holiday = HolidayRule(self.holidays, tz=self.utc)

        self.assertEqual(
            holiday.next(dt),
            (
                self.utc.localize(datetime.datetime(2016, 12, 25, 0, 0, 0)),
                self.utc.localize(datetime.datetime(2016, 12, 25, 23, 59, 59))
            )
        )

    def test_next_during_holiday(self):
        dt = self.utc.localize(datetime.datetime(2016, 12, 25, 12, 0, 0))
        holiday = HolidayRule(self.holidays, tz=self.utc)

        self.assertEqual(
            holiday.next(dt),
            (
                dt,
                self.utc.localize(datetime.datetime(2016, 12, 25, 23, 59, 59))
            )
        )

    def test_next_after_holiday(self):
        dt = self.utc.localize(datetime.datetime(2016, 12, 26, 0, 0, 0))
        holiday = HolidayRule(self.holidays, tz=self.utc)

        self.assertEqual(
            holiday.next(dt),
            (
                self.utc.localize(datetime.datetime(2017, 12, 25, 0, 0, 0)),
                self.utc.localize(datetime.datetime(2017, 12, 25, 23, 59, 59))
            )
        )

    def test_next_during_holiday_start_edge(self):
        dt = self.utc.localize(datetime.datetime(2016, 12, 25, 0, 0, 0))
        holiday = HolidayRule(self.holidays, tz=self.utc)

        self.assertEqual(
            holiday.next(dt),
            (
                dt,
                self.utc.localize(datetime.datetime(2016, 12, 25, 23, 59, 59))
            )
        )

    def test_next_during_holiday_end_edge(self):
        dt = self.utc.localize(datetime.datetime(2016, 12, 25, 23, 59, 59))
        holiday = HolidayRule(self.holidays, tz=self.utc)

        self.assertEqual(
            holiday.next(dt),
            (
                self.utc.localize(datetime.datetime(2016, 12, 25, 0, 0, 0)),
                dt
            )
        )

    def test_next_during_holiday_cross_timezone(self):
        dt = self.pst.localize(datetime.datetime(2016, 12, 24, 20, 0, 0))
        holiday = HolidayRule(self.holidays, tz=self.utc)

        self.assertEqual(
            holiday.next(dt),
            (
                dt.astimezone(self.utc),
                self.utc.localize(datetime.datetime(2016, 12, 25, 23, 59, 59))
            )
        )

    def test_previous_before_holiday(self):
        dt = self.utc.localize(datetime.datetime(2016, 1, 22, 0, 0, 0))
        holiday = HolidayRule(self.holidays, tz=self.utc)

        self.assertEqual(
            holiday.previous(dt),
            (
                self.utc.localize(datetime.datetime(2015, 12, 25, 0, 0, 0)),
                self.utc.localize(datetime.datetime(2015, 12, 25, 23, 59, 59))
            )
        )

    def test_previous_after_holiday(self):
        dt = self.utc.localize(datetime.datetime(2016, 12, 27, 0, 0, 0))
        holiday = HolidayRule(self.holidays, tz=self.utc)

        self.assertEqual(
            holiday.previous(dt),
            (
                self.utc.localize(datetime.datetime(2016, 12, 25, 0, 0, 0)),
                self.utc.localize(datetime.datetime(2016, 12, 25, 23, 59, 59))
            )
        )

    def test_previous_during_holiday(self):
        dt = self.utc.localize(datetime.datetime(2016, 12, 25, 12, 0, 0))
        holiday = HolidayRule(self.holidays, tz=self.utc)

        self.assertEqual(
            holiday.previous(dt),
            (
                self.utc.localize(datetime.datetime(2016, 12, 25, 0, 0, 0)),
                dt
            )
        )

    def test_next_with_holiday_module(self):
        dt = self.utc.localize(datetime.datetime(2015, 12, 23, 12, 0, 0))
        holiday = HolidayRule(holidaymodule.US(), tz=self.utc)

        self.assertEqual(
            holiday.next(dt),
            (
                self.utc.localize(datetime.datetime(2015, 12, 25, 0, 0, 0)),
                self.utc.localize(datetime.datetime(2015, 12, 25, 23, 59, 59)),
            )
        )

    def test_previous_with_holiday_module(self):
        dt = self.utc.localize(datetime.datetime(2015, 12, 26, 12, 0, 0))
        holiday = HolidayRule(holidaymodule.US(), tz=self.utc)

        self.assertEqual(
            holiday.previous(dt),
            (
                self.utc.localize(datetime.datetime(2015, 12, 25, 0, 0, 0)),
                self.utc.localize(datetime.datetime(2015, 12, 25, 23, 59, 59)),
            )
        )
