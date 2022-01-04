from scripts.financial_report import PriceList
from datetime import datetime as dt


def test_get_time_factor():
    date1 = dt(2021, 12, 31, 10)
    date2 = dt(2021, 12, 31, 12)
    date3 = dt(2021, 12, 31, 15)
    date4 = dt(2021, 12, 31, 20)

    price_list = PriceList()

    assert price_list._get_time_factor(date1) == 0.75
    assert price_list._get_time_factor(date2) == 0.75
    assert price_list._get_time_factor(date3) == 1.25
    assert price_list._get_time_factor(date4) == 1
