"""
Petabyte - Production-grade Database tools and models for Polynode

:copyright: 2021-2022 Derailed.
:license: LGPL-3.0
"""

import base64
import binascii
from functools import wraps
from typing import Callable

import itsdangerous
from flask import request

from .errors import PetabyteException
from .models.hadron import User


def remove_apps(func: Callable):
    @wraps(func)
    def inner(*args, **kwargs):
        if request.user.bot:
            raise PetabyteException(9, 'Applications cannot use this endpoint.', 403)

        return func(*args, **kwargs)

    return inner


def requires_authorization(func: Callable):
    @wraps(func)
    def inner(*args, **kwargs):
        # authorizes a request from a user.
        token = request.headers.get('Authorization', None)

        if token is None:
            raise PetabyteException(5, 'No Authorization Provided.', 401)

        fragmented = token.split('.')
        user_id = fragmented[0]

        try:
            user_id = base64.b64decode(user_id.encode())
            user_id = int(user_id)
        except (ValueError, binascii.Error):
            raise PetabyteException(6, 'Invalid Authorization Provided.', 401)

        try:
            user: User = User.select(user_id)
        except:
            raise PetabyteException(7, 'Invalid Authorization Provided.', 401)

        signer = itsdangerous.TimestampSigner(user.password)

        try:
            signer.unsign(token)
        except (itsdangerous.BadSignature):
            raise PetabyteException(
                8, 'Outdated or Invalid Authorization Provided.', 401
            )

        request.user = user
        request.user_token = token

        return func(user, *args, **kwargs)

    return inner
