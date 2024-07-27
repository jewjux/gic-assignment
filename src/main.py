from utils.bank_app import bank_app
from .models.bank_account import BankAccount

if __name__ == "__main__":
    account = BankAccount()
    bank_app(account)