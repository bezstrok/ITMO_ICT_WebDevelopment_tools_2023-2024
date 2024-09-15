from . import base

__all__ = [
    "CategoryToTransactionDTO",
]


class CategoryToTransactionDTO(base.Base):
    category_id: int
    transaction_id: int
