from datetime import datetime as dt
import datetime
from faker import Faker
import pytz

TZ = pytz.timezone("Europe/Moscow")
my_date = dt.now(tz=TZ)
print(my_date.isoformat())

date_time_str = '2018-06-29 00:00:00.100000'
date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S.%f')
timezone_date_time_obj = TZ.localize(date_time_obj)
print(timezone_date_time_obj)
print(timezone_date_time_obj.tzinfo)


fake = Faker()
print(fake.iso8601(tzinfo=TZ))