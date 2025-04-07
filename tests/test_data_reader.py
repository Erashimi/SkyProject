import logging
import os
import unittest

import pandas as pd

from src.data_reader import load_csv_transactions, load_excel_transactions

logging.basicConfig(level=logging.INFO)


class TestTransactionLoaders(unittest.TestCase):

    def setUp(self):
        self.data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
        self.csv_file_path = os.path.join(self.data_dir, "transactions.csv")
        self.excel_file_path = os.path.join(self.data_dir, "operations.xlsx")

        # Создание тестового CSV-файла
        if not os.path.exists(self.csv_file_path):
            pd.DataFrame({"column1": [1, 2, 3], "column2": ["a", "b", "c"]}).to_csv(self.csv_file_path, index=False)

        # Создание тестового Excel-файла
        if not os.path.exists(self.excel_file_path):
            df = pd.DataFrame(
                {
                    "Дата операции": ["01.01.2023 00:00:00", "02.01.2023 00:00:00"],
                    "Номер карты": [123, 456],
                    "Статус": ["success", "failed"],
                    "Сумма операции": [-100.0, 200.0],
                    "Валюта операции": ["USD", "EUR"],
                    "Категория": ["shop", "transfer"],
                }
            )
            df.to_excel(self.excel_file_path, index=False)

    def tearDown(self):
        if os.path.exists(self.csv_file_path):
            os.remove(self.csv_file_path)
        if os.path.exists(self.excel_file_path):
            os.remove(self.excel_file_path)

    def test_load_csv_transactions(self):
        transactions = load_csv_transactions()
        self.assertIsInstance(transactions, list)
        self.assertGreaterEqual(len(transactions), 0)

    def test_load_excel_transactions(self):
        transactions = load_excel_transactions()
        self.assertIsInstance(transactions, list)
        self.assertGreaterEqual(len(transactions), 0)
        # Проверка структуры данных
        if transactions:
            self.assertIn("operationAmount", transactions[0])
            self.assertIn("amount", transactions[0]["operationAmount"])
            self.assertIn("currency", transactions[0]["operationAmount"])

    def test_load_csv_transactions_empty_file(self):
        # Тест на случай, если CSV-файл пуст
        if os.path.exists(self.csv_file_path):
            os.remove(self.csv_file_path)
        transactions = load_csv_transactions()
        self.assertEqual(transactions, [])

    def test_load_excel_transactions_empty_file(self):
        # Тест на случай, если Excel-файл пуст
        if os.path.exists(self.excel_file_path):
            os.remove(self.excel_file_path)
        transactions = load_excel_transactions()
        self.assertEqual(transactions, [])


if __name__ == "__main__":
    unittest.main()
