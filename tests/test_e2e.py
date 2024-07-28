import pytest
from decimal import Decimal

from src.models.bank_account import BankAccount
from src.service.view import BankView
from src.service.controller import BankApp


@pytest.fixture
def account():
    return BankAccount()


def test_deposit_negative_amount(
    account: BankAccount, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture
):
    """
    Test negative deposit amount.

    :param account: The BankAccount instance to test.
    :param monkeypatch: The pytest fixture to modify builtins.
    :param capsys: The pytest fixture to capture stdout and stderr.
    """
    inputs = iter(["d", "-100", "q", "q"])
    monkeypatch.setattr("builtins.input", lambda *args: next(inputs))

    account = BankAccount()
    view = BankView()
    BankApp(account, view).run()

    captured = capsys.readouterr()
    assert "Your amount must be a positive number." in captured.out
    assert account.balance == Decimal("0.0")
    assert len(account.transactions) == 0


def test_deposit_non_number(
    account: BankAccount, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture
):
    """
    Test non number deposit input.

    :param account: The BankAccount instance to test.
    :param monkeypatch: The pytest fixture to modify builtins.
    :param capsys: The pytest fixture to capture stdout and stderr.
    """
    inputs = iter(["d", "abc%$!", "q", "q"])
    monkeypatch.setattr("builtins.input", lambda *args: next(inputs))

    account = BankAccount()
    view = BankView()
    BankApp(account, view).run()

    captured = capsys.readouterr()
    assert "Invalid amount. Please try again." in captured.out
    assert account.balance == Decimal("0.0")
    assert len(account.transactions) == 0


def test_deposit_empty(
    account: BankAccount, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture
):
    """
    Test empty deposit input.

    :param account: The BankAccount instance to test.
    :param monkeypatch: The pytest fixture to modify builtins.
    :param capsys: The pytest fixture to capture stdout and stderr.
    """
    inputs = iter(["d", "", "q", "q"])
    monkeypatch.setattr("builtins.input", lambda *args: next(inputs))

    account = BankAccount()
    view = BankView()
    BankApp(account, view).run()

    captured = capsys.readouterr()
    assert "Invalid amount. Please try again." in captured.out
    assert account.balance == Decimal("0.0")
    assert len(account.transactions) == 0


def test_deposit_multiple_negative_amount(
    account: BankAccount, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture
):
    """
    Test 2 negative deposit numbers followed by a positive deposit number.

    :param account: The BankAccount instance to test.
    :param monkeypatch: The pytest fixture to modify builtins.
    :param capsys: The pytest fixture to capture stdout and stderr.
    """
    inputs = iter(["d", "-100", "-500", "500", "q"])
    monkeypatch.setattr("builtins.input", lambda *args: next(inputs))

    account = BankAccount()
    view = BankView()
    BankApp(account, view).run()

    captured = capsys.readouterr()
    assert "Your amount must be a positive number." in captured.out
    assert "Your amount must be a positive number." in captured.out
    assert account.balance == Decimal("500.0")
    assert len(account.transactions) == 1
    assert "Thank you for banking with AwesomeGIC Bank." in captured.out


def test_deposit_large_numbers(
    account: BankAccount, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture
):
    """
    Test large deposit amount.

    :param account: The BankAccount instance to test.
    :param monkeypatch: The pytest fixture to modify builtins.
    :param capsys: The pytest fixture to capture stdout and stderr.
    """
    inputs = iter(["d", "9999999999999999.99", "q"])
    monkeypatch.setattr("builtins.input", lambda *args: next(inputs))

    account = BankAccount()
    view = BankView()
    BankApp(account, view).run()

    captured = capsys.readouterr()
    assert (
        "Thank you. $9999999999999999.99 has been deposited to your account."
        in captured.out
    )
    assert account.balance == Decimal("9999999999999999.99")
    assert len(account.transactions) == 1


def test_deposit_long_numbers(
    account: BankAccount, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture
) -> None:
    """
    Test large deposit amount.

    :param account: The BankAccount instance to test.
    :param monkeypatch: The pytest fixture to modify builtins.
    :param capsys: The pytest fixture to capture stdout and stderr.
    """
    inputs = iter(["d", "99.9999", "0.0001", "q", "q"])
    monkeypatch.setattr("builtins.input", lambda *args: next(inputs))

    view = BankView()
    BankApp(account, view).run()

    captured = capsys.readouterr()
    assert "Your amount should be rounded to the cent." in captured.out
    assert "Your amount should be rounded to the cent." in captured.out
    assert account.balance == Decimal("0.0")
    assert len(account.transactions) == 0


