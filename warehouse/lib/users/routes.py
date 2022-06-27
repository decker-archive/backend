"""
Copyright (c) 2022 Anavereum Inc. All Rights Reserved.
"""
from fastapi import Cookie, Header

from warehouse.db import get_date, hashpass
from warehouse.lib.payloads import CreateUser, EditUser
from warehouse.lib.users.basic import User


async def create_user(payload: CreateUser):
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
    transmission['_tk'] = user.create_token()

    return transmission


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


async def get_user(user_id: int, venera_authorization: str = Cookie(default=None)):
    User.from_authorization(token=venera_authorization)

    try:
        user = User.from_id(user_id)
    except:
        return {'err_code': 2, 'message': 'User does not exist'}

    return user.for_transmission()
