from src.service.view import BankView
from src.service.controller import BankApp
from src.models.bank_account import BankAccount

if __name__ == "__main__":
    account = BankAccount()
    view = BankView()
    BankApp(account, view).run()
