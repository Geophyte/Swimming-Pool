from scripts.accountant import PriceList, Accountant
from datetime import datetime as dt


def test_get_time_factor():
    date1 = dt(2021, 12, 31, 10)
    date2 = dt(2021, 12, 31, 12)
    date3 = dt(2021, 12, 31, 15)
    date4 = dt(2021, 12, 31, 20)

    price_list = PriceList('../data/info.json')

    assert price_list._get_time_factor(date1) == 0.75
    assert price_list._get_time_factor(date2) == 1.25
    assert price_list._get_time_factor(date3) == 1.25
    assert price_list._get_time_factor(date4) == 1


def test_ticket_price():
    age1 = "child"
    age2 = "student"
    age3 = "normal"
    age4 = "senior"
    date1 = dt(2022, 1, 10, 10)
    date2 = dt(2022, 1, 10, 15)
    date3 = dt(2022, 1, 10, 19)
    date4 = dt(2022, 1, 14, 17)

    price_list = PriceList('../data/info.json')

    assert price_list.ticket_price(age1, date1) == 3
    assert price_list.ticket_price(age2, date2) == 10
    assert price_list.ticket_price(age3, date3) == 12
    assert price_list.ticket_price(age4, date4) == 12.5


def test_lane_price():
    date1 = dt(2022, 1, 10, 10)
    date2 = dt(2022, 1, 10, 15)
    date3 = dt(2022, 1, 10, 19)
    date4 = dt(2022, 1, 14, 17)

    price_list = PriceList('../data/info.json')

    assert price_list.lane_price(date1) == 15
    assert price_list.lane_price(date2) == 25
    assert price_list.lane_price(date3) == 20
    assert price_list.lane_price(date4) == 31.25


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
