from unittest.mock import patch

from src.external_api import convert_to_rub


def test_convert_rub():
    transaction = {"operationAmount": {"amount": "100", "currency": {"code": "RUB"}}}
    assert convert_to_rub(transaction) == 100.0


@patch("src.external_api.requests.get")
def test_convert_usd(mock_get):
    mock_response = {"rates": {"RUB": 90.5}, "success": True}
    mock_get.return_value.json.return_value = mock_response
    mock_get.return_value.raise_for_status.return_value = None

    transaction = {"operationAmount": {"amount": "10", "currency": {"code": "USD"}}}
    assert convert_to_rub(transaction) == 10 * 90.5
