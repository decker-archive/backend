"""
Petabyte - Production-grade Database tools and models for Polynode

:copyright: 2021-2022 Derailed.
:license: LGPL-3.0
"""
from pydantic import BaseModel


class PartialUser(BaseModel):
    id: str
    username: str
    discriminator: str
    flags: int
    avatar: str


class User(PartialUser):
    banner: str
    bio: str
    bot: bool
    email: str = None
    password: str = None


class CreateUser(BaseModel):
    email: str
    password: str
    username: str
