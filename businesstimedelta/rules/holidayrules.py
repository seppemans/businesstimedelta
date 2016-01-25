import datetime
from rule import Rule


class HolidayRule(Rule):
    def __init__(self, holidays, *args, **kwargs):
        """
        Args:
            start_time: a Time object that defines the start of a work day
            end_time: a Time object that defines the end of a work day
            working_days: days of the working week (0 = Monday)
            tz: a pytz timezone
        """
        kwargs['time_off'] = kwargs.get('time_off', True)
        self.holidays = holidays
        super(HolidayRule, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<HolidayRule: %s>' % (self.holidays)

    def next_holiday(self, date, reverse=False, max_days=365*2):
        """To support both the Holidays module as well as lists of dates,
        make sure to check we don't keep looping forever here."""

        count = 0
        while True:
            if date in self.holidays:
                return date

            if reverse:
                date -= datetime.timedelta(days=1)
            else:
                date += datetime.timedelta(days=1)

            count += 1
            if count > max_days:
                return None

    def next(self, dt, reverse=False):
        localized_dt = dt.astimezone(self.tz)
        next_holiday = self.next_holiday(localized_dt.date(), reverse=reverse)
        start = self.tz.localize(datetime.datetime.combine(next_holiday, datetime.time(0, 0, 0)))
        end = self.tz.localize(datetime.datetime.combine(next_holiday, datetime.time(23, 59, 59)))

        # If we are in the range now, set the start or end date to now.
        if start < dt and end > dt:
            if reverse:
                end = dt
            else:
                start = dt

        return (start, end)

    def previous(self, *args, **kwargs):
        kwargs['reverse'] = True
        return self.next(*args, **kwargs)
