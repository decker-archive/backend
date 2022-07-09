###############################################################################
# The contents of this file are subject to the Common Public Attribution
# License Version 1.0. (the "License"); you may not use this file except in
# compliance with the License. You may obtain a copy of the License at
# http://plufify.com/assets/license. The License is based on the Mozilla Public
# License Version 1.1, but Sections 14 and 15 have been added to cover use of
# software over a computer network and provide for limited attribution for the
# Original Developer. In addition, Exhibit A has been modified to be consistent
# with Exhibit B.
#
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License for
# the specific language governing rights and limitations under the License.
#
# The Original Code is plufify.
#
# The Original Developer is the Initial Developer.  The Initial Developer of
# the Original Code is Plufify.
#
# All portions of the code written by plufify are Copyright (c) 2021-2022 plufify
# Inc. All Rights Reserved.
###############################################################################

from typing import Optional

from fastapi import APIRouter, Header

from warehouse.db import get_date, hashpass, validate_version
from warehouse.lib.errors import AlreadyLoggedin, InvalidCredentials
from warehouse.lib.payloads import CreateUser, EditUser
from warehouse.models.user import User

users = APIRouter()


@users.post('/v{version}/users', status_code=201)
async def create_user(
    version: str,
    payload: CreateUser,
    authorization: Optional[str] = Header(),
):
    validate_version(version=version)

    if authorization:
        raise AlreadyLoggedin()

    user = User(
        version=int(version),
        email=payload.email,
        discriminator=User.gendiscrim(payload.username),
        password=payload.password,
        username=payload.username,
        joined_at=get_date(),  # type: ignore
        avatar_url='',
        banner_url='',
        flags=1,
        bio='',
        locale='en-US',
    )

    await user.commit()

    transmission = user.for_transmission(False)
    transmission['_token'] = user.create_token()

    return transmission


@users.post('/v{version}/users/login/', status_code=203, response_model=str)
async def login(
    version: str,
    email: str,
    password: str,
):
    validate_version(version=version)

    u = await User.login(email=email, password=password, version=int(version))

    if u is None:
        raise InvalidCredentials()

    return u.create_token()


@users.patch('/v{version}/users/@me')
def edit_user(version: str, payload: EditUser, authorization: str = Header()):
    validate_version(version=version)

    user = User.from_authorization(token=authorization, version=int(version))

    edited_content = {}

    if payload.username:
        edited_content['username'] = payload.username

    if payload.email:
        edited_content['email'] = payload.email

    if payload.password:
        edited_content['password'] = hashpass(payload.password)

    if payload.bio:
        edited_content['bio'] = payload.bio

    user.commit_edit(**edited_content)

    return user.for_transmission(False)


@users.get('/v{version}/users/@me')
def get_me(version: str, authorization: str = Header()):
    validate_version(version=version)

    me = User.from_authorization(authorization, version=version)

    return me.for_transmission(False)


@users.get('/v{version}/users/{id}')
def get_user(version: str, id: int, authorization: str = Header()):
    validate_version(version=version)

    User.from_authorization(authorization, version=version)

    user = User.from_id(id, version=version)

    return user.for_transmission()
