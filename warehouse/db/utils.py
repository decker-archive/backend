"""
Copyright (c) 2022 Mozaiku Inc. All Rights Reserved.
"""
import asyncio
import datetime

import bcrypt

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
    result = await loop.run_in_executor(None, bcrypt.checkpw, pswd.encode(), hpswd.encode())
    return result

BANNED_NAMES = [
   'create',
   'delete',
   'blog',
   'wiki',
   'support',
	'venera',
	'moderators',
	'place',
	'changelog'
]
