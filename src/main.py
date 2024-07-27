# To enable running from within the file
import sys
from pathlib import Path
project_root = str(Path(__file__).resolve().parents[1])
sys.path.append(project_root)

from src.service.bank_service import bank_app
from src.models.bank_account import BankAccount

if __name__ == "__main__":
    account = BankAccount()
    bank_app(account)