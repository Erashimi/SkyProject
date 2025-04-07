import json
import logging
import os
from datetime import datetime
from typing import Dict

os.makedirs("logs", exist_ok=True)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler("logs/utils.log", mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def load_transactions(file_path: str) -> list:
    """Загружает транзакции из JSON-файла"""
    logger.debug(f"Загрузка файла: {file_path}")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            result = data if isinstance(data, list) else []
            logger.info(f"Успешно загружено {len(result)} транзакций")
            return result
    except FileNotFoundError as e:
        logger.error(f"Файл не найден: {file_path}", exc_info=True)
        return []
    except json.JSONDecodeError as e:
        logger.error(f"Ошибка декодирования JSON: {file_path}", exc_info=True)
        return []


def get_greeting(time: datetime) -> str:
    """Возвращает приветствие в зависимости от времени."""
    hour = time.hour
    if 5 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 17:
        return "Добрый день"
    elif 17 <= hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def load_user_settings() -> Dict:
    """Загружает пользовательские настройки."""
    try:
        with open("user_settings.json", "r") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Ошибка загрузки настроек: {e}")
        return {"user_currencies": [], "user_stocks": []}
