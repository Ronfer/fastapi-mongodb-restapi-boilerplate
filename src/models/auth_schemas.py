from pydantic import BaseModel, Field, EmailStr
from bson.objectid import ObjectId
from typing import Optional
from ..utils import *


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


# class TokenData(BaseModel):
#     id: Optional[str] = None


