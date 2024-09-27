import typing as tp
from datetime import datetime

from pydantic import model_validator

from . import base

__all__ = [
    "BudgetCUDTO",
    "BudgetGetDTO",
]


class BudgetCUDTO(base.Base):
    amount: float
    start_date: datetime
    end_date: datetime

    @model_validator(mode="after")
    def validate_after(self) -> tp.Self:
        if self.start_date >= self.end_date:
            raise ValueError("Start date must be before end date")
        return self


class BudgetGetDTO(base.Base):
    id: int
    amount: float
    start_date: datetime
    end_date: datetime
