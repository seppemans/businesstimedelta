import datetime
import unittest
import pytz
from ...rules.workdayrules import WorkDayRule, LunchTimeRule


class WorkDayRuleTest(unittest.TestCase):
    def setUp(self):
        self.pst = pytz.timezone('US/Pacific')
        self.utc = pytz.timezone('UTC')
        self.workdayrule = WorkDayRule(
            start_time=datetime.time(9),
            end_time=datetime.time(17),
            working_days=[0, 1, 2, 3, 4],
            tz=self.utc)

    def test_next_during_weekend(self):
        dt = self.utc.localize(datetime.datetime(2016, 1, 23, 13, 14, 0))

        self.assertEqual(
            self.workdayrule.next(dt),
            (
                self.utc.localize(datetime.datetime(2016, 1, 25, 9, 0, 0)),
                self.utc.localize(datetime.datetime(2016, 1, 25, 17, 0, 0))
            )
        )

    def test_next_during_working_day(self):
        dt = self.utc.localize(datetime.datetime(2016, 1, 25, 10, 0, 0))

        self.assertEqual(
            self.workdayrule.next(dt),
            (
                dt,
                self.utc.localize(datetime.datetime(2016, 1, 25, 17, 0, 0))
            )
        )

    def test_next_before_working_day(self):
        dt = self.utc.localize(datetime.datetime(2016, 1, 25, 3, 0, 0))

        self.assertEqual(
            self.workdayrule.next(dt),
            (
                self.utc.localize(datetime.datetime(2016, 1, 25, 9, 0, 0)),
                self.utc.localize(datetime.datetime(2016, 1, 25, 17, 0, 0))
            )
        )

    def test_previous_during_working_day(self):
        dt = self.utc.localize(datetime.datetime(2016, 1, 25, 10, 0, 0))

        self.assertEqual(
            self.workdayrule.previous(dt),
            (
                self.utc.localize(datetime.datetime(2016, 1, 25, 9, 0, 0)),
                dt
            )
        )

    def test_previous_during_weekend(self):
        dt = self.utc.localize(datetime.datetime(2016, 1, 23, 13, 14, 0))

        self.assertEqual(
            self.workdayrule.previous(dt),
            (
                self.utc.localize(datetime.datetime(2016, 1, 22, 9, 0, 0)),
                self.utc.localize(datetime.datetime(2016, 1, 22, 17, 0, 0)),
            )
        )

    def test_previous_at_working_day_start(self):
        dt = self.utc.localize(datetime.datetime(2016, 1, 25, 9, 00, 0))

        self.assertEqual(
            self.workdayrule.previous(dt),
            (
                self.utc.localize(datetime.datetime(2016, 1, 22, 9, 0, 0)),
                self.utc.localize(datetime.datetime(2016, 1, 22, 17, 0, 0)),
            )
        )

    def test_previous_at_working_day_end(self):
        dt = self.utc.localize(datetime.datetime(2016, 1, 25, 17, 00, 0))

        self.assertEqual(
            self.workdayrule.previous(dt),
            (
                self.utc.localize(datetime.datetime(2016, 1, 25, 9, 0, 0)),
                self.utc.localize(datetime.datetime(2016, 1, 25, 17, 0, 0)),
            )
        )

    def test_previous_after_working_day_end(self):
        dt = self.utc.localize(datetime.datetime(2016, 1, 25, 18, 00, 0))

        self.assertEqual(
            self.workdayrule.previous(dt),
            (
                self.utc.localize(datetime.datetime(2016, 1, 25, 9, 0, 0)),
                self.utc.localize(datetime.datetime(2016, 1, 25, 17, 0, 0)),
            )
        )


class LunchTimeRuleTest(unittest.TestCase):
    def setUp(self):
        self.utc = pytz.timezone('UTC')
        self.lunchtimerule = LunchTimeRule(
            start_time=datetime.time(12),
            end_time=datetime.time(13),
            working_days=[0, 1, 2, 3, 4],
            tz=self.utc)

    def test_next_during_lunch_time(self):
        dt = self.utc.localize(datetime.datetime(2016, 1, 25, 12, 30, 0))

        self.assertEqual(
            self.lunchtimerule.next(dt),
            (
                dt,
                self.utc.localize(datetime.datetime(2016, 1, 25, 13, 0, 0))
            )
        )

    def test_lunch_time_off(self):
        self.assertEqual(self.lunchtimerule.time_off, True)
