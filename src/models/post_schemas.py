# from bson.objectid import ObjectId
# from fastapi.params import Body
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional
from bson.objectid import ObjectId
from ..utils import *


class PostBase(BaseModel):
    title: str = Field(...)
    content: str = Field(...)
    published: bool = True
    rating: Optional[int] = None


class CreatePost(PostBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    owner_id: str = None
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "title": "example title",
                "content": "example content",
                "published": True,
                "rating": 5,
            }
        }


class UpdatePost(PostBase):
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "title": "example title",
                "content": "example content",
                "published": True,
                "rating": 5,
            }
        }


class ResponsePost(PostBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    owner_id: str = None
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


