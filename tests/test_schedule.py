from scripts.schedule import Schedule, OpeningHours
from datetime import datetime as dt


def test_is_open():
    d1 = dt(2021, 12, 27, 10, 0)
    d2 = dt(2021, 12, 27, 7, 0)
    d3 = dt(2021, 12, 27, 21, 0)

    oh = OpeningHours()

    assert oh.is_open(d1)
    assert not oh.is_open(d2)
    assert not oh.is_open(d3)


def test_find_next_date():
    day1 = dt(1980, 12, 28, 12, 0)
    day2 = dt(1980, 12, 29, 20, 0)
    day3 = dt(1980, 12, 29, 14, 0)
    day4 = dt(1980, 12, 30, 10, 0)

    schedule = Schedule(20)

    result1 = schedule.find_next_date(1, day1)
    result2 = schedule.find_next_date(1, day2)
    result3 = schedule.find_next_date(10, day3)
    result4 = schedule.find_next_date(4, day4)

    assert result1 == dt(1980, 12, 28, 16, 0)
    assert result2 == dt(1980, 12, 30, 8, 0)
    assert result3 == dt(1980, 12, 29, 15, 0)
    assert result4 == dt(1981, 1, 1, 8, 0)
