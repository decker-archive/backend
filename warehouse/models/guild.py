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
# the Original Code is Venera.
#
# All portions of the code written by venera are Copyright (c) 2021-2022 venera
# Inc. All Rights Reserved.
###############################################################################

from typing import Optional

from warehouse.db import Guild as GuildDB
from warehouse.db import GuildFeature, GuildMember, get_date, snowflake_factory
from warehouse.lib.errors import (
    AlreadyMember,
    GuildAlreadyExists,
    GuildDoesNotExist,
    MemberIsMod,
    NotAMember,
)
from warehouse.lib.users import User
from warehouse.models import Thing


class Guild(Thing):
    def __init__(
        self,
        version: int,
        id: Optional[int] = None,
        name: Optional[str] = None,
        description: Optional[str] = '',
        icon: Optional[str] = '',
        banner: Optional[str] = '',
        owner_id: Optional[int | User] = None,
        nsfw: bool = False,
        verified: Optional[bool] = False,
        permissions: int = 0,
    ):
        self._exists = id != None

        self._id = id
        self._name = name
        self._description = description
        self._icon = icon
        self._banner = banner
        self._nsfw = nsfw
        self._verified = verified
        self._permissions = permissions
        self._owner = User.from_id(owner_id) if isinstance(owner_id, int) else owner_id
        self._features = []
        self.version = version

        if self._exists:
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
    def from_id(cls, id: int, version: int):
        try:
            gdb: GuildDB = GuildDB.objects(GuildDB.id == id).get()
        except:
            raise GuildDoesNotExist()

        self = cls(
            version=version,
            id=gdb.id,
            name=gdb.name,
            description=gdb.description,
            icon=gdb.icon,
            banner=gdb.banner,
            nsfw=gdb.nsfw,
            verified=gdb.verified,
            owner_id=gdb.owner_id,  # type: ignore
            permissions=gdb.permissions,
        )
        self._db = gdb

        return self

    def for_transmission(self) -> dict:
        ret = {}

        ret['id'] = str(self._id)
        ret['name'] = self._name
        ret['description'] = self._description
        ret['icon'] = self._icon
        ret['banner'] = self._banner
        ret['nsfw'] = self._nsfw
        ret['verified'] = self._verified
        ret['owner'] = self._owner.for_transmission()  # type: ignore
        ret['features'] = self._features
        ret['_version'] = self.version

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

        try:
            GuildDB.objects(GuildDB.name == self._name).get()
        except:
            pass
        else:
            raise GuildAlreadyExists()

        self._db: GuildDB = GuildDB.create(
            id=snowflake_factory.manufacture(),
            name=self._name,
            description=self._description,
            icon=self._icon,
            banner=self._banner,
            nsfw=self._nsfw,
            verified=self._verified,
            owner_id=self._owner._id,  # type: ignore
            permissions=self._permissions,
        )

    def edit(
        self,
        name: Optional[str] = None,
        nsfw: Optional[bool] = None,
        description: Optional[str] = None,
    ):
        e = {}

        if name:
            self._name = name
            e['name'] = name

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
            mute=False,
            deaf=False,
            pending=False,
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
