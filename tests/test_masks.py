from src.masks import get_mask_account, get_mask_card_number


def test_get_mask_card_number(card_numbers):
    input_number, expected = card_numbers
    assert get_mask_card_number(input_number) == expected


def test_get_mask_account(account_numbers):
    input_number, expected = account_numbers
    assert get_mask_account(input_number) == expected
