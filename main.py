# Python
import json
from uuid import UUID
from datetime import date
from datetime import datetime
from typing import Optional, List

# Pydantic
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field

# FastAPI
from fastapi import FastAPI
from fastapi import status
from fastapi import Body
from fastapi import Form

app = FastAPI()

# Models

class UserBase(BaseModel):
    user_id: UUID = Field(...)
    email: EmailStr = Field(..., example="victor@example.com")

class UserLogin(UserBase):
    password: str = Field(
        ...,
        min_length=8,
        max_length=20
    )

class User(UserBase):

    first_name: str = Field(
        ...,
        min_length=1,
        max_length=20,
        example = "Victor"
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example = "Martinez"
    )
    birth_date: Optional[date] = Field(default=None, exmaple=1995-6-17)

class UserRegister(User):
    password: str = Field(
        ...,
        min_length=8,
        max_length=20,
        exmaple= "holasoyVictor"
    )
class Tweet(BaseModel):
    tweet_id: UUID = Field(...)
    content: str = Field(
        ...,
        min_length=1,
        max_length=256
    )
    created_at: datetime = Field(default=datetime.now())
    updated_at: Optional[datetime] = Field(default=None)
    by: User = Field(...)

class LoginOut(BaseModel):
    email: EmailStr = Field(...)
    message: str = Field(default="Login Successfully!")

"""# Auxiliar funcion

## funcion reed
def read_data(file):
    with open("{}.json".format(file), "r+", encoding="utf-8") as f:
        return json.loads(f.read())

## funcion write
def read_data(file, results):
    with open("{}.json".format(file), "r+", encoding="utf-8") as f:
        f.seek(0)
        f.write(json.dumps(results))"""

# !Path  Operations

## Users
# * Register User
@app.post(
    path="/signup",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="Register a User",
    tags=["Users"]
)

def signup(user: UserRegister = Body(...)):
    """
    Signup

    This path operations register a user in the app.

    Parameters:
        - Request body parameter
            - user: UserRegister

    Returns a json with the basic user information:
        - user_id: UUID
        - email: Emailstr
        - first_name: str
        - last:_name: str
        - birth_date: datetime
    """
    with open("users.json", "r+", encoding="utf-8") as f:
        results = json.loads(f.read())
        user_dict = user.dict()
        user_dict["user_id"] = str(user_dict["user_id"])
        user_dict["birth_date"] = str(user_dict["birth_date"])
        results.append(user_dict)
        f.seek(0)
        f.write(json.dumps(results))
        return user

# * Login a user
@app.post(
    path="/login",
    response_model=LoginOut,
    status_code=status.HTTP_200_OK,
    summary="Login a User",
    tags=["Users"]
)

def login(
    email: EmailStr = Form(...),
    password: str = Form(...)):
    """
    Login

    This path operation login a Personin the app

    Parameters:
    - Request body parametrs:
        - email: Emailstr
        - password: str

    Returns LoginOut model with username and message and
    """

    with open("users.json", "r+", encoding="utf-8") as f:
        datos = json.loads(f.read())
        for user in datos:
            if email == user['email'] and password == user['password']:
                return LoginOut(email=email)
            else:
                return LoginOut(email=email, message="Login Unsuccessfully!")


# * Show all users
@app.get(
    path="/users",
    response_model=List[User],
    status_code=status.HTTP_200_OK,
    summary="Show all users",
    tags=["Users"]
)

def show_all_users():
    """
    Get Users

    This path operation shows all users created in the app

    Parameters: None

    Returns a list with the basic user information of all users created in the app:
    - user_id: UUID
    - email: Emailstr
    - first_name: str
    - last_name: str
    - birth_date: datetime
    """
    with open("users.json", "r", encoding="utf-8") as f:
        results = json.loads(f.read())
        return results

# *Show a user
@app.get(
    path="/signup{user_id}",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Show a user",
    tags=["Users"]
)

def show_a_user():
    pass

# * Delete a user
@app.delete(
    path="/users/{user_id}/delete",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Delete a User",
    tags=["Users"]
)

def delete_a_user():
    pass

# *Actualizar usuario
@app.put(
    path="/users/{user_id}/update",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Update a User",
    tags=["Users"]
)

def update_a_user():
    pass

## Tweets

# *Show all tweets
@app.get(
    path="/",
    response_model=List[Tweet],
    status_code=status.HTTP_200_OK,
    summary="Show all Tweets",
    tags=["Tweets"]
    )

def home():
    """
    Get Users

    This path operation shows all tweets created in the app

    Parameters: None

    Returns a json list with all tweets in the app, with the following keys:
    - tweet_id: UUID
    - content: str
    - created_at: datetime
    - updated_at: Optional[datetime]
    - by: User
    """
    with open("tweets.json", "r", encoding="utf-8") as f:
        results = json.loads(f.read())
        return results

# *Post tweet
@app.post(
    path="/post",
    response_model=Tweet,
    status_code=status.HTTP_201_CREATED,
    summary="Post a tweet",
    tags=["Tweets"]
)

def post(tweet: Tweet = Body(...)):
    """
    Post a Tweet

    This path operation post a Tweet in the app

    Parameters:
    - Request Body parameter
        - tweet: Tweet

    Returns a JSON with the basic tweet information:
    - tweet_id: UUID
    - content: str
    - created_at: datetime
    - updated_at: Optional[datetime]
    - by: User
    """
    with open("tweets.json", "r+", encoding="utf-8") as f:
        results = json.loads(f.read())
        tweet_dict = tweet.dict()
        tweet_dict["tweet_id"] = str(tweet_dict["tweet_id"])
        tweet_dict["created_at"] = str(tweet_dict["created_at"])
        tweet_dict["updated_at"] = str(tweet_dict["updated_at"])
        tweet_dict["by"]["user_id"] = str(tweet_dict["by"]["user_id"])
        tweet_dict["by"]["birth_date"] = str(tweet_dict["by"]["birth_date"])

        results.append(tweet_dict)
        f.seek(0)
        f.write(json.dumps(results))
        return tweet

# *Show a tweet
@app.get(
    path="/post/{tweet_id}",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Show a Tweet",
    tags=["Tweets"]
)

def show_a_tweet():
    pass

# *Delete a tweet
@app.delete(
    path="/tweet/{tweet_id}/delete",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Delete a Tweet",
    tags=["Tweets"]
)

def delete_a_tweet():
    pass

# *Update a tweet
@app.put(
    path="/tweet/{tweet_id}/update",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="update a Tweet",
    tags=["Tweets"]
)

def update_a_tweet():
    pass