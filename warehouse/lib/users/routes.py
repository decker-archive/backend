"""
Copyright (c) 2022 Anavereum Inc. All Rights Reserved.
"""
import random

from fastapi import Header

from warehouse.db import get_date
from warehouse.lib.payloads import CreateUser, EditUser
from warehouse.lib.users.basic import User


async def create_user(payload: CreateUser):
    discriminator: str | None = None

    for _ in range(600):
        try:
            discriminator: str | None = '%04d' % random.randint(0, 9999)
            User.user_exists(payload.username, discriminator)
        except:
            pass

    if not discriminator:
        return {
            'err_code': 1,
            'message': 'Username has been used too much, please try another one.',
        }

    user = User(
        email=payload.email,
        password=payload.password,
        username=payload.username,
        discriminator=discriminator,
        joined_at=get_date(),
        avatar_url='',
        banner_url='',
        flags=1,
        bio='',
        locale='en-US',
    )

    await user.commit()

    transmission = user.for_transmission()
    transmission['_tk'] = user.create_token()

    return transmission


async def edit_user(payload: EditUser, authorization: str = Header(default=None)):
    user = User.from_authorization(token=authorization)

    # TODO: Finish
