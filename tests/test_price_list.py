from datetime import datetime, timedelta
from scripts.price_list import get_time_interval


def test_get_time_interval():
    for h in range(8, 23, 4):
        delta = timedelta(0, 0, 0, 0, 0, h)

        t = datetime(2021, 12, 21, 8) + delta
        if t.time().hour <= 12:
            result = 'morning'
        elif t.time().hour < 18:
            result = 'afternoon'
        else:
            result = 'evening'

        assert get_time_interval(t) == result
