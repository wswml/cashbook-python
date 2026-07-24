"""Pydantic 数据验证模型"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class UserCreate(BaseModel):
    username: str
    password: str
    name: Optional[str] = None
    email: Optional[str] = None


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    name: Optional[str] = None
    email: Optional[str] = None
    create_date: datetime

    class Config:
        from_attributes = True


class BookCreate(BaseModel):
    book_name: str
    budget: Optional[float] = 0


class BookResponse(BaseModel):
    id: int
    book_id: str
    book_name: str
    share_key: Optional[str] = None
    user_id: int
    budget: Optional[float] = None
    create_date: datetime

    class Config:
        from_attributes = True


class BookMemberResponse(BaseModel):
    user_id: int
    role: str
    joined_at: datetime
    name: Optional[str] = None

    class Config:
        from_attributes = True


class FlowCreate(BaseModel):
    book_id: str
    day: str
    flow_type: Optional[str] = "支出"
    industry_type: Optional[str] = None
    pay_type: Optional[str] = None
    money: Optional[float] = 0
    name: Optional[str] = None
    description: Optional[str] = None
    attribution: Optional[str] = None


class FlowResponse(BaseModel):
    id: int
    user_id: int
    book_id: str
    day: str
    flow_type: Optional[str] = None
    industry_type: Optional[str] = None
    pay_type: Optional[str] = None
    money: Optional[float] = None
    name: Optional[str] = None
    description: Optional[str] = None
    invoice: Optional[str] = None
    origin: Optional[str] = None
    attribution: Optional[str] = None
    eliminate: Optional[int] = 0

    class Config:
        from_attributes = True


class BudgetCreate(BaseModel):
    book_id: str
    month: str
    budget: float


class ShareKeyCreate(BaseModel):
    id: int


class ShareKeyJoin(BaseModel):
    key: str


class MemberRemove(BaseModel):
    book_id: str
    target_user_id: int


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[int] = None
