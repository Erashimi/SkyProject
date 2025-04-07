import unittest

from src.masks import get_mask_account, get_mask_card_number


class TestMaskingFunctions(unittest.TestCase):

    def test_get_mask_card_number_valid(self):
        self.assertEqual(get_mask_card_number("1234567812347197"), "**** **** **** 7197")
        self.assertEqual(get_mask_card_number("9876543212345678"), "**** **** **** 5678")

    def test_get_mask_account_valid(self):
        self.assertEqual(get_mask_account("1234567890123456"), "**3456")
        self.assertEqual(get_mask_account("987654321"), "**4321")

    def test_get_mask_account_empty(self):
        result = get_mask_account("")
        self.assertEqual(result, "**")

    def test_get_mask_account_invalid(self):
        self.assertEqual(get_mask_account("abcd"), "**abcd")


if __name__ == "__main__":
    unittest.main()
