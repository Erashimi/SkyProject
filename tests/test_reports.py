import json
import logging
import unittest

import pandas as pd

from src.reports import report_to_file, spending_by_category

# Настройка логгирования для тестов
logging.basicConfig(level=logging.INFO)


class TestReports(unittest.TestCase):

    def setUp(self):
        # Создание тестового датафрейма
        self.transactions = pd.DataFrame(
            {
                "date": [
                    pd.to_datetime("2020-01-01"),
                    pd.to_datetime("2020-02-01"),
                    pd.to_datetime("2020-03-01"),
                    pd.to_datetime("2020-04-01"),
                    pd.to_datetime("2020-05-01"),
                ],
                "Категория": ["Супермаркеты", "Ж/д билеты", "Супермаркеты", "Ж/д билеты", "Супермаркеты"],
                "Сумма платежа": [-100, -200, -50, -150, -300],
            }
        )

    def test_spending_by_category_empty(self):
        # Тестирование функции spending_by_category с пустым результатом
        result = spending_by_category(self.transactions, "")
        self.assertEqual(len(result), 0)  # Проверка пустого датафрейма

    def test_report_to_file(self):
        # Тестирование декоратора report_to_file
        @report_to_file(filename="test_report.json")
        def test_function():
            return {"test": "data"}

        test_function()
        with open("test_report.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            self.assertEqual(data, {"test": "data"})  # Проверка содержимого файла

        # Удаление тестового файла
        import os

        os.remove("test_report.json")


if __name__ == "__main__":
    unittest.main()
