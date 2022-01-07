from datetime import datetime as dt, timedelta, time
from pathlib import Path
from typing import TextIO
import os
import errno
import json
import math


class OpeningHours:
    def __init__(self) -> None:
        # Wczytaj godzinny otwarcia z ../data/info.json
        info_rel_path = "../data/info.json"
        info_abs_path = Path(__file__).parent / info_rel_path

        with open(info_abs_path, 'r') as info_file:
            info = json.load(info_file)

        # Przekonweruj wczytany słownik liczb na słownik klas 'time'
        for day in info["OpeningHours"]:
            opening_hour = time(info["OpeningHours"][day][0], 0)
            closing_hour = time(info["OpeningHours"][day][1], 0)
            info["OpeningHours"][day][0] = opening_hour
            info["OpeningHours"][day][1] = closing_hour
        self._opening_hours = info["OpeningHours"]

    # Zwraca prawdę jeśli podana data znajduje się podczas godzin otwarcia
    # pływalni
    def is_open(self, date: dt) -> bool:
        day_of_week = date.strftime('%A')
        open_time = self._opening_hours[day_of_week][0]
        close_time = self._opening_hours[day_of_week][1]

        if open_time <= date.time() and date.time() <= close_time:
            return True
        return False

    # Zwraca listę 24 elementową w której każy element odpowiada
    # godzinie [0-23] i wypełnia ją jedynkami w przedziale od
    # godzina_otwarcia (włącznie) do godzina zamknięcia (wyłącznie)
    def get_opening_hours(self, date: dt) -> list:
        day_of_week = date.strftime('%A')
        open_time = self._opening_hours[day_of_week][0]
        close_time = self._opening_hours[day_of_week][1]

        result = [0] * 24
        for i in range(open_time.hour, close_time.hour):
            result[i] = 1
        return result


# Zwraca ścieżkę bezwzględną do pliku z terminarzem
def get_schedule_path(date: dt) -> str:
    year = date.year
    month = date.strftime('%B').lower()

    schedule_rel_path = f"../data/{year}/{date.month}_{month}_schedule.json"
    return Path(__file__).parent / schedule_rel_path


# Działa jak 'open' przy okazji tworząc plik jeśli nie istnieje,
# otwiera go używając daty zamiast ścieżki
def open_schedule(mode: str, date: dt) -> TextIO:
    schedule_abs_path = get_schedule_path(date)

    # Stwórz foldery jeśli nie istnieją
    if not os.path.exists(os.path.dirname(schedule_abs_path)):
        try:
            os.makedirs(os.path.dirname(schedule_abs_path))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise

    # Stwórz plik jeśli nie istnieje
    if not os.path.isfile(schedule_abs_path):
        open(schedule_abs_path, 'a').close()

    return open(schedule_abs_path, mode)


