from datetime import datetime
from decimal import Decimal

from .transaction_type import TransactionType
from .transaction import Transaction


class BankAccount:
    """
    Class to represent a Bank Account.
    """

    def __init__(self):
        """
        Initialise bank account with balance of 0.0 and no transactions.
        """
        # Private attributes only modifiable within the class
        self.__balance: Decimal = Decimal("0.0")
        self.__transactions: list = []

    def create_transaction(
        self, amount: Decimal, transaction_type: TransactionType
    ) -> bool:
        """
        Private method to create the transaction and update the balance.

        :param amount: The amount to deposit or withdraw.
        :param transaction_type: The type of transaction (CREDIT, DEBIT).

        :return bool: Flag if creation of transaction is successful.
        """
        match transaction_type:
            # Deposit
            case TransactionType.CREDIT:
                self.__balance += amount
                self.__transactions.append(
                    Transaction(datetime.now(), amount, self.__balance)
                )
                return True

            # Withdrawal
            case TransactionType.DEBIT:
                if amount <= self.__balance:
                    self.__balance -= amount
                    self.__transactions.append(
                        Transaction(datetime.now(), -amount, self.__balance)
                    )
                    return True

                elif amount > self.__balance:
                    return False

            case _:
                print("Invalid transaction type detected.")
                return False

    def print_statement(self) -> None:
        """
        Print the account statement to show all transactions.
        """
        # Transaction history exists
        if len(self.__transactions) > 0:
            # Formatting maximum width of | Amount |
            max_amount_width = max(len(f"{t.amount:.2f}") for t in self.__transactions)
            max_amount_width = max(max_amount_width, len("Amount"))

            # Formatting maximum width of | Balance |
            max_balance_width = max(
                len(f"{t.balance:.2f}") for t in self.__transactions
            )
            max_balance_width = max(max_balance_width, len("Balance"))

            # Formatting width of Date |
            date_width = len("dd MMM yyyy HH:mm:ssAM")

            # Print headers (Date, Amount, Balance) in formatted widths
            print(
                f"{'Date'.ljust(date_width)} | {'Amount'.ljust(max_amount_width)} | {'Balance'.ljust(max_balance_width)}"
            )

            # Print all transactions
            for transaction in self.__transactions:
                print(
                    transaction.format_transaction(max_amount_width, max_balance_width)
                )

        # No transaction history
        else:
            print(f"{'Date'.ljust(20)} | {'Amount'.ljust(10)} | {'Balance'.ljust(10)}")
            print("No transactions found.")

    @property
    def balance(self) -> Decimal:
        """
        Read-only property to get the current balance.

        :return Decimal: The current balance.
        """
        return self.__balance

    @property
    def transactions(self) -> list:
        """
        Read-only property to get the account transactions.

        :return list: The account transactions.
        """
        return self.__transactions
