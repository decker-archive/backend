"""
Copyright (c) 2022 Mozaiku Inc. All Rights Reserved.
"""
from fastapi import Response, Cookie, APIRouter

from warehouse.db import get_date, hashpass
from warehouse.lib.errors import AlreadyLoggedin, InvalidCredentials
from warehouse.lib.payloads import CreateUser, EditUser, Login
from warehouse.lib.users.basic import User

users = APIRouter()

@users.post('/api/users', status_code=201)
async def create_user(
    response: Response,
    payload: CreateUser,
    venera_authorization: str | None = Cookie(default=None),
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
    venera_authorization: str | None = Cookie(default=None),
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
async def logout(response: Response):
    try:
        response.delete_cookie('venera_authorization', secure=True, httponly=True)
    except:
        return {'success': False}
    else:
        return {'success': True}

@users.patch('/api/users/@me')
async def edit_user(
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
async def get_user(username: str):
    user = User.from_username(username=username)

    return user.for_transmission()
