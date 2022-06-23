"""
Copyright (c) 2022 Anavereum Inc. All Rights Reserved.
"""
from cassandra.cqlengine import columns, models

class Guild(models.Model):
    __table_name__ = 'guilds'
    id: int = columns.BigInt(primary_key=True)
    name: str = columns.Text()
    description: str = columns.Text()
    vanity_url: str = columns.Text(index=True)
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
    name: str = columns.Text()
