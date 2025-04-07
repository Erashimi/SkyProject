## Описание проекта

Данный проект представляет собой систему для работы с банковскими транзакциями. Он позволяет загружать данные о транзакциях из различных форматов (CSV, Excel), обрабатывать их, фильтровать по различным критериям и генерировать отчеты.

## Структура проекта

Проект состоит из нескольких модулей, каждый из которых выполняет свою функцию:

### 1. `data_reader.py`
Модуль для загрузки транзакций из файлов (CSV и Excel).
- `load_csv_transactions()`: Загружает транзакции из CSV-файла.
- `load_excel_transactions()`: Загружает транзакции из Excel-файла и преобразует их в нужный формат.

### 2. `decorators.py`
Модуль с декоратором для логирования выполнения функций.
- `log(filename=None)`: Декоратор для логирования результатов выполнения функций.

### 3. `external_api.py`
Модуль для работы с внешними API для конвертации валют и получения цен акций.
- `convert_to_rub(transaction: dict)`: Конвертирует сумму транзакции в рубли.
- `get_stock_prices(stocks: List[str])`: Получает цены акций с Alpha Vantage.
- `get_exchange_rates(currencies: List[str])`: Получает курсы валют.

### 4. `generators.py`
Модуль с генераторами для фильтрации и обработки транзакций.
- `filter_by_currency(transactions, currency_code)`: Генератор, возвращающий транзакции с заданной валютой.
- `transaction_descriptions(transactions)`: Генератор, возвращающий описание каждой транзакции.
- `card_number_generator(start, end)`: Генератор номеров карт в заданном диапазоне.

### 5. `main.py`
Основной модуль для запуска приложения и взаимодействия с пользователем.
- `main()`: Запускает приложение и обрабатывает ввод пользователя.

### 6. `masks.py`
Модуль для маскировки номеров карт и счетов.
- `get_mask_card_number(card_number: str)`: Маскирует номер карты.
- `get_mask_account(account_number: str)`: Маскирует номер счета.

### 7. `processing.py`
Модуль для обработки данных.
- `filter_by_state(data: list[dict], state: str)`: Фильтрует список словарей по значению ключа 'state'.
- `sort_by_date(data: list[dict], reverse: bool)`: Сортирует список операций по дате.

### 8. `reports.py`
Модуль для генерации отчетов.
- `report_to_file(filename: Optional[str])`: Декоратор для сохранения результатов отчета в JSON-файл.
- `spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str])`: Возвращает траты по категории за последние 3 месяца.

### 9. `run.py`
Модуль для запуска анализа транзакций через командную строку.
- `main()`: Обрабатывает команды для анализа данных о транзакциях, включая главную страницу, кешбек и расходы.

### 10. `services.py`
Модуль для анализа кешбэка по категориям.
- `calculate_cashback_by_category(data: List[Dict], year: int, month: int)`: Анализирует выгодность категорий для повышенного кешбэка.

### 11. `transaction_utils.py`
Утилиты для работы с транзакциями.
- `filter_transactions_by_description(transactions: List[Dict], search_str: str)`: Фильтрует транзакции по описанию.
- `count_transactions_by_categories(transactions: List[Dict], categories: List[str])`: Считает количество операций по категориям.
- `filter_transactions_by_status(transactions: List[Dict], status: str)`: Фильтрует транзакции по статусу.

### 12. `utils.py`
Утилиты для работы с данными и логированием.
- `load_transactions(file_path: str)`: Загружает транзакции из JSON-файла.
- `get_greeting(time: datetime)`: Возвращает приветствие в зависимости от времени.
- `load_user_settings()`: Загружает пользовательские настройки.

### 13. `views.py`
Модуль для генерации представлений и обработки данных.
- `home_page(datetime_str: str)`: Генерирует JSON-ответ для главной страницы с фильтрацией по текущему месяцу.

### 14. `widget.py`
Модуль для работы с виджетами.
- `mask_account_card(data: str)`: Маскирует номер карты или счета.
- `get_date(date_str: str)`: Преобразует строку даты в формат "ДД.ММ.ГГГГ".

### Запуск программы (реализован через консоль)

####
```
python src/main.py
```
#### Запуск анализа выгодных категорий повышенного кешбэка
```
python run.py cashback
```
#### Вывод списка трат за выбранный период
```
python run.py home
```
#### Вывод списка трат по выбранной категории
```
python run.py spending
```

