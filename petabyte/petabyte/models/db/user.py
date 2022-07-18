"""
Petabyte - Production-grade Database tools and models for Polynode

:copyright: 2021-2022 Derailed.
:license: LGPL-3.0
"""
from cassandra.cqlengine import columns, models

from petabyte.forge import forger


class User(models.Model):
    __table_name__ = 'users'
    id: int = columns.BigInt(primary_key=True, partition_key=True, default=forger.forge)
    email: str = columns.Text(index=True)
    password: str = columns.Text()
    username: str = columns.Text(index=True)
    discriminator: str = columns.Text()
    avatar: str = columns.Text(default='')
    banner: str = columns.Text(default='')
    flags: int = columns.Integer(default=0)
    bio: str = columns.Text(default='')
    bot: bool = columns.Boolean(default=False)


# NOTE: This is something like a bot
class Application(models.Model):
    __table_name__ = 'applications'
    id: int = columns.BigInt(primary_key=True)
    name: str = columns.Text()
    icon: str = columns.Text(default='')
    description: str = columns.Text(default='')
    public: bool = columns.Boolean(default=False)
    owner_id: int = columns.BigInt(index=True)
    team_id: int = columns.BigInt(index=True)


class GuildPosition(models.Model):
    __table_name__ = 'guild_positions'
    user_id: int = columns.BigInt(primary_key=True)
    guild_id: int = columns.BigInt()
    group_id: int = columns.BigInt()
    square: int = columns.Integer()


class UserSettings(models.Model):
    __table_name__ = 'user_settings'
    user_id: int = columns.BigInt(primary_key=True)
    locale: str = columns.Text()
    developer_mode: bool = columns.Boolean()
    theme: str = columns.Text(default='dark')


def transform_user(user: User | dict, keep_email: bool = False):
    data = user.__dict__ if not isinstance(user, dict) else user
    for k, v in data.items():
        if 'id' in k:
            data[k] = str(v)

    if data.get('password'):
        data.pop('password')

    if not keep_email:
        data.pop('email')

    return data
