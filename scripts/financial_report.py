from datetime import datetime as dt, time
from pathlib import Path
from typing import TextIO
from datetime import datetime
import json
import os
import errno


class PriceList:
    def __init__(self) -> None:
        # Wczytaj cennik z ../data/info.json
        info_rel_path = "../data/info.json"
        info_abs_path = Path(__file__).parent / info_rel_path

        with open(info_abs_path, 'r') as info_file:
            info = json.load(info_file)

            # Cena podstawowa zależy od wieku
            self._client_age = info['PriceList']['client_age']

            # Współczynniki ceny zależą od dnia, godz, itd.
            self._day_of_entry = info['PriceList']['day_of_entry']
            self._time_of_entry = info['PriceList']['time_of_entry']

            # Cena podstawowa wynajmu toru
            self._lane_price = info['PriceList']['lane_price']

    # Zwraca współczynnik dla przedziału czasu
    def _get_time_factor(self, date: datetime) -> float:
        t = date.time()
        for interval in self._time_of_entry:
            begin = time(interval['begin'], 0)
            end = time(interval['end'], 0)
            if begin <= t and t <= end:
                return interval['factor']

    # Zwraca koszt biletu
    def ticket_price(self, age: str, date: datetime) -> float:
        price = self._client_age[age]
        price *= self._day_of_entry[date.strftime('%A')]
        price *= self._get_time_factor(date)
        return round(price, 2)

    # Zwraca koszt wynajęcia toru
    def lane_price(self, date: datetime) -> float:
        price = self._lane_price
        price *= self._day_of_entry[date.strftime('%A')]
        price *= self._get_time_factor(date)

        return price


# Zwraca ścieżkę bezwzględną do pliku z raportem finansowym
def get_report_path(date: dt = dt.now()) -> str:
    year = date.year
    month = date.strftime('%B').lower()

    report_rel_path = f"../data/{year}/{date.month}_{month}_report.json"
    return Path(__file__).parent / report_rel_path


# Działa jak 'open' przy okazji tworząc plik jeśli nie istnieje,
# otwiera go używając daty zamiast ścieżki
def open_report(date: dt = dt.now()) -> TextIO:
    report_abs_path = get_report_path(date)

    # Stwórz foldery jeśli nie istnieją
    if not os.path.exists(os.path.dirname(report_abs_path)):
        try:
            os.makedirs(os.path.dirname(report_abs_path))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise

    # Stwórz plik jeśli nie istnieje
    if not os.path.isfile(report_abs_path):
        open(report_abs_path, 'a').close()

    return open(report_abs_path, 'r+')


class FinancialReport:
    def __init__(self) -> None:
        self._price_list = PriceList()

    def _update_report(self, report: dict, date: dt = dt.now()) -> None:
        with open_report('w', date) as schedule_file:
            json.dump(report, schedule_file, indent=4)

    def _read_report(self, date: dt = dt.now()) -> dict:
        with open_report('r', date) as schedule_file:
            try:
                return json.load(schedule_file)
            except json.JSONDecodeError:
                temp = {
                    'lanes': 0,
                    'lane_income': 0,
                    'tickets': 0,
                    'ticket_income': 0,
                    'sum': 0
                }
                return temp

    def regsiter_transaction(self, ticket: dict) -> float:
        report = self._read_report(ticket['date'])

        if ticket['type'] == 'private_client':
            report['tickets'] += 1
            price = self._price_list.ticket_price(ticket['age'], ticket['date'])
            report['ticket_income'] += price
        else:
            report['lanes'] += 1
            price = self._price_list.lane_price(ticket['date'])
            report['lane_income'] += price
            
        report['sum'] += price
        self._update_report(report, ticket['date'])

        return price
