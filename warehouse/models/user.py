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

import random
from typing import Optional

from warehouse.db import hashpass, snowflake_factory, verifypass
from warehouse.db.models import User as UserDB
from warehouse.lib.errors import CommitError, UserAlreadyExists, UserDoesNotExist
from warehouse.lib.users.authorization import create_token, verify_token


class User:
    def __init__(
        self,
        version: int,
        id: Optional[int] = None,
        email: Optional[str] = None,
        password: Optional[str] = None,
        username: Optional[str] = None,
        discriminator: Optional[str] = None,
        joined_at: Optional[str] = None,
        avatar: Optional[str] = None,
        banner: Optional[str] = None,
        flags: Optional[int] = None,
        bio: Optional[str] = None,
        verified: bool = False,
        locale: Optional[str] = None,
    ):
        self._exists: bool = id != None

        self._id = id
        self._email = email
        self._password = password
        self._username = username
        self._discriminator = discriminator
        self._joined_at = joined_at
        self._avatar = avatar
        self._banner = banner
        self._flags = flags
        self._bio = bio
        self._verified = verified
        self._locale = locale
        self.version = version

    @classmethod
    async def login(cls, email: str, password: str, version: int):
        try:
            db: UserDB = UserDB.objects(UserDB.email == email).get()
        except:
            return

        if not await verifypass(password, db.password):
            return

        self = cls(
            version=version,
            id=db.id,
            email=db.email,
            password=db.password,
            username=db.username,
            discriminator=db.discriminator,
            joined_at=db.joined_at,
            avatar=db.avatar,
            banner=db.banner,
            flags=db.flags,
            bio=db.bio,
            verified=db.verified,
            locale=db.locale,
        )
        self._db = db

        return self

    @classmethod
    def from_username(cls, username: str, version: int):
        try:
            udb: UserDB = UserDB.objects(UserDB.username == username).get()
        except:
            raise UserDoesNotExist()

        self = cls(
            version=version,
            id=udb.id,
            email=udb.email,
            password=udb.password,
            username=udb.username,
            discriminator=udb.discriminator,
            joined_at=udb.joined_at,
            avatar=udb.avatar,
            banner=udb.banner,
            flags=udb.flags,
            bio=udb.bio,
            verified=udb.verified,
            locale=udb.locale,
        )
        self._db = udb

        return self

    @classmethod
    def from_id(cls, id: int, version: int):
        try:
            udb: UserDB = UserDB.objects(UserDB.id == id).get()
        except:
            raise UserDoesNotExist()

        self = cls(
            version=version,
            id=udb.id,
            email=udb.email,
            password=udb.password,
            username=udb.username,
            joined_at=udb.joined_at,
            avatar=udb.avatar,
            banner=udb.banner,
            flags=udb.flags,
            bio=udb.bio,
            verified=udb.verified,
            locale=udb.locale,
        )
        self._db = udb

        return self

    @classmethod
    def from_authorization(cls, token: str, version: int) -> "User":
        tokeninfo = verify_token(token=token)

        self = cls.from_id(tokeninfo.id, version=version)

        return self

    def create_token(self):
        return create_token(self._id)  # type: ignore

    async def commit(self):
        """
        Commit this user to the database.
        """
        if self._exists:
            raise CommitError('This user already exists.')

        self._password = await hashpass(self._password)  # type: ignore

        udb: UserDB = UserDB.create(
            id=snowflake_factory.manufacture(),
            email=self._email,
            password=self._password,
            discriminator=self._discriminator,
            username=self._username,
            joined_at=self._joined_at,
            avatar=self._avatar,
            banner=self._banner,
            flags=self._flags,
            bio=self._bio,
            verified=self._verified,
            locale=self._locale,
        )

        self._db = udb

        self._id = udb.id

    def commit_edit(
        self,
        email: Optional[str] = None,
        password: Optional[str] = None,
        username: Optional[str] = None,
        bio: Optional[str] = None,
    ):
        d: dict[str, str] = {}

        if email:
            d['email'] = email

        if username:
            d['username'] = username

        if bio:
            d['bio'] = bio

        if password:
            d['password'] = password

        self._db = self._db.update(**d)

        for k, v in d.keys():
            setattr(self, '_' + k, v)

    def for_transmission(self, remove_email: bool = True):
        dict_return = {}

        dict_return['id'] = str(self._id)
        dict_return['username'] = self._username
        dict_return['discriminator'] = self._discriminator
        dict_return['avatar'] = self._avatar
        dict_return['banner'] = self._banner
        if not remove_email:
            dict_return['email'] = self._email
        dict_return['joined_at'] = self._joined_at
        dict_return['bio'] = self._bio
        dict_return['verified'] = self._verified
        dict_return['locale'] = self._locale
        dict_return['flags'] = self._flags
        dict_return['_version'] = self.version

        return dict_return

    @classmethod
    def gendiscrim(self, username: str):
        discriminator: str | None = None

        for _ in range(600):
            try:
                discriminator: str | None = '%04d' % random.randint(0, 9999)
                User.user_exists(username, discriminator)
            except:
                pass

        if not discriminator:
            raise UserAlreadyExists()

        return discriminator
