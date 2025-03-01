import pytest

from src.widget import get_date, mask_account_card


def test_mask_account_card(account_card_data):
    input_str, expected = account_card_data
    assert mask_account_card(input_str) == expected


def test_mask_invalid_input():
    with pytest.raises(ValueError):
        mask_account_card("InvalidStringWithoutSpace")


def test_get_date(date_data):
    input_date, expected = date_data
    assert get_date(input_date) == expected


def test_get_date_invalid():
    with pytest.raises(ValueError):
        get_date("2023")
