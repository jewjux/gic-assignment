# Banking System

A simple banking system application written in Python. This application allows users to perform basic banking operations such as depositing money, withdrawing money, and printing account statements.

## Features

- **Deposit**: Add a specified amount to the account balance.
- **Withdraw**: Subtract a specified amount from the account balance.
- **Print Statement**: Display a list of all transactions with dates, amounts, and balances.
- **Quit**: Exit the application.

## Installation and Usage
### Option 1: With Docker (Recommended)
Configured Dockerfile which:
1. Sets up a lightweight Python 3.10 environment with a virtual environment
2. Installs dependencies from a requirements file
3. Runs the specified Python module

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
Note: Please ensure your python environment is 3.10

Creating virtual environment: ```python -m venv venv```

Activate virtual environment: ```source venv/bin/activate```

Install requirements: ```pip install -r requirements.txt```

Running the app: ```python -m src.main```

Running the tests: ```pytest```
