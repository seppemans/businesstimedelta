import datetime
import unittest
import pytz
from ...rules.rules import Rules
from ...rules.workdayrules import WorkDayRule, LunchTimeRule


class RulesTest(unittest.TestCase):
    def setUp(self):
        self.utc = pytz.timezone('UTC')
        self.workdayrule = WorkDayRule(
            start_time=datetime.time(9),
            end_time=datetime.time(17),
            working_days=[0, 1, 2, 3, 4],
            tz=self.utc)
        self.lunchbreak = LunchTimeRule(
            start_time=datetime.time(12),
            end_time=datetime.time(13),
            working_days=[0, 1, 2, 3, 4],
            tz=self.utc)
        self.rules = Rules([
            self.workdayrule,
            self.lunchbreak])

    def test_next_during_lunch_break(self):
        dt = self.utc.localize(datetime.datetime(2016, 1, 25, 12, 30, 0))

        self.assertEqual(
            self.rules.next(dt),
            (
                self.utc.localize(datetime.datetime(2016, 1, 25, 13, 0, 0)),
                self.utc.localize(datetime.datetime(2016, 1, 25, 17, 0, 0))
            )
        )

    def test_next_before_lunch_break(self):
        dt = self.utc.localize(datetime.datetime(2016, 1, 25, 12, 0, 0))

        self.assertEqual(
            self.rules.next(dt),
            (
                self.utc.localize(datetime.datetime(2016, 1, 25, 13, 0, 0)),
                self.utc.localize(datetime.datetime(2016, 1, 25, 17, 0, 0))
            )
        )

    def test_previous_during_lunch_break(self):
        dt = self.utc.localize(datetime.datetime(2016, 1, 25, 12, 30, 0))

        self.assertEqual(
            self.rules.previous(dt),
            (
                self.utc.localize(datetime.datetime(2016, 1, 25, 9, 0, 0)),
                self.utc.localize(datetime.datetime(2016, 1, 25, 12, 0, 0))
            )
        )

    def test_previous_at_end_of_lunch_break(self):
        dt = self.utc.localize(datetime.datetime(2016, 1, 25, 13, 0, 0))

        self.assertEqual(
            self.rules.previous(dt),
            (
                self.utc.localize(datetime.datetime(2016, 1, 25, 9, 0, 0)),
                self.utc.localize(datetime.datetime(2016, 1, 25, 12, 0, 0))
            )
        )

    def test_previous_after_lunch_break(self):
        dt = self.utc.localize(datetime.datetime(2016, 1, 25, 13, 30, 0))

        self.assertEqual(
            self.rules.previous(dt),
            (
                self.utc.localize(datetime.datetime(2016, 1, 25, 13, 0, 0)),
                self.utc.localize(datetime.datetime(2016, 1, 25, 13, 30, 0))
            )
        )
