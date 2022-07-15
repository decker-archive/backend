"""
Polynode - Production Grade node for Derailed
Copyright (C) 2022 Derailed.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>. 
"""
from cassandra.cqlengine import columns, models


class User(models.Model):
    __table_name__ = 'users'
    id: int = columns.BigInt(primary_key=True, partition_key=True)
    email: str = columns.Text(index=True)
    password: str = columns.Text()
    username: str = columns.Text(index=True)
    discriminator: str = columns.Text()
    joined_at: str = columns.DateTime()
    avatar: str = columns.Text()
    banner: str = columns.Text()
    flags: int = columns.Integer()
    bio: str = columns.Text()
    verified: bool = columns.Boolean()


class GuildPosition(models.Model):
    user_id: int = columns.BigInt(primary_key=True)
    guild_id: int = columns.BigInt()
    group: str = columns.Text()
    square: int = columns.Integer()


class UserSettings(models.Model):
    user_id: int = columns.Integer(primary_key=True)
    locale: str = columns.Text()
    developer_mode: bool = columns.Boolean()
    theme: str = columns.Text(default='dark')
