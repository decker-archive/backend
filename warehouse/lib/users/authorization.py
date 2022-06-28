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

import base64
import binascii

import itsdangerous

from warehouse.db import User
from warehouse.lib.errors import AuthenticationError


def create_token(user_id: int, user_password: str) -> str:
    signer = itsdangerous.TimestampSigner(user_password)
    string_user_id = str(user_id)
    encoded_user_id = base64.b64encode(string_user_id.encode())

    return signer.sign(encoded_user_id).decode()


def verify_token(token: str):
    if token is None or not isinstance(token, str):
        raise AuthenticationError()

    fragmented = token.split('.')
    encoded_user_id = fragmented[0]

    try:
        decoded_user_id = base64.b64decode(encoded_user_id.encode())
        user_id = int(decoded_user_id)
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
