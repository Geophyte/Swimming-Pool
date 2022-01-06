from scripts.scheduler import Scheduler
from datetime import datetime as dt


def test_is_valid_reservation():
    schedule = {
        1: [(1, 0), (0, 0), (5, 1), (20, 0)]
    }

    s = Scheduler()

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

    assert s._is_valid_reservation(schedule, ticket1)
    assert s._is_valid_reservation(schedule, ticket2)
    assert not s._is_valid_reservation(schedule, ticket3)
    assert not s._is_valid_reservation(schedule, ticket4)
    assert not s._is_valid_reservation(schedule, ticket5)
