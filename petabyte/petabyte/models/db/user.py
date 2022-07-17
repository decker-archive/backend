"""
Petabyte - Production-grade Database tools and models for Polynode
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
    bot: bool = columns.Boolean()


# NOTE: This is something like a bot
class Application(models.Model):
    __table_name__ = 'applications'
    id: int = columns.BigInt(primary_key=True)
    name: str = columns.Text()
    icon: str = columns.Text()
    description: str = columns.Text()
    public: bool = columns.Boolean()
    owner_id: int = columns.BigInt(index=True)
    team_id: int = columns.BigInt(index=True)
    token: str = columns.Text()


class GuildPosition(models.Model):
    __table_name__ = 'guild_positions'
    user_id: int = columns.BigInt(primary_key=True)
    guild_id: int = columns.BigInt()
    group_id: int = columns.BigInt()
    square: int = columns.Integer()


class UserSettings(models.Model):
    __table_name__ = 'user_settings'
    user_id: int = columns.Integer(primary_key=True)
    locale: str = columns.Text()
    developer_mode: bool = columns.Boolean()
    theme: str = columns.Text(default='dark')
