# Swimming pool

## Temat
Napisz program do obsługi pływalni. Pływalnia ma nazwę, godziny pracy, cennik oraz określoną liczbę torów. Są dwa rodzaje klientów na pływalni: szkółki pływackie i klienci indywidualni. Klienci mogą rezerwować bilety na pływalnie na wyznaczoną godzinę. Minimalny czas rezerwacji to jedna godzina. Maksymalna liczba dostępnych biletów jest równa pięć razy liczba wolnych torów. Szkółki pływackie mogą rezerwować cały tor. W jednym momencie szkółki pływackie nie mogą zarezerwować więcej niż 35% wszystkich torów.

Program obsługujący pływalnie powinien umożliwiać rezerwację biletów dla klientów indywidualnych oraz rezerwację torów dla szkółek pływackich z uwzględnieniem dostępności i warunków opisanych powyżej. W przypadku braku miejsc na wybrany przez klienta termin, program powinien zaproponować najbliższy możliwy termin. Program ma przechowywać historię rezerwacji oraz na koniec dnia tworzyć raport finansowy, pokazujący jaki jest przychód pływalni danego dnia. Cennik pływalni powinien być zróżnicowany, w zależności od pory dnia, dnia tygodnia oraz rodzaju klienta.

## Pliki
data/info.json - plik z wszystkimi danymi o pływalni

data/[yyyy]/[...]_schedule.json - plik zawierający liczbę możliwych do zarezerwowania biletów indywidualnych i torów w danym dniu o danej godzinie miesiąca

data/[yyyy]/[...]_report.json - plik zawierający raport finansowy dla każdego dnia miesiąca

scripts/accountant.py - moduł zawierający klasy: Accountant zajmującej się sporządzaniem raportu finansowego z danego dnia oraz PriceList zajmująca się wyliczaniem kosztu zakupu biletów oraz wynajęcia toru

scripts/scheduler.py - moduł zawierający klasy: Scheduler zajmującej się rezerwacją biletów na podany termin oraz OpeningHours zajmująca się interpretacją wczytancy godzin otwarcia

scripts/ui.py - moduł zawierający klasę UI z funkcjami pomocniczymi dla modułu main.py

scripts/main.py - moduł wykonujący opisany w temacie program
