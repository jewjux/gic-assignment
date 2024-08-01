import pytest
import unittest
from unittest.mock import MagicMock, patch
from decimal import Decimal
from src.service.controller import BankAccount, BankView, BankApp, TransactionType


@pytest.fixture
def mock_account():
    account = BankAccount()
    account.create_transaction = MagicMock(return_value=True)
    return account


@pytest.fixture
def mock_view():
    return MagicMock(spec=BankView)


@pytest.fixture
def bank_app(mock_account, mock_view):
    return BankApp(mock_account, mock_view)


class SettingUpTestCase(unittest.TestCase):
    def setUp(self):
        self.mock_account = BankAccount()
        self.mock_view = MagicMock(spec=BankView)
        self.mock_bank_app = BankApp(self.mock_account, self.mock_view)


class TestValidateInput(SettingUpTestCase):
    def setUp(self):
        super().setUp()

    def test_valid_input(self):
        self.assertEqual(self.mock_bank_app.validate_input("100.00"), Decimal("100.00"))

    def test_valid_input_with_two_decimal_places(self):
        self.assertEqual(self.mock_bank_app.validate_input("123.45"), Decimal("123.45"))

    def test_negative_input(self):
        self.assertIsNone(self.mock_bank_app.validate_input("-100.00"))
        self.mock_bank_app.view.error_negative_amount.assert_called_once()

    def test_zero_input(self):
        self.assertIsNone(self.mock_bank_app.validate_input("0.00"))
        self.mock_bank_app.view.error_zero_amount.assert_called_once()

    def test_invalid_rounding(self):
        self.assertIsNone(self.mock_bank_app.validate_input("100.123"))
        self.mock_bank_app.view.error_rounding.assert_called_once()

    def test_non_number_input(self):
        self.assertIsNone(self.mock_bank_app.validate_input("abc"))
        self.mock_bank_app.view.error_non_number.assert_called_once()

    def test_special_characters_input(self):
        self.assertIsNone(self.mock_bank_app.validate_input("!%$"))
        self.mock_bank_app.view.error_non_number.assert_called_once()


class TestHandleDeposit(SettingUpTestCase):

    def setUp(self):
        super().setUp()

        def mock_validate_input(input):
            if input == "100.00":
                return Decimal("100.00")  # Mock valid input
            else:
                self.mock_view.error_non_number()
                return None

        self.mock_account.create_transaction = MagicMock()
        self.mock_bank_app.validate_input = MagicMock(side_effect=mock_validate_input)

    def test_handle_deposit_valid_amount(self):
        with patch.object(
            self.mock_view, "prompt_for_deposit", side_effect=["100.00", "q"]
        ), patch.object(
            self.mock_bank_app, "validate_input", return_value=Decimal("100.00")
        ), patch.object(
            self.mock_account, "create_transaction", return_value=True
        ):

            self.mock_bank_app.handle_deposit()
            self.mock_view.prompt_for_deposit.assert_called_once()
            self.mock_account.create_transaction.assert_called_once_with(
                Decimal("100.00"), TransactionType.CREDIT
            )
            self.mock_view.show_deposit_success.assert_called_once_with(
                Decimal("100.00")
            )

    def test_handle_deposit_invalid_amount(self):
        with patch.object(
            self.mock_view, "prompt_for_deposit", side_effect=["invalid", "q"]
        ):

            self.mock_bank_app.handle_deposit()
            self.mock_view.error_non_number.assert_called_once()
            self.mock_account.create_transaction.assert_not_called()
            self.mock_view.show_deposit_success.assert_not_called()

    def test_handle_deposit_invalid_then_valid_amount(self):

        with patch.object(
            self.mock_view, "prompt_for_deposit", side_effect=["invalid", "100.00", "q"]
        ):

            self.mock_bank_app.handle_deposit()
            self.mock_view.error_non_number.assert_called_once()
            self.mock_account.create_transaction.assert_called_once_with(
                Decimal("100.00"), TransactionType.CREDIT
            )
            self.mock_view.show_deposit_success.assert_called_once_with(
                Decimal("100.00")
            )

    def test_handle_deposit_with_whitespace(self):
        with patch.object(
            self.mock_view, "prompt_for_deposit", side_effect=[" 100.00", "q"]
        ), patch.object(
            self.mock_bank_app, "validate_input", return_value=Decimal("100.00")
        ):

            self.mock_bank_app.handle_deposit()
            self.mock_view.show_deposit_success.assert_called_once_with(
                Decimal("100.00")
            )

    def test_handle_deposit_with_special_characters(self):
        with patch.object(
            self.mock_view, "prompt_for_deposit", side_effect=["$100.00", "q"]
        ):

            self.mock_bank_app.handle_deposit()
            self.mock_view.error_non_number.assert_called_once()


