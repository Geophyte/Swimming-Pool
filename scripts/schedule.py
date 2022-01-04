from datetime import datetime as dt, timedelta, time
from pathlib import Path
from typing import TextIO
import os
import errno
import json
import calendar
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
            info["OpeningHours"][day][0] = time(info["OpeningHours"][day][0], 0)
            info["OpeningHours"][day][1] = time(info["OpeningHours"][day][1], 0)
        self._opening_hours = info["OpeningHours"]

    # Zwraca prawdę jeśli podana data znajduje się podczas godzin otwarcia
    # pływalni
    def is_open(self, date: dt = dt.now()) -> bool:
        day_of_week = date.strftime('%A')
        open_time = self._opening_hours[day_of_week][0]
        close_time = self._opening_hours[day_of_week][1]

        if open_time <= date.time() and date.time() <= close_time:
            return True
        return False

    # Zwraca listę 24 elementową w której każy element odpowiada
    # godzinie [1-24] i wypełnia ją jedynkami w przedziale od
    # godzina_otwarcia (włącznie) do godzina zamknięcia (wyłącznie)
    def get_opening_hours(self, date: dt = dt.now()) -> list:
        day_of_week = date.strftime('%A')
        open_time = self._opening_hours[day_of_week][0]
        close_time = self._opening_hours[day_of_week][1]

        result = [0] * 24
        for i in range(open_time.hour, close_time.hour):
            result[i] = 1
        return result


# Zwraca ścieżkę bezwzględną do pliku z terminarzem
def get_schedule_path(date: dt = dt.now()) -> str:
    year = date.year
    month = date.strftime('%B').lower()

    schedule_rel_path = f"../data/{year}/{date.month}_{month}_schedule.json"
    return Path(__file__).parent / schedule_rel_path


# Działa jak 'open' przy okazji tworząc plik jeśli nie istnieje,
# otwiera go używając daty zamiast ścieżki
def open_schedule(mode: str, date: dt = dt.now()) -> TextIO:
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


class Schedule:
    # Inicjalizuje klasę Schedule,
    def __init__(self) -> None:
        self._opening_hours = OpeningHours()

        # Wczytaj liczbe torów z ../data/info.json
        info_rel_path = "../data/info.json"
        info_abs_path = Path(__file__).parent / info_rel_path

        with open(info_abs_path, 'r') as info_file:
            info = json.load(info_file)

        self._LANES = info['NUMBER_OF_LANES']
        self._MAX_LANES = math.floor(self._LANES * 0.35)
        self._TICKETS = self._LANES * 5

    # Aktualizuje plik z terminarzem na podstawie słownika 'schedule'
    def _update_schedule(self, schedule: dict, date: dt = dt.now()) -> None:
        with open_schedule('w', date) as schedule_file:
            json.dump(schedule, schedule_file, indent=4)

    # Wczytuje słownik z terminarza, jeśli jest pusty inicjalizuje cały miesiąc
    def _read_schedule(self, date: dt = dt.now()) -> dict:
        with open_schedule('r', date) as schedule_file:
            try:
                temp = json.load(schedule_file)
                temp = {int(k): _ for k, _ in temp.items()}
                return temp
            except json.JSONDecodeError:
                return self._init_month(date)

    # Inicjalizuje miesiąc ustawiając każdą godzinę
    # w godzinach otwarcia na maksimum dostępnych biletów
    def _init_month(self, date: dt = dt.now()) -> dict:
        start_date = dt(date.year, date.month, 1)
        day_count = calendar.monthrange(date.year, date.month)[1]

        month_schedule = dict()
        for n in range(1, day_count + 1):
            temp = self._opening_hours.get_opening_hours(start_date)
            temp = [x * self._TICKETS for x in temp]
            month_schedule[n] = zip(temp, [0] * 24)
            start_date += timedelta(days=1)

        return month_schedule

    def _validate_reservation(self, schedule: dict, ticket: dict) -> bool:
        date = ticket['date']
        if ticket['type'] == 'private_client':
            if schedule[date.day][date.hour][0] - 1 < 0:
                return False
            return True
        else:
            if schedule[date.day][date.hour][0] - 5 < 0:
                return False
            if schedule[date.day][date.hour][1] + 1 > self._MAX_LANES:
                return False
            return True

    # Rezerwuje bilet tj. odejmuje liczbę rezerwowanych biletów od
    # liczby dostępnych biletów o danej godzinie. Jeśli to możliwe zwraca True
    # w przeciwnym wypadku rezerwacja się nieudaje i zwraca False
    def reserve_ticket(self, ticket: dict) -> bool:
        date = ticket['date']
        schedule = self._read_schedule(date)

        if self._validate_reservation(schedule, ticket):
            if ticket['type'] == 'private_client':
                schedule[date.day][date.hour][0] -= 1
            else:
                schedule[date.day][date.hour][0] -= 5
                schedule[date.day][date.hour][1] += 1
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
            if self._validate_reservation(schedule, ticket):
                return i
            i += timedelta(hours=1)

        # Jeśli nie ma dostępnego terminu w tym miesiącu
        # zaczyna szukać w następnym
        if date.month + 1 > 12:
            ticket['date'] = dt(date.year + 1, 1, 1, 1, 0)
        else:
            ticket['date'] = dt(date.year, date.month + 1, 1, 1, 0)

        return self.find_next_date(ticket)