def test_withdraw_negative_amount(
    account: BankAccount, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture
):
    """
    Test negative withdrawal amount.

    :param account: The BankAccount instance to test.
    :param monkeypatch: The pytest fixture to modify builtins.
    :param capsys: The pytest fixture to capture stdout and stderr.
    """
    inputs = iter(["d", "500", "w", "-100", "q", "q"])
    monkeypatch.setattr("builtins.input", lambda *args: next(inputs))

    account = BankAccount()
    view = BankView()
    BankApp(account, view).run()

    captured = capsys.readouterr()
    assert "Thank you. $500.00 has been deposited to your account." in captured.out
    assert "Your amount must be a positive number." in captured.out
    assert account.balance == Decimal("500.0")
    assert len(account.transactions) == 1


def test_withdraw_insufficient_funds(
    account: BankAccount, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture
):
    """
    Test attempting to withdraw money from the account with insufficient funds.

    :param account: The BankAccount instance to test.
    :param monkeypatch: The pytest fixture to modify builtins.
    :param capsys: The pytest fixture to capture stdout and stderr.
    """
    inputs = iter(["w", "100", "q", "q"])
    monkeypatch.setattr("builtins.input", lambda *args: next(inputs))

    account = BankAccount()
    view = BankView()
    BankApp(account, view).run()

    captured = capsys.readouterr()
    assert "Your bank account has insufficient funds." in captured.out
    assert account.balance == Decimal("0.0")
    assert len(account.transactions) == 0


def test_withdraw_exact_balance(
    account: BankAccount, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture
):
    """
    Test withdrawing all balance.

    :param account: The BankAccount instance to test.
    :param monkeypatch: The pytest fixture to modify builtins.
    :param capsys: The pytest fixture to capture stdout and stderr.
    """
    inputs = iter(["d", "100", "w", "100", "q"])
    monkeypatch.setattr("builtins.input", lambda *args: next(inputs))

    account = BankAccount()
    view = BankView()
    BankApp(account, view).run()

    captured = capsys.readouterr()
    assert "Thank you. $100.00 has been deposited to your account." in captured.out
    assert "Thank you. $100.00 has been withdrawn." in captured.out
    assert account.balance == Decimal("0.0")
    assert len(account.transactions) == 2


def test_withdraw_slightly_insufficient_funds(
    account: BankAccount, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture
):
    """
    Test attempting to withdraw $100.01 from the account with $100.

    :param account: The BankAccount instance to test.
    :param monkeypatch: The pytest fixture to modify builtins.
    :param capsys: The pytest fixture to capture stdout and stderr.
    """
    inputs = iter(["d", "100", "w", "100.01", "q", "q"])
    monkeypatch.setattr("builtins.input", lambda *args: next(inputs))

    view = BankView()
    BankApp(account, view).run()

    captured = capsys.readouterr()
    assert "Your bank account has insufficient funds." in captured.out
    assert account.balance == Decimal("100.0")
    assert len(account.transactions) == 1


def test_print_empty(
    account: BankAccount, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture
):
    """
    Test print empty bank statement.

    :param account: The BankAccount instance to test.
    :param monkeypatch: The pytest fixture to modify builtins.
    :param capsys: The pytest fixture to capture stdout and stderr.
    """
    inputs = iter(["p", "q"])
    monkeypatch.setattr("builtins.input", lambda *args: next(inputs))

    account = BankAccount()
    view = BankView()
    BankApp(account, view).run()

    captured = capsys.readouterr()
    assert "Date" in captured.out
    assert "Amount" in captured.out
    assert "Balance" in captured.out
    assert "No transactions found." in captured.out


def test_print_large_balance(
    account: BankAccount, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture
):
    """
    Test print large account balance.

    :param account: The BankAccount instance to test.
    :param monkeypatch: The pytest fixture to modify builtins.
    :param capsys: The pytest fixture to capture stdout and stderr.
    """
    inputs = iter(["d", "9999999999999999.99", "p", "q"])
    monkeypatch.setattr("builtins.input", lambda *args: next(inputs))

    account = BankAccount()
    view = BankView()
    BankApp(account, view).run()

    captured = capsys.readouterr()
    assert (
        "Thank you. $9999999999999999.99 has been deposited to your account."
        in captured.out
    )
    assert "9999999999999999.99" in captured.out


