from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.params import Body
from . import models
from . database import engine
from . routers import post, user, auth, vote
from .config import settings


# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins =["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Welcome to FastAPI!!!!1"}



# def find_post(id):
#     for p in my_posts:
#         if p["id"] == id:
#             return p
        

# def find_index_post(id):
#     for index, post in enumerate(my_posts):
#         if post["id"] == id:
#             return index

app.include_router(post.router)

app.include_router(user.router)

app.include_router(auth.router)

app.include_router(vote.router)