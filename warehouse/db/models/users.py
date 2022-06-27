"""
Copyright (c) 2022 Anavereum Inc. All Rights Reserved.
"""
from cassandra.cqlengine import columns, models


class User(models.Model):
    __table_name__ = 'users'
    id: int = columns.BigInt(primary_key=True, partition_key=True)
    email: str = columns.Text(index=True)
    password: str = columns.Text()
    display_name: str = columns.Text()
    username: str = columns.Text(index=True)
    joined_at: str = columns.DateTime()
    avatar_url: str = columns.Text()
    banner_url: str = columns.Text()
    flags: int = columns.Integer()
    bio: str = columns.Text()
    verified: bool = columns.Boolean()
    locale: str = columns.Text()
