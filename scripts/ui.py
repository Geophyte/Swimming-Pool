from datetime import datetime as dt, timedelta
from pathlib import Path
import json


class UI:
    def __init__(self) -> None:
        # Wczytaj nazwę pływalni z ../data/info.json
        info_rel_path = "../data/info.json"
        info_abs_path = Path(__file__).parent / info_rel_path

        with open(info_abs_path, 'r') as info_file:
            info = json.load(info_file)

        self._NAME = info['NAME']

        self._ticket_age_options = ['Dziecko', 'Student', 'Normalny', 'Senior']
        self._ticket_age = ['child', 'student', 'normal', 'senior']
        self._ticket_type_options = ['Klient indywidualny', 'Wynajęcie toru']
        self._ticket_type = ['private_client', 'swimming_school']

    def clear(self) -> None:
        print('\n' * 100)
        print('#' * 20)
        print(self._NAME)
        print('#' * 20)
        print('\n')

    def input_option(self, options: list) -> int:
        for i, option in enumerate(options):
            print(f'{i}) {option}')
        option = int(input('Opcja: '))
        if option >= len(options):
            # self.clear()
            print('Podaj poprawną opcje')
            return self.input_option(options)
        return option

    def input_date(self) -> dt:
        date = input('Data [yyyy-mm-dd]: ')

        try:
            date = dt.strptime(date, '%Y-%m-%d')
        except ValueError:
            self.clear()
            print('Wprowadź poprawną datę')
            return self.input_date()

        hour = int(input('Godzina: '))

        if 0 >= hour or hour > 24:
            self.clear()
            print('Podaj godzinę w przedziale 0-23')
            return self.input_date()

        date += timedelta(hours=hour)

        if dt.now() >= date:
            self.clear()
            print('Podaj termin, który jeszcze nie minął')
            return self.input_date()

        return date

    def input_ticket(self, date: dt) -> dict:
        print('Typ biletu: ')
        type = self.input_option(self._ticket_type_options)

        if type == 0:
            print('Kategoria wiekowa: ')
            age = self.input_option(self._ticket_age_options)
        else:
            age = 0

        return {
            'type': self._ticket_type[type],
            'age': self._ticket_age[age],
            'date': date
            }


if __name__ == '__main__':
    dt.strptime('2022-01-07', '%Y-%m-%d')
