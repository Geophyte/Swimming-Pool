from datetime import datetime as dt, time, timedelta
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
            # Wybierz początek i koniec przedziału czasowego
            begin = time(interval['hours'][0], 0)
            end = time(interval['hours'][1], 0)

            # Sprawdź czy podany czas znajduje się w przedziale czasowym
            # i zwróć współczynnik czasu jeśli tak
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
def get_report_path(date: dt) -> str:
    year = date.year
    month = date.strftime('%B').lower()

    report_rel_path = f"../data/{year}/{date.month}_{month}_report.json"
    return Path(__file__).parent / report_rel_path


# Działa jak 'open' przy okazji tworząc plik jeśli nie istnieje,
# otwiera go używając daty zamiast ścieżki
def open_report(mode: str, date: dt) -> TextIO:
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

    return open(report_abs_path, mode)


class Accountant:
    def __init__(self) -> None:
        self._price_list = PriceList()

    # Aktualizuje plik z raportem na podstawie słownika 'report'
    def _update_report(self, report: dict, date: dt) -> None:
        with open_report('w', date) as schedule_file:
            json.dump(report, schedule_file, indent=4)

    # Wczytuje słownik z raportu, jeśli jest pusty inicjalizuje cały miesiąc
    def _read_report(self, date: dt) -> dict:
        with open_report('r', date) as schedule_file:
            try:
                # Wczytaj plik
                report = json.load(schedule_file)
                # Przekonwertuj klucze słownika z str na int
                report = {int(k): _ for k, _ in report.items()}
                return report
            except json.JSONDecodeError:
                return self._init_month(date)

    # Inicjalizuje raporty finansowe na cały miesiąc
    def _init_month(self, date: dt) -> dict:
        start_date = dt(date.year, date.month, 1)
        date = start_date

        # Ustaw dla każdego dnia miesiąca wyzerowany raport
        month_report = dict()
        while date.month == start_date.month:
            month_report[date.day] = {
                'lanes': 0,
                'lane_income': 0,
                'tickets': 0,
                'ticket_income': 0,
                'sum': 0
            }
            date += timedelta(days=1)
        return month_report

    # Rejestruje tranzakcje w raporcie na daną datę
    def regsiter_transaction(self, ticket: dict) -> float:
        date = ticket['date']
        report = self._read_report(date)

        if ticket['type'] == 'private_client':
            report[date.day]['tickets'] += 1
            price = self._price_list.ticket_price(ticket['age'], date)
            report[date.day]['ticket_income'] += price
        else:
            report[date.day]['lanes'] += 1
            price = self._price_list.lane_price(date)
            report[date.day]['lane_income'] += price

        report[date.day]['sum'] += price
        self._update_report(report, date)

        return price

    # Wypisuje raport z podanego dnia
    def print_report(self, date: dt) -> None:
        report = self._read_report(date)[date.day]

        print(f"Raport z dnia {date.date()}:")
        print(f"\tSprzedane bilety indywidualne: {report['tickets']}")
        print(f"\tZarezerwowane tory: {report['lanes']}")
        print(f"\tPrzychód z biletów: {report['ticket_income']}")
        print(f"\tPrzychód z torów: {report['lane_income']}")
        print(f"\tŁączny przychód: {report['sum']}")


if __name__ == '__main__':
    accountant = Accountant()
    date = dt(1984, 12, 1, 10)

    ticket = {
        'age': 'normal',
        'type': 'private_lient',
        'date': date
    }

    print(accountant.regsiter_transaction(ticket))
    accountant.print_report(date)
