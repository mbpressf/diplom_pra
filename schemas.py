from datetime import date
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


class UserCreate(BaseModel):
    email: str
    password: str = Field(min_length=6, max_length=128)


class UserLogin(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    id: int
    email: str

    model_config = ConfigDict(from_attributes=True)


class CategoryBase(BaseModel):
    name: str = Field(min_length=1, max_length=64)
    color: str = Field(default="#10B981", min_length=4, max_length=16)


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=64)
    color: Optional[str] = Field(default=None, min_length=4, max_length=16)


class CategoryOut(CategoryBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class TransactionBase(BaseModel):
    amount: float = Field(gt=0)
    type: Literal["income", "expense"]
    category_id: int
    date: date
    description: str = Field(default="", max_length=255)


class TransactionCreate(TransactionBase):
    pass


class TransactionOut(TransactionBase):
    id: int
    category: CategoryOut

    model_config = ConfigDict(from_attributes=True)


class SummaryOut(BaseModel):
    total_income: float
    total_expense: float
    balance: float
    savings_rate: float


class CategoryAnalyticsItem(BaseModel):
    category: str
    color: str
    amount: float


class MonthAnalyticsItem(BaseModel):
    month: str
    income: float
    expense: float
