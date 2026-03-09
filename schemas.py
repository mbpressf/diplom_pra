from datetime import date
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: EmailStr) -> str:
        return value.strip().lower()


class UserLogin(BaseModel):
    email: EmailStr
    password: str

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: EmailStr) -> str:
        return value.strip().lower()


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


class VaultUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=64)
    target_amount: Optional[float] = Field(default=None, ge=0)


class VaultTransfer(BaseModel):
    amount: float = Field(gt=0)


class VaultOut(BaseModel):
    id: int
    name: str
    balance: float
    target_amount: float
    net_balance: float
    available_to_spend: float
    progress_percent: float

    model_config = ConfigDict(from_attributes=True)
