from enum import Enum

__all__ = ["TransactionType"]


class TransactionType(str, Enum):
    deposit = "deposit"
    withdraw = "withdraw"
