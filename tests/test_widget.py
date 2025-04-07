import unittest
from unittest.mock import patch

from src.widget import get_date, mask_account_card


class TestMaskingFunctions(unittest.TestCase):

    @patch("src.widget.get_mask_account")
    @patch("src.widget.get_mask_card_number")
    def test_mask_account_card(self, mock_get_mask_card_number, mock_get_mask_account):
        mock_get_mask_account.return_value = "1234"
        mock_get_mask_card_number.return_value = "5678"

        # Тест для счета
        result = mask_account_card("Счет 1234567890")
        mock_get_mask_account.assert_called_once_with("1234567890")
        self.assertEqual(result, "Счет 1234")

        # Тест для карты
        mock_get_mask_account.reset_mock()
        mock_get_mask_card_number.reset_mock()
        result = mask_account_card("Карта 1234567890")
        mock_get_mask_card_number.assert_called_once_with("1234567890")
        self.assertEqual(result, "Карта 5678")

    def test_get_date(self):
        # Тест для корректной даты
        date_str = "2023-09-01"
        expected_result = "01.09.2023"
        self.assertEqual(get_date(date_str), expected_result)

        # Тест для некорректной даты (слишком короткая строка)
        with self.assertRaises(ValueError):
            get_date("2023-09")

        # Тест для некорректной даты (неправильный формат)
        with self.assertRaises(ValueError):
            get_date("01.09.2023")

        # Тест для некорректной даты (месяц или день не цифры)
        with self.assertRaises(ValueError):
            get_date("2023-XX-01")


if __name__ == "__main__":
    unittest.main()
