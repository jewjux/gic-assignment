import pytest
from decimal import Decimal
from main import bank_app
from bank_account import BankAccount

@pytest.fixture
def account() -> BankAccount:
    """
    Fixture to create new BankAccount instance for each test.

    :return: A BankAccount instance.
    """
    return BankAccount()

#################
## BASIC TESTS ##
#################

def test_initial_balance(account: BankAccount) -> None:
    """
    Test that initial balance of account is 0.0

    :param account: The BankAccount instance to test.
    """
    assert account.balance == 0.0

def test_deposit(account: BankAccount, capsys: pytest.CaptureFixture) -> None:
    """
    Test depositing money into the account.

    :param account: The BankAccount instance to the test.
    :param capsys: The pytest fixture to capture stdout and stderr
    """
    account.deposit(500)
    captured = capsys.readouterr()
    assert "Thank you. $500.00 has been deposited to your account." in captured.out
    assert account.balance == 500
    assert len(account.transactions) == 1

def test_withdraw(account: BankAccount, capsys: pytest.CaptureFixture) -> None:
    """
    Test withdrawing money from the account.

    :param account: The BankAccount instance to test.
    :param capsys: The pytest fixture to capture stdout and stderr.
    """
    account.deposit(500)
    account.withdraw(100)
    captured = capsys.readouterr()
    assert "Thank you. $100.00 has been withdrawn." in captured.out
    assert account.balance == 400
    assert len(account.transactions) == 2

def test_print_statement(account: BankAccount, capsys: pytest.CaptureFixture) -> None:
    """
    Test printing the account statement.

    :param account: The BankAccount instance to test.
    :param capsys: The pytest fixture to capture stdout and stderr.
    """
    account.deposit(500)
    account.withdraw(100)
    account.print_statement()
    captured = capsys.readouterr()
    assert "500.00" in captured.out
    assert "-100.00" in captured.out
    assert "400.00" in captured.out

################
## EDGE CASES ##
################
def test_deposit_negative_amount(account: BankAccount,monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture) -> None:
    """
    Test negative deposit amount.

    :param account: The BankAccount instance to test.
    :param monkeypatch: The pytest fixture to modify builtins.
    :param capsys: The pytest fixture to capture stdout and stderr.
    """
    inputs = iter(['d', '-100', 'b', 'q'])
    monkeypatch.setattr('builtins.input', lambda *args: next(inputs))

    bank_app(account)

    captured = capsys.readouterr()
    assert "Your deposit amount must be a positive number." in captured.out
    assert account.balance == 0.0
    assert len(account.transactions) == 0

def test_deposit_non_number(account: BankAccount,monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture) -> None:
    """
    Test non number deposit input.

    :param account: The BankAccount instance to test.
    :param monkeypatch: The pytest fixture to modify builtins.
    :param capsys: The pytest fixture to capture stdout and stderr.
    """
    inputs = iter(['d', 'abc%$!', 'b', 'q'])
    monkeypatch.setattr('builtins.input', lambda *args: next(inputs))

    bank_app(account)

    captured = capsys.readouterr()
    assert "Invalid deposit amount. Please try again." in captured.out
    assert account.balance == 0.0
    assert len(account.transactions) == 0

def test_deposit_empty(account: BankAccount,monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture) -> None:
    """
    Test empty deposit input.

    :param account: The BankAccount instance to test.
    :param monkeypatch: The pytest fixture to modify builtins.
    :param capsys: The pytest fixture to capture stdout and stderr.
    """
    inputs = iter(['d', '', 'b', 'q'])
    monkeypatch.setattr('builtins.input', lambda *args: next(inputs))

    bank_app(account)

    captured = capsys.readouterr()
    assert "Invalid deposit amount. Please try again." in captured.out
    assert account.balance == 0.0
    assert len(account.transactions) == 0

def test_deposit_multiple_negative_amount(account: BankAccount,monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture) -> None:
    """
    Test 2 negative deposit numbers followed by a positive deposit number.

    :param account: The BankAccount instance to test.
    :param monkeypatch: The pytest fixture to modify builtins.
    :param capsys: The pytest fixture to capture stdout and stderr.
    """
    inputs = iter(['d', '-100', '-500', '500', 'q'])
    monkeypatch.setattr('builtins.input', lambda *args: next(inputs))

    bank_app(account)

    captured = capsys.readouterr()
    assert "Your deposit amount must be a positive number." in captured.out
    assert "Your deposit amount must be a positive number." in captured.out
    assert account.balance == 500
    assert "Thank you for banking with AwesomeGIC Bank." in captured.out

