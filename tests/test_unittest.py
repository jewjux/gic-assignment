import pytest
from decimal import Decimal
from datetime import datetime

from src.models.transaction_type import TransactionType
from src.models.bank_account import BankAccount
from src.models.transaction import Transaction
from src.service.view import BankView
from src.service.controller import BankApp


@pytest.fixture
def account() -> BankAccount:
    """
    Fixture to create new BankAccount instance for each test.

    :return: A BankAccount instance.
    """
    return BankAccount()


def test_bank_account_init(account: BankAccount):
    """
    Test that initial balance of account is 0.0 and no transactions.

    :param account: The BankAccount instance to test.
    """
    assert account.balance == Decimal("0.0")
    assert len(account.transactions) == 0


def test_deposit(account: BankAccount):
    """
    Test depositing money into the account.

    :param account: The BankAccount instance to the test.
    """
    account.create_transaction(Decimal("500.0"), TransactionType.CREDIT)
    assert account.balance == Decimal("500.0")
    assert len(account.transactions) == 1


def test_withdraw(account: BankAccount):
    """
    Test withdrawing money from the account.

    :param account: The BankAccount instance to test.
    """
    account.create_transaction(Decimal("500.0"), TransactionType.CREDIT)
    account.create_transaction(Decimal("100.0"), TransactionType.DEBIT)
    assert account.balance == Decimal("400.0")
    assert len(account.transactions) == 2


def test_print_statement(account: BankAccount, capsys: pytest.CaptureFixture):
    """
    Test printing the account statement.

    :param account: The BankAccount instance to test.
    :param capsys: The pytest fixture to capture stdout and stderr.
    """
    account.create_transaction(Decimal("500.0"), TransactionType.CREDIT)
    account.create_transaction(Decimal("100.0"), TransactionType.DEBIT)
    account.print_statement()
    captured = capsys.readouterr()
    assert "500.00" in captured.out
    assert "-100.00" in captured.out
    assert "400.00" in captured.out


def test_transaction_init():
    """
    Test intialising a transaction.
    """
    transaction = Transaction(datetime.now(), Decimal("500.0"), Decimal("500.0"))
    assert transaction.amount == Decimal("500.0")


def test_check_input_valid():
    """
    Test valid inputs for amount.
    """
    view = BankView()
    app = BankApp(account, view)
    assert app.validate_input("500") == Decimal("500.0")
    assert app.validate_input("500.50") == Decimal("500.50")


def test_validate_input_invalid():
    """
    Test invalid inputs for amount.
    """
    view = BankView()
    app = BankApp(account, view)
    assert app.validate_input("abc") is None
    assert app.validate_input("%$!") is None
    assert app.validate_input("500,50") is None
    assert app.validate_input("-500") is None


def test_private_balance_encapsulation(account):
    with pytest.raises(AttributeError):
        account.__balance


def test_private_transactions_encapsulation(account):
    with pytest.raises(AttributeError):
        account.__transactions


def test_multiple_transactions(account):
    """
    Test multiple deposit and withdrawal.

    :param account: The BankAccount instance to the test.
    """
    account.create_transaction(Decimal("500.0"), TransactionType.CREDIT)
    account.create_transaction(Decimal("200.0"), TransactionType.DEBIT)
    account.create_transaction(Decimal("300.0"), TransactionType.CREDIT)
    assert account.balance == Decimal("600.0")
    assert len(account.transactions) == 3
