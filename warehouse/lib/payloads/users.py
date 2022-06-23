"""
Copyright (c) 2022 Anavereum Inc. All Rights Reserved.
"""
from pydantic import BaseModel, Field

NUMS = '1234567890'
NUMBER_REGEX = r'[0-9]+'
URL_REGEX = r'((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*'


class CreateUser(BaseModel):
    username: str = Field(
        max_length=30,
    )
    email: str = Field(
        max_length=45, regex=r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    )
    password: str


class EditUser(BaseModel):
    discriminator: str | None = Field(
        max_length=4,
        regex=NUMBER_REGEX
    )
    avatar_url: str | None = Field(max_length=50, regex=URL_REGEX)
    banner_url: str | None = Field(max_length=50, regex=URL_REGEX)


def valid_discriminator(d: str) -> bool:
    for l in d:
        if l not in NUMS:
            return False

    return True