def test_print_large_withdrawal(
    account: BankAccount, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture
):
    """
    Test print large account balance.

    :param account: The BankAccount instance to test.
    :param monkeypatch: The pytest fixture to modify builtins.
    :param capsys: The pytest fixture to capture stdout and stderr.
    """
    inputs = iter(["d", "9999999999999999.99", "w", "1999999999999999.99", "p", "q"])
    monkeypatch.setattr("builtins.input", lambda *args: next(inputs))

    account = BankAccount()
    view = BankView()
    BankApp(account, view).run()

    captured = capsys.readouterr()
    assert (
        "Thank you. $9999999999999999.99 has been deposited to your account."
        in captured.out
    )
    assert "Thank you. $1999999999999999.99 has been withdrawn." in captured.out
    assert "9999999999999999.99" in captured.out
    assert "8000000000000000.00" in captured.out


def test_print_multiple_deposit(
    account: BankAccount, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture
):
    """
    Test print multiple deposit amounts.

    :param account: The BankAccount instance to test.
    :param monkeypatch: The pytest fixture to modify builtins.
    :param capsys: The pytest fixture to capture stdout and stderr.
    """
    inputs = iter(["d", "500", "d", "400", "d", "300", "p", "q"])
    monkeypatch.setattr("builtins.input", lambda *args: next(inputs))

    account = BankAccount()
    view = BankView()
    BankApp(account, view).run()

    captured = capsys.readouterr()
    assert "Thank you. $500.00 has been deposited to your account." in captured.out
    assert "Thank you. $400.00 has been deposited to your account." in captured.out
    assert "Thank you. $300.00 has been deposited to your account." in captured.out
    assert "500.00" in captured.out
    assert "900.00" in captured.out
    assert "1200.00" in captured.out


def test_print_multiple_withdraw(
    account: BankAccount, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture
):
    """
    Test print multiple withdrawal amounts.

    :param account: The BankAccount instance to test.
    :param monkeypatch: The pytest fixture to modify builtins.
    :param capsys: The pytest fixture to capture stdout and stderr.
    """
    inputs = iter(["d", "1000", "w", "500", "w", "400", "p", "q"])
    monkeypatch.setattr("builtins.input", lambda *args: next(inputs))

    account = BankAccount()
    view = BankView()
    BankApp(account, view).run()

    captured = capsys.readouterr()
    assert "Thank you. $1000.00 has been deposited to your account." in captured.out
    assert "Thank you. $500.00 has been withdrawn." in captured.out
    assert "Thank you. $400.00 has been withdrawn." in captured.out
    assert "1000.00" in captured.out
    assert "500.00" in captured.out
    assert "100.00" in captured.out


def test_print_multiple_deposit_and_withdraw(
    account: BankAccount, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture
):
    """
    Test print multiple deposit and withdrawal amounts.

    :param account: The BankAccount instance to test.
    :param monkeypatch: The pytest fixture to modify builtins.
    :param capsys: The pytest fixture to capture stdout and stderr.
    """
    inputs = iter(["d", "1000", "w", "500", "d", "400", "w", "300", "p", "q"])
    monkeypatch.setattr("builtins.input", lambda *args: next(inputs))

    account = BankAccount()
    view = BankView()
    BankApp(account, view).run()

    captured = capsys.readouterr()
    assert "Thank you. $1000.00 has been deposited to your account." in captured.out
    assert "Thank you. $500.00 has been withdrawn." in captured.out
    assert "Thank you. $400.00 has been deposited to your account." in captured.out
    assert "Thank you. $300.00 has been withdrawn." in captured.out
    assert "1000.00" in captured.out
    assert "500.00" in captured.out
    assert "900.00" in captured.out
    assert "600.00" in captured.out


def test_error_invalid_actions(
    account: BankAccount, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture
):
    """
    Test different invalid inputs for main menu.

    :param account: The BankAccount instance to test.
    :param monkeypatch: The pytest fixture to modify builtins.
    :param capsys: The pytest fixture to capture stdout and stderr.
    """
    inputs = iter(["c", "%!$", "123", "q"])
    monkeypatch.setattr("builtins.input", lambda *args: next(inputs))

    account = BankAccount()
    view = BankView()
    BankApp(account, view).run()

    captured = capsys.readouterr()
    assert "Invalid option. Please try again." in captured.out
    assert "Invalid option. Please try again." in captured.out
    assert "Invalid option. Please try again." in captured.out
    assert "Invalid option. Please try again." in captured.out
