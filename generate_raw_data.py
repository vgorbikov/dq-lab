from datetime import datetime, date, timedelta, timezone
import random

random.seed(42)
START_TIME = datetime(2023, 1, 1, 0, 0, 1, 1, timezone(timedelta(hours=3)))
CLIENT_COUNT = 500
PRODUCT_COUNT = 900


last_time = START_TIME

for i in range(10000):
    last_time = last_time + timedelta(seconds=random.randint(1, 10000))

print(START_TIME)
print(last_time)