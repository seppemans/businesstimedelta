import datetime


class BusinessTimeDelta(object):
    def __init__(self, rule, hours=0, seconds=0):
        self.rule = rule
        self.timedelta = datetime.timedelta(
            seconds=seconds,
            hours=hours)

    def __repr__(self):
        hours = self.timedelta.days * 24
        hours += (self.timedelta.seconds - self.timedelta.seconds % (60*60)) / (60*60)
        seconds = self.timedelta.seconds % (60*60)
        return '<BusinessTimeDelta %s hours %s seconds>' % (hours, seconds)

    def __eq__(self, other):
        return self.timedelta == other.timedelta

    def __add__(self, dt):
        td_left = self.timedelta
        while True:
            period_start, period_end = self.rule.next(dt)
            period_delta = period_end - period_start

            # If we ran out of timedelta, return
            if period_delta > td_left:
                return period_start + td_left

            td_left -= period_delta
            dt = period_end

    def __radd__(self, dt):
        return self.__add__(dt)

    def __sub__(self, dt):
        td_left = self.timedelta
        while True:
            period_start, period_end = self.rule.previous(dt)
            period_delta = period_end - period_start

            # If we ran out of timedelta, return
            if period_delta > td_left:
                return period_end - td_left

            td_left -= period_delta
            dt = period_start

    def __rsub__(self, dt):
        return self.__sub__(dt)
