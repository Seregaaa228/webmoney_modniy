from pydantic import BaseModel, Field, validator
from typing import Optional


class RegistrationBillModel(BaseModel):
    owner: str


class BillTransactionModel(BaseModel):
    sender: str
    receiver :str
    money: int


class BillModel(BaseModel):
    id: str
    owner: str
    balance: int
    status: int


class BaseBillModel(BaseModel):
    id: str
    balance: int
