import re
from collections import Counter
from typing import Dict, List


def filter_transactions_by_description(transactions: List[Dict], search_str: str) -> List[Dict]:
    """Фильтрует транзакции по наличию строки в описании (с использованием re)"""
    pattern = re.compile(re.escape(search_str))
    return [tx for tx in transactions if pattern.search(tx.get("description", ""))]


def count_transactions_by_categories(transactions: List[Dict], categories: List[str]) -> Dict[str, int]:
    """Считает количество операций по категориям с использованием Counter"""
    descriptions = [tx.get("description", "") for tx in transactions]
    description_counter = Counter(descriptions)
    return {category: description_counter.get(category, 0) for category in categories}


def filter_transactions_by_status(transactions: List[Dict], status: str) -> List[Dict]:
    """Фильтрует транзакции по статусу (без учёта регистра)"""
    status_upper = status.upper()
    return [tx for tx in transactions if tx.get("status", "").upper() == status_upper]
