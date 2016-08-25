import datetime
import pytz


def localize_unlocalized_dt(dt):
    """Turn naive datetime objects into UTC.
    Don't do anything if the datetime object is aware.
    https://docs.python.org/3/library/datetime.html#datetime.timezone
    """
    if dt.tzinfo is not None and dt.tzinfo.utcoffset(dt) is not None:
        return dt
    return pytz.utc.localize(dt)


class BusinessTimeDelta(object):
    def __init__(self, rule, hours=0, seconds=0, timedelta=None):
        self.rule = rule

        if timedelta:
            self.timedelta = timedelta
        else:
            self.timedelta = datetime.timedelta(
                seconds=seconds,
                hours=hours)

    def __repr__(self):
        return '<BusinessTimeDelta %s hours %s seconds>' % (self.hours, self.seconds)

    def __eq__(self, other):
        return self.timedelta == other.timedelta

    def __add__(self, other):
        if isinstance(other, BusinessTimeDelta) and other.rule == self.rule:
            return BusinessTimeDelta(self.rule, timedelta=self.timedelta + other.timedelta)

        elif isinstance(other, datetime.datetime):
            dt = localize_unlocalized_dt(other)
            td_left = self.timedelta
            while True:
                period_start, period_end = self.rule.next(dt)
                period_delta = period_end - period_start

                # If we ran out of timedelta, return
                if period_delta >= td_left:
                    return period_start + td_left

                td_left -= period_delta
                dt = period_end

        raise NotImplementedError

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, BusinessTimeDelta) and other.rule == self.rule:
            return BusinessTimeDelta(self.rule, timedelta=self.timedelta - other.timedelta)

        elif isinstance(other, datetime.datetime):
            dt = localize_unlocalized_dt(other)
            td_left = self.timedelta
            while True:
                period_start, period_end = self.rule.previous(dt)
                period_delta = period_end - period_start

                # If we ran out of timedelta, return
                if period_delta >= td_left:
                    return period_end - td_left

                td_left -= period_delta
                dt = period_start

    def __rsub__(self, other):
        return self.__sub__(other)

    @property
    def hours(self):
        return int(self.timedelta.total_seconds() // (60 * 60))

    @property
    def seconds(self):
        return int(self.timedelta.total_seconds() % (60 * 60))