def test_deposit_large_numbers(account: BankAccount, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture) -> None:
    """
    Test large deposit amount.

    :param account: The BankAccount instance to test.
    :param monkeypatch: The pytest fixture to modify builtins.
    :param capsys: The pytest fixture to capture stdout and stderr.
    """
    inputs = iter(['d', '9999999999999999.99', 'q'])
    monkeypatch.setattr('builtins.input', lambda *args: next(inputs))

    bank_app(account)

    captured = capsys.readouterr()
    assert "Thank you. $9999999999999999.99 has been deposited to your account." in captured.out
    assert account.balance == Decimal('9999999999999999.99')
    assert len(account.transactions) == 1

def test_deposit_large_numbers(account: BankAccount, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture) -> None:
    """
    Test large deposit amount.

    :param account: The BankAccount instance to test.
    :param monkeypatch: The pytest fixture to modify builtins.
    :param capsys: The pytest fixture to capture stdout and stderr.
    """
    inputs = iter(['d', '99.9999', 'b', 'q'])
    monkeypatch.setattr('builtins.input', lambda *args: next(inputs))

    bank_app(account)

    captured = capsys.readouterr()
    assert "We only accept values rounded to the cent." in captured.out
    assert account.balance == 0.0
    assert len(account.transactions) == 0

def test_deposit_minimum_number(account: BankAccount, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture) -> None:
    """
    Test minimum deposit amount.

    :param account: The BankAccount instance to test.
    :param monkeypatch: The pytest fixture to modify builtins.
    :param capsys: The pytest fixture to capture stdout and stderr.
    """
    inputs = iter(['d', '0.01', 'q'])
    monkeypatch.setattr('builtins.input', lambda *args: next(inputs))

    bank_app(account)

    captured = capsys.readouterr()
    assert "Thank you. $0.01 has been deposited to your account." in captured.out
    assert account.balance == Decimal('0.01')
    assert len(account.transactions) == 1

def test_deposit_small_number(account: BankAccount, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture) -> None:
    """
    Test too small deposit amount.

    :param account: The BankAccount instance to test.
    :param monkeypatch: The pytest fixture to modify builtins.
    :param capsys: The pytest fixture to capture stdout and stderr.
    """
    inputs = iter(['d', '0.0001', 'b', 'q'])
    monkeypatch.setattr('builtins.input', lambda *args: next(inputs))

    bank_app(account)

    captured = capsys.readouterr()
    assert "We only accept values rounded to the cent." in captured.out
    assert account.balance == 0.0
    assert len(account.transactions) == 0

def test_withdraw_negative_amount(account: BankAccount, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture) -> None:
    """
    Test negative withdrawal amount.

    :param account: The BankAccount instance to test.
    :param monkeypatch: The pytest fixture to modify builtins.
    :param capsys: The pytest fixture to capture stdout and stderr.
    """
    inputs = iter(['d', '500', 'w', '-100', 'b', 'q'])
    monkeypatch.setattr('builtins.input', lambda *args: next(inputs))

    bank_app(account)

    captured = capsys.readouterr()
    assert "Thank you. $500.00 has been deposited to your account." in captured.out
    assert account.balance == 500
    assert len(account.transactions) == 1
    assert "Your withdrawal amount must be a positive number." in captured.out
    assert account.balance == 500
    assert len(account.transactions) == 1

def test_withdraw_insufficient_funds(account: BankAccount, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture) -> None:
    """
    Test attempting to withdraw money from the account with insufficient funds.

    :param account: The BankAccount instance to test.
    :param monkeypatch: The pytest fixture to modify builtins.
    :param capsys: The pytest fixture to capture stdout and stderr.
    """
    inputs = iter(['w', '100', 'b', 'q'])
    monkeypatch.setattr('builtins.input', lambda *args: next(inputs))

    bank_app(account)

    captured = capsys.readouterr()
    assert "Your bank account has insufficient funds." in captured.out
    assert account.balance == 0.0
    assert len(account.transactions) == 0

def test_withdraw_slightly_insufficient_funds(account: BankAccount, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture) -> None:
    """
    Test attempting to withdraw $100.01 from the account with $100.

    :param account: The BankAccount instance to test.
    :param monkeypatch: The pytest fixture to modify builtins.
    :param capsys: The pytest fixture to capture stdout and stderr.
    """
    inputs = iter(['d', '100', 'w', '100.01', 'b', 'q'])
    monkeypatch.setattr('builtins.input', lambda *args: next(inputs))

    bank_app(account)

    captured = capsys.readouterr()
    assert "Your bank account has insufficient funds." in captured.out
    assert account.balance == 100
    assert len(account.transactions) == 1

