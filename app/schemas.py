from typing import Optional, Literal
from pydantic import BaseModel, EmailStr, conint
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    model_config = {
        "from_attributes": True}
    

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class PostBase(BaseModel): 
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut



    model_config = {
        "from_attributes": True}
    

class PostOut(BaseModel):
    Post: Post
    votes: int 

    model_config = {
        "from_attributes": True}    


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None



class Vote(BaseModel):
    post_id:int
    dir: Literal[0, 1]