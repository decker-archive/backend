"""
Copyright (c) 2022 Mozaiku Inc. All Rights Reserved.
"""
from fastapi import Cookie, APIRouter

from warehouse.lib.errors import AuthenticationError
from warehouse.lib.guilds.basic import Guild
from warehouse.lib.payloads import CreateGuild, EditGuild
from warehouse.lib.users.basic import User

guilds = APIRouter()

@guilds.post('/api/guilds')
async def create_guild(
    payload: CreateGuild,
    venera_authorization: str = Cookie(default=None),
):
    owner = User.from_authorization(venera_authorization)

    g = Guild(
        name=payload.name,
        description=payload.description,
        owner_id=owner,
        nsfw=payload.nsfw,
    )

    g.commit()

@guilds.patch('/api/g/{guild_name}')
async def edit_guild(
    guild_name: str,
    payload: EditGuild,
    venera_authorization: str = Cookie(default=None),
):
    user = User.from_authorization(venera_authorization)
    guild = Guild.from_name(guild_name)

    member = guild.get_member(user)

    if not member.mod and not member.owner:
        raise AuthenticationError()

    d = {}

    if payload.display_name:
        d['display_name'] = payload.display_name

    if payload.nsfw:
        d['nsfw'] = payload.nsfw

    if payload.description:
        d['description'] = payload.description

    guild.edit(**d)

    return guild.for_transmission()

@guilds.get('/api/g/{guild_name}')
async def get_guild(
    guild_name: str
):
    guild = Guild.from_name(guild_name)

    return guild.for_transmission()
