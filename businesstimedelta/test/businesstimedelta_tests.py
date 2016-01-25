import datetime
import unittest
import pytz
from ..rules import Rules, WorkDayRule, LunchTimeRule, HolidayRule
from ..businesstimedelta import BusinessTimeDelta
import holidays as pyholidays


class BusinessTimeDeltaTest(unittest.TestCase):
    def setUp(self):
        self.pst = pytz.timezone('US/Pacific')
        self.utc = pytz.timezone('UTC')
        self.workdayrule = WorkDayRule(
            start_time=datetime.time(9),
            end_time=datetime.time(17),
            working_days=[0, 1, 2, 3, 4],
            tz=self.utc)

    def test_add_less_than_one_period(self):
        td = BusinessTimeDelta(self.workdayrule, hours=2)
        dt = self.utc.localize(datetime.datetime(2016, 1, 23, 13, 14, 0))

        self.assertEqual(
            dt + td,
            self.utc.localize(datetime.datetime(2016, 1, 25, 11, 0, 0))
        )

    def test_add_more_than_one_period(self):
        td = BusinessTimeDelta(self.workdayrule, hours=12)
        dt = self.utc.localize(datetime.datetime(2016, 1, 23, 13, 14, 0))

        self.assertEqual(
            dt + td,
            self.utc.localize(datetime.datetime(2016, 1, 26, 13, 0, 0))
        )

    def test_subtract_less_than_one_period(self):
        td = BusinessTimeDelta(self.workdayrule, hours=2)
        dt = self.utc.localize(datetime.datetime(2016, 1, 25, 11, 14, 0))

        self.assertEqual(
            dt - td,
            self.utc.localize(datetime.datetime(2016, 1, 25, 9, 14, 0))
        )

    def test_subtract_more_than_one_period(self):
        td = BusinessTimeDelta(self.workdayrule, hours=8)
        dt = self.utc.localize(datetime.datetime(2016, 1, 25, 11, 14, 0))

        self.assertEqual(
            dt - td,
            self.utc.localize(datetime.datetime(2016, 1, 22, 11, 14, 0))
        )


class ReadmeTest(unittest.TestCase):
    def test_readme(self):
        workday = WorkDayRule(
            start_time=datetime.time(9),
            end_time=datetime.time(18),
            working_days=[0, 1, 2, 3, 4],
            tz=pytz.utc)

        lunchbreak = LunchTimeRule(
            start_time=datetime.time(12),
            end_time=datetime.time(13),
            working_days=[0, 1, 2, 3, 4])

        businesshrs = Rules([workday, lunchbreak])

        start = datetime.datetime(2016, 1, 18, 9, 0, 0)
        end = datetime.datetime(2016, 1, 25, 9, 0, 0)
        self.assertEqual(
            str(businesshrs.difference(start, end)),
            "<BusinessTimeDelta 40 hours 0 seconds>"
        )

        self.assertEqual(
            str(start + BusinessTimeDelta(businesshrs, hours=40)),
            "2016-01-25 09:00:00+00:00"
        )

        self.assertEqual(
            str(end - BusinessTimeDelta(businesshrs, hours=40)),
            "2016-01-15 18:00:00+00:00"
        )

        ca_holidays = pyholidays.US(state='CA')
        holidays = HolidayRule(ca_holidays)
        businesshrs = Rules([workday, lunchbreak, holidays])

        start = datetime.datetime(2015, 12, 21, 9, 0, 0)
        end = datetime.datetime(2015, 12, 28, 9, 0, 0)
        self.assertEqual(
            str(businesshrs.difference(start, end)),
            "<BusinessTimeDelta 32 hours 0 seconds>"
        )

    def test_readme_localized(self):
        santiago_workday = WorkDayRule(
            start_time=datetime.time(9),
            end_time=datetime.time(18),
            working_days=[0, 1, 2, 3, 4],
            tz=pytz.timezone('America/Santiago'))

        santiago_lunchbreak = LunchTimeRule(
            start_time=datetime.time(12),
            end_time=datetime.time(13),
            working_days=[0, 1, 2, 3, 4],
            tz=pytz.timezone('America/Santiago'))

        santiago_businesshrs = Rules([santiago_workday, santiago_lunchbreak])

        sf_start = datetime.datetime(2016, 1, 18, 9, 0, 0, tzinfo=pytz.timezone('America/Los_Angeles'))
        sf_end = datetime.datetime(2016, 1, 18, 18, 0, 0, tzinfo=pytz.timezone('America/Los_Angeles'))

        self.assertEqual(
            str(santiago_businesshrs.difference(sf_start, sf_end)),
            "<BusinessTimeDelta 4 hours 0 seconds>"
        )
