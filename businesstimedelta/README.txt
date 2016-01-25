#This module helps you calculate the difference in working hours between two datetimes. 
# It supports time zones.

#Define your business hours::
import datetime
import pytz
import businesstimedelta

workday = businesstimedelta.rules.WorkDayRule(
    start_time=datetime.time(9),
    end_time=datetime.time(17),
    working_days=[0, 1, 2, 3, 4],
    tz=pytz.utc)

# Take out the lunch break
lunchbreak = businesstimedelta.LunchTimeRule(
    start_time=datetime.time(12), 
    end_time=datetime.time(13),
    working_days=[0, 1, 2, 3, 4],
    tz=pytz.utc)

# Combine!
businesshrs = businesstimedelta.Rules([workday, lunchbreak])


#Business hours between two datetimes::
start = datetime.datetime(2015, 1, 18, 7, 0, 0, tzinfo=pytz.utc)
end = datetime.datetime(2015, 1, 22, 18, 0, 0, tzinfo=pytz.utc)
print businesshrs.difference(start, end)
# <BusinessTimeDelta 35 hours 0 seconds>

#Add business hours to a datetime::
start = datetime.datetime(2015, 1, 18, 8, 0, 0, tzinfo=pytz.utc)
print start + businesstimedelta.BusinessTimeDelta(businesshrs, hours=35)
#    <BusinessTimeDelta 1 days 28800 seconds>