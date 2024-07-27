from decimal import Decimal, InvalidOperation

from ..models.transaction_type import TransactionType
from ..models.bank_account import BankAccount

def check_input(input: str) -> Decimal:
    """
    Function to check input for positive number, 2 decimal place, and non-number inputs.

    :param input: The input to check.

    :return Decimal: The amount to deposit or withdraw.
    """
    try:
        input = Decimal(input)
        if abs(input.as_tuple().exponent) <= 2: # Checking to see if number input is less than 2dp
            if input > 0:
                return input
            elif input < 0:
                print("Your amount must be a positive number. Please try again.\nEnter [q] to return to main page.")
                return None
            else:
                print("Your amount is too small. Please try again.\nEnter [q] to return to main page.")
                return None
        else:
            print("Your amount should be rounded to the cent. Please try again.\nEnter [q] to return to main page.")
            return None
    except InvalidOperation:
        print("Invalid amount. Please try again.\nEnter [q] to return to main page.")
        return None

def bank_app(account: BankAccount) -> None:
    """
    Function to run the simple banking system.

    Main functions include:
    - Depositing an amount
    - Withdrawing an amount
    - Printing an account statement

    :param account: A BankAccount instance.
    """

    # Continuously remain in main page unless user quits
    while True:
        print("Welcome to AwesomeGIC Bank! What would you like to do?")
        print("[D]eposit")
        print("[W]ithdraw")
        print("[P]rint statement")
        print("[Q]uit")
        action = input().strip().lower()

        match action:
            # Deposit
            case 'd':
                # Continuously prompt for valid deposit amount
                while True:
                    deposit_input = str(input("Please enter the amount to deposit: "))
                    if deposit_input.strip().lower() == "q":
                        break
                    amount = check_input(deposit_input)
                    if amount != None:
                        log_success = account.log_transaction(amount, TransactionType.CREDIT)
                        if log_success: break
                        else: continue

            # Withdraw
            case 'w':
                # Continuously prompt for valid withdrawal amount
                while True:
                    withdrawal_input = input("Please enter the amount to withdraw: ")
                    if withdrawal_input.strip().lower() == "q":
                        break
                    amount = check_input(withdrawal_input)
                    if amount != None:
                        log_success = account.log_transaction(amount, TransactionType.DEBIT)
                        if log_success: break
                        else: continue

            # Print statement
            case 'p':
                account.print_statement()
        
            # Quit
            case 'q':
                print("Thank you for banking with AwesomeGIC Bank.")
                print("Have a nice day!")
                break

            case _:
                print("Invalid option. Please try again.")