from pathlib import Path
from datetime import datetime, time
import json


# Zwraca przedział czasu
def get_time_interval(t: datetime) -> str:
    t = t.time()
    if time(0, 0, 0) <= t and t <= time(12, 0, 0):
        return 'morning'
    elif time(12, 0, 0) < t and t <= time(18, 0, 0):
        return 'afternoon'
    else:
        return 'evening'


class Price_list:
    def __init__(self) -> None:
        # Wczytaj cennik z ../data/price_list.json
        price_list_rel_path = "../data/price_list.json"
        price_list_abs_path = Path(__file__).parent / price_list_rel_path

        with open(price_list_abs_path, 'r') as price_list_file:
            p_list = json.load(price_list_file)

            # Cena podstawowa zależy od wieku
            self._client_age = p_list['client_age']

            # Współczynniki ceny zależne od dnia, godz, itd.
            self._client_type = p_list['client_type']
            self._day_of_entry = p_list['day_of_entry']
            self._time_of_entry = p_list['time_of_entry']

            # Cena podstawowa wynajmu toru
            self._lane_price = p_list['lane_price']

    # Zwraca koszt biletu
    def calculate_price(self, age: str, r_date: datetime,
                        type: str = 'private_client') -> float:
        price = self._client_age[age]
        price *= self._day_of_entry[r_date.strftime('%A')]
        price *= self._time_of_entry[get_time_interval(r_date)]
        price *= self._client_type[type]
        return round(price, 2)

    # Zwraca koszt wynajęcia toru
    def calculate_lane_price(self, age: str, r_date: datetime) -> float:
        price = self.calculate_price(age, r_date, 'swimming_school')
        price *= 5

        price += self._lane_price
        return price
