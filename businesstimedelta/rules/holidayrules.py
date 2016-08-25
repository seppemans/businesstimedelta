import datetime
from .rule import Rule
from ..businesstimedelta import localize_unlocalized_dt


class HolidayRule(Rule):
    def __init__(self, holidays, *args, **kwargs):
        """This rule represents a set of holidays.
        Args:
            holidays: a list with dates, or an object from the Holidays python module.
        """
        kwargs['time_off'] = kwargs.get('time_off', True)
        self.holidays = holidays
        super(HolidayRule, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<HolidayRule: %s>' % (self.holidays)

    def next_holiday(self, date, reverse=False, max_days=365 * 5):
        """ Get the next holiday
        Args:
            date: Find the next holiday after (or at) this date.
            max_days: Allowing both a list of dates as well as an object defined by
                the Holidays module requires a loop to test the holidays object against
                individual dates. To avoid getting stuck in an infinite loop here we need
                to give an upper limit of days to look into the future."""

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
        """Get the start and end of the next holiday after a datetime
        Args:
            dt: datetime
        """
        dt = localize_unlocalized_dt(dt)
        localized_dt = dt.astimezone(self.tz)
        next_holiday = self.next_holiday(localized_dt.date(), reverse=reverse)
        start = self.tz.localize(
            datetime.datetime.combine(
                next_holiday, datetime.time(0, 0, 0)))
        end = start + datetime.timedelta(days=1)

        # If we are in the range now, set the start or end date to now.
        if start < dt and end > dt:
            if reverse:
                end = dt
            else:
                start = dt

        return (start, end)

    def previous(self, *args, **kwargs):
        """Reverse of next function
        """
        kwargs['reverse'] = True
        return self.next(*args, **kwargs)