class TestHandleWithdrawal(SettingUpTestCase):

    def setUp(self):
        super().setUp()

        def mock_validate_input(input):
            if input == "100.00":
                return Decimal("100.00")  # Mock valid input
            else:
                self.mock_view.error_non_number()
                return None

        self.mock_account.create_transaction = MagicMock()
        self.mock_bank_app.validate_input = MagicMock(side_effect=mock_validate_input)

    # prompt_for_withdrawal
    # create_transaction
    def test_handle_withdrawal_valid_amount(self):
        with patch.object(
            self.mock_view, "prompt_for_withdrawal", side_effect=["100.00", "q"]
        ), patch.object(
            self.mock_bank_app, "validate_input", return_value=Decimal("100.00")
        ), patch.object(
            self.mock_account, "create_transaction", return_value=True
        ):

            self.mock_bank_app.handle_withdrawal()
            self.mock_view.prompt_for_withdrawal.assert_called_once()
            self.mock_account.create_transaction.assert_called_once_with(
                Decimal("100.00"), TransactionType.DEBIT
            )
            self.mock_view.show_withdrawal_success.assert_called_once_with(
                Decimal("100.00")
            )

    # error valid_input
    def test_handle_withdrawal_invalid_amount(self):
        with patch.object(
            self.mock_view, "prompt_for_withdrawal", side_effect=["invalid", "q"]
        ):

            self.mock_bank_app.handle_withdrawal()
            self.mock_view.error_non_number.assert_called_once()
            self.mock_account.create_transaction.assert_not_called()
            self.mock_view.show_withdrawal_success.assert_not_called()

    # error_insufficient_funds
    def test_handle_withdrawal_insufficient_funds(self):
        with patch.object(
            self.mock_view, "prompt_for_withdrawal", side_effect=["100.00", "q"]
        ), patch.object(self.mock_account, "create_transaction", return_value=False):

            self.mock_bank_app.handle_withdrawal()
            self.mock_view.error_insufficient_funds.assert_called_once()

    def test_handle_withdrawal_invalid_then_valid_amount(self):

        with patch.object(
            self.mock_view,
            "prompt_for_withdrawal",
            side_effect=["invalid", "100.00", "q"],
        ):
            self.mock_bank_app.handle_withdrawal()
            self.mock_view.error_non_number.assert_called_once()
            self.mock_account.create_transaction.assert_called_once_with(
                Decimal("100.00"), TransactionType.DEBIT
            )
            self.mock_view.show_withdrawal_success.assert_called_once_with(
                Decimal("100.00")
            )

    def test_handle_withdrawal_with_whitespace(self):
        with patch.object(
            self.mock_view, "prompt_for_withdrawal", side_effect=[" 100.00", "q"]
        ), patch.object(
            self.mock_bank_app, "validate_input", return_value=Decimal("100.00")
        ):

            self.mock_bank_app.handle_withdrawal()
            self.mock_view.show_withdrawal_success.assert_called_once_with(
                Decimal("100.00")
            )

    def test_handle_withdrawal_with_special_characters(self):
        with patch.object(
            self.mock_view, "prompt_for_withdrawal", side_effect=["$100.00", "q"]
        ):

            self.mock_bank_app.handle_withdrawal()
            self.mock_view.error_non_number.assert_called_once()


class TestRun(SettingUpTestCase):

    def setUp(self):
        super().setUp()
        self.mock_account.print_statement = MagicMock()

    def test_print_menu(self):
        with patch("builtins.input", side_effect=["p", "q"]):

            self.mock_bank_app.run()
            self.mock_view.show_menu.assert_called()
            self.mock_account.print_statement.assert_called()
            self.mock_view.show_goodbye.assert_called()

    def test_print_error_invalid_action(self):
        with patch("builtins.input", side_effect=["invalid", "q"]):

            self.mock_bank_app.run()
            self.mock_view.error_invalid_action.assert_called()
