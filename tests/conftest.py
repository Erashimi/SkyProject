import pytest


@pytest.fixture(
    params=[
        ("7000792289606361", "7000 79** **** 6361"),
        ("1234567812345678", "1234 56** **** 5678"),
        ("1111222233334444", "1111 22** **** 4444"),
    ]
)
def card_numbers(request):
    return request.param


@pytest.fixture(
    params=[("73654108430135874305", "**4305"), ("12345678901234567890", "**7890"), ("09876543210987654321", "**4321")]
)
def account_numbers(request):
    return request.param


@pytest.fixture
def sample_data():
    return [
        {"state": "EXECUTED", "date": "2023-01-01"},
        {"state": "CANCELED", "date": "2023-02-01"},
        {"state": "EXECUTED", "date": "2023-03-01"},
    ]


@pytest.fixture(
    params=[
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        ("Счет 73654108430135874305", "Счет **4305"),
        ("MasterCard 1234567812345678", "MasterCard 1234 56** **** 5678"),
    ]
)
def account_card_data(request):
    return request.param


@pytest.fixture(
    params=[
        ("2018-07-11T02:26:18.671407", "11.07.2018"),
        ("2023-12-31T23:59:59.999999", "31.12.2023"),
        ("2020-01-01T00:00:00.000000", "01.01.2020"),
    ]
)
def date_data(request):
    return request.param


@pytest.fixture
def sample_transactions():
    return [
        {
            "id": 1,
            "operationAmount": {"amount": "100", "currency": {"code": "USD"}},
            "description": "Payment 1",
        },
        {
            "id": 2,
            "operationAmount": {"amount": "200", "currency": {"code": "EUR"}},
            "description": "Payment 2",
        },
        {
            "id": 3,
            "operationAmount": {"amount": "300", "currency": {"code": "USD"}},
            "description": "Payment 3",
        },
    ]


@pytest.fixture
def empty_transactions():
    return []


@pytest.fixture
def status_transactions():
    return [
        {"description": "Payment", "status": "EXECUTED"},
        {"description": "Transfer", "status": "CANCELED"},
        {"description": "Payment", "status": "PENDING"},
    ]
