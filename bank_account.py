from datetime import datetime
from decimal import Decimal

from transaction import Transaction

class BankAccount:
    """
    Class to represent a Bank Account.
    """
    def __init__(self):
        """
        Initialise bank account with balance of 0.0 and no transactions.
        """
        self.balance: Decimal = Decimal('0.0')
        self.transactions = []

    def deposit(self, amount: str) -> None:
        """
        Deposit specified amount into bank account.

        :param amount: The amount to deposit.
        """
        self.balance += amount
        self.transactions.append(Transaction(datetime.now(), amount, self.balance))
        print(f"Thank you. ${amount:.2f} has been deposited to your account.")
            

    def withdraw(self, amount: Decimal) -> None:
        """
        Withdraw a specified amount from the bank account.

        :param amount: The amount to withdraw.
        """
        self.balance -= amount
        self.transactions.append(Transaction(datetime.now(), -amount, self.balance))
        print(f"Thank you. ${amount:.2f} has been withdrawn.")

    def print_statement(self) -> None:
        """
        Print the account statement to show all transactions.

        :return: The account statement as a string.
        """
        if len(self.transactions) > 0:
            max_amount_width = max(len(f"{t.amount:.2f}") for t in self.transactions)
            max_amount_width = max(max_amount_width, len("Amount"))
            max_balance_width = max(len(f"{t.balance:.2f}") for t in self.transactions)
            max_balance_width = max(max_balance_width, len("Balance"))

            date_width = len("dd MMM yyyy HH:mm:ssAM")
            print(f"{'Date'.ljust(date_width)} | {'Amount'.ljust(max_amount_width)} | {'Balance'.ljust(max_balance_width)}")
            for transaction in self.transactions:
                print(transaction.format_transaction(max_amount_width, max_balance_width))
        else:
            print(f"{'Date'.ljust(20)} | {'Amount'.ljust(10)} | {'Balance'.ljust(10)}")
            print("No transactions found.")