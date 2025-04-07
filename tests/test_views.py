import logging
import unittest
from unittest.mock import patch

from src.views import home_page

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TestHomePageFunction(unittest.TestCase):

    def test_valid_date(self):
        # Тест с корректной датой
        datetime_str = "2023-04-01 12:00:00"
        response = home_page(datetime_str)
        self.assertNotIn("error", response)

    def test_invalid_date(self):
        # Тест с некорректной датой
        datetime_str = "2023-04-01"
        response = home_page(datetime_str)
        self.assertIn("error", response)

    @patch("src.data_reader.load_excel_transactions")
    def test_empty_transactions(self, mock_load_excel_transactions):
        # Тест с пустым списком транзакций
        mock_load_excel_transactions.return_value = []
        datetime_str = "2020-04-01 12:00:00"
        response = home_page(datetime_str)
        self.assertEqual(response["cards"], [])
        self.assertEqual(response["top_transactions"], [])

    @patch("src.utils.load_user_settings")
    @patch("src.external_api.get_exchange_rates")
    @patch("src.external_api.get_stock_prices")
    def test_user_settings_and_external_api(
        self, mock_get_stock_prices, mock_get_exchange_rates, mock_load_user_settings
    ):
        # Тест настроек пользователя и внешних API
        mock_load_user_settings.return_value = {"user_currencies": ["USD", "EUR"], "user_stocks": ["AAPL", "GOOG"]}
        mock_get_exchange_rates.return_value = {"USD": 60.0, "EUR": 70.0}
        mock_get_stock_prices.return_value = {"AAPL": 150.0, "GOOG": 2000.0}
        datetime_str = "2023-04-01 12:00:00"
        response = home_page(datetime_str)
        self.assertIn("currency_rates", response)
        self.assertIn("stock_prices", response)


if __name__ == "__main__":
    unittest.main()