class Scheduler:
    def __init__(self) -> None:
        self._opening_hours = OpeningHours()

        # Wczytaj liczbe torów z ../data/info.json
        info_rel_path = "../data/info.json"
        info_abs_path = Path(__file__).parent / info_rel_path

        with open(info_abs_path, 'r') as info_file:
            info = json.load(info_file)

        # Ustaw liczbę torów, max liczby torów do wynajęcia i
        # max liczbę biletów możliwą do sprzedania
        self._LANES = info['NUMBER_OF_LANES']
        self._MAX_LANES = math.floor(self._LANES * 0.35)
        self._TICKETS = self._LANES * 5

    # Aktualizuje plik z terminarzem na podstawie słownika 'schedule'
    def _update_schedule(self, schedule: dict, date: dt) -> None:
        with open_schedule('w', date) as schedule_file:
            json.dump(schedule, schedule_file)

    # Wczytuje słownik z terminarza, jeśli jest pusty inicjalizuje cały miesiąc
    def _read_schedule(self, date: dt) -> dict:
        with open_schedule('r', date) as schedule_file:
            try:
                # Wczytaj plik
                schedule = json.load(schedule_file)
                # Przekonwertuj klucze słownika z str na int
                schedule = {int(k): _ for k, _ in schedule.items()}
                return schedule
            except json.JSONDecodeError:
                return self._init_month(date)

    # Inicjalizuje miesiąc ustawiając każdą godzinę
    # w godzinach otwarcia na maksimum dostępnych biletów
    def _init_month(self, date: dt) -> dict:
        start_date = dt(date.year, date.month, 1)
        date = start_date

        month_schedule = dict()
        while date.month == start_date.month:
            # Ustaw 24-elementową listę max_tickets by były wypełniona
            # jedynkami w przedziale <godzina_otwarcia, godzina zamknięcia)
            max_tickets = self._opening_hours.get_opening_hours(date)

            # Przemnóż każdy element max_lanes i max_tickets przez maksymalną
            # liczbę dostępnych torów i miejsc do rezerwacji
            max_lanes = [x * self._MAX_LANES for x in max_tickets]
            max_tickets = [x * self._TICKETS for x in max_tickets]

            # Ustaw terminarz na każdy dzień by był sklejeniem listy
            # max_tickets i max_lanes, a następnie przekonwertuj na
            # listę list
            month_schedule[date.day] = list(zip(max_tickets, max_lanes))
            month_schedule[date.day] = [list(x) for x in month_schedule[date.day]]

            # inkrementuj datę o jeden dzień
            date += timedelta(days=1)

        return month_schedule

    # Zwraca True jeśli można zarezerwować biet na podaną godzinę
    def _is_valid_reservation(self, schedule: dict, ticket: dict) -> bool:
        date = ticket['date']

        if ticket['type'] == 'private_client':
            if schedule[date.day][date.hour][0] - 1 < 0:
                return False
            return True
        else:
            if schedule[date.day][date.hour][0] - 5 < 0: # Czy to dobry warunek?
                return False
            if schedule[date.day][date.hour][1] - 1 < 0:
                return False
            return True

    # Rezerwuje bilet tj. odejmuje liczbę rezerwowanych biletów od
    # liczby dostępnych biletów o danej godzinie. Jeśli to możliwe zwraca True
    # w przeciwnym wypadku rezerwacja się nieudaje i zwraca False
    def reserve_ticket(self, ticket: dict) -> bool:
        date = ticket['date']
        schedule = self._read_schedule(date)

        if self._is_valid_reservation(schedule, ticket):
            if ticket['type'] == 'private_client':
                schedule[date.day][date.hour][0] -= 1
            else:
                schedule[date.day][date.hour][0] -= 5
                schedule[date.day][date.hour][1] -= 1
            self._update_schedule(schedule, date)
            return True
        return False

    # Znajduje najbliższy termin na który jest możliwa rezerwacja biletu
    def find_next_date(self, ticket: dict) -> dt:
        date = ticket['date']
        schedule = self._read_schedule(date)

        # Szuka terminu w tym miesiącu po podanej dacie
        i = date
        while i.month == date.month:
            ticket['date'] = i
            if self._is_valid_reservation(schedule, ticket):
                return i
            i += timedelta(hours=1)

        # Jeśli nie ma dostępnego terminu w tym miesiącu
        # zaczyna szukać w następnym
        if date.month + 1 > 12:
            ticket['date'] = dt(date.year + 1, 1, 1)
        else:
            ticket['date'] = dt(date.year, date.month + 1, 1)

        return self.find_next_date(ticket)

    # Wypisuje pozostałe bilety / tory w określonym dniu
    def print_day_schedule(self, date: dt) -> None:
        schedule = self._read_schedule(date)

        print(f'{date.date()}:')
        for i, left in enumerate(schedule[date.day]):
            print(f'    {i}: {left}')


if __name__ == '__main__':
    scheduler = Scheduler()
    date = dt(1984, 12, 1, 10, 0)

    ticket = {
        'type': 'private_client',
        'date': date
    }

    if not scheduler.reserve_ticket(ticket):
        next_date = scheduler.find_next_date(ticket)
        ticket['date'] = next_date
        scheduler.reserve_ticket(ticket)
    scheduler.print_day_schedule(ticket['date'])
