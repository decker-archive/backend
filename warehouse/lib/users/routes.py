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

from fastapi import Response, Cookie, APIRouter

from warehouse.db import get_date, hashpass
from warehouse.lib.errors import AlreadyLoggedin, InvalidCredentials
from warehouse.lib.payloads import CreateUser, EditUser, Login
from warehouse.lib.users.basic import User
from typing import Optional

users = APIRouter()

@users.post('/api/users', status_code=201)
async def create_user(
    response: Response,
    payload: CreateUser,
    venera_authorization: Optional[str] = Cookie(default=None),
):
    if venera_authorization:
        raise AlreadyLoggedin()

    user = User(
        email=payload.email,
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
    response.set_cookie(
        'venera_authorization', user.create_token(), secure=True, httponly=True
    )

    return transmission

@users.get('/api/users/login/', status_code=203, response_model=str)
async def login(
    response: Response,
    email: str,
    password: str,
    venera_authorization: Optional[str] = Cookie(default=None),
):
    if venera_authorization:
        raise AlreadyLoggedin()

    u = await User.login(email=email, password=password)

    if u is None:
        raise InvalidCredentials()

    response.set_cookie(
        'venera_authorization', u.create_token(), secure=True, httponly=True
    )

    return ''

@users.get('/api/users/logout')
def logout(response: Response):
    try:
        response.delete_cookie('venera_authorization', secure=True, httponly=True)
    except:
        return {'success': False}
    else:
        return {'success': True}

@users.patch('/api/users/@me')
def edit_user(
    payload: EditUser, venera_authorization: str = Cookie(default=None)
):
    user = User.from_authorization(token=venera_authorization)

    edited_content = {}

    if payload.username:
        edited_content['username'] = payload.username

    if payload.email:
        edited_content['email'] = payload.email

    if payload.password:
        edited_content['password'] = hashpass(payload.password)

    if payload.avatar_url:
        edited_content['avatar_url'] = payload.avatar_url

    if payload.banner_url:
        edited_content['banner_url'] = payload.banner_url

    if payload.bio:
        edited_content['bio'] = payload.bio

    user.commit_edit(**edited_content)

    return user.for_transmission(False)

@users.get('/api/users/@me')
def get_me(venera_authorization: str = Cookie(default=None)):
    me = User.from_authorization(venera_authorization)

    return me.for_transmission()

@users.get('/api/users/{username}')
def get_user(username: str):
    user = User.from_username(username=username)

    return user.for_transmission()
