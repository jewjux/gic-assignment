from decimal import Decimal


class BankView:
    """
    Class to display menu and print messages.
    """

    @staticmethod
    def show_menu() -> None:
        """
        Display menu message.
        """
        print("Welcome to AwesomeGIC Bank! What would you like to do?")
        print("[D]eposit")
        print("[W]ithdraw")
        print("[P]rint statement")
        print("[Q]uit")

    @staticmethod
    def prompt_for_deposit() -> None:
        """
        Display deposit prompt.
        """
        return input("Please enter the amount to deposit: ")

    @staticmethod
    def prompt_for_withdrawal() -> None:
        """
        Display withdrawal prompt.
        """
        return input("Please enter the amount to withdraw: ")

    @staticmethod
    def show_deposit_success(amount: Decimal) -> None:
        """
        Display deposit success.
        """
        print(f"Thank you. ${amount: .2f} has been deposited to your account.")

    @staticmethod
    def show_withdrawal_success(amount: Decimal) -> None:
        """
        Display withdrawal success.
        """
        print(f"Thank you. ${amount: .2f} has been withdrawn.")

    @staticmethod
    def error_insufficient_funds() -> None:
        """
        Display error for insufficient funds.
        """
        print(
            "Your bank account has insufficient funds. Please try again.\nEnter [q] to return to main page."
        )

    @staticmethod
    def error_invalid_action() -> None:
        """
        Display error for invalid action option.
        """
        print("Invalid option. Please try again.")

    @staticmethod
    def show_goodbye() -> None:
        """
        Display quit message.
        """
        print("Thank you for banking with AwesomeGIC Bank.")
        print("Have a nice day!")

    @staticmethod
    def error_negative_amount() -> None:
        """
        Display error for negative input amount.
        """
        print(
            "Your amount must be a positive number. Please try again.\nEnter [q] to return to main page."
        )

    @staticmethod
    def error_zero_amount() -> None:
        """
        Display error for zero amount.
        """
        print(
            "Your amount is too small. Please try again.\nEnter [q] to return to main page."
        )

    @staticmethod
    def error_rounding() -> None:
        """
        Display error for input rounding.
        """
        print(
            "Your amount should be rounded to the cent. Please try again.\nEnter [q] to return to main page."
        )

    @staticmethod
    def error_non_number() -> None:
        """
        Display error for non number input.
        """
        print("Invalid amount. Please try again.\nEnter [q] to return to main page.")
