import logging
from datetime import datetime
from typing import Dict

from src.data_reader import load_excel_transactions
from src.external_api import get_exchange_rates, get_stock_prices
from src.masks import get_mask_account, get_mask_card_number
from src.utils import get_greeting, load_user_settings

logger = logging.getLogger(__name__)


def home_page(datetime_str: str) -> Dict:
    """Генерирует JSON-ответ для главной страницы с фильтрацией по текущему месяцу."""
    try:
        dt = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
    except ValueError as e:
        logger.error(f"Ошибка формата даты: {datetime_str} - {e}")
        return {"error": "Неверный формат даты. Используйте YYYY-MM-DD HH:MM:SS"}

    # Фильтрация: с 1 числа месяца до указанной даты
    start_of_month = dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    transactions = load_excel_transactions()

    filtered = [
        tx
        for tx in transactions
        if (start_of_month <= tx["date"] <= dt) and (tx["status"] == "OK") and (tx["amount"] < 0)
    ]

    # Обработка карт
    cards = {}
    for tx in filtered:
        try:
            from_value = str(tx.get("from", "")).strip()
            if not from_value:
                continue

            if "счет" in from_value.lower():
                masked = get_mask_account(from_value)
                last_digits = from_value[-4:] if len(from_value) >= 4 else ""
            else:
                masked = get_mask_card_number(from_value)
                last_digits = "".join([c for c in from_value if c.isdigit()])[-4:]

            amount = abs(tx["amount"])
            cards.setdefault(last_digits, {"total_spent": 0.0, "cashback": 0.0, "masked_number": masked})
            cards[last_digits]["total_spent"] += amount
            cards[last_digits]["cashback"] += amount * 0.01

        except Exception as e:
            logger.error(f"Ошибка обработки транзакции: {tx} - {e}")

    # Топ-5 транзакций
    top_transactions = sorted(filtered, key=lambda x: abs(x["amount"]), reverse=True)[:5]

    # Загрузка настроек и данных
    settings = load_user_settings()

    return {
        "greeting": get_greeting(dt),
        "cards": [
            {
                "last_digits": k,
                "total_spent": round(v["total_spent"], 2),
                "cashback": round(v["cashback"], 2),
                "masked_number": v["masked_number"],
            }
            for k, v in cards.items()
        ],
        "top_transactions": [
            {
                "date": tx["date"].strftime("%d.%m.%Y"),
                "amount": abs(tx["amount"]),
                "category": tx.get("category", "Другое"),
                "description": tx.get("description", "Без описания"),
            }
            for tx in top_transactions
        ],
        "currency_rates": get_exchange_rates(settings.get("user_currencies", [])),
        "stock_prices": get_stock_prices(settings.get("user_stocks", [])),
    }
