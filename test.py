import unittest
from unittest.mock import patch, mock_open
from update import check_available_updates, decor_sha_calc
import hashlib


# Testowanie dostępności aktualizacji
class TestCheckUpdates(unittest.TestCase):
    """
    Testowanie dostępnych aktualizacji
    """
    def test_check_updates(self):
        """
        Sprawdza przypadek gdy jest możliwa aktualizacja
        :1.0.6:
        """
        dane = {
            'updateData': {
                'revisions': [
                    {'software': {'version': '1.0.4'}},
                    {'software': {'version': '1.0.3'}},
                ]
            },
            'updateData_beta': {
                'revisions': [
                    {'software': {'version': '1.0.3'}},
                    {'software': {'version': '1.0.6'}},
                ]
            }
        }
        current_version = '1.0.4'
        which_type = 'software'
        stage = 'beta'
        result = check_available_updates(dane, current_version, which_type, stage)
        self.assertEqual(result, '1.0.6')

    def test_none_updates(self):
        """
        Sprawdza przypadek gdy nie ma możliwych aktualizacji
        :None:
        """
        dane = {
            'updateData': {
                'revisions': [
                    {'software': {'version': '1.0.2'}},
                    {'software': {'version': '1.0.3'}},
                ]
            },
            'updateData_beta': {
                'revisions': [
                    {'software': {'version': '1.0.2'}},
                    {'software': {'version': '1.0.3'}},
                ]
            }
        }
        current_version = '1.0.4'
        which_type = 'software'
        result = check_available_updates(dane, current_version, which_type)
        self.assertIsNone(result)


# Pusta funkcja do dekorowania (musi być url żeby dobrze dekorowało)
def dummy(url):
    return "dummy_file_path"


# Udekorowanie dummy
decor_dummy = decor_sha_calc(dummy)


class TestShaDecorator(unittest.TestCase):
    """
    Testowanie poprawności sumy kontrolnej
    """
    @patch("builtins.open", new_callable=mock_open, read_data=b"test file content")
    def test_sha_decorator_with_correct_sha256(self, mock_file):
        """
        Sprawdza przypadek gdy sha jest poprawne
        :True:
        """
        sha256 = hashlib.sha256()
        sha256.update(b"test file content")
        expected_sha256 = sha256.hexdigest()
        result = decor_dummy("http://test.pl/aco", expected_sha256)
        self.assertTrue(result)

    @patch("builtins.open", new_callable=mock_open, read_data=b"test file content")
    def test_sha_decorator_with_incorrect_sha256(self, mock_file):
        """
        Sprawdza przypadek gdy sha jest niepoprawne
        :False:
        """
        incorrect_sha256 = "AcoAco"
        result = decor_dummy("http://test.pl/aco", incorrect_sha256)
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
