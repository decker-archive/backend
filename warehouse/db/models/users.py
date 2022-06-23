"""
Copyright (c) 2022 Anavereum Inc. All Rights Reserved.
"""
import datetime

from cassandra.cqlengine import columns, models


class User(models.Model):
    id: int = columns.BigInt(primary_key=True, partition_key=True)
    email: str = columns.Text(index=True)
    password: str = columns.Text()
    username: str = columns.Text(index=True)
    discriminator = columns.Text()
    joined_at: datetime.datetime | str = columns.DateTime()
    avatar_url: str = columns.Text()
    banner_url: str = columns.Text()
    flags: int = columns.Integer()
    bio: str = columns.Text()
    verified: bool = columns.Boolean()
    locale: str = columns.Text()
