from decimal import Decimal, InvalidOperation

from ..models.transaction_type import TransactionType
from ..models.bank_account import BankAccount
from .view import BankView

class BankApp:

    def __init__(self, account: BankAccount, view: BankView):
        """
        Initialise bank application with model and view.
        """
        self.account: BankAccount = account
        self.view: BankView = view
    
    def run(self) -> None:
        """
        Function to run the continuous banking service.

        Main services include:
        - Depositing an amount
        - Withdrawing an amount
        - Printing an account statement
        """
        while True:

            self.view.show_menu()
            action = input().strip().lower()

            match action:

                # Deposit
                case 'd':
                    self.handle_deposit()
                
                # Withdraw
                case 'w':
                    self.handle_withdrawal()
                
                # Print statement
                case 'p':
                    self.account.print_statement()

                # Quit
                case 'q':
                    self.view.show_goodbye()
                    break

                #Invalid action
                case _:
                    self.view.error_invalid_action()
    
    def check_input(self, input: str) -> Decimal:
        """
        Function to check input for positive number, 2 decimal place, and non-number inputs. Throws error for negative amount, zero amount, error in rounding (more than 2 decimal places)

        :param input: The input to check.

        :return Decimal: The valid amount.
        """
        try:
            
            input = Decimal(input)

            # Check if number input has valid rounding (2 or less decimal places)
            if abs(input.as_tuple().exponent) <= 2:

                if input > 0:
                    return input
                
                elif input < 0:
                    self.view.error_negative_amount()
                    return None
                
                else:
                    self.view.error_zero_amount()
                    return None
                
            else:
                self.view.error_rounding()
                return None
            
        except InvalidOperation:
            self.view.error_non_number()
            return None

    def handle_deposit(self):
        """
        Function to carry out the flow of a deposit:

        - Prompts for user input for amount
        - Checks the input for valid amount
        - Logs the valid deposit as a transaction
        """
        # Flag for whether logging of the deposit is successful
        log_success: bool = False

        # Continuously prompt for valid deposit amount
        while True:
            deposit_input = self.view.prompt_for_deposit()

            # Exit to main page
            if deposit_input.strip().lower() == "q":
                break
            
            # Checks whether input deposit amount is valid
            amount = self.check_input(deposit_input)

            # Amount is valid number
            if amount is not None:
                # Attempting to log the deposit
                log_success = self.account.log_transaction(amount, TransactionType.CREDIT)

                # Valid deposit, logging successful
                if log_success: 
                    self.view.show_deposit_success(amount)
                    break
    
    def handle_withdrawal(self):
        """
        Function to carry out the flow of a withdrawal:

        - Prompts for user input for amount
        - Checks the input for valid amount
        - Logs the valid withdrawal as a transaction
        """
        # Flag for whether logging of the withdrawal is successful
        log_success: bool = False

        # Continuously prompt for valid withdrawal amount
        while True:
            withdrawal_input = self.view.prompt_for_withdrawal()

            # Exit to main page
            if withdrawal_input.strip().lower() == "q":
                break

            # Checks whether input withdrawal amount is valid
            amount = self.check_input(withdrawal_input)

            # Amount is valid number
            if amount is not None:

                # Attempting to log the withdrawal
                log_success = self.account.log_transaction(amount, TransactionType.DEBIT)

                # Valid withdrawal, logging successful
                if log_success:
                    self.view.show_withdrawal_success(amount)
                    break

                # Invalid withdrawal due to insufficient funds
                else:
                    self.view.error_insufficient_funds()