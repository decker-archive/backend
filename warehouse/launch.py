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

import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from warehouse.db import connect
from warehouse.lib import guilds, users
from warehouse.lib.errors import (
    AlreadyLoggedin,
    AlreadyMember,
    AuthenticationError,
    GuildAlreadyExists,
    GuildDoesNotExist,
    MemberIsMod,
    NotAMember,
    UserDoesNotExist,
    InvalidCredentials
)

load_dotenv()

debug = os.getenv('DEBUG')

app = FastAPI(
    debug=True if debug == 'true' else False,
    openapi_url=None,
    default_response_class=ORJSONResponse,
)

# Routes: users
app.include_router(users.users)

# Routes: guilds
app.include_router(guilds.guilds)

@app.on_event('startup')
async def on_startup():
    connect()

# Exception Handlers
@app.exception_handler(AuthenticationError)
async def auth_error(*_):
    return ORJSONResponse(
        {'erv': '401: Authentication Failed'},
        status_code=401,
        media_type='application/json',
    )


@app.exception_handler(GuildDoesNotExist)
async def guild_notfound(*_):
    return ORJSONResponse(
        {'erv': '404: Guild Not Found'}, status_code=404, media_type='application/json'
    )


@app.exception_handler(GuildAlreadyExists)
async def guild_exists(*_):
    return ORJSONResponse(
        {'erv': '400: This guild already exists'},
        status_code=400,
        media_type='application/json',
    )


@app.exception_handler(MemberIsMod)
async def member_mod(*_):
    return ORJSONResponse(
        {'erv': '403: This member is a mod'},
        status_code=403,
        media_type='application/json',
    )


@app.exception_handler(AlreadyMember)
async def alreadymember(*_):
    return ORJSONResponse(
        {'erv': '400: You have already joined this guild'},
        status_code=400,
        media_type='application/json',
    )


@app.exception_handler(UserDoesNotExist)
async def user_notfound(*_):
    return ORJSONResponse(
        {'erv': '404: User not found'}, status_code=404, media_type='application/json'
    )


@app.exception_handler(AlreadyLoggedin)
async def already_loggedin(*_):
    return ORJSONResponse(
        {'erv': '400: You are already logged into another account'},
        status_code=400,
        media_type='application/json',
    )


@app.exception_handler(NotAMember)
async def notamember(*_):
    return ORJSONResponse(
        {'erv': '404: This user is not a member'},
        status_code=404,
        media_type='application/json',
    )


@app.exception_handler(InvalidCredentials)
async def invalid_creds(*_):
    return ORJSONResponse(
        {'erv': '403: Invalid username or password'},
        status_code=403,
        media_type='application/json'
    )
