import datetime
import unittest
import pytz
from ...rules.workdayrules import WorkDayRule
from ...businesstimedelta import BusinessTimeDelta


class RuleTest(unittest.TestCase):
    def setUp(self):
        self.pst = pytz.timezone('US/Pacific')
        self.utc = pytz.timezone('UTC')
        self.workdayrule = WorkDayRule(
            start_time=datetime.time(9),
            end_time=datetime.time(17),
            working_days=[0, 1, 2, 3, 4],
            tz=self.utc)

    def test_difference_less_than_one_period(self):
        start_dt = self.utc.localize(datetime.datetime(2016, 1, 21, 10, 0, 0))
        end_dt = self.utc.localize(datetime.datetime(2016, 1, 21, 10, 0, 5))

        self.assertEqual(
            self.workdayrule.difference(start_dt, end_dt),
            BusinessTimeDelta(self.workdayrule, seconds=5)
        )

    def test_difference_more_than_one_period(self):
        start_dt = self.utc.localize(datetime.datetime(2016, 1, 20, 10, 0, 0))
        end_dt = self.utc.localize(datetime.datetime(2016, 1, 21, 10, 0, 5))

        self.assertEqual(
            self.workdayrule.difference(start_dt, end_dt),
            BusinessTimeDelta(self.workdayrule, hours=8, seconds=5)
        )

    def test_difference_several_days_period(self):
        start_dt = self.utc.localize(datetime.datetime(2016, 1, 18, 2, 0, 0))
        end_dt = self.utc.localize(datetime.datetime(2016, 1, 24, 0, 0, 0))

        self.assertEqual(
            self.workdayrule.difference(start_dt, end_dt),
            BusinessTimeDelta(self.workdayrule, hours=8 * 5)
        )


class AdversarialRuleTest(unittest.TestCase):
    def test_no_workday_hours(self):
        self.workdayrule = WorkDayRule(
            start_time=datetime.time(9),
            end_time=datetime.time(9),
            working_days=[0, 1, 2, 3, 4])

        start_dt = datetime.datetime(2016, 1, 21, 10, 0, 0)
        end_dt = datetime.datetime(2016, 1, 21, 10, 0, 5)

        self.assertEqual(
            self.workdayrule.difference(start_dt, end_dt),
            BusinessTimeDelta(self.workdayrule, seconds=0, hours=0)
        )


class NightShiftRuleTest(unittest.TestCase):
    def setUp(self):
        self.utc = pytz.timezone('UTC')
        self.workdayrule = WorkDayRule(
            start_time=datetime.time(23),
            end_time=datetime.time(1),
            working_days=[0, 1, 2, 3, 4],
            tz=self.utc)

    def test_difference_overnight(self):
        start_dt = self.utc.localize(datetime.datetime(2016, 1, 21, 10, 0, 0))
        end_dt = self.utc.localize(datetime.datetime(2016, 1, 22, 10, 0, 0))

        self.assertEqual(
            BusinessTimeDelta(self.workdayrule, hours=2),
            self.workdayrule.difference(start_dt, end_dt)
        )
