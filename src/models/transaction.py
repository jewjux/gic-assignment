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
        # Private attributes only modifiable within the class
        self.__date: datetime = date
        self.__amount: Decimal = amount
        self.__balance: Decimal = balance

    def format_transaction(self, max_amount_width, max_balance_width) -> str:
        """
        Return the transaction as a formatted line with the maximum widths.

        :return: A single formatted transaction.
        """
        date_str = self.__date.strftime("%d %b %Y %I:%M:%S%p")
        amount_str = f"{self.__amount:.2f}".ljust(max_amount_width)
        balance_str = f"{self.__balance:.2f}".ljust(max_balance_width)
        return f"{date_str} | {amount_str} | {balance_str}"

    @property
    def date(self) -> datetime:
        """
        Read-only property to get the current date.

        :return datetime: The date of the transaction.
        """
        return self.__date

    @property
    def amount(self) -> Decimal:
        """
        Read-only property to get the current amount.

        :return Decimal: The amount of the transaction.
        """
        return self.__amount

    @property
    def balance(self) -> Decimal:
        """
        Read-only property to get the current balance.

        :return Decimal: The balance after the transaction.
        """
        return self.__balance
