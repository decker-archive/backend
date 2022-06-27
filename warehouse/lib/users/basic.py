"""
Copyright (c) 2022 Mozaiku Inc. All Rights Reserved.
"""
from warehouse.db import User as UserDB
from warehouse.db import hashpass, snowflake_factory
from warehouse.lib.errors import CommitError, UserAlreadyExists, UserDoesNotExist
from warehouse.lib.users.authorization import create_token, verify_token


class User:
    def __init__(
        self,
        id: int | None = None,
        email: str | None = None,
        password: str | None = None,
        username: str | None = None,
        joined_at: str | None = None,
        avatar_url: str | None = None,
        banner_url: str | None = None,
        flags: int | None = None,
        bio: str | None = None,
        verified: bool = False,
        locale: str | None = None,
    ):
        self._exists: bool = id != None

        self._id = id
        self._email = email
        self._password = password
        self._username = username
        self._joined_at = joined_at
        self._avatar_url = avatar_url
        self._banner_url = banner_url
        self._flags = flags
        self._bio = bio
        self._verified = verified
        self._locale = locale

    @classmethod
    def from_id(cls, id: int):
        try:
            udb: UserDB = UserDB.objects(UserDB.id == id).get()
        except:
            raise UserDoesNotExist()

        self = cls(
            id=udb.id,
            email=udb.email,
            password=udb.password,
            username=udb.username,
            joined_at=udb.joined_at,
            avatar_url=udb.avatar_url,
            banner_url=udb.banner_url,
            flags=udb.flags,
            bio=udb.bio,
            verified=udb.verified,
            locale=udb.locale,
        )
        self._db = udb

        return self

    @classmethod
    def user_exists(cls, username: str, discriminator: str) -> None:
        try:
            UserDB.objects(
                UserDB.username == username, UserDB.discriminator == discriminator
            ).get()
        except:
            raise UserAlreadyExists()

    @classmethod
    def from_authorization(cls, token: str) -> "User":
        user = verify_token(token=token)

        self = cls(
            id=user.id,
            email=user.email,
            password=user.password,
            username=user.username,
            discriminator=user.discriminator,
            joined_at=user.joined_at,
            avatar_url=user.avatar_url,
            banner_url=user.banner_url,
            flags=user.flags,
            bio=user.bio,
            verified=user.verified,
            locale=user.locale,
        )

        self._db = user

        return self

    def create_token(self):
        return create_token(self._id, self._password)  # type: ignore

    async def commit(self):
        """
        Commit this user to the database.
        """
        if self._exists:
            raise CommitError('This user already exists.')

        try:
            UserDB.objects(UserDB.username == self._username).get()
        except:
            pass
        else:
            raise UserAlreadyExists()

        self._password = await hashpass(self._password)  # type: ignore

        udb: UserDB = UserDB.create(
            id=snowflake_factory.manufacture(),
            email=self._email,
            password=self._password,  # type: ignore
            username=self._username,
            discriminator=self._discriminator,
            joined_at=self._joined_at,
            avatar_url=self._avatar_url,
            banner_url=self._banner_url,
            flags=self._flags,
            bio=self._bio,
            verified=self._verified,
            locale=self._locale,
        )

        self._db = udb

        self._id = udb.id

    def commit_edit(
        self,
        email: str | None = None,
        username: str | None = None,
        avatar_url: str | None = None,
        banner_url: str | None = None,
        bio: str | None = None,
    ):
        d: dict[str, str] = {}

        if email:
            d['email'] = email

        if username:
            d['username'] = username

        if avatar_url:
            d['avatar_url'] = avatar_url

        if banner_url:
            d['banner_url'] = banner_url

        if bio:
            d['bio'] = bio

        self._db = self._db.update(**d)

        for k, v in d.keys():
            setattr(self, '_' + k, v)

    def for_transmission(self, remove_email: bool = True):
        dict_return = {}

        dict_return['id'] = str(self._id)
        if not remove_email:
            dict_return['email'] = self._email
        dict_return['username'] = self._username
        dict_return['discriminator'] = self._discriminator
        dict_return['joined_at'] = self._joined_at
        dict_return['avatar_url'] = self._avatar_url
        dict_return['banner_url'] = self._banner_url
        dict_return['flags'] = self._flags
        dict_return['bio'] = self._bio
        dict_return['verified'] = self._verified
        dict_return['locale'] = self._verified

        return dict_return
