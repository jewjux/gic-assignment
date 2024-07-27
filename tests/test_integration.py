import pytest
from decimal import Decimal

from src.models.bank_account import BankAccount

@pytest.fixture
def account() -> BankAccount:
    """
    Fixture to create new BankAccount instance for each test.

    :return: A BankAccount instance.
    """
    return BankAccount()

def test_multiple_transactions(account):
    """
    Test multiple deposit and withdrawal.

    :param account: The BankAccount instance to the test.
    """
    account.log_transaction(Decimal('500.0'), 'credit')
    account.log_transaction(Decimal('200.0'), 'debit')
    account.log_transaction(Decimal('300.0'), 'credit')
    assert account.balance == Decimal('600.0')
    assert len(account.transactions) == 3