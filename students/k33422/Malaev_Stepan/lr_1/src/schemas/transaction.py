from . import base
from .. import enums

__all__ = [
    "TransactionCUDTO",
    "TransactionGetDTO",
]


class TransactionCUDTO(base.Base):
    amount: float
    transaction_type: enums.TransactionType


class TransactionGetDTO(base.Base):
    id: int
    amount: float
    transaction_type: enums.TransactionType
