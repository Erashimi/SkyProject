# Учебный проект по обработке финансовых операций

Проект предоставляет инструменты для работы с банковскими операциями:
- Маскирование номеров карт и счетов
- Фильтрация и сортировка операций
- Преобразование форматов дат

## Модули

### 1. masks.py

**Функции маскирования**

- `get_mask_card_number(card_number: str) -> str`
-Преобразует номер карты формата `XXXX XXXX XXXX XXXX` в `XXXX XX** **** XXXX`
  - Пример:
  `get_mask_card_number("7000792289606361")  # "7000 79** **** 6361"`
- `get_mask_account(account_number: str) -> str`
-Возвращает номер счета в формате `**XXXX` (последние 4 цифры)
  - Пример:
  `get_mask_account("73654108430135874305")  # "**4305"`

### 2. processing.py

**Обработка данных**

- `filter_by_state(data: list[dict], state: str = "EXECUTED") -> list[dict]`
-Фильтрует операции по статусу (EXECUTED/CANCELED)
  - Пример:
```
transactions = [
    {"state": "EXECUTED", "date": "2023-01-01"},
    {"state": "CANCELED", "date": "2023-02-01"}
]
filter_by_state(transactions)  # Возвращает только выполненную операцию
```

`sort_by_date(data: list[dict], reverse: bool = True) -> list[dict]`
-Сортирует операции по дате (по убыванию по умолчанию)

### 3. widget.py

**Вспомогательные функции**

- `mask_account_card(data: str) -> str`
-Маскирует номер карты/счета в строке. Автоматически определяет тип данных.
    - Пример:
```
mask_account_card("Visa Platinum 7000792289606361")  # "Visa Platinum 7000 79** **** 6361"
mask_account_card("Счет 73654108430135874305")       # "Счет **4305"
```

`get_date(date_str: str) -> str`
-Конвертирует дату из YYYY-MM-DDTHH:MM:SS в DD.MM.YYYY
    - Пример:
`get_date("2018-07-11T02:26:18.671407")  # "11.07.2018"`

### 4. generators.py

**Содержит генераторы для обработки данных**

1. Фильтрация транзакций по валюте:
```
from generators import filter_by_currency

transactions = [...]
for tx in filter_by_currency(transactions, "USD"):
    print(tx)
```
2. Получение описаний транзакций:
```
from generators import transaction_descriptions

for desc in transaction_descriptions(transactions):
    print(desc)
```
3. Генерация номеров карт:
```
from generators import card_number_generator

for card_number in card_number_generator(1, 5):
    print(card_number)
# 0000 0000 0000 0001
# 0000 0000 0000 0002
# ...
# 0000 0000 0000 0005
```

### Тестирование

Проект включает 4 тестовых модуля с использованием pytest:

Структура тестов
```
tests/
├── conftest.py    # Фикстуры с параметризованными данными
├── test_generators.py      # Тесты генераторов
├── test_masks.py      # Тесты масок карт и счетов
├── test_processing.py # Тесты фильтрации и сортировки
└── test_widget.py     # Тесты виджетов
```

Пример запуска тестов:

`pytest tests/ -v`