def test_withdraw_multiple_insufficient_funds(account: BankAccount, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture) -> None:
    """
    Test attempting to withdraw multiple amounts from the account, only some are invalid.

    :param account: The BankAccount instance to test.
    :param monkeypatch: The pytest fixture to modify builtins.
    :param capsys: The pytest fixture to capture stdout and stderr.
    """
    inputs = iter(['d', '100', 'w', '90', 'w', '20', 'b', 'q'])
    monkeypatch.setattr('builtins.input', lambda *args: next(inputs))

    bank_app(account)

    captured = capsys.readouterr()
    assert "Your bank account has insufficient funds." in captured.out
    assert account.balance == 10
    assert len(account.transactions) == 2

def test_withdraw_non_number(account: BankAccount,monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture) -> None:
    """
    Test non number withdrawal input.

    :param account: The BankAccount instance to test.
    :param monkeypatch: The pytest fixture to modify builtins.
    :param capsys: The pytest fixture to capture stdout and stderr.
    """
    inputs = iter(['w', 'abc%$!', 'b', 'q'])
    monkeypatch.setattr('builtins.input', lambda *args: next(inputs))

    bank_app(account)

    captured = capsys.readouterr()
    assert "Invalid withdrawal amount. Please try again." in captured.out
    assert account.balance == 0.0
    assert len(account.transactions) == 0

def test_withdraw_empty(account: BankAccount,monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture) -> None:
    """
    Test empty withdrawal input.

    :param account: The BankAccount instance to test.
    :param monkeypatch: The pytest fixture to modify builtins.
    :param capsys: The pytest fixture to capture stdout and stderr.
    """
    inputs = iter(['d', '100', 'w', '', 'b', 'q'])
    monkeypatch.setattr('builtins.input', lambda *args: next(inputs))

    bank_app(account)

    captured = capsys.readouterr()
    assert "Invalid withdrawal amount. Please try again." in captured.out
    assert account.balance == 100
    assert len(account.transactions) == 1

def test_withdraw_minimum_number(account: BankAccount, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture) -> None:
    """
    Test minimum withdrawal amount.

    :param account: The BankAccount instance to test.
    :param monkeypatch: The pytest fixture to modify builtins.
    :param capsys: The pytest fixture to capture stdout and stderr.
    """
    inputs = iter(['d', '500', 'w', '0.01', 'q'])
    monkeypatch.setattr('builtins.input', lambda *args: next(inputs))

    bank_app(account)

    captured = capsys.readouterr()
    assert "Thank you. $0.01 has been withdrawn." in captured.out
    assert account.balance == Decimal('499.99')
    assert len(account.transactions) == 2

def test_withdraw_small_number(account: BankAccount, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture) -> None:
    """
    Test too small withdrawal amount.

    :param account: The BankAccount instance to test.
    :param monkeypatch: The pytest fixture to modify builtins.
    :param capsys: The pytest fixture to capture stdout and stderr.
    """
    inputs = iter(['w', '0.0001', 'b', 'q'])
    monkeypatch.setattr('builtins.input', lambda *args: next(inputs))

    bank_app(account)

    captured = capsys.readouterr()
    assert "We only accept values rounded to the cent." in captured.out
    assert account.balance == 0.0
    assert len(account.transactions) == 0

def test_withdraw_exact_balance(account: BankAccount, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture) -> None:
    """
    Test withdrawing all balance.

    :param account: The BankAccount instance to test.
    :param monkeypatch: The pytest fixture to modify builtins.
    :param capsys: The pytest fixture to capture stdout and stderr.
    """
    inputs = iter(['d', '100', 'w', '100', 'q'])
    account = BankAccount()

    monkeypatch.setattr('builtins.input', lambda *args: next(inputs))

    bank_app(account)

    captured = capsys.readouterr()
    assert "Thank you. $100.00 has been deposited to your account." in captured.out
    assert "Thank you. $100.00 has been withdrawn." in captured.out
    assert account.balance == Decimal('0.00')
    assert len(account.transactions) == 2

