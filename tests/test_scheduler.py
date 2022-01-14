from scripts.scheduler import OpeningHours, Scheduler
from datetime import datetime as dt


def test_get_opening_hours():
    list1 = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0]
    list2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0]
    date1 = dt(2022, 1, 10)
    date2 = dt(2022, 1, 14)

    opening_hours = OpeningHours('../data/info.json')

    assert opening_hours.get_opening_hours(date1) == list1
    assert opening_hours.get_opening_hours(date2) == list2


def test_init_month():
    scheduler = Scheduler('../data/info.json')
    date = dt(2022, 1, 1)

    schedule = scheduler._init_month(date)

    assert schedule[1][8] == [0, 0]
    assert schedule[1][9] == [50, 3]
    assert schedule[1][17] == [50, 3]
    assert schedule[1][18] == [0, 0]

    assert schedule[3][7] == [0, 0]
    assert schedule[3][8] == [50, 3]
    assert schedule[3][19] == [50, 3]
    assert schedule[3][20] == [0, 0]


def test_is_valid_reservation():
    schedule = {
        1: [(1, 0), (0, 0), (5, 1), (20, 0)]
    }

    scheduler = Scheduler('../data/info.json')

    ticket1 = {
        'type': 'private_client',
        'date': dt(2021, 12, 1, 0, 0)
    }
    ticket2 = {
        'type': 'swimming_school',
        'date': dt(2021, 12, 1, 2, 0)
    }
    ticket3 = {
        'type': 'swimming_school',
        'date': dt(2021, 12, 1, 1, 0)
    }
    ticket4 = {
        'type': 'swimming_school',
        'date': dt(2021, 12, 1, 0, 0)
    }
    ticket5 = {
        'type': 'swimming_school',
        'date': dt(2021, 12, 1, 3, 0)
    }

    assert scheduler._is_valid_reservation(schedule, ticket1)
    assert scheduler._is_valid_reservation(schedule, ticket2)
    assert not scheduler._is_valid_reservation(schedule, ticket3)
    assert not scheduler._is_valid_reservation(schedule, ticket4)
    assert not scheduler._is_valid_reservation(schedule, ticket5)
