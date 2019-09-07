# BusinessTimeDelta
Python's timedelta for business time. This module helps you calculate the exact working time between two datetimes. It supports common scenarios such as custom schedules, holidays, and time zones.

[![Build Status](https://travis-ci.org/seppemans/businesstimedelta.svg?branch=master)](https://travis-ci.org/seppemans/businesstimedelta)

## Installation
Use pip to install BusinessTimeDelta.

```shell
pip install businesstimedelta
```

## Example Use
Define your business hours

```python
import datetime
import pytz
import businesstimedelta

# Define a working day
workday = businesstimedelta.WorkDayRule(
    start_time=datetime.time(9),
    end_time=datetime.time(18),
    working_days=[0, 1, 2, 3, 4])

# Take out the lunch break
lunchbreak = businesstimedelta.LunchTimeRule(
    start_time=datetime.time(12),
    end_time=datetime.time(13),
    working_days=[0, 1, 2, 3, 4])

# Combine the two
businesshrs = businesstimedelta.Rules([workday, lunchbreak])
```

Calculate the business time between two datetimes

```python
start = datetime.datetime(2016, 1, 18, 9, 0, 0)
end = datetime.datetime(2016, 1, 22, 18, 0, 0)
bdiff = businesshrs.difference(start, end)

print bdiff
# <BusinessTimeDelta 40 hours 0 seconds>

print "%s hours and %s seconds" % (bdiff.hours, bdiff.seconds)
# 40 hours and 0 seconds
```

Business time arithmetic

```python
print start + businesstimedelta.BusinessTimeDelta(businesshrs, hours=40)
# 2016-01-22 18:00:00+00:00

print end - businesstimedelta.BusinessTimeDelta(businesshrs, hours=40)
# 2016-01-18 09:00:00+00:00
```

To define holidays, simply use the [Holidays](https://pypi.python.org/pypi/holidays) package

```python
import holidays as pyholidays

ca_holidays = pyholidays.US(state='CA')
holidays = businesstimedelta.HolidayRule(ca_holidays)
businesshrs = businesstimedelta.Rules([workday, lunchbreak, holidays])

# Christmas is on Friday 2015/12/25
start = datetime.datetime(2015, 12, 21, 9, 0, 0)
end = datetime.datetime(2015, 12, 28, 9, 0, 0)
print businesshrs.difference(start, end)
# <BusinessTimeDelta 32 hours 0 seconds>
```

## Timezones
If your datetimes are not timezone aware, they will be localized to UTC (see example above).

Let's say you want to calculate the business time overlap between a working day in San Francisco and in Santiago, Chile:
```python
santiago_workday = businesstimedelta.WorkDayRule(
    start_time=datetime.time(9),
    end_time=datetime.time(18),
    working_days=[0, 1, 2, 3, 4],
    tz=pytz.timezone('America/Santiago'))

santiago_lunchbreak = businesstimedelta.LunchTimeRule(
    start_time=datetime.time(12),
    end_time=datetime.time(13),
    working_days=[0, 1, 2, 3, 4],
    tz=pytz.timezone('America/Santiago'))

santiago_businesshrs = businesstimedelta.Rules([santiago_workday, santiago_lunchbreak])

sf_tz = pytz.timezone('America/Los_Angeles')
sf_start = sf_tz.localize(datetime.datetime(2016, 1, 18, 9, 0, 0))
sf_end = sf_tz.localize(datetime.datetime(2016, 1, 18, 18, 0, 0))

print santiago_businesshrs.difference(sf_start, sf_end)
# <BusinessTimeDelta 4 hours 0 seconds>
```

## Overnight Shifts
```python
# Day shift
workday = WorkDayRule(
    start_time=datetime.time(9),
    end_time=datetime.time(17),
    working_days=[0, 1, 2, 3, 4],
    tz=pytz.utc)

# Night shift
nightshift = businesstimedelta.WorkDayRule(
    start_time=datetime.time(23),
    end_time=datetime.time(7),
    working_days=[0, 1, 2, 3, 4])

businesshrs = businesstimedelta.Rules([workday, nightshift])

start = datetime.datetime(2016, 1, 18, 9, 0, 0)
end = datetime.datetime(2016, 1, 22, 18, 0, 0)
bdiff = businesshrs.difference(start, end)

print bdiff
# <BusinessTimeDelta 80 hours 0 seconds>
```
