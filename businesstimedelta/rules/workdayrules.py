import datetime
from .rule import Rule
from ..businesstimedelta import localize_unlocalized_dt


class WorkDayRule(Rule):
    """Basic implementation of a working day that starts and ends some days of
    the week at the same start and end time. Ex. Monday through Friday in the EST timezone.

    Overnight shifts can be represented by setting end time less than start time.
    """

    def __init__(self, start_time=datetime.time(9), end_time=datetime.time(18),
                 working_days=[0, 1, 2, 3, 4], *args, **kwargs):
        """
        Args:
            start_time: a Time object that defines the start of a work day
            end_time: a Time object that defines the end of a work day
            working_days: days of the working week (0 = Monday)
            tz: a pytz timezone
        """
        kwargs['time_off'] = kwargs.get('time_off', False)
        super(WorkDayRule, self).__init__(*args, **kwargs)
        self.start_time = start_time
        self.end_time = end_time
        self.working_days = working_days

    def next(self, dt, reverse=False):
        dt = localize_unlocalized_dt(dt)
        localized_dt = dt.astimezone(self.tz)

        # Figure out what the first upcoming working date is
        working_date = localized_dt.date()

        if working_date.weekday() in self.working_days and localized_dt.time() < max(self.start_time, self.end_time):
            # Today is the working day to use in further calculations if there is
            # any working time left in this day. Ie, if the current time is
            # - less than the end time (for normal cases)
            # - less than the start time (for overnight work days)
            pass
        else:
            while True:
                working_date += datetime.timedelta(days=1)
                if working_date.weekday() in self.working_days:
                    break

        # We know the target working date now. Just figure out the start and end times.
        start = self.tz.localize(datetime.datetime.combine(working_date, self.start_time))

        # In the case this working day has some overnight time, add one day to the end date
        if self.end_time < self.start_time:
            working_date += datetime.timedelta(days=1)

        end = self.tz.localize(datetime.datetime.combine(working_date, self.end_time))

        # If we are in the range now, set the start or end date to now.
        if start < dt and end > dt:
            start = dt

        return (start, end)

    def previous(self, dt, *args, **kwargs):
        dt = localize_unlocalized_dt(dt)
        localized_dt = dt.astimezone(self.tz)

        # Figure out what is the first upcoming working date
        working_date = localized_dt.date()
        if working_date.weekday() in self.working_days \
           and localized_dt.time() > self.start_time:
            pass  # Today is the working date
        else:
            while True:
                working_date -= datetime.timedelta(days=1)
                if working_date.weekday() in self.working_days:
                    break

        # We know the target working date now. Just figure out the start and end times.
        start = self.tz.localize(datetime.datetime.combine(working_date, self.start_time))
        end = self.tz.localize(datetime.datetime.combine(working_date, self.end_time))

        # If we are in the range now, set the start or end date to now.
        if start < dt and end > dt:
            end = dt

        return (start, end)


class LunchTimeRule(WorkDayRule):
    """Convenience function for lunch breaks."""
    def __init__(self, start_time=datetime.time(12), end_time=datetime.time(13),
                 working_days=[0, 1, 2, 3, 4], *args, **kwargs):
        super(LunchTimeRule, self).__init__(
            start_time=start_time,
            end_time=end_time,
            working_days=working_days,
            time_off=True,
            *args, **kwargs)
