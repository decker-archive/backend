###############################################################################
# The contents of this file are subject to the Common Public Attribution
# License Version 1.0. (the "License"); you may not use this file except in
# compliance with the License. You may obtain a copy of the License at
# http://veneralab.com/assets/license. The License is based on the Mozilla Public
# License Version 1.1, but Sections 14 and 15 have been added to cover use of
# software over a computer network and provide for limited attribution for the
# Original Developer. In addition, Exhibit A has been modified to be consistent
# with Exhibit B.
#
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License for
# the specific language governing rights and limitations under the License.
#
# The Original Code is venera.
#
# The Original Developer is the Initial Developer.  The Initial Developer of
# the Original Code is venera Inc.
#
# All portions of the code written by venera are Copyright (c) 2021-2022 venera
# Inc. All Rights Reserved.
###############################################################################

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
