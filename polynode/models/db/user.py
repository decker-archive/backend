"""
Polynode - Production Grade node for Derailed
Copyright (C) 2022 Derailed.
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
