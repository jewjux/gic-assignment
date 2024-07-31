import pytest
import unittest
from unittest.mock import MagicMock, patch, call
from decimal import Decimal, InvalidOperation
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
        self.assertEqual(self.mock_bank_app.validate_input('100.00'), Decimal('100.00'))

    def test_valid_input(self):
        self.assertEqual(self.mock_bank_app.validate_input('100.00'), Decimal('100.00'))

    def test_valid_input_with_two_decimal_places(self):
        self.assertEqual(self.mock_bank_app.validate_input('123.45'), Decimal('123.45'))

    def test_negative_input(self):
        self.assertIsNone(self.mock_bank_app.validate_input('-100.00'))
        self.mock_bank_app.view.error_negative_amount.assert_called_once()

    def test_zero_input(self):
        self.assertIsNone(self.mock_bank_app.validate_input('0.00'))
        self.mock_bank_app.view.error_zero_amount.assert_called_once()

    def test_invalid_rounding(self):
        self.assertIsNone(self.mock_bank_app.validate_input('100.123'))
        self.mock_bank_app.view.error_rounding.assert_called_once()

    def test_non_number_input(self):
        self.assertIsNone(self.mock_bank_app.validate_input('abc'))
        self.mock_bank_app.view.error_non_number.assert_called_once()

    def test_special_characters_input(self):
        self.assertIsNone(self.mock_bank_app.validate_input('!%$'))
        self.mock_bank_app.view.error_non_number.assert_called_once()

class TestHandleDeposit(SettingUpTestCase):
    
    def setUp(self):
        super().setUp()

        def mock_validate_input(input):
            if input == 'invalid':
                self.mock_view.error_non_number()
                return None
            else:
                return Decimal('100.00')  # Mock valid input
        
        self.mock_account.create_transaction = MagicMock()
        self.mock_bank_app.validate_input = MagicMock(side_effect=mock_validate_input)

    def test_handle_deposit_valid_amount(self):
        with patch.object(self.mock_view, 'prompt_for_deposit', side_effect=['100.00', 'q']), \
            patch.object(self.mock_bank_app, 'validate_input', return_value=Decimal('100.00')), \
            patch.object(self.mock_account, 'create_transaction', return_value=True):
            
            self.mock_bank_app.handle_deposit()
            self.mock_view.prompt_for_deposit.assert_called_once()
            self.mock_account.create_transaction.assert_called_once_with(Decimal('100.00'), TransactionType.CREDIT)
            self.mock_view.show_deposit_success.assert_called_once_with(Decimal('100.00'))

    def test_handle_deposit_invalid_amount(self):
        with patch.object(self.mock_view, 'prompt_for_deposit', side_effect=['invalid', 'q']), \
            patch.object(self.mock_bank_app, 'validate_input', side_effect=self.mock_bank_app.validate_input):
            
            self.mock_bank_app.handle_deposit()
            self.mock_view.error_non_number.assert_called_once()
            self.mock_account.create_transaction.assert_not_called()
            self.mock_view.show_deposit_success.assert_not_called()

    def test_handle_deposit_invalid_then_valid_amount(self):
        
        with patch.object(self.mock_view, 'prompt_for_deposit', side_effect=['invalid', '100.00', 'q']), \
            patch.object(self.mock_bank_app, 'validate_input', side_effect=self.mock_bank_app.validate_input):
            
            self.mock_bank_app.handle_deposit()
            self.mock_view.error_non_number.assert_called_once()
            self.mock_account.create_transaction.assert_called_once_with(Decimal('100.00'), TransactionType.CREDIT)
            self.mock_view.show_deposit_success.assert_called_once_with(Decimal('100.00'))

