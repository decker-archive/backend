"""
Copyright (c) 2022 Mozaiku Inc. All Rights Reserved.
"""
from warehouse.db import Guild as GuildDB
from warehouse.db import GuildFeature, GuildMember, get_date, snowflake_factory
from warehouse.lib.errors import AlreadyMember, GuildAlreadyExists, NotAMember
from warehouse.lib.users import User


class Guild:
    def __init__(
        self,
        id: int | None = None,
        name: str | None = None,
        description: str | None = '',
        icon_url: str | None = '',
        banner_url: str | None = '',
        owner_id: int | None = None,
        nsfw: bool = False,
        permissions: int | None = None,
        verified: str | None = None,
    ):
        self.exists = id != None

        self._id = id
        self._name = name
        self._description = description
        self._icon_url = icon_url
        self._banner_url = banner_url
        self._nsfw = nsfw
        self._permissions = permissions
        self._verified = verified
        self._owner = User.from_id(owner_id)
        self._features = []

        if self.exists:
            iterg: list[GuildFeature] = GuildFeature.objects(
                GuildFeature.guild_id == self._id
            ).all()

            for feature in iterg:
                self._features.append(feature.name)

    def create_feature(self, name: str) -> None:
        GuildFeature.create(
            guild_id=self._id, name=name, feature_id=snowflake_factory.manufacture()
        )

    def commit(self):
        """
        Commit this guild to the db
        """

        if self.exists:
            raise GuildAlreadyExists()

        try:
            GuildDB.objects(GuildDB.name == self._name).get()
        except:
            pass
        else:
            raise GuildAlreadyExists()

        self._db = GuildDB.create(
            id=snowflake_factory.manufacture(),
            name=self._name,
            description=self._description,
            icon_url=self._icon_url,
            banner_url=self._banner_url,
            nsfw=self._nsfw,
            permissions=self._permissions,
            verified=self._verified,
            owner_id=self._owner._id,
        )

    def member_exists(self, user: User):
        try:
            GuildMember.objects(
                GuildMember.user_id == user._id, GuildMember.guild_id == self._id
            ).get()
        except:
            return False
        else:
            return True

    def add_member(self, user: User):
        if self.member_exists(user=user):
            raise AlreadyMember()

        GuildMember.create(
            user_id=user._id,
            guild_id=self._id,
            avatar_url='',
            banner_url='',
            joined_at=get_date(),
            nick='',
            owner=False,
        )

    def remove_member(self, user: User):
        if not self.member_exists(user=user):
            raise NotAMember()
