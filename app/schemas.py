from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

#################### USER ####################


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


#################### POST ####################


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    pass


class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse

    class Config:
        from_attributes = True


class PostVoteResponse(BaseModel):
    Post: PostResponse
    votes: int

    class Config:
        from_attributes = True


#################### VOTE ####################


class VoteBase(BaseModel):
    post_id: int
    # 1 for upvote, 0 for remove vote
    dir: int = Field(..., le=1, ge=0)


class VoteResponse(BaseModel):
    user_id: int
    post_id: int
    created_at: datetime

    class Config:
        from_attributes = True


#################### TOKEN ###################


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
