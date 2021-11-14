from fastapi import FastAPI
from .routes import post, user, auth


app = FastAPI()
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)