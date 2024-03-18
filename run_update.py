from update import main
import argparse
import unittest
import test

parser = argparse.ArgumentParser(description='Program sprawdzający czy jest możliwość aktualizacji oprogramowania.\n'
                                             'Sprawdza się zarówno oprogramowanie sprzętowe (firmware) oraz '
                                             'oprogramowanie zwykłe (software). Dodatkową opcją jest uruchomienie'
                                             'wbudowanych testów jednostkowych.')
parser.add_argument('Firmware', type=str, nargs='?', help='Aktualna wersja firmware, (default 1.0.6)', default="1.0.6")
parser.add_argument('Software', type=str, nargs='?', help='Aktualna wersja software, (default 1.5.0)', default="1.5.0")
parser.add_argument('--test', action='store_true', help='Uruchom wbudowane testy jednostkowe')

args = parser.parse_args()

if __name__ == "__main__":
    if args.subtract:
        loader = unittest.TestLoader()            # Załaduj i uruchom testy jednostkowe
        suite = loader.loadTestsFromModule(test)  # Załaduj wszystkie testy
        unittest.TextTestRunner().run(suite)
    else:
        main(args.Firmware, args.Software)        # Odpal szukanie aktualizacji
