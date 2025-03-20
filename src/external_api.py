import os

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("EXCHANGE_RATES_API_KEY")
BASE_URL = "https://api.apilayer.com/exchangerates_data/latest"


def convert_to_rub(transaction: dict) -> float:
    """Конвертирует сумму транзакции в рубли"""
    amount = float(transaction["operationAmount"]["amount"])
    currency = transaction["operationAmount"]["currency"]["code"]

    if currency == "RUB":
        return amount

    response = requests.get(BASE_URL, params={"base": currency, "symbols": "RUB"}, headers={"apikey": API_KEY})
    response.raise_for_status()
    rate = response.json()["rates"]["RUB"]

    return round(amount * rate, 2)
