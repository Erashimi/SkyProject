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
    """Загружает транзакции из Excel-файла в папке data"""
    file_path = os.path.join(DATA_DIR, "transactions_excel.xlsx")
    try:
        df = pd.read_excel(file_path, engine="openpyxl")
        logger.info(f"Успешно загружен Excel: {file_path}")
        return df.to_dict("records")
    except Exception as e:
        logger.error(f"Ошибка загрузки Excel: {e}")
        return []
