from datetime import datetime as dt, timedelta, time
from pathlib import Path
from typing import TextIO
import os
import errno
import json
import calendar


class OpeningHours:
    def __init__(self) -> None:
        # Wczytaj godzinny otwarcia z ../data/opening_hours.json
        opening_hours_rel_path = "../data/opening_hours.json"
        opening_hours_abs_path = Path(__file__).parent / opening_hours_rel_path

        with open(opening_hours_abs_path, 'r') as opening_hours_file:
            oh_list = json.load(opening_hours_file)

        # Przekonweruj wczytany słownik liczb na słownik klas 'time'
        for day in oh_list:
            oh_list[day][0] = time(oh_list[day][0], 0)
            oh_list[day][1] = time(oh_list[day][1], 0)
        self._opening_hours = oh_list

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
            result[i - 1] = 1
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
    # jako argument przyjmuje maksimum dostępnych biletów
    def __init__(self, tickets: int) -> None:
        self._opening_hours = OpeningHours()
        self._tickets = tickets

    # Aktualizuje plik z terminarzem na podstawie słownika 'schedule'
    def _update_schedule(self, schedule: dict,
                         date: dt = dt.now()) -> None:
        with open_schedule('w', date) as schedule_file:
            json.dump(schedule, schedule_file)

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
            temp = [x * self._tickets for x in temp]
            month_schedule[n] = temp
            start_date += timedelta(days=1)

        return month_schedule

    # Rezerwuje bilet tj. odejmuje liczbę rezerwowanych biletów od
    # liczby dostępnych biletów o danej godzinie. Jeśli to możliwe zwraca True
    # w przeciwnym wypadku rezerwacja się nieudaje i zwraca False
    def reserve_tickets(self, date: dt = dt.now(), ticket: dict) -> bool:
        schedule = self._read_schedule(date)

        if ticket['type'] == 'private_client':
            number = 1
        else:
            number = 5

        if schedule[date.day] - number < 0:
            return False

        schedule[date.day] -= number
        self._update_schedule(schedule, date)
        return True

    # Znajduje najbliższy termin na który jest możliwa rezerwacja biletu
    def find_next_date(self, number: int = 1, date: dt = dt.now()) -> dt:
        schedule = self._read_schedule(date)

        # 'Zaokrągla w górę' date do pełnych godzin
        if date.minute > 0:
            date = dt(date.year, date.month, date.day, date.hour, 0)
            date += timedelta(hours=1)

        # Szuka terminu w tym miesiącu po podanej dacie
        i = date
        while i.month == date.month:
            if schedule[i.day][i.hour - 1] - number >= 0:
                return i
            i += timedelta(hours=1)

        # Jeśli nie ma dostępnego terminu w tym miesiącu
        # zaczyna szukać w następnym
        if date.month + 1 > 12:
            next_month = dt(date.year + 1, 1, 1, 1, 0)
        else:
            next_month = dt(date.year, date.month + 1, 1, 1, 0)

        return self.find_next_date(number, next_month)
