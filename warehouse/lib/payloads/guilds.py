"""
Copyright (c) 2022 Mozaiku Inc. All Rights Reserved.
"""
from pydantic import BaseModel, Field

from warehouse.lib.payloads.users import USERNAME_REGEX


class CreateGuild(BaseModel):
    name: str = Field(regex=USERNAME_REGEX)
    nsfw: bool = Field(default=False)
    description: str = Field(default='', max_length=400)


class EditGuild(BaseModel):
    display_name: str | None
    nsfw: bool | None
    description: str | None
