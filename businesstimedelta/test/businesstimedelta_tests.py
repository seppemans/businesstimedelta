import datetime
import unittest
import pytz
from ..rules.workdayrules import WorkDayRule
from ..businesstimedelta import BusinessTimeDelta


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
