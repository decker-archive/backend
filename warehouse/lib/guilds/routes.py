###############################################################################
# The contents of this file are subject to the Common Public Attribution
# License Version 1.0. (the "License"); you may not use this file except in
# compliance with the License. You may obtain a copy of the License at
# http://onamii.com/assets/license. The License is based on the Mozilla Public
# License Version 1.1, but Sections 14 and 15 have been added to cover use of
# software over a computer network and provide for limited attribution for the
# Original Developer. In addition, Exhibit A has been modified to be consistent
# with Exhibit B.
#
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License for
# the specific language governing rights and limitations under the License.
#
# The Original Code is onamii.
#
# The Original Developer is the Initial Developer.  The Initial Developer of
# the Original Code is Onamii.
#
# All portions of the code written by onamii are Copyright (c) 2021-2022 onamii
# Inc. All Rights Reserved.
###############################################################################

from fastapi import APIRouter, Header

from warehouse.db.utils import validate_version
from warehouse.lib.errors import AuthenticationError
from warehouse.models.guild import Guild
from warehouse.lib.payloads import CreateGuild, EditGuild
from warehouse.models.user import User

guilds = APIRouter()


@guilds.post('/v{version}/guilds')
async def create_guild(
    version: str,
    payload: CreateGuild,
    authorization: str = Header(),
):
    validate_version(version=version)

    owner = User.from_authorization(authorization, int(version))

    g = Guild(
        int(version),
        name=payload.name,
        description=payload.description,
        owner_id=owner,
        nsfw=payload.nsfw,
    )

    g.commit()

    return g.for_transmission()


@guilds.patch('/v{version}/guilds/{guild_id}')
async def edit_guild(
    version: str, guild_id: int, payload: EditGuild, authorization: str = Header()
):
    validate_version(version=version)

    user = User.from_authorization(authorization, int(version))
    guild = Guild.from_id(guild_id, version=version)

    member = guild.get_member(user)

    # TODO: Permission handling
    if not member.owner:
        raise AuthenticationError()

    d = {}

    if payload.name:
        d['name'] = payload.name

    if payload.nsfw:
        d['nsfw'] = payload.nsfw

    if payload.description:
        d['description'] = payload.description

    guild.edit(**d)

    return guild.for_transmission()


@guilds.get('/v{version}/guilds/{guild_id}')
async def get_guild(version: str, guild_id: int, authorization: str = Header()):
    validate_version(version=version)
    user = User.from_authorization(authorization, version=version)

    guild = Guild.from_id(guild_id, int(version))

    guild.get_member(user)

    return guild.for_transmission()
