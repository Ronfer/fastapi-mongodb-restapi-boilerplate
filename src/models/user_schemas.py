from ..utils import *
from pydantic import BaseModel, Field, EmailStr
from bson.objectid import ObjectId


class UserBase(BaseModel):
    email: EmailStr
    password: str


class CreateUser(UserBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "email": "example@gmail.com",
                "password": "example123",
            }
        }

class UserResponse(BaseModel):
    email: EmailStr