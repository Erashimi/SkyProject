from unittest.mock import mock_open, patch

from src.utils import load_transactions


def test_load_transactions_valid_file():
    data = '[{"id": 1}, {"id": 2}]'
    with patch("builtins.open", mock_open(read_data=data)):
        result = load_transactions("dummy.json")
        assert result == [{"id": 1}, {"id": 2}]


def test_load_transactions_invalid_data():
    with patch("builtins.open", mock_open(read_data="{}")):
        result = load_transactions("invalid.json")
        assert result == []


def test_load_transactions_file_not_found():
    result = load_transactions("nonexistent.json")
    assert result == []
