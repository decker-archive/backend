"""
Copyright (c) 2022 Mozaiku Inc. All Rights Reserved.
"""
from pydantic import BaseModel, Field, EmailStr

USERNAME_REGEX = r'^(?=.{3,21}$)(?![_.])(?!.*[_.]{2})[a-zA-Z0-9._]+(?<![_.])$'
URL_REGEX = r'[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*'


class Login(BaseModel):
    email: EmailStr
    password: str


class CreateUser(BaseModel):
    username: str = Field(max_length=30, regex=USERNAME_REGEX)
    email: EmailStr
    password: str


class EditUser(BaseModel):
    username: str | None = Field(max_length=30, regex=USERNAME_REGEX)
    email: EmailStr | None
    password: str | None
    avatar_url: str | None = Field(max_length=50, regex=URL_REGEX)
    banner_url: str | None = Field(max_length=50, regex=URL_REGEX)
    bio: str | None = Field(max_length=300)
