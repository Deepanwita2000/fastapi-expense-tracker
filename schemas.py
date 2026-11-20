from pydantic import BaseModel, EmailStr, Field
from datetime import date
from decimal import Decimal
from typing import Optional

# from_attributes=True allows Pydantic to read values directly from SQLAlchemy ORM objects.
# USER SCHEMAS

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str = Field(min_length=8)


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    model_config = {"from_attributes": True}


# CATEGORY SCHEMAS

class CategoryCreate(BaseModel):
    name: str


class CategoryResponse(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}


# EXPENSE SCHEMAS

class ExpenseCreate(BaseModel):
    title: str = Field(min_length=1 , max_length=200)
    amount: Decimal = Field(gt=0, max_digits=10, decimal_places=2)
    description: Optional[str] = Field(default=None , max_length=500)
    expense_date: date
    category_id: int = Field(gt=0)






class ExpenseResponse(BaseModel):
    id: int
    title: str
    amount: Decimal
    description: Optional[str]
    expense_date: date
    user_id: int
    category_id: int

    model_config = {"from_attributes": True}




class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str




class ExpenseListResponse(BaseModel):
    total: int
    page: int
    limit: int
    total_pages: int
    expenses: list[ExpenseResponse]
