"""
Copyright (c) 2022 Mozaiku Inc. All Rights Reserved.
"""
from pydantic import BaseModel, Field

EMAIL_REGEX = r'r\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
USERNAME_REGEX = r'^(?=.{8,20}$)(?![_.])(?!.*[_.]{2})[a-zA-Z0-9._]+(?<![_.])$'
URL_REGEX = r'[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*'


class CreateUser(BaseModel):
    username: str = Field(max_length=30, regex=USERNAME_REGEX)
    email: str = Field(max_length=45, regex=EMAIL_REGEX)
    password: str


class EditUser(BaseModel):
    username: str | None = Field(max_length=30, regex=USERNAME_REGEX)
    email: str | None = Field(max_length=45, regex=EMAIL_REGEX)
    password: str | None
    avatar_url: str | None = Field(max_length=50, regex=URL_REGEX)
    banner_url: str | None = Field(max_length=50, regex=URL_REGEX)
    bio: str | None = Field(max_length=300)
