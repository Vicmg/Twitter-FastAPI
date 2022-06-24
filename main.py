#Python
from uuid import UUID
from datetime import date
from typing import Optional
# Pydantic
from pydantic import BaseModel,EmailStr,Field
# FastAPI
from fastapi import FastAPI

app = FastAPI()

# Models

class User(BaseModel):
    user_id: UUID = Field(...)
    email: EmailStr = Field(...)
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=20
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    brith_date: Optional[date] = Field(default=None)
class Tweet(BaseModel):
    pass

@app.get(path="/")
def home():
    return {"Twitter API":"Working!"}

