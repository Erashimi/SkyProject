import json
import logging
import os

os.makedirs("logs", exist_ok=True)

logger = logging.getLogger("utils")
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
