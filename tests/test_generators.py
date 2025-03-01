import pytest
from src.generators import filter_by_currency, transaction_descriptions, card_number_generator

def test_filter_by_currency_with_matches(sample_transactions):
    result = list(filter_by_currency(sample_transactions, "USD"))
    assert len(result) == 2
    assert [tx["id"] for tx in result] == [1, 3]

def test_filter_by_currency_no_matches(sample_transactions):
    result = list(filter_by_currency(sample_transactions, "GBR"))
    assert len(result) == 0

def test_filter_by_currency_empty_list(empty_transactions):
    result = list(filter_by_currency(empty_transactions, "USD"))
    assert len(result) == 0

def test_transaction_descriptions(sample_transactions):
    result = list(transaction_descriptions(sample_transactions))
    assert result == ["Payment 1", "Payment 2", "Payment 3"]

def test_transaction_descriptions_empty(empty_transactions):
    result = list(transaction_descriptions(empty_transactions))
    assert len(result) == 0

@pytest.mark.parametrize(
    "start, end, expected",
    [
        (1, 1, ["0000 0000 0000 0001"]),
        (1, 3, [
            "0000 0000 0000 0001",
            "0000 0000 0000 0002",
            "0000 0000 0000 0003"
        ]),
        (9999999999999999, 9999999999999999, ["9999 9999 9999 9999"]),
        (3, 1, []),
    ]
)
def test_card_number_generator(start, end, expected):
    result = list(card_number_generator(start, end))
    assert result == expected

def test_card_number_formatting():
    gen = card_number_generator(1234567812345678, 1234567812345678)
    assert next(gen) == "1234 5678 1234 5678"
