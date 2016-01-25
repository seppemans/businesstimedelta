import pytz
import datetime
from ..businesstimedelta import BusinessTimeDelta


class Rule(object):
    """This object contains 'blocks' of time. It can define either working hours
    or an exclusions of working hous (such as holidays, lunch break)"""
    def __init__(self, tz=pytz.timezone('US/Pacific'), time_off=False):
        self.tz = tz
        self.time_off = time_off

    def next(self, dt):
        """Returns the start and end of the upcoming (or current) block of time
        that falls within this BusinessTime.

        Args:
            dt: an aware datetime object.
        Output:
            tuple of (start, end) of the first upcoming business time
            in aware datetime objects.
        """
        raise NotImplementedError

    def previous(self, *args, **kwargs):
        """Same as next, but backwards in time"""
        raise NotImplementedError

    def difference(self, dt1, dt2):
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
                return BusinessTimeDelta(self, hours=result.days*24, seconds=result.seconds)

            dt = period_end
            td_sum += period_delta
