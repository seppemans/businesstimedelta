import pytz
import datetime
from ..businesstimedelta import BusinessTimeDelta, localize_unlocalized_dt


class Rule(object):
    """This object defines 'blocks' of time. It can define either working hours
    or an exclusion of working hours (such as holidays, lunch breaks, etc)"""
    def __init__(self, tz=pytz.utc, time_off=False):
        self.tz = tz
        self.time_off = time_off

    def next(self, dt):
        """Returns the start and end of the upcoming (or current) block of time
        that falls within this BusinessTime.

        Args:
            dt: a datetime object.
        Output:
            tuple of (start, end) of the first upcoming business time
            in aware datetime objects.
        """
        raise NotImplementedError

    def previous(self, *args, **kwargs):
        """Same as next, but backwards in time"""
        raise NotImplementedError

    def difference(self, dt1, dt2):
        """Calculate the business time between two datetime objects."""
        dt1 = localize_unlocalized_dt(dt1)
        dt2 = localize_unlocalized_dt(dt2)
        start_dt, end_dt = sorted([dt1, dt2])
        td_sum = datetime.timedelta()
        dt = start_dt

        while True:
            period_start, period_end = self.next(dt)
            period_delta = period_end - period_start

            # If we are past the end_dt, we are done!
            if period_end > end_dt:
                last_day_add = max(end_dt - period_start, datetime.timedelta())
                result = td_sum + last_day_add
                return BusinessTimeDelta(self, hours=result.days * 24, seconds=result.seconds)

            dt = period_end
            td_sum += period_delta
