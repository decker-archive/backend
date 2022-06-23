"""
Copyright (c) 2022 Anavereum Inc. All Rights Reserved.
"""
from warehouse.db import User as UserDB
from warehouse.db import hashpass, snowflake_factory
from warehouse.lib.errors import CommitError, UserAlreadyExists
from warehouse.lib.users.authorization import create_token, verify_token


class User:
    def __init__(
        self,
        id: int | None = None,
        email: str | None = None,
        password: str | None = None,
        username: str | None = None,
        discriminator: str | None = None,
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
        self._discriminator = discriminator
        self._joined_at = joined_at
        self._avatar_url = avatar_url
        self._banner_url = banner_url
        self._flags = flags
        self._bio = bio
        self._verified = verified
        self._locale = locale

    @classmethod
    def user_exists(cls, username: str, discriminator: str) -> None:
        try:
            UserDB.objects(
                username=username,
                discriminator=discriminator
            ).get()
        except:
            raise UserAlreadyExists()

    @classmethod
    def from_authorization(cls, token: str) -> "User":
        user = verify_token(token=token)

        return cls(
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
            locale=user.locale
        )

    def create_token(self):
        return create_token(
            self._id,
            self._password
        )

    async def commit(self):
        """
        Commit this user to the database.
        """
        if self._exists:
            raise CommitError('This user already exists.')

        self._password = await hashpass(self._password)

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

        self._id = udb.id

    def for_transmission(self):
        dict_return = {}

        dict_return['id'] = str(self._id)
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
