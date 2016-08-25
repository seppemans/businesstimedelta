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

    def test_add_exactly_one_period(self):
        td = BusinessTimeDelta(self.workdayrule, hours=8)
        dt = self.utc.localize(datetime.datetime(2016, 1, 22, 9, 0, 0))

        self.assertEqual(
            dt + td,
            self.utc.localize(datetime.datetime(2016, 1, 22, 17, 0, 0))
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

    def test_subtract_exactly_one_period(self):
        td = BusinessTimeDelta(self.workdayrule, hours=8)
        dt = self.utc.localize(datetime.datetime(2016, 1, 22, 18, 0, 0))

        self.assertEqual(
            dt - td,
            self.utc.localize(datetime.datetime(2016, 1, 22, 9, 0, 0))
        )

    def test_subtract_more_than_one_period(self):
        td = BusinessTimeDelta(self.workdayrule, hours=8)
        dt = self.utc.localize(datetime.datetime(2016, 1, 25, 11, 14, 0))

        self.assertEqual(
            dt - td,
            self.utc.localize(datetime.datetime(2016, 1, 22, 11, 14, 0))
        )

    def test_negation(self):
        td = BusinessTimeDelta(self.workdayrule, hours=120)
        dt = self.utc.localize(datetime.datetime(2016, 1, 25, 11, 14, 0))
        self.assertEqual(
            dt,
            dt + td - td
        )

    def test_hours_and_seconds_property(self):
        orig_td = datetime.timedelta(seconds=(3600*2)+1)
        td = BusinessTimeDelta(self.workdayrule, timedelta=orig_td)
        self.assertEqual(td.hours, 2)
        self.assertEqual(td.seconds, 1)

    def test_large_hours_and_seconds_property(self):
        orig_td = datetime.timedelta(seconds=(3600*365)+1)
        td = BusinessTimeDelta(self.workdayrule, timedelta=orig_td)
        self.assertEqual(td.hours, 365)
        self.assertEqual(td.seconds, 1)

    def test_small_hours_and_seconds_property(self):
        orig_td = datetime.timedelta(seconds=1)
        td = BusinessTimeDelta(self.workdayrule, timedelta=orig_td)
        self.assertEqual(td.hours, 0)
        self.assertEqual(td.seconds, 1)


class BusinessTimeDeltaArithmeticTest(unittest.TestCase):
    def setUp(self):
        self.utc = pytz.timezone('UTC')
        self.workdayrule = WorkDayRule(
            start_time=datetime.time(9),
            end_time=datetime.time(17),
            working_days=[0, 1, 2, 3, 4],
            tz=self.utc)

    def test_addition(self):
        td = BusinessTimeDelta(self.workdayrule, hours=2)
        td2 = BusinessTimeDelta(self.workdayrule, hours=3)
        self.assertEqual(
            td + td2,
            BusinessTimeDelta(self.workdayrule, hours=5)
        )

    def test_subtraction(self):
        td = BusinessTimeDelta(self.workdayrule, hours=3)
        td2 = BusinessTimeDelta(self.workdayrule, hours=1)
        self.assertEqual(
            td - td2,
            BusinessTimeDelta(self.workdayrule, hours=2)
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

        bdiff = businesshrs.difference(start, end)
        self.assertEqual(bdiff.hours, 40)
        self.assertEqual(bdiff.seconds, 0)

        self.assertEqual(
            str(start + BusinessTimeDelta(businesshrs, hours=40)),
            "2016-01-22 18:00:00+00:00"
        )

        self.assertEqual(
            str(end - BusinessTimeDelta(businesshrs, hours=40)),
            "2016-01-18 09:00:00+00:00"
        )

        ca_holidays = pyholidays.US(state='CA')
        holidays = HolidayRule(ca_holidays)
        businesshrs = Rules([workday, lunchbreak, holidays])

        start = datetime.datetime(2015, 12, 21, 9, 0, 0)
        end = datetime.datetime(2015, 12, 28, 9, 0, 0)
        bdiff = businesshrs.difference(start, end)
        self.assertEqual(bdiff.hours, 32)
        self.assertEqual(bdiff.seconds, 0)

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

        sf_tz = pytz.timezone('America/Los_Angeles')
        sf_start = sf_tz.localize(datetime.datetime(2016, 1, 18, 9, 0, 0))
        sf_end = sf_tz.localize(datetime.datetime(2016, 1, 18, 18, 0, 0))

        bdiff = santiago_businesshrs.difference(sf_start, sf_end)
        self.assertEqual(bdiff.hours, 4)
        self.assertEqual(bdiff.seconds, 0)
