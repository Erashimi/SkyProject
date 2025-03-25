from datetime import datetime

from src.data_reader import load_csv_transactions, load_excel_transactions  # load_json_transactions
from src.masks import get_mask_account, get_mask_card_number
from src.transaction_utils import (
    count_transactions_by_categories,
    filter_transactions_by_description,
    filter_transactions_by_status,
)


def print_transaction(tx: dict) -> None:
    """ Выводит транзакцию в заданном формате """
    date = datetime.strptime(tx["date"], "%Y-%m-%dT%H:%M:%S.%f").strftime("%d.%m.%Y")
    description = tx["description"]

    from_to = tx.get("from", "")
    if "счет" in from_to.lower():
        from_str = get_mask_account(from_to)
    else:
        from_str = get_mask_card_number(from_to)

    to = get_mask_account(tx["to"]) if "счет" in tx["to"].lower() else get_mask_card_number(tx["to"])

    print(f"{date} {description}")
    if from_str:
        print(f"{from_str} -> {to}")
    else:
        print(f"Счет {to}")
    print(f"Сумма: {tx['amount']} {tx['currency']}\n")


def main():
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")

    while True:
        choice = input("Выберите необходимый пункт меню:\n1. JSON\n2. CSV\n3. XLSX\n> ")
        if choice in {"1", "2", "3"}:
            break
        print("Некорректный ввод. Попробуйте снова.")

    if choice == "1":
        pass
    #        transactions = load_json_transactions('data/transactions.json')
    elif choice == "2":
        transactions = load_csv_transactions("data/transactions.csv")
    else:
        transactions = load_excel_transactions("data/transactions_excel.xlsx")

    while True:
        status = input("Введите статус (EXECUTED/CANCELED/PENDING): ").upper()
        if status in {"EXECUTED", "CANCELED", "PENDING"}:
            break
        print(f"Статус операции '{status}' недоступен.")

    filtered = filter_transactions_by_status(transactions, status)

    sort_date = input("Отсортировать операции по дате? (Да/Нет): ").lower() == "да"
    if sort_date:
        order = input("Отсортировать по возрастанию или по убыванию? ").lower()
        reverse = order == "по убыванию"
        filtered.sort(key=lambda x: x["date"], reverse=reverse)

    rub_only = input("Выводить только рублевые тразакции? (Да/Нет): ").lower() == "да"
    if rub_only:
        filtered = [tx for tx in filtered if tx["currency"] == "RUB"]

    search_word = (
        input("Отфильтровать список транзакций по определенному слову в описании? (Да/Нет): ").lower() == "да"
    )
    if search_word:
        word = input("Введите слово для поиска: ")
        filtered = filter_transactions_by_description(filtered, word)

    if not filtered:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации.")
        return

    print(f"\nВсего банковских операций в выборке: {len(filtered)}\n")
    for tx in filtered:
        print_transaction(tx)

    categories = list(set(tx.get("description", "") for tx in filtered))
    category_stats = count_transactions_by_categories(filtered, categories)
    print("\nСтатистика по категориям:")
    for category, count in category_stats.items():
        print(f"- {category}: {count} операций")


if __name__ == "__main__":
    main()
