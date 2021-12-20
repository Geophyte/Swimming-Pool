_client_type = {
    'private_client': 1,
    'swimming_school': 0.25
}
_client_age = {
    'child': 5,             # 0-7 lat
    'student': 8,           # za pokazaniem legitymacji
    'normal': 16,           # brak zniżki
    'senior': 8             # w wieku emerytalnym
}
_day_of_entry = {
    'monday': 1,
    'tuesday': 1,
    'wednesday': 1,
    'thurstday': 1,
    'friday': 1.25,
    'saturday': 1.25,
    'sunday': 1.25
}
_time_of_entry = {
    'morning': 0.75,        # 0-12
    'afternoon': 1.25,      # 12-18
    'evening': 1            # 18-24
}

_lane_price = 20            # Podstawowa cena wynajmu toru


# Zwraca koszt biletu
def calculate_price(age: str, day: str, time: str, type: str = 'private_client') -> float:
    price = _client_type[type] * _client_age[age] * _day_of_entry[day] * _time_of_entry[time]
    return round(price, 2)


# Zwraca koszt wynajęcia toru
def calculate_lane_price(age: str, day: str, time: str) -> float:
    return _lane_price + calculate_price(age, day, time, 'swimming_school') * 5


# Wyposuje cennik w terminalu
def print_price_list():
    print('=' * 40)
    print("\tPRIVATE CLIENT")
    print('=' * 40)
    for weekday in _day_of_entry:
        print(f'{weekday}:')
        for age in _client_age:
            for time in _time_of_entry:
                price = calculate_price(age, weekday, time)
                print(f'\t{age}.{time}: {price:.2f} zl')

    print('=' * 40)
    print("\tSWIMMING SCHOOL")
    print('=' * 40)
    for weekday in _day_of_entry:
        print(f'{weekday}:')
        for age in _client_age:
            for time in _time_of_entry:
                row_price = calculate_lane_price(age, weekday, time)
                price = calculate_price(age, weekday, time)
                spare = round((price * 5 - row_price) / 5, 2)
                print(f'\t{age}.{time}: {row_price:.2f} zl, oszcz: {spare:.2f} zl')


if __name__ == "__main__":
    print_price_list()