def test_print_empty(account: BankAccount, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture) -> None:
    """
    Test print empty bank statement.

    :param account: The BankAccount instance to test.
    :param monkeypatch: The pytest fixture to modify builtins.
    :param capsys: The pytest fixture to capture stdout and stderr.
    """
    inputs = iter(['p', 'q'])
    monkeypatch.setattr('builtins.input', lambda *args: next(inputs))

    bank_app(account)

    captured = capsys.readouterr()
    assert "Date" in captured.out
    assert "Amount" in captured.out
    assert "Balance" in captured.out
    assert "No transactions found." in captured.out

def test_print_large_balance(account: BankAccount, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture) -> None:
    """
    Test print large account balance.

    :param account: The BankAccount instance to test.
    :param monkeypatch: The pytest fixture to modify builtins.
    :param capsys: The pytest fixture to capture stdout and stderr.
    """
    inputs = iter(['d', '9999999999999999.99', 'p', 'q'])
    monkeypatch.setattr('builtins.input', lambda *args: next(inputs))

    bank_app(account)

    captured = capsys.readouterr()
    assert "Thank you. $9999999999999999.99 has been deposited to your account." in captured.out
    assert "9999999999999999.99" in captured.out

def test_print_large_withdrawal(account: BankAccount, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture) -> None:
    """
    Test print large account balance.

    :param account: The BankAccount instance to test.
    :param monkeypatch: The pytest fixture to modify builtins.
    :param capsys: The pytest fixture to capture stdout and stderr.
    """
    inputs = iter(['d', '9999999999999999.99', 'w', '1999999999999999.99', 'p', 'q'])
    monkeypatch.setattr('builtins.input', lambda *args: next(inputs))

    bank_app(account)

    captured = capsys.readouterr()
    assert "Thank you. $9999999999999999.99 has been deposited to your account." in captured.out
    assert "Thank you. $1999999999999999.99 has been withdrawn." in captured.out
    assert "9999999999999999.99" in captured.out
    assert "8000000000000000.00" in captured.out

def test_print_multiple_deposit(account: BankAccount, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture) -> None:
    """
    Test print multiple deposit amounts.

    :param account: The BankAccount instance to test.
    :param monkeypatch: The pytest fixture to modify builtins.
    :param capsys: The pytest fixture to capture stdout and stderr.
    """
    inputs = iter(['d', '500', 'd', '400', 'd', '300', 'p', 'q'])
    monkeypatch.setattr('builtins.input', lambda *args: next(inputs))

    bank_app(account)

    captured = capsys.readouterr()
    assert "Thank you. $500.00 has been deposited to your account." in captured.out
    assert "Thank you. $400.00 has been deposited to your account." in captured.out
    assert "Thank you. $300.00 has been deposited to your account." in captured.out
    assert "500.00" in captured.out
    assert "900.00" in captured.out
    assert "1200.00" in captured.out

def test_print_multiple_withdraw(account: BankAccount, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture) -> None:
    """
    Test print multiple withdrawal amounts.

    :param account: The BankAccount instance to test.
    :param monkeypatch: The pytest fixture to modify builtins.
    :param capsys: The pytest fixture to capture stdout and stderr.
    """
    inputs = iter(['d', '1000', 'w', '500', 'w', '400', 'p', 'q'])
    monkeypatch.setattr('builtins.input', lambda *args: next(inputs))

    bank_app(account)

    captured = capsys.readouterr()
    assert "Thank you. $1000.00 has been deposited to your account." in captured.out
    assert "Thank you. $500.00 has been withdrawn." in captured.out
    assert "Thank you. $400.00 has been withdrawn." in captured.out
    assert "1000.00" in captured.out
    assert "500.00" in captured.out
    assert "100.00" in captured.out

def test_print_multiple_deposit_and_withdraw(account: BankAccount, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture) -> None:
    """
    Test print multiple deposit and withdrawal amounts.

    :param account: The BankAccount instance to test.
    :param monkeypatch: The pytest fixture to modify builtins.
    :param capsys: The pytest fixture to capture stdout and stderr.
    """
    inputs = iter(['d', '1000', 'w', '500', 'd', '400', 'w', '300', 'p', 'q'])
    monkeypatch.setattr('builtins.input', lambda *args: next(inputs))

    bank_app(account)

    captured = capsys.readouterr()
    assert "Thank you. $1000.00 has been deposited to your account." in captured.out
    assert "Thank you. $500.00 has been withdrawn." in captured.out
    assert "Thank you. $400.00 has been deposited to your account." in captured.out
    assert "Thank you. $300.00 has been withdrawn." in captured.out
    assert "1000.00" in captured.out
    assert "500.00" in captured.out
    assert "900.00" in captured.out
    assert "600.00" in captured.out