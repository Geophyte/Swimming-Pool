from ui import UI
from accountant import Accountant
from scheduler import Scheduler
from datetime import datetime as dt, timedelta


# Możliwe do wykonania operacje
menu_options = [
    'Kup bilet', 'Dzisiejszy raport', 'Dzisiejszy terminarz', 'Wyjście'
    ]
date_options = [
    'Teraz', 'Wybierz termin'
    ]
ticket_option = [
    'Kup bilet na wyznaczoną godzinę', 'Anuluj'
    ]

# Zmienne globalne
ui = UI()
accountant = Accountant('../data/info.json')
scheduler = Scheduler('../data/info.json')


# Pyta użytkownika o informacje związane z biletem.
# Jeśli to możliwe kupuje i rezerwuje wprowadzony bilet
def buy_ticket() -> None:
    print('Wybierz termin: ')
    option = ui.input_option(date_options)

    # 0: Kup bilet na najbliższą przyszłą godzinę
    # 1: Kup bilet na wprowadzony termin
    if option == 0:
        date = dt.now()

        # Zaokrąglij godzinę 'w górę' do pełnej godziny
        if date.minute > 0:
            date = dt(date.year, date.month, date.day, date.hour)
            date += timedelta(hours=1)

        ticket = ui.input_ticket(date)
    else:
        ticket = ui.input_ticket(ui.input_date())

    # Jeśli nie uda się zarezewować biletu zaproponuj najbliższą możliwą datę
    if not scheduler.reserve_ticket(ticket):
        next_date = scheduler.find_next_date(ticket)
        print('\nNie można kupić biletu na wyznaczony termin.')
        print(f'Najblizszy możliwy termin to: {next_date}')

        option = ui.input_option(ticket_option)

        # 0: Kup bilet na podaną datę
        # 1: Anuluj kupowanie biletu
        if option == 0:
            ticket['date'] = next_date
            scheduler.reserve_ticket(ticket)
        else:
            return

    # Zarejestruj transakcję
    price = accountant.regsiter_transaction(ticket)
    print(f"Pomyślnie zakupiono bilet na termin {ticket['date']}")
    print(f"Cena: {price}")
    input('Kliknji Enter, aby kontynuować')


def main() -> None:
    ui.clear()
    option = ui.input_option(menu_options)

    # 0: Kup bilet
    # 1: Wypisz raport z dzisiaj
    # 2: Wypisz terminarz z dzisiaj
    # 3: Wyjście
    if option == 0:
        ui.clear()
        buy_ticket()
    elif option == 1:
        ui.clear()
        accountant.print_report(dt.now())
        input('Kliknji Enter, aby kontynuować')
    elif option == 2:
        ui.clear()
        scheduler.print_day_schedule(dt.now())
        input('Kliknji Enter, aby kontynuować')
    else:
        return
    return main()


if __name__ == '__main__':
    main()
