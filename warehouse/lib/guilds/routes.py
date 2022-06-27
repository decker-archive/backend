"""
Copyright (c) 2022 Mozaiku Inc. All Rights Reserved.
"""
from fastapi import Cookie, Response, status

from warehouse.lib.guilds.basic import Guild
from warehouse.lib.payloads import CreateGuild, EditGuild
from warehouse.lib.users.basic import User


async def create_guild(
    payload: CreateGuild,
    resp: Response,
    venera_authorization: str = Cookie(default=None),
):
    owner = User.from_authorization(venera_authorization)

    g = Guild(
        name=payload.name,
        description=payload.description,
        owner_id=owner,
        nsfw=payload.nsfw,
    )

    try:
        g.commit()
    except:
        resp.status_code = status.HTTP_400_BAD_REQUEST
        return {'err': 'Guild Already Exists'}

async def edit_guild(
    guild_name: str,
    resp: Response,
    payload: EditGuild,
    venera_authorization: str = Cookie(default=None)
):
    user = User.from_authorization(venera_authorization)
    guild = Guild.from_name(guild_name)

    member = guild.get_member(user)

    if not member.mod and not member.owner:
        resp.status_code = status.HTTP_403_FORBIDDEN
        return {
            'err': 'Not a Moderator'
        }

    d = {}

    if payload.display_name:
        d['display_name'] = payload.display_name

    if payload.nsfw:
        d['nsfw'] = payload.nsfw

    if payload.description:
        d['description'] = payload.description

    guild.edit(
        **d
    )

    return guild.for_transmission()
