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

from warehouse.db import Guild as GuildDB
from warehouse.db import GuildFeature, GuildMember, get_date, snowflake_factory, BANNED_NAMES
from warehouse.lib.errors import (
    AlreadyMember,
    GuildAlreadyExists,
    GuildDoesNotExist,
    MemberIsMod,
    NotAMember,
)
from warehouse.lib.users import User
from typing import Optional


class Guild:
    def __init__(
        self,
        id: Optional[int] = None,
        name: Optional[str] = None,
        display_name: Optional[str] = '',
        description: Optional[str] = '',
        icon_url: Optional[str] = '',
        banner_url: Optional[str] = '',
        owner_id: Optional[int | User] = None,
        nsfw: bool = False,
        verified: Optional[bool] = None,
        permissions: int = 0,
        archived: bool = False

    ):
        self.exists = id != None

        self._id = id
        self._name = name
        self._display_name = display_name
        self._description = description
        self._icon_url = icon_url
        self._banner_url = banner_url
        self._nsfw = nsfw
        self._verified = verified
        self._permissions = permissions
        self._archived = archived
        self._owner = User.from_id(owner_id) if isinstance(owner_id, int) else owner_id
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

    @classmethod
    def from_name(cls, name: str):
        try:
            gdb: GuildDB = GuildDB.objects(GuildDB.name == name).get()
        except:
            raise GuildDoesNotExist()

        self = cls(
            id=gdb.id,
            name=gdb.name,
            display_name=gdb.display_name,
            description=gdb.description,
            icon_url=gdb.icon_url,
            banner_url=gdb.banner_url,
            nsfw=gdb.nsfw,
            verified=gdb.verified,
            owner_id=gdb.owner_id, # type: ignore
            archived=gdb.archived,
            permissions=gdb.permissions
        )
        self._db = gdb

        return self

    def for_transmission(self) -> dict:
        ret = {}

        ret['id'] = str(self._id)
        ret['name'] = self._name
        ret['display_name'] = self._display_name
        ret['description'] = self._description
        ret['icon_url'] = self._icon_url
        ret['banner_url'] = self._banner_url
        ret['nsfw'] = self._nsfw
        ret['verified'] = self._verified
        ret['owner'] = self._owner.for_transmission() # type: ignore
        ret['features'] = self._features

        if self._archived is None:
            ret['archived'] = False
        else:
            ret['archived'] = self._archived

        if self._permissions is None:
            ret['permissions'] = 0
        else:
            ret['permissions'] = self._permissions

        return ret

    def commit(self):
        """
        Commit this guild to the db
        """

        if self.exists:
            raise GuildAlreadyExists()

        if self._name in BANNED_NAMES:
            raise GuildAlreadyExists()

        try:
            GuildDB.objects(GuildDB.name == self._name).get()
        except:
            pass
        else:
            raise GuildAlreadyExists()

        self._db: GuildDB = GuildDB.create(
            id=snowflake_factory.manufacture(),
            name=self._name,
            display_name=self._display_name,
            description=self._description,
            icon_url=self._icon_url,
            banner_url=self._banner_url,
            nsfw=self._nsfw,
            verified=self._verified,
            owner_id=self._owner._id, # type: ignore
            permissions=self._permissions,
            archived=self._archived
        )

    def edit(
        self,
        display_name: Optional[str] = None,
        nsfw: Optional[bool] = None,
        description: Optional[str] = None,
    ):
        e = {}

        if display_name:
            self._display_name = display_name
            e['display_name'] = display_name

        if nsfw is not None:
            self._nsfw = nsfw
            e['nsfw'] = nsfw

        if description:
            self._description = description
            e['description'] = description

        self._db = self._db.update(**e)

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
            mod=False,
        )

    def remove_member(self, user: User):
        if not self.member_exists(user=user):
            raise NotAMember()

        member = self.get_member(user=user)

        if member.mod or member.owner:
            raise MemberIsMod()

        member.delete()

    def get_member(self, user: User):
        try:
            member: GuildMember = GuildMember.objects(
                GuildMember.user_id == user._id, GuildMember.guild_id == self._id
            ).get()
        except:
            raise NotAMember()

        return member
