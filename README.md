# Учебный проект по Python

## Обработка финансовых операций

Модуль для фильтрации и сортировки банковских операций. Содержит две основные функции:
- `filter_by_state()` — фильтрация операций по статусу
- `sort_by_date()` — сортировка операций по дате

### Установка
1. Скопируйте файл модуля (например, `transaction_processing.py`) в свой проект
2. Для работы требуется Python 3.6 или новее
3. Дополнительные зависимости не требуются

### Использование
```python
from transaction_processing import filter_by_state, sort_by_date
Фильтрация операций
Функция filter_by_state(data: list[dict], state: str = 'EXECUTED') -> list[dict]

data — список словарей с операциями
state — опциональный фильтр статуса (по умолчанию 'EXECUTED')
Пример:

Копировать
transactions = [
    {'id': 1, 'state': 'EXECUTED'},
    {'id': 2, 'state': 'CANCELED'},
    {'id': 3, 'state': 'EXECUTED'}
]