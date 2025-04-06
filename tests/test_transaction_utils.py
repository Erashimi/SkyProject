from src.transaction_utils import (
    count_transactions_by_categories,
    filter_transactions_by_description,
    filter_transactions_by_status,
)


def test_filter_by_description(status_transactions):
    result = filter_transactions_by_description(status_transactions, "Pay")
    assert len(result) == 2


def test_count_categories(status_transactions):
    categories = ["Payment", "Transfer"]
    result = count_transactions_by_categories(status_transactions, categories)
    assert result == {"Payment": 2, "Transfer": 1}


def test_filter_by_status(status_transactions):
    result = filter_transactions_by_status(status_transactions, "executed")
    assert len(result) == 1
