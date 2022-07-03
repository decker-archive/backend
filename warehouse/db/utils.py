###############################################################################
# The contents of this file are subject to the Common Public Attribution
# License Version 1.0. (the "License"); you may not use this file except in
# compliance with the License. You may obtain a copy of the License at
# http://mozaku.com/assets/license. The License is based on the Mozilla Public
# License Version 1.1, but Sections 14 and 15 have been added to cover use of
# software over a computer network and provide for limited attribution for the
# Original Developer. In addition, Exhibit A has been modified to be consistent
# with Exhibit B.
#
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License for
# the specific language governing rights and limitations under the License.
#
# The Original Code is mozaku.
#
# The Original Developer is the Initial Developer.  The Initial Developer of
# the Original Code is Mozaku.
#
# All portions of the code written by mozaku are Copyright (c) 2021-2022 mozaku
# Inc. All Rights Reserved.
###############################################################################

import asyncio
import datetime

import bcrypt

from warehouse.lib.errors import InvalidVersion

VALID_VERSIONS = ['1']
BUCKET_SIZE = 1000 * 60 * 60 * 24 * 4


def get_date():
    return datetime.datetime.now(datetime.timezone.utc)


def get_bucket(obj: int):
    timestamp = obj >> 22
    return timestamp // BUCKET_SIZE


async def hashpass(pswd: str) -> str:
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(
        None, bcrypt.hashpw, pswd.encode(), bcrypt.gensalt(16)
    )
    return result.decode()


async def verifypass(pswd: str, hpswd: str) -> bool:
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(
        None, bcrypt.checkpw, pswd.encode(), hpswd.encode()
    )
    return result


def validate_version(version: str) -> None:
    if version not in VALID_VERSIONS:
        raise InvalidVersion()
