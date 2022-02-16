from pydantic import BaseModel, Field, validator
from typing import Optional


class RegistrationModel(BaseModel):
    login: str
    password: str




class BaseUserModel(BaseModel):
    id: str
    login: str


class UserModel(BaseUserModel):
    id: str
    login: str
    bills: int
    balance: int
    password: str


class AuthUserModel(BaseModel):
    username: str
    password: str
