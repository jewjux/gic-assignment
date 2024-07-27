from decimal import Decimal
from datetime import datetime
class Transaction:
    """
    Class to represent a single transaction.
    """
    def __init__(self, date: datetime, amount: Decimal, balance: Decimal):
        """
        Initialise the transaction with date, amount, balance.

        :param date: The date of the transaction.
        :param amount: The amount of the transaction.
        :param balance: The balance after the transaction.
        """
        self.date: datetime = date
        self.amount: Decimal = amount
        self.balance: Decimal = balance

    def format_transaction(self, max_amount_width, max_balance_width) -> str:
        """
        Return the transaction as a formatted line with the maximum widths.

        :return: A single formatted transaction.
        """
        date_str = self.date.strftime("%d %b %Y %I:%M:%S%p")
        amount_str = f"{self.amount:.2f}".ljust(max_amount_width)
        balance_str = f"{self.balance:.2f}".ljust(max_balance_width)
        return f"{date_str} | {amount_str} | {balance_str}"