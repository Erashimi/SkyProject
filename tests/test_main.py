from unittest.mock import patch

import pytest

from src.main import main


@pytest.fixture
def mock_transactions():
    return [
        {
            "date": "2023-10-01T12:00:00.000",
            "description": "Payment",
            "status": "EXECUTED",
            "from": "Счет 1234567890123456",
            "to": "Счет 6543210987654321",
            "amount": "1000",
            "currency": "RUB",
        },
        {
            "date": "2023-09-15T14:30:00.000",
            "description": "Transfer",
            "status": "CANCELED",
            "from": "Visa 1234567812345678",
            "to": "Счет 8765432109876543",
            "amount": "500",
            "currency": "USD",
        },
    ]


@patch("src.main.load_csv_transactions")
@patch("builtins.input")
def test_main_csv_success(mock_input, mock_load_csv, mock_transactions, capsys):
    mock_input.side_effect = ["2", "EXECUTED", "нет", "нет", "нет"]
    mock_load_csv.return_value = mock_transactions

    main()

    captured = capsys.readouterr()
    assert "01.10.2023 Payment" in captured.out
    assert "Сумма: 1000 RUB" in captured.out
    assert "Всего банковских операций в выборке: 1" in captured.out
    assert "Статистика по категориям" in captured.out


@patch("src.main.load_excel_transactions")
@patch("builtins.input")
def test_main_excel_invalid_status(mock_input, mock_load_excel, mock_transactions, capsys):
    mock_input.side_effect = ["3", "TEST", "CANCELED", "нет", "нет", "нет"]
    mock_load_excel.return_value = mock_transactions

    main()

    captured = capsys.readouterr()
    assert "Статус операции 'TEST' недоступен" in captured.out
    assert "15.09.2023 Transfer" in captured.out
    assert "Сумма: 500 USD" in captured.out


@patch("src.main.load_excel_transactions")
@patch("builtins.input")
def test_main_excel_sorting(mock_input, mock_load_excel, capsys):
    test_data = [
        {
            "date": "2023-01-01T00:00:00.000",
            "description": "A",
            "status": "EXECUTED",
            "from": "Visa 1234567812345678",
            "to": "Счет 8765432109876543",
            "amount": "1000",
            "currency": "RUB",
        },
        {
            "date": "2023-02-01T00:00:00.000",
            "description": "B",
            "status": "EXECUTED",
            "from": "Счет 1234567890123456",
            "to": "Visa 8765432187654321",
            "amount": "500",
            "currency": "USD",
        },
    ]
    mock_input.side_effect = ["3", "EXECUTED", "да", "по убыванию", "нет", "нет"]
    mock_load_excel.return_value = test_data

    main()

    captured = capsys.readouterr()
    assert captured.out.index("01.02.2023") < captured.out.index("01.01.2023")


@patch("src.main.load_csv_transactions")
@patch("builtins.input")
def test_main_empty_result(mock_input, mock_load_csv, capsys):
    mock_input.side_effect = ["2", "PENDING", "нет", "нет", "нет"]
    mock_load_csv.return_value = []

    main()

    captured = capsys.readouterr()
    assert "Не найдено ни одной транзакции" in captured.out


@patch("src.main.load_csv_transactions")
@patch("builtins.input")
def test_main_rub_filter(mock_input, mock_load_csv, mock_transactions, capsys):
    mock_input.side_effect = ["2", "EXECUTED", "нет", "да", "нет"]
    mock_load_csv.return_value = mock_transactions

    main()

    captured = capsys.readouterr()
    assert "1000 RUB" in captured.out
    assert "500 USD" not in captured.out
