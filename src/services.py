import logging
from collections import defaultdict
from typing import Dict, List

logger = logging.getLogger(__name__)


def calculate_cashback_by_category(data: List[Dict], year: int, month: int) -> Dict[str, float]:
    """
    Анализирует выгодность категорий для повышенного кешбэка.
    Возвращает сумму кешбэка (1% от расходов) по категориям за указанный месяц.

    Args:
        data: Список транзакций
        year: Год анализа
        month: Месяц анализа (1-12)

    Returns:
        Словарь {категория: сумма_кешбэка}
    """
    try:
        # Фильтрация транзакций по дате
        filtered = filter(
            lambda tx: (tx["date"].year == year and tx["date"].month == month and tx["amount"] < 0), data
        )

        # Агрегация сумм по категориям
        cashback = defaultdict(float)
        for tx in filtered:
            category = tx.get("category", "Другое")
            cashback[category] += abs(tx["amount"]) * 0.01

        return dict(cashback)

    except Exception as e:
        logger.error(f"Ошибка анализа кешбэка: {str(e)}")
        return {}
