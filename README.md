# python_task

## Wstęp
Aplikacja do sprawdzenia możliwych aktualizacji oprogramowania to narzędzie wiersza poleceń napisane w języku Python. Umożliwia ona pobranie aktualizacji oprogramowania (software oraz firmware) z zewnętrznego serwera. Aplikacja oferuje tryb testowy dla sprawdzenia działania najważniejszych bloków kodu. Jeżeli potrzebujesz jedynie modułu odpowiedzialnego za sprawdzanie dostępnych aktualizacji pobierz plik "update.py"

## Wymagania
- Python
- Adres serwera z którego będą pobierane dane
- Zewnętrzne pakiety:
  - packaging (potrzebny do obsługi wersji w ekosystemie Python)
  - tqdm (potrzebny do utworzenia graficznego paska postępu pobieranych plików)

## Konfiguracja

### Otrzymaj adres URL
Aby w prawidłowy sposób używać aplikacji, otrzymaj adres serwera z którego zosaną pobrane informacje o możliwości aktualizacji oprogramowania. 
Po otrzymaniu adresu zmodyfikuj w następujący sposób plik "update.py":
1. Otwórz plik "update.py"
2. Znajdź w nim funkcję "main" oraz zmienną "data" (okolice 187 linijki)
3. Zmień string "your_url" na otrzymany adres serwera
4. Zapisz zmiany

![obraz](https://github.com/RibbeGlob/python_task/assets/108761666/60f27c0a-bfd6-4648-acd0-96393867c5ff)

### Zainstaluj wymagane zewnętrzne pakiety
Aby aplikacja działała w prawidłowy sposób należy zainstalować wcześniej wymienione pakiety (packaging oraz tqdm). Istnieje wiele możliwych podejść do instalacji pakietów, jednakże tutaj zostanie pokazany sposób instalacji poprzez system do zarządzania pakietami (pip ang. Preffered Installer Program).

1. Włącz terminal
2. Wpisz w nim
   ```
   pip install packaging
3. Następnie wpisz w nim
   ```
   pip install tqdm
Jeżeli prawidłowo zostały wpisane komendy, pip zainstalował wymagane pakiety.

## Działanie programu

### Dostępne opcje
Aplikację można uruchomić w trzech trybach:
- Tryb domyślny (włącza moduł z domyślnymi wartościami)
- Tryb ręczny (użytkownik wpisuje w terminalu wersję obecnego oprogramowania
- Tryb testowy (zostają włączone testy najważniejszych bloków programu

Dostępne opcje przy włączeniu aplikacji
```
usage: run_update.py [-h] [--test] [Firmware] [Software]
positional arguments:
  Firmware    Aktualna wersja firmware, (default 1.0.6)
  Software    Aktualna wersja software, (default 1.5.0)

options:
  -h, --help  show this help message and exit
  --test      Uruchom wbudowane testy jednostkowe
```

### Uruchomienie programu
- Pobierz wszystkie pliki z tego rezpozytorium a następnie je wypakuj.
- Za pomocą terminala przejdź do lokalizacji wypakowanych plików
- Uruchom program poleceniem
  ```
  python run_update.exe (wpisując odpowiednie argumenty wybierasz tryb działania pracy programu)

Przykładowe uruchomienie programu:
![obraz](https://github.com/RibbeGlob/python_task/assets/108761666/35706301-699c-4a47-9407-4f9900972ca1)


