from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
from .routes import post, user, auth

# allowed_urls = ["*"]
# allowed_urls = ["https://www.google.com"]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=allowed_urls,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

app = FastAPI()
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)