import pytest
from decimal import Decimal

from src.models.transaction_type import TransactionType
from src.models.bank_account import BankAccount

@pytest.fixture
def account() -> BankAccount:
    """
    Fixture to create new BankAccount instance for each test.

    :return: A BankAccount instance.
    """
    return BankAccount()