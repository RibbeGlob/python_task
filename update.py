import urllib.request
import urllib.error
import json
import os
import time
from packaging import version
from tqdm import tqdm
import hashlib


def save_cache(data):
    """
    Funkcja odpowiedzialna za zapisywanie bufora
    """
    cache_file = 'updateCache.json'
    try:
        with open(cache_file, 'w') as file:
            json.dump(data, file)
    except IOError as e:
        print(f"Błąd podczas zapisywania bufora: {e}")


def decor_check_cache(func):
    """
    Dekorator odpowiedzialny za sprawdzanie bufora danych
    """
    cache_file = 'updateCache.json'
    cache_duration = 3600

    def wrapper(*args, **kwargs):
        try:
            if os.path.exists(cache_file) and time.time() - os.path.getmtime(cache_file) < cache_duration:
                try:
                    with open(cache_file, 'r') as file:
                        data = json.load(file)
                        return data
                except json.JSONDecodeError:
                    print('Błąd parsowania buforowanych danych')
        except Exception as e:
            print(f"Błąd podczas sprawdzania bufora: {e}")

        data = func(*args, **kwargs)
        save_cache(data)
        return data
    return wrapper


@decor_check_cache
def download_json(url, timeout=10):
    """
    Funkcja odpowiedzialna za pobieranie pliku JSON z serwera
    """
    max_retries = 3
    delay = 5
    for attempt in range(max_retries):
        try:
            with urllib.request.urlopen(url, timeout=timeout) as response:
                data = json.loads(response.read().decode())
                return data
        except urllib.error.HTTPError as e:
            print(f'HTTP error: {e.code} {e.reason}')
            time.sleep(delay)
        except urllib.error.URLError as e:
            print(f'URL error: {e.reason}')
            time.sleep(delay)
        except json.JSONDecodeError:
            print('Błąd parsowania')
            time.sleep(delay)
        except Exception as e:
            print(f'Unexpected error: {e}')
            time.sleep(delay)

    return None


def check_available_updates(data, current_version, check_type, stage='stable'):
    """
    Funkcja odpowiedzialna za sprawdzanie czy jest nowsza wersja oprogramowania
    """
    branch_key = 'updateData' if stage == 'stable' else f'updateData_{stage}'
    revisions = data[branch_key]['revisions']
    available_update = None
    for revision in revisions:
        checked_version = version.parse(revision[check_type]['version'])
        if checked_version > version.parse(current_version):
            available_update = revision[check_type]['version']
    return available_update


def decor_sha_calc(func):
    """
    Dekorator odpowiedzialny za obliczanie sumy kontrolnej pobranego pliku
    """
    def wrapper(url, expected_sha256):
        local_filename = func(url)
        if not local_filename:
            return False
        try:
            with open(local_filename, 'rb') as f:
                calculated_sha256 = hashlib.sha256(f.read()).hexdigest()
            if expected_sha256 and calculated_sha256 != expected_sha256:
                print(f"Suma kontrolna nie zgadza się.")
                return False
            print(f"Plik {local_filename} został pobrany i zweryfikowany")
            return True
        except Exception as e:
            print(f"Wystąpił błąd: {str(e)}")
            return False

    return wrapper


@decor_sha_calc
def download_file(url):
    """
    Funkcja odpowiedzialna za pobieranie pliku
    """
    timestamp = int(time.time())
    filename = f"{timestamp}_{url.split('/')[-1]}"
    try:
        with urllib.request.urlopen(url) as response, open(filename, 'wb') as out_file:
            total_length = response.getheader('content-length')
            pbar = tqdm(total=int(total_length) if total_length else None, unit='B', unit_scale=True, desc=filename)
            for data in iter(lambda: response.read(4096), b''):
                out_file.write(data)
                pbar.update(len(data))
            pbar.close()
    except urllib.error.URLError as e:
        print(f"Cannot download the file: {e.reason}")
        return None
    except Exception as e:
        print(f"Error during file download: {e}")
        return None

    return filename


def download_manager(chosen_stage, data, available):
    """
    Funkcja odpowiedzialna za sterowanie pobieranymi plikami
    """
    print(f"Pobieram aktualizację {chosen_stage}...")
    branch_key = 'updateData' if chosen_stage == 'stable' else f'updateData_{chosen_stage}'
    updates = available[chosen_stage]

    for revision in data[branch_key]['revisions']:
        # Aktualizacja firmware
        if 'firmware' in revision and revision['firmware']['version'] == updates.get('firmware', {}):
            download_file(revision['firmware']['file'], revision['firmware'].get('sha256', ''))

        # Aktualizacja software oraz kernela
        if 'software' in revision and revision['software']['version'] == updates.get('software', {}):
            download_file(revision['software']['file'], revision['software'].get('sha256', ''))
            if 'kernel' in revision['software']:
                kernel_info = revision['software']['kernel']
                download_file(kernel_info, revision['software'].get('kernel_sha256', ''))

    print("Pobieranie zakończone")


def available_updates(available, data):
    """
    Funkcja odpowiedzialna za wyświetlanie dostępnych aktualizacji oraz ich wybór
    """
    print("Dostępne etapy aktualizacji:")
    for stage, updates in available.items():
        print(f"- {stage}: Firmware: {updates['firmware']}, Software: {updates['software']}")
    while True:
        chosen_stage = input("Wybierz etap aktualizacji (stable/beta/long_term): ").strip()
        if chosen_stage in available:
            decision = input(f"Czy chcesz przeprowadzić aktualizację {chosen_stage}? (tak/nie): ").strip().lower()
            if decision == "tak":
                download_manager(chosen_stage, data, available)
                break
            else:
                print("Aktualizacja anulowana")
                break
        else:
            print("Nieprawidłowy wybór etapu")


def main(current_firmware, current_software):
    """
    Główna funkcja programu
    Konieczne jest umiejscowienie prawidłowego adresu w zaznaczonym miejscu, w innym wypadku program nie będzie działał
    """
    data = download_json('your_url')   # Tutaj umieść prawidłowy url
    if data is None:
        print("Nie udało się pobrać danych o aktualizacji")
        try:
            os.remove("updateCache.json")
        except FileNotFoundError:
            pass
        return

    stages = ['stable', 'beta', 'long_term']
    available = {}
    for stage in stages:
        firmware_update = check_available_updates(data, current_firmware, 'firmware', stage) or 'brak'
        software_update = check_available_updates(data, current_software, 'software', stage) or 'brak'
        if firmware_update != 'brak' or software_update != 'brak':
            available[stage] = {
                'firmware': firmware_update,
                'software': software_update
            }

    if available:
        available_updates(available, data)
    else:
        print("Brak dostępnych aktualizacji")


# Przykładowe uruchomienie programu
if __name__ == '__main__':
    main('1.0.6', '1.5.0')