class TestHandleWithdrawal(SettingUpTestCase):
    
    def setUp(self):
        super().setUp()
        # self.mock_account.create_transaction = MagicMock(return_value=True)
        def mock_validate_input(input):
            if input == 'invalid':
                self.mock_view.error_non_number()
                return None
            else:
                return Decimal('100.00')  # Mock valid input
        
        self.mock_account.create_transaction = MagicMock()
        self.mock_bank_app.validate_input = MagicMock(side_effect=mock_validate_input)
        self.mock_view.prompt_for_withdrawal
    
    # prompt_for_withdrawal
    # create_transaction
    def test_handle_withdrawal_valid_amount(self):
        def side_effect():
            # Return a sequence of inputs
            inputs = ['100.0', 'q']
            return inputs.pop(0)
        
        with patch.object(self.mock_view, 'prompt_for_withdrawal', side_effect=side_effect), \
            patch.object(self.mock_bank_app, 'validate_input', return_value=Decimal('100.00')), \
            patch.object(self.mock_account, 'create_transaction', return_value=True):
            
            self.mock_bank_app.handle_withdrawal()
            self.mock_view.prompt_for_withdrawal.assert_called_once()
            self.mock_account.create_transaction.assert_called_once_with(Decimal('100.00'), TransactionType.DEBIT)
            self.mock_view.show_withdrawal_success.assert_called_once_with(Decimal('100.00'))
    
    # error valid_input
    def test_handle_withdrawal_invalid_amount(self):
        with patch.object(self.mock_view, 'prompt_for_withdrawal', side_effect=['invalid', 'q']), \
            patch.object(self.mock_bank_app, 'validate_input', side_effect=self.mock_bank_app.validate_input):
            
            self.mock_bank_app.handle_withdrawal()
            self.mock_view.error_non_number.assert_called_once()
            self.mock_account.create_transaction.assert_not_called()
            self.mock_view.show_withdrawal_success.assert_not_called()
    
    # error_insufficient_funds

    def test_handle_withdrawal_insufficient_funds(self):
        with patch.object(self.mock_view, 'prompt_for_withdrawal', side_effect=['100.0', 'q']), \
            patch.object(self.mock_account, 'create_transaction', return_value=False):

            self.mock_bank_app.handle_withdrawal()
            self.mock_view.error_insufficient_funds.assert_called_once()

'''


def test_handle_deposit_error_rounding(bank_app):
   with patch('builtins.input', side_effect=['0.001', 'q']), \
        patch.object(BankView, 'error_rounding'):
       
       bank_app.handle_deposit()
       BankView.error_rounding.assert_called_once()

def test_handle_deposit_error_negative(bank_app):
   with patch('builtins.input', side_effect=['-100', 'q']), \
        patch.object(BankView, 'error_negative_amount'):
       
       bank_app.handle_deposit()
       BankView.error_negative_amount.assert_called_once()




def test_handle_withdrawal_valid_amount(bank_app, mock_account):
   with patch('builtins.input', side_effect=['100.00', 'q']), \
        patch.object(BankView, 'show_withdrawal_success'), \
        patch.object(bank_app, 'validate_input', return_value=Decimal('100.00')):
       bank_app.handle_withdrawal()
       mock_account.create_transaction.assert_called_once_with(Decimal('100.00'), TransactionType.DEBIT)
       BankView.show_withdrawal_success.assert_called_once_with(Decimal('100.00'))



def test_handle_deposit_with_whitespace(bank_app):
   with patch('builtins.input', side_effect=[' 100.00 ', 'q']), \
        patch.object(BankView, 'show_deposit_success'), \
        patch.object(bank_app, 'validate_input', return_value=Decimal('100.00')):
       bank_app.handle_deposit()
       BankView.show_deposit_success.assert_called_once_with(Decimal('100.00'))

def test_handle_deposit_with_special_characters(bank_app):
   with patch('builtins.input', side_effect=['$100.00', 'q']), \
        patch.object(BankView, 'error_non_number'), \
        patch.object(bank_app, 'validate_input', side_effect=[None, None]):
       bank_app.handle_deposit()
       BankView.error_non_number.assert_called_once()

def test_handle_withdrawal_with_whitespace(bank_app, mock_account):
   with patch('builtins.input', side_effect=[' 100.00 ', 'q']), \
        patch.object(BankView, 'show_withdrawal_success'), \
        patch.object(bank_app, 'validate_input', return_value=Decimal('100.00')):
       bank_app.handle_withdrawal()
       mock_account.create_transaction.assert_called_once_with(Decimal('100.00'), TransactionType.DEBIT)
       BankView.show_withdrawal_success.assert_called_once_with(Decimal('100.00'))
       
def test_handle_withdrawal_with_special_characters(bank_app):
   with patch('builtins.input', side_effect=['$100.00', 'q']), \
        patch.object(BankView, 'error_non_number'), \
        patch.object(bank_app, 'validate_input', side_effect=[None, None]):
       bank_app.handle_withdrawal()
       BankView.error_non_number.assert_called_once()

def test_print_statement(bank_app, mock_account):
   mock_account.print_statement = MagicMock()
   with patch('builtins.input', side_effect=['p', 'q']), \
        patch.object(BankView, 'show_menu'), \
        patch.object(BankView, 'show_goodbye'):
       bank_app.run()
       BankView.show_menu.assert_called()
       mock_account.print_statement.assert_called()
       BankView.show_goodbye.assert_called()
'''
