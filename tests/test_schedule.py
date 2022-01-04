from scripts.schedule import Schedule
from datetime import datetime as dt


def test_validate_reservation():
    schedule = {
        1: [(1, 0), (5, 0), (20, 3)]
    }

    s = Schedule()

    ticket1 = {
        'age': 'child',
        'type': 'private_client',
        'date': dt(2021, 12, 1, 1, 0)
    }
    ticket2 = {
        'age': 'child',
        'type': 'swimming_school',
        'date': dt(2021, 12, 1, 2, 0)
    }
    ticket3 = {
        'age': 'child',
        'type': 'swimming_school',
        'date': dt(2021, 12, 1, 1, 0)
    }
    ticket4 = {
        'age': 'child',
        'type': 'swimming_school',
        'date': dt(2021, 12, 1, 3, 0)
    }

    assert s._validate_reservation(schedule, ticket1)
    assert s._validate_reservation(schedule, ticket2)
    assert not s._validate_reservation(schedule, ticket3)
    assert not s._validate_reservation(schedule, ticket4)
