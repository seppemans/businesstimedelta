=================
BusinessTimeDelta
=================
It's timedelta, but for business hours. This module helps you calculate the difference in working hours between two datetimes. It supports holidays common situations like time zones, holidays, etc.

Installation
------------

To install BusinessTimeDelta: ::

    pip install businesstimedelta


Example Use
-----------

Define your business hours::

    import datetime
    import pytz
    import businesstimedelta

    # Define a working day
    workday = businesstimedelta.rules.WorkDayRule(
        start_time=datetime.time(9),
        end_time=datetime.time(18),
        working_days=[0, 1, 2, 3, 4],
        tz=pytz.utc)

    # Take out the lunch break
    lunchbreak = businesstimedelta.LunchTimeRule(
        start_time=datetime.time(12),
        end_time=datetime.time(13),
        working_days=[0, 1, 2, 3, 4],
        tz=pytz.utc)

    # Combine the two
        businesshrs = businesstimedelta.BusinessTimeRules([workday, lunchbreak])

Calculate the business time between two datetimes::

    start = datetime.datetime(2016, 1, 18, 9, 0, 0, tzinfo=pytz.utc)
    end = datetime.datetime(2016, 1, 25, 9, 0, 0, tzinfo=pytz.utc)
    print businesshrs.difference(start, end)
    # <BusinessTimeDelta 40 hours 0 seconds>

Add business time to a datetime::

    start = datetime.datetime(2016, 1, 18, 8, 0, 0, tzinfo=pytz.utc)
    print start + businesstimedelta.BusinessTimeDelta(businesshrs, hours=40)
    # 2016-01-25 09:00:00+00:00

To define holidays, simply use the Holidays package::

    pip install holidays
    import holidays as pyholidays

    ca_holidays = pyholidays.US(state='CA')
    holidays = businesstimedelta.HolidayRule(ca_holidays)
    businesshrs = businesstimedelta.BusinessTimeRules([workday, lunchbreak, holidays])

    # Christmas is on Friday 2015/12/25
    start = datetime.datetime(2015, 12, 21, 9, 0, 0, tzinfo=pytz.utc)
    end = datetime.datetime(2015, 12, 28, 9, 0, 0, tzinfo=pytz.utc)
    print businesshrs.difference(start, end)
    # <BusinessTimeDelta 32 hours 0 seconds>
