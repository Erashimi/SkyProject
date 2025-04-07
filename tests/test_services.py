import logging
import unittest
from datetime import datetime
from typing import Dict, List
from unittest.mock import patch

from src.services import calculate_cashback_by_category

# Настройка логгирования для тестов
logging.basicConfig(level=logging.INFO)


class TestCalculateCashbackByCategory(unittest.TestCase):

    def test_empty_data(self):
        """Тест на пустой список транзакций."""
        data: List[Dict] = []
        year = 2023
        month = 1
        result = calculate_cashback_by_category(data, year, month)
        self.assertEqual(result, {})

    def test_no_transactions_in_month(self):
        """Тест на отсутствие транзакций в указанном месяце."""
        data = [
            {"date": datetime(2023, 2, 1), "amount": -100, "category": "Еда"},
            {"date": datetime(2023, 3, 1), "amount": -200, "category": "Транспорт"},
        ]
        year = 2023
        month = 1
        result = calculate_cashback_by_category(data, year, month)
        self.assertEqual(result, {})

    def test_cashback_calculation(self):
        """Тест на правильный расчет кешбэка."""
        data = [
            {"date": datetime(2023, 1, 1), "amount": -100, "category": "Еда"},
            {"date": datetime(2023, 1, 15), "amount": -200, "category": "Транспорт"},
            {"date": datetime(2023, 1, 20), "amount": -50, "category": "Еда"},
        ]
        year = 2023
        month = 1
        expected_result = {"Еда": 1.5, "Транспорт": 2.0}  # (100 + 50) * 0.01  # 200 * 0.01
        result = calculate_cashback_by_category(data, year, month)
        self.assertEqual(result, expected_result)

    def test_error_handling(self):
        """Тест на обработку ошибок."""
        data = [{"date": datetime(2023, 1, 1), "amount": "invalid", "category": "Еда"}]
        year = 2023
        month = 1
        result = calculate_cashback_by_category(data, year, month)
        self.assertEqual(result, {})

    @patch("src.services.logger")
    def test_logging_on_error(self, mock_logger):
        """Тест на логирование ошибок."""
        data = [{"date": datetime(2023, 1, 1), "amount": "invalid", "category": "Еда"}]
        year = 2023
        month = 1
        calculate_cashback_by_category(data, year, month)
        mock_logger.error.assert_called_once()


if __name__ == "__main__":
    unittest.main()
