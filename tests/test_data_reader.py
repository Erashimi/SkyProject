from unittest.mock import Mock, patch

from src.data_reader import load_csv_transactions, load_excel_transactions


@patch("src.data_reader.pd.read_csv")
def test_load_csv_transactions_success(mock_read_csv):
    mock_df = Mock()
    mock_df.to_dict.return_value = [{"id": 1}]
    mock_read_csv.return_value = mock_df

    result = load_csv_transactions()
    assert result == [{"id": 1}]


@patch("src.data_reader.pd.read_csv")
def test_load_csv_transactions_error(mock_read_csv):
    mock_read_csv.side_effect = Exception("CSV error")
    result = load_csv_transactions()
    assert result == []


@patch("src.data_reader.pd.read_excel")
def test_load_excel_transactions_success(mock_read_excel):
    mock_df = Mock()
    mock_df.to_dict.return_value = [{"amount": 100}]
    mock_read_excel.return_value = mock_df

    result = load_excel_transactions()
    assert result == [{"amount": 100}]


@patch("src.data_reader.pd.read_excel")
def test_load_excel_transactions_error(mock_read_excel):
    mock_read_excel.side_effect = Exception("Excel error")
    result = load_excel_transactions()
    assert result == []
