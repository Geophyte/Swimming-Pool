from scripts._schedule import Schedule
from financial_report import FinancialReport
from datetime import datetime as dt


NUM_OF_LANES = 10
NUM_OF_TICEKTS = NUM_OF_LANES * 5

menue_options = ['Kup bilet', 'Wyjście']
date_options = ['Najbliższa godzina', 'Konkretna data']
ticket_age = ['Dziecko', 'Student', 'Normalny', 'Senior']
ticket_type = ['Klient indywidualny', 'Wynajęcie toru']

schedule = Schedule(NUM_OF_TICEKTS)
report = FinancialReport()


def clear() -> None:
    print('\n' * 100)


def input_option(options: list) -> int:
    for i, option in enumerate(options):
        print(f'{i}) {option}')
    option = int(input("Opcja: "))
    if option >= len(options):
        clear()
        print("Podaj poprawną opcje")
        return input_option()
    return option


def input_date(num_of_tickets: int) -> dt:
    option = input_option(date_options)
    if option == 0:
        schedule.find_next_date(num_of_tickets)
    # TO DO
    # dodaj try, except dla niewłaściwej daty


def input_ticket() -> dict:
    print("Wybierz typ biletu:")
    t_type = input_option(ticket_type)
    clear()
    if t_type == 0:
        print("Wybierz kategorię wiekową:")
        age = input_option(ticket_age)
        clear()
    else:
        age = 0

    print("Data wejścia:")
    if t_type == 0:
        date = input_date(1)
    else:
        date = input_date(5)

    ticket = {
        'age': ticket_age[age],
        'type': ticket_type[t_type],
        'date': date
    }
    return ticket


def main():
    while True:
        option = input_option(menue_options)

        if option == 0:
            pass
        else:
            break


if __name__ == '__main__':
    main()
