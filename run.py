import argparse
import json
from datetime import datetime

import pandas as pd

from src.data_reader import load_excel_transactions
from src.reports import spending_by_category
from src.services import calculate_cashback_by_category
from src.views import home_page


def input_date(prompt: str, fmt: str = "%Y-%m-%d") -> datetime:
    """Запрашивает дату у пользователя с валидацией формата."""
    while True:
        try:
            date_str = input(prompt)
            return datetime.strptime(date_str, fmt)
        except ValueError:
            print(f"Неверный формат. Используйте {fmt}")


def main():
    # Парсинг аргументов командной строки
    parser = argparse.ArgumentParser(description="Банковские транзакции: анализ данных")
    parser.add_argument(
        "command",
        choices=["home", "cashback", "spending"],
        help="Выберите задачу: home - главная, cashback - кешбек, spending - траты",
    )
    args = parser.parse_args()

    # Загрузка данных
    transactions = load_excel_transactions()
    df_transactions = pd.DataFrame(transactions)

    if args.command == "home":
        # Задача 1: Главная страница
        date_str = input("Введите дату и время (формат: ГГГГ-ММ-ДД ЧЧ:ММ:СС): ")
        result = home_page(date_str)
        print("\nРезультат:")
        print(json.dumps(result, indent=2, ensure_ascii=False))

    elif args.command == "cashback":
        # Задача 2: Анализ кешбэка
        year = int(input("Введите год для анализа (например 2020): "))
        month = int(input("Введите месяц для анализа (1-12): "))
        result = calculate_cashback_by_category(transactions, year, month)
        print("\nСуммы кешбэка по категориям:")
        for category, amount in result.items():
            print(f"- {category}: {amount:.2f} руб.")

    elif args.command == "spending":
        category = input("Введите категорию для анализа: ")
        date = input_date("Введите дату отсчета (формат ГГГГ-ММ-ДД): ")
        try:
            result = spending_by_category(df_transactions, category, date.strftime("%Y-%m-%d"))
            print("\nТраты за последние 3 месяца:")
            if not result.empty:
                # Подготовка данных для вывода
                output_cols = ["date", "amount"]
                if "description" in result.columns:
                    output_cols.append("description")
                formatted = result[output_cols].copy()
                formatted["date"] = formatted["date"].dt.strftime("%d.%m.%Y")
                formatted["amount"] = formatted["amount"].abs().apply(lambda x: f"{x:.2f} RUB")
                print(formatted.to_string(index=False))
            else:
                print("Нет транзакций по указанной категории")
        except Exception as e:
            print(f"Ошибка: {str(e)}")


if __name__ == "__main__":
    main()
