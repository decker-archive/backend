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

from cassandra.cqlengine import columns, models


class Guild(models.Model):
    __table_name__ = 'guild'
    id: int = columns.BigInt(primary_key=True)
    name: str = columns.Text()
    description: str = columns.Text()
    vanity_url: str = columns.Text(index=True)
    icon: str = columns.Text()
    banner: str = columns.Text()
    owner_id: str = columns.Text(index=True)
    nsfw: bool = columns.Boolean()
    permissions = columns.BigInt()
    verified: bool = columns.Boolean()
    created_at: str = columns.DateTime()


class GuildFeature(models.Model):
    __table_name__ = 'guild_features'
    guild_id: int = columns.BigInt(primary_key=True)
    feature_id: int = columns.BigInt()
    name: str = columns.Text()


class GuildMember(models.Model):
    __table_name__ = 'guild_members'
    user_id: int = columns.BigInt(primary_key=True)
    guild_id: int = columns.BigInt(primary_key=True)
    avatar_url: str = columns.Text()
    banner_url: str = columns.Text()
    joined_at: str = columns.DateTime()
    nick: str = columns.Text()
    owner: bool = columns.Boolean()
    mute: bool = columns.Boolean()
    deaf: bool = columns.Boolean()
    pending: bool = columns.Boolean()


class GuildMemberRole(models.Model):
    __table_name__ = 'guild_member_roles'
    user_id: int = columns.BigInt(primary_key=True, partition_key=True)
    guild_id: int = columns.BigInt(primary_key=True, partition_key=True)
    role_id: int = columns.BigInt()
