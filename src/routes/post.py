import os

from fastapi import APIRouter, Depends, HTTPException, status #, Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from dotenv import load_dotenv
from typing import List
from ..models.post_schemas import *
from ..db import connect_to_database
from ..auth import AuthHandler


load_dotenv()

router = APIRouter(prefix="/posts", tags=["Posts"])
auth_handler = AuthHandler()
client = connect_to_database(os.environ.get("MONGO_URI"))


@router.post("/", response_description="Create new post", response_model=CreatePost)
async def create_post(post: CreatePost, user_id = Depends(auth_handler.auth_wrapper)):
    """
    [summary]
    Create post
    """
    post = jsonable_encoder(post)
    post["owner_id"] = user_id
    new_post = await client["posts"]["posts"].insert_one(post)
    return JSONResponse({"message": "Post created!"}, status_code=status.HTTP_201_CREATED)


@router.get("/", response_description="Get all posts", response_model=List[ResponsePost])
async def get_posts(user_id = Depends(auth_handler.auth_wrapper)):
    """
    [summary]
    Get all posts
    """
    # results = await client["posts"]["posts"].find().to_list(1000)
    results = await client["posts"]["posts"].find({"owner_id": user_id}).to_list(1000)
    return results


# @router.get("/{id}", response_description="Get single post", response_model=CreatePost)
# async def get_post(id: str):
#     """
#     [summary]
#     Get specific post with id
#     """
#     #keksi keino pysäyttää koodi jos id on liian pitkä tai lyhyt (24)
#     # if len(id) is not 24:
#     #     return {"data": "not valid id"}

#     # if (post := await db["posts"].find_one({"_id": ObjectId(id)})) is not None:
#     if (post := await client["posts"]["posts"].find_one({"_id": id})) is not None:
#         return post
#     else:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")


@router.get("/{id}", response_description="Get single post", response_model=ResponsePost)
async def get_post(id: str, user_id = Depends(auth_handler.auth_wrapper)):
    """
    [summary]
    Get specific post with id
    """
    if (check_post := await client["posts"]["posts"].find_one({"_id": id})) is not None:
        if check_post["owner_id"] != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    elif (check_post := await client["posts"]["posts"].find_one({"_id": id})) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {id} not found")
    # if (post := await db["posts"].find_one({"_id": ObjectId(id)})) is not None: # <-- Use this if id has ObjectId BSON format in the db
    if (single_post := await client["posts"]["posts"].find_one({"_id": id})) is not None:
        return single_post


# @router.put("/{id}", response_description="Update post")
# async def update_post(id: str, post: UpdatePost):
#     """
#     [summary]
#     Update post
#     """
#     post = {k: v for k, v in post.dict().items() if v is not None}
#     if len(post) < 1:
#         return JSONResponse({"error": "request is empty"}, status_code=status.HTTP_404_NOT_FOUND)
#     if len(post) >= 1:
#         update_post = await client["posts"]["posts"].update_one({"_id": id}, {"$set": post})
#         return JSONResponse({"message": "Post updated!"}, status_code=status.HTTP_201_CREATED)
    # Miksei toimi?
    # if post == None:
    #     raise HTTPException(status_code=404, detail=f"Post {id}  Changed in version 2.2: Added hint parameter.was not found")


@router.put("/{id}", response_description="Update post")
async def update_post(id: str, post: UpdatePost, user_id = Depends(auth_handler.auth_wrapper)):
    """
    Update post
    """
    post = {k: v for k, v in post.dict().items() if v is not None}
    
    if (check_post := await client["posts"]["posts"].find_one({"_id": id})) is not None:
        if check_post["owner_id"] != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    if (check_post := await client["posts"]["posts"].find_one({"_id": id})) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {id} not found")
    
    update = await client["posts"]["posts"].update_one({"_id": id}, {"$set": post})
    return JSONResponse({"message": "Post updated!"}, status_code=status.HTTP_201_CREATED)


# @router.delete('/{id}', response_description="Delete post")
# async def delete_post(id: str, user_id = Depends(auth_handler.auth_wrapper)):
#     """
#     Delete post
#     """
#     deleted_post: DeleteResult = await client["posts"]["posts"].delete_one({"_id": id})
#     if deleted_post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {id} not found")
#     return JSONResponse({"message": "Post deleted!"}, status_code=status.HTTP_204_NO_CONTENT)


@router.delete('/{id}', response_description="Delete post")
async def delete_post(id: str, user_id = Depends(auth_handler.auth_wrapper)):
    """
    Delete post
    """
    if (check_post := await client["posts"]["posts"].find_one({"_id": id})) is not None:
        if check_post["owner_id"] != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    elif (check_post := await client["posts"]["posts"].find_one({"_id": id})) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {id} not found")
    
    delete_post = await client["posts"]["posts"].delete_one({"_id": id})

    return JSONResponse({"message": "Post deleted!"}, status_code=status.HTTP_204_NO_CONTENT)