from decimal import Decimal, InvalidOperation
from bank_account import BankAccount

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
                    deposit_input = input("Please enter the amount to deposit: ")
                    if deposit_input.strip().lower() == "b":
                        break
                    try:
                        amount = Decimal(deposit_input)
                        # Checking to see if number input is less than 2dp
                        if abs(amount.as_tuple().exponent) <= 2:
                            if amount > 0:
                                account.deposit(amount)
                                break
                            elif amount < 0:
                                print("Your deposit amount must be a positive number. Please try again.\nEnter [b] to return to main page.")
                            else:
                                print("Your deposit amount is too small. Please try again.\nEnter [b] to return to main page.")
                        else:
                            print("We only accept values rounded to the cent. Please try again.\nEnter [b] to return to main page.")
                    except InvalidOperation:
                        print("Invalid deposit amount. Please try again.\nEnter [b] to return to main page.")

            # Withdraw
            case 'w':
                # Continuously prompt for valid withdrawal amount
                while True:
                    withdrawal_input = input("Please enter the amount to withdraw: ")
                    if withdrawal_input.strip().lower() == "b":
                        break
                    try:
                        amount = Decimal(withdrawal_input)
                        # Checking to see if number input is less than 2dp
                        if abs(amount.as_tuple().exponent) <= 2:
                            if amount > 0 and amount <= account.balance:
                                account.withdraw(amount)
                                break
                            elif amount < 0:
                                print("Your withdrawal amount must be a positive number. Please try again.\nEnter [b] to return to main page.")
                            elif amount > account.balance:
                                print("Your bank account has insufficient funds. Please try again.\nEnter [b] to return to main page.")
                            else:
                                print("Your withdrawal amount is too small. Please try again.\nEnter [b] to return to main page.")
                        else:
                            print("We only accept values rounded to the cent. Please try again.\nEnter [b] to return to main page.")
                    except InvalidOperation:
                        print("Invalid withdrawal amount. Please try again.\nEnter [b] to return to main page.")

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

if __name__ == "__main__":
    account = BankAccount()
    bank_app(account)