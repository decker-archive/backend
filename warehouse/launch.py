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
    InvalidCredentials,
    InvalidVersion,
    MemberIsMod,
    NotAMember,
    UserDoesNotExist,
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
# Code Values:
# 10000+: Invalid Data
# 20000+: Authorization Failed or Invalid, etc.
# 30000+: Server Errors
# 40000+: Not Found
# 50000+: User Errors


@app.exception_handler(AuthenticationError)
async def auth_error(*_):
    return ORJSONResponse(
        {'message': 'Authentication Failed', 'code': 20002},
        status_code=401,
        media_type='application/json',
    )


@app.exception_handler(GuildDoesNotExist)
async def guild_notfound(*_):
    return ORJSONResponse(
        {'message': 'Guild Not Found', 'code': 40002},
        status_code=404,
        media_type='application/json',
    )


@app.exception_handler(GuildAlreadyExists)
async def guild_exists(*_):
    return ORJSONResponse(
        {'message': 'This guild already exists', 'code': 10002},
        status_code=400,
        media_type='application/json',
    )


@app.exception_handler(MemberIsMod)
async def member_mod(*_):
    return ORJSONResponse(
        {'message': 'This member is a mod', 'code': 20001},
        status_code=403,
        media_type='application/json',
    )


@app.exception_handler(AlreadyMember)
async def alreadymember(*_):
    return ORJSONResponse(
        {'message': 'You have already joined this guild', 'code': 50004},
        status_code=400,
        media_type='application/json',
    )


@app.exception_handler(UserDoesNotExist)
async def user_notfound(*_):
    return ORJSONResponse(
        {'message': 'User not found', 'code': 40001},
        status_code=404,
        media_type='application/json',
    )


@app.exception_handler(AlreadyLoggedin)
async def already_loggedin(*_):
    return ORJSONResponse(
        {'message': 'You are already logged into another account', 'code': 50003},
        status_code=400,
        media_type='application/json',
    )


@app.exception_handler(NotAMember)
async def notamember(*_):
    return ORJSONResponse(
        {'message': 'This user is not a member', 'code': 10001},
        status_code=404,
        media_type='application/json',
    )


@app.exception_handler(InvalidCredentials)
async def invalid_creds(*_):
    return ORJSONResponse(
        {'message': 'Invalid username or password', 'code': 50002},
        status_code=403,
        media_type='application/json',
    )


@app.exception_handler(InvalidVersion)
async def invalid_version(*_):
    return ORJSONResponse(
        {'message': 'Invalid API Version', 'code': 50001},
        status_code=400,
        media_type='application/json',
    )


@app.exception_handler(404)
async def notfound(*_):
    return ORJSONResponse(
        {'message': 'Not Found', 'code': 0},
        status_code=404,
        media_type='application/json',
    )


@app.exception_handler(405)
async def invalid_method(*_):
    return ORJSONResponse(
        {'message': 'Invalid Method', 'code': 0},
        status_code=405,
        media_type='application/json',
    )
