import pytest
from ..utils import (add,
                    subtract,
                    multiply,
                    divide,
                    BankAccount)

@pytest.fixture
def empty_bank_account():
    return BankAccount(0)

@pytest.mark.parametrize("num1, num2, expected", [
    (1,6,7),
    (5,5,10),
    (42,44,86)
])
def test_add(num1, num2, expected):
    assert add(num1, num2) == expected


def test_subtract():
    assert subtract(9, 4) == 5


def test_multiply():
    assert multiply(4, 3) == 12


def test_divde():
    assert divide(20, 5) == 4


def test_bank_initial_amount():
    bank_account = BankAccount(100)
    assert bank_account.balance == 100

def test_bank_zero_balance(empty_bank_account):
    assert empty_bank_account.balance == 0


# @pytest.mark.parametrize("deposited, withdrew, expected", [
#     (200, 100, 100),
#     (50, 10, 40),
#     (1200, 200, 1000)
# ])
# def test_bank_transaction(empty_bank_account, deposited, withdrew, expected):
#     empty_bank_account.deposit(deposited)
#     empty_bank_account.withdraw(withdrew)
#     assert empty_bank_account.balance == expected