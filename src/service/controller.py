from decimal import Decimal, InvalidOperation

from ..models.transaction_type import TransactionType
from ..models.bank_account import BankAccount
from .view import BankView


class BankApp:
    """
    Class to run the bank service.
    """

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
                case "d":
                    self.handle_deposit()

                # Withdraw
                case "w":
                    self.handle_withdrawal()

                # Print statement
                case "p":
                    self.account.print_statement()

                # Quit
                case "q":
                    self.view.show_goodbye()
                    break

                # Invalid action
                case _:
                    self.view.error_invalid_action()

    def validate_input(self, input: str) -> Decimal:
        """
        Function to validate input for:
        - positive number
        - 2 decimal place
        - non-number inputs.

        Throws error for:
        - negative amount
        - zero amount
        - rounding (more than 2 decimal places)

        :param input: The input to validate.

        :return Decimal: The valid amount.
        """
        try:
            input = Decimal(input)

            # Invalid rounding (more than 2 decimal places)
            if abs(input.as_tuple().exponent) > 2:
                self.view.error_rounding()
                return None

            if input > 0:
                return input

            elif input < 0:
                self.view.error_negative_amount()
                return None

            else:
                self.view.error_zero_amount()
                return None

        # Invalid non number (eg: 'abc', '!%$')
        except InvalidOperation:
            self.view.error_non_number()
            return None

    def handle_deposit(self):
        """
        Function to carry out the flow of a deposit:

        - Prompts for user input for amount
        - Checks the input for valid amount
        - Creates the transaction from the valid deposit
        """
        while True:
            deposit_input = self.view.prompt_for_deposit()

            # Exit to main page
            if deposit_input.strip().lower() == "q":
                break

            amount = self.validate_input(deposit_input)

            if amount is not None:
                is_successful = self.account.create_transaction(
                    amount, TransactionType.CREDIT
                )

                if is_successful:
                    self.view.show_deposit_success(amount)
                    break

    def handle_withdrawal(self):
        """
        Function to carry out the flow of a withdrawal:

        - Prompts for user input for amount
        - Checks the input for valid amount
        - Creates the transaction from the valid withdrawal
        """
        while True:
            withdrawal_input = self.view.prompt_for_withdrawal()

            # Exit to main page
            if withdrawal_input.strip().lower() == "q":
                break

            amount = self.validate_input(withdrawal_input)

            if amount is not None:
                is_successful = self.account.create_transaction(
                    amount, TransactionType.DEBIT
                )

                if is_successful:
                    self.view.show_withdrawal_success(amount)
                    break

                else:
                    self.view.error_insufficient_funds()
