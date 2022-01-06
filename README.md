# Swimming pool

## Temat
Napisz program do obsługi pływalni. Pływalnia ma nazwę, godziny pracy, cennik oraz określoną liczbę torów. Są dwa rodzaje klientów na pływalni: szkółki pływackie i klienci indywidualni. Klienci mogą rezerwować bilety na pływalnie na wyznaczoną godzinę. Minimalny czas rezerwacji to jedna godzina. Maksymalna liczba dostępnych biletów jest równa pięć razy liczba wolnych torów. Szkółki pływackie mogą rezerwować cały tor. W jednym momencie szkółki pływackie nie mogą zarezerwować więcej niż 35% wszystkich torów.

Program obsługujący pływalnie powinien umożliwiać rezerwację biletów dla klientów indywidualnych oraz rezerwację torów dla szkółek pływackich z uwzględnieniem dostępności i warunków opisanych powyżej. W przypadku braku miejsc na wybrany przez klienta termin, program powinien zaproponować najbliższy możliwy termin. Program ma przechowywać historię rezerwacji oraz na koniec dnia tworzyć raport finansowy, pokazujący jaki jest przychód pływalni danego dnia. Cennik pływalni powinien być zróżnicowany, w zależności od pory dnia, dnia tygodnia oraz rodzaju klienta.

## Dokumentacja
Program pobiera dane do działania z data/info.json

## Pytania
Czy wynajęcie toru jest jak zakup 5 biletów (z uwzględnieniem max 35% torów)?
