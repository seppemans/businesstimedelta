#BusinessTimeDelta
Python's timedelta for business time. This module helps you calculate the exact difference in working time between two datetimes. It supports common scenarios such as custom schedules, holidays, and time zones.

##Installation
Use pip to install BusinessTimeDelta.

```shell
pip install businesstimedelta
```

##Example Use
Define your business hours

```python
import datetime
import pytz
import businesstimedelta

# Define a working day
workday = businesstimedelta.WorkDayRule(
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
businesshrs = businesstimedelta.Rules([workday, lunchbreak])
```

Calculate the business time between two datetimes

```python
start = datetime.datetime(2016, 1, 18, 9, 0, 0, tzinfo=pytz.utc)
end = datetime.datetime(2016, 1, 25, 9, 0, 0, tzinfo=pytz.utc)
print businesshrs.difference(start, end)
# <BusinessTimeDelta 40 hours 0 seconds>
```

Add business time to a datetime

```python
start = datetime.datetime(2016, 1, 18, 8, 0, 0, tzinfo=pytz.utc)
print start + businesstimedelta.BusinessTimeDelta(businesshrs, hours=40)
# 2016-01-25 09:00:00+00:00
```

To define holidays, simply use the [Holidays](https://pypi.python.org/pypi/holidays) package

```python
import holidays as pyholidays

ca_holidays = pyholidays.US(state='CA')
holidays = businesstimedelta.HolidayRule(ca_holidays)
businesshrs = businesstimedelta.Rules([workday, lunchbreak, holidays])

# Christmas is on Friday 2015/12/25
start = datetime.datetime(2015, 12, 21, 9, 0, 0, tzinfo=pytz.utc)
end = datetime.datetime(2015, 12, 28, 9, 0, 0, tzinfo=pytz.utc)
print businesshrs.difference(start, end)
# <BusinessTimeDelta 32 hours 0 seconds>
```