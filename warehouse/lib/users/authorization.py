"""
Copyright (c) 2022 Mozaiku Inc. All Rights Reserved.
"""
import base64
import binascii

import itsdangerous

from warehouse.db import User
from warehouse.lib.errors import AuthenticationError


def create_token(user_id: int, user_password: str) -> str:
    signer = itsdangerous.TimestampSigner(user_password)
    user_id = str(user_id)  # type: ignore
    user_id = base64.b64encode(user_id.encode())  # type: ignore

    return signer.sign(user_id).decode()  # type: ignore


def verify_token(token: str):
    if token is None or not isinstance(token, str):
        raise AuthenticationError()

    fragmented = token.split('.')
    user_id = fragmented[0]

    try:
        user_id = base64.b64decode(user_id.encode())
        user_id = int(user_id)
    except (ValueError, binascii.Error):
        raise AuthenticationError()

    try:
        user: User = User.objects(User.id == user_id).get()
    except:
        raise AuthenticationError()

    signer = itsdangerous.TimestampSigner(user.password)

    try:
        signer.unsign(token)

        return user
    except (itsdangerous.BadSignature):
        raise AuthenticationError()
