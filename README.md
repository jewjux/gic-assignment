# Banking System

A simple banking system application written in Python. This application allows users to perform basic banking operations such as depositing money, withdrawing money, and printing account statements.

## Features

- **Deposit**: Add a specified amount to the account balance.
- **Withdraw**: Subtract a specified amount from the account balance.
- **Print Statement**: Display a list of all transactions with dates, amounts, and balances.
- **Quit**: Exit the application.

## Installation
Building the Docker image (using Linux Ubuntu distribution):
    ```sh
        docker build -t my-linux-env .
        ```

Running a container using the Docker image:
    ```sh
        docker run -it my-linux-env /bin/bash
        ```

Create a virtual environment:
    ```sh
    python -m venv venv
    ```

Activate the virtual environment:
    ```sh
        source venv/bin/activate
        ```

Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

Run the application from the command line:
```sh
python -m src.main
