import logging
import os
from typing import Dict, List

import pandas as pd

logger = logging.getLogger(__name__)

# Путь к data относительно текущего модуля (придумать замену)
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")


def load_csv_transactions() -> List[Dict]:
    """Загружает транзакции из CSV-файла в папке data"""
    file_path = os.path.join(DATA_DIR, "transactions.csv")
    try:
        df = pd.read_csv(file_path)
        logger.info(f"Успешно загружен CSV: {file_path}")
        return df.to_dict("records")
    except Exception as e:
        logger.error(f"Ошибка загрузки CSV: {e}")
        return []


def load_excel_transactions() -> List[Dict]:
    """Загружает транзакции из Excel и преобразует в нужный формат"""
    file_path = os.path.join(DATA_DIR, "operations.xlsx")
    try:
        # Загрузка данных с правильным форматом даты
        df = pd.read_excel(
            file_path,
            parse_dates=["Дата операции"],
            date_format=lambda x: pd.to_datetime(x, format="%d.%m.%Y %H:%M:%S", dayfirst=True),
            thousands=",",
            decimal=".",
            engine="openpyxl",
        )

        # Переименование колонок
        df = df.rename(
            columns={
                "Дата операции": "date",
                "Номер карты": "from",
                "Статус": "status",
                "Сумма операции": "amount",
                "Валюта операции": "currency",
                "Категория": "category",
            }
        )

        df["from"] = df["from"].astype(str).replace("nan", "")
        df["date"] = pd.to_datetime(df["date"], format="%d.%m.%Y %H:%M:%S")

        # Создаем структуру operationAmount
        df["operationAmount"] = df.apply(
            lambda row: {
                "amount": abs(row["amount"]),  # Пример: -160.89 → 160.89
                "currency": {"code": row["currency"]},
            },
            axis=1,
        )

        # Преобразуем в список словарей
        transactions = df.to_dict("records")

        logger.info(f"Успешно загружено {len(transactions)} транзакций")
        return df.to_dict("records")
    except Exception as e:
        logger.error(f"Ошибка загрузки Excel: {e}")
        return []
