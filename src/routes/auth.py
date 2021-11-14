import os

from fastapi import APIRouter, Depends, HTTPException, status #, Response
from fastapi.responses import JSONResponse
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from dotenv import load_dotenv
from typing import List
from ..models.auth_schemas import *
from ..db import connect_to_database
from ..auth import AuthHandler


load_dotenv()

router = APIRouter(tags=["Authentication"])
client = connect_to_database(os.environ.get("MONGO_URI"))
auth_handler = AuthHandler()


@router.post('/login', response_description="Login", response_model=Token)
async def login(auth_details: UserLogin):
    
    #Find and match user email from the db
    user = await client["users"]["users"].find_one({"email": auth_details.email})

    #If not found from db show error
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credentials")
    
    #IF hashed passwords doesn't match show error
    if not auth_handler.verify_password(auth_details.password, user["password"]):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credentials")
    
    #create token and add user id to it
    access_token = auth_handler.create_access_token(user["_id"])

    # return { 'token': token }
    return {"access_token": access_token, "token_type": "bearer"}


#Test if the auth works (if token is valid you get message)
@router.get('/protected')
def protected(user_id=Depends(auth_handler.auth_wrapper)):
    return { "data": user_id}

