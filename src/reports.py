import json
import logging
from datetime import datetime
from functools import wraps
from typing import Callable, Optional

import pandas as pd

logger = logging.getLogger(__name__)


def report_to_file(filename: Optional[str] = None) -> Callable:
    """
    Декоратор для сохранения результатов отчета в JSON-файл.

    Args:
        filename: Имя файла (если None, генерируется автоматически)
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            output_file = filename or f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

            try:
                with open(output_file, "w", encoding="utf-8") as f:
                    json.dump(result, f, indent=2, ensure_ascii=False, default=str)
                logger.info(f"Отчет сохранен в {output_file}")
            except Exception as e:
                logger.error(f"Ошибка сохранения отчета: {str(e)}")

            return result

        return wrapper

    return decorator


@report_to_file()
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """
    Возвращает траты по категории за последние 3 месяца от указанной даты.

    Args:
        transactions: Датафрейм с транзакциями
        category: Категория для анализа
        date: Дата отсчета (формат: YYYY-MM-DD)

    Returns:
        Отфильтрованный датафрейм
    """
    try:
        # Парсинг даты
        target_date = pd.to_datetime(date) if date else datetime.now()
        start_date = target_date - pd.DateOffset(months=3)

        # Фильтрация
        mask = (
            (transactions["date"] >= start_date)
            & (transactions["date"] <= target_date)
            & (transactions["category"] == category)
            & (transactions["amount"] < 0)
        )

        return transactions.loc[mask].reset_index(drop=True)

    except Exception as e:
        logger.error(f"Ошибка формирования отчета: {str(e)}")
        return pd.DataFrame()
