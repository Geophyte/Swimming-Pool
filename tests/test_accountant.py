from scripts.accountant import PriceList, Accountant
from datetime import datetime as dt


def test_get_time_factor():
    date1 = dt(2021, 12, 31, 10)
    date2 = dt(2021, 12, 31, 12)
    date3 = dt(2021, 12, 31, 15)
    date4 = dt(2021, 12, 31, 20)

    price_list = PriceList('../data/info.json')

    assert price_list._get_time_factor(date1) == 0.75
    assert price_list._get_time_factor(date2) == 0.75
    assert price_list._get_time_factor(date3) == 1.25
    assert price_list._get_time_factor(date4) == 1


def test_init_month():
    accountant = Accountant('../data/info.json')
    date = dt(2022, 2, 1)

    month_report = accountant._init_month(date)
    empty_report = {
        'lanes': 0,
        'lane_income': 0,
        'tickets': 0,
        'ticket_income': 0,
        'sum': 0
        }

    assert len(month_report) == 28
    for day in month_report:
        assert month_report[day] == empty_report
