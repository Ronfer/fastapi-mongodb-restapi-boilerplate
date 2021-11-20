import os

from fastapi import APIRouter, Depends, HTTPException, status #, Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from dotenv import load_dotenv
from typing import List
from ..models.user_schemas import *
from ..db import connect_to_database
from ..auth import AuthHandler


router = APIRouter(prefix="/users", tags=["Users"])
load_dotenv()
auth_handler = AuthHandler()
client = connect_to_database(os.environ.get("MONGO_URI"))


@router.post("/", response_description="Create new user", response_model=CreateUser)
async def create_user(user: CreateUser):
    """
    [summary]
    Create new user
    """
    hashed_pwd = auth_handler.get_password_hash(user.password)
    user.password = hashed_pwd
    
    user = jsonable_encoder(user)
    new_user = await client["users"]["users"].insert_one(user)
    return JSONResponse({"message": F"User {user['email']} created!"}, status_code=status.HTTP_201_CREATED)


@router.get("/{id}", response_description="Get user with id", response_model=UserResponse)
async def get_user(id: str):
    """
    [summary]
    Get user with id
    """
    if (user := await client["users"]["users"].find_one({"_id": id})) is not None:
        return user
    else:
        raise HTTPException(status_code=404, detail=f"User with id: {id} was not found")