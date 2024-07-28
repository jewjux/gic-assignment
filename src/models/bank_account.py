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
        self.__balance: Decimal = Decimal('0.0')
        self.__transactions: list = []
    
    def __log_transaction(self, amount: Decimal, transaction_type: TransactionType) -> bool:
        """
        Private method to log the transaction and update the balance.

        :param amount: The amount to deposit or withdraw.
        :param transaction_type: 'credit' or 'debit' for different deposit or withdrawal.

        :return bool: Flag if logging is successful.
        """
        match transaction_type:
            # Deposit
            case TransactionType.CREDIT:
                self.__balance += amount
                self.__transactions.append(Transaction(datetime.now(), amount, self.__balance))
                return True

            # Withdrawal
            case TransactionType.DEBIT:
                if amount <= self.__balance:
                    self.__balance -= amount
                    self.__transactions.append(Transaction(datetime.now(), -amount, self.__balance))
                    return True
                
                elif amount > self.__balance:
                    return False
            
            case _:
                print("Invalid transaction type detected.")
                return False
    
    def log_transaction(self, amount: Decimal, transaction_type: str) -> bool:
        """
        Public method to log the transaction and update the balance.
        Calls the private __log_transaction method.
        """
        return self.__log_transaction(amount, transaction_type)
    
    def print_statement(self) -> None:
        """
        Print the account statement to show all transactions.
        """
        if len(self.__transactions) > 0:
            max_amount_width = max(len(f"{t.amount:.2f}") for t in self.__transactions)
            max_amount_width = max(max_amount_width, len("Amount"))
            max_balance_width = max(len(f"{t.balance:.2f}") for t in self.__transactions)
            max_balance_width = max(max_balance_width, len("Balance"))

            date_width = len("dd MMM yyyy HH:mm:ssAM")
            print(f"{'Date'.ljust(date_width)} | {'Amount'.ljust(max_amount_width)} | {'Balance'.ljust(max_balance_width)}")
            for transaction in self.__transactions:
                print(transaction.format_transaction(max_amount_width, max_balance_width))
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