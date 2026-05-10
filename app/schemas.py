from pydantic import BaseModel
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class QuestionCreate(BaseModel):
    title: str
    content: str

class QuestionResponse(BaseModel):
    id: int
    title: str
    content: str
    ai_answer: str | None
    status: str
    created_at: datetime

    class Config:
        from_attributes = True