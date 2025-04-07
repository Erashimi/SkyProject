import logging
import os
from typing import Dict, List

import requests
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
load_dotenv()

EXCHANGE_RATES_API_KEY = os.getenv("EXCHANGE_RATES_API_KEY")
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")


# def convert_to_rub(transaction: dict) -> float:
#     """Конвертирует сумму транзакции в рубли"""
#     amount = float(transaction["operationAmount"]["amount"])
#     currency = transaction["operationAmount"]["currency"]["code"]
#
#     if currency == "RUB":
#         return amount
#
#     response = requests.get(BASE_URL, params={"base": currency, "symbols": "RUB"}, headers={"apikey": API_KEY})
#     response.raise_for_status()
#     rate = response.json()["rates"]["RUB"]
#
#     return round(amount * rate, 2)


def convert_to_rub(transaction: dict) -> float:
    """Конвертирует сумму транзакции в рубли"""
    try:
        amount = float(transaction["operationAmount"]["amount"])
        currency = transaction["operationAmount"]["currency"]["code"]

        if currency == "RUB":
            return amount

        response = requests.get(
            "https://api.apilayer.com/exchangerates_data/latest",
            params={"base": currency, "symbols": "RUB"},
            headers={"apikey": EXCHANGE_RATES_API_KEY},
        )
        response.raise_for_status()
        rate = response.json()["rates"]["RUB"]
        return round(amount * rate, 2)

    except Exception as e:
        logger.error(f"Ошибка конвертации: {str(e)}")
        return 0.0


def get_stock_prices(stocks: List[str]) -> List[Dict]:
    """Получает цены акций с Alpha Vantage."""
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
    if not api_key:
        logger.error("Ключ Alpha Vantage не найден!")
        return []

    prices = []
    for idx, stock in enumerate(stocks):
        try:
            # Ограничение: 5 запросов/минута для бесплатного API
            if idx > 0 and idx % 5 == 0:
                time.sleep(60)

            url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock}&apikey={api_key}"
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            data = response.json()

            # Обработка ответа
            quote = data.get("Global Quote", {}) or data.get("global_quote", {})
            price_str = quote.get("05. price", "0") or quote.get("05_price", "0")
            price = float(price_str) if price_str.replace(".", "", 1).isdigit() else 0.0

            prices.append({"stock": stock, "price": round(price, 2)})

        except Exception as e:
            logger.error(f"Ошибка для {stock}: {str(e)}")
            prices.append({"stock": stock, "price": 0.0})

    return prices


def get_exchange_rates(currencies: List[str]) -> List[Dict]:
    try:
        response = requests.get(
            "https://api.apilayer.com/exchangerates_data/latest",
            params={"base": "RUB", "symbols": ",".join(currencies)},
            headers={"apikey": EXCHANGE_RATES_API_KEY},
        )
        response.raise_for_status()
        rates = response.json()["rates"]

        return [{"currency": c, "rate": round(1 / rate, 2)} for c, rate in rates.items()]  # RUB за 1 валюту
    except Exception as e:
        logger.error(f"Ошибка: {str(e)}")
        return []
