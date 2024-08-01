# Banking System

A simple banking system application written in Python. This application allows users to perform basic banking operations such as depositing money, withdrawing money, and printing account statements.

## Features

- **Deposit**: Add a specified amount to the account balance.
- **Withdraw**: Subtract a specified amount from the account balance.
- **Print Statement**: Display a list of all transactions with dates, amounts, and balances.
- **Quit**: Exit the application.

## Assumptions
- The account starts with a balance of 0.
- User interactions are via command line input.
- No maximum limit on the amount that can be deposited or withdrawn in a single transaction.
- The system does not save the state of the account or transactions. All data is lost when the application is closed.

## Design
| File | Name | Description |
| --- | --- | --- |
| [`bank_account.py`](src/models/bank_account.py) | BankAccount | Handles the core functionalities of a bank account such as depositing, withdrawing, and maintaining the balance. |
| [`transaction.py`](src/models/transaction.py) | Transaction | Records individual transactions, including the amount and the timestamp. |
| [`controller.py`](src/service/controller.py) | BankApp | Manages the interaction between the user interface (CLI) and the BankAccount, handling user inputs and commands. |
| [`view.py`](src/service/view.py) | BankView | Manages the display of information to the user, such as prompts, responses, and account statements. |
| [`main.py`](src/main.py) | main() | Initializes the system and manages the main loop for user interactions. |

## Installation and Usage
### Option 1: With Docker (Recommended)
Using Docker will enable setting up a lightweight Python 3.10 environment and installing dependencies to a virtual environment.

Building the Docker image named "gic":
    ```docker build -t gic .
        ```

Running the app:
    ```docker run -it --rm gic
        ```

Running the tests:
    ```docker run -it --rm gic pytest
        ```

### Option 2: Without Docker
NOTE: Please ensure your python environment is 3.10 for this option.

Creating virtual environment: ```python -m venv venv```

Activate virtual environment: ```source venv/bin/activate```

Install requirements: ```pip install -r requirements.txt```

Running the app: ```python -m src.main```

Running the tests: ```pytest```
