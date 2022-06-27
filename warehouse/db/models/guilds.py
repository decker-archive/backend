"""
Copyright (c) 2022 Anavereum Inc. All Rights Reserved.
"""
from cassandra.cqlengine import columns, models


class Guild(models.Model):
    __table_name__ = 'guild'
    id: int = columns.BigInt(primary_key=True)
    name: str = columns.Text(index=True)
    description: str = columns.Text()
    icon_url: str = columns.Text()
    banner_url: str = columns.Text()
    owner_id: str = columns.Text(index=True)
    nsfw: bool = columns.Boolean()
    large: bool = columns.Boolean()
    permissions: int = columns.BigInt()
    splash_url: str = columns.Text()
    verified: bool = columns.Boolean()


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