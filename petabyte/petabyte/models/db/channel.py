"""
Petabyte - Production-grade Database tools and models for Polynode
Copyright (C) 2022 Derailed.
"""
from cassandra.cqlengine import columns, models

from polynode.utils import transform_ids

CHANNEL_TYPES = {
    0: 'GUILD_TEXT_CHANNEL',
    1: 'DIRECT_MESSAGE',
    2: 'GUILD_VOICE_CHANNEL',
    3: 'GROUP_DIRECT_MESSAGE',
    4: 'GUILD_CATEGORY',
    5: 'GUILD_PUBLIC_THREAD',
    6: 'GUILD_PRIVATE_THREAD',
    7: 'GUILD_STAGE',
    8: 'GUILD_FORUM',
}


class Channel(models.Model):
    __table_name__ = 'channels'
    id: int = columns.BigInt(primary_key=True)
    guild_id: int = columns.BigInt()
    type: int = columns.Integer()
    position: int = columns.Integer()
    name: str = columns.Text()
    topic: str = columns.Text()
    nsfw: bool = columns.Boolean()
    last_message_id: int = columns.BigInt()
    bitrate: int = columns.Integer()
    user_limit: int = columns.Integer()
    rate_limit_per_user: int = columns.Integer()
    icon: str = columns.Text()
    owner_id: int = columns.BigInt()
    application_id: int = columns.BigInt()
    parent_id: int = columns.BigInt(index=True)
    last_pin_timestamp: str = columns.DateTime()
    voice_region: str = columns.Text()
    auto_archive_duration: int = columns.Integer()
    permissions: str = columns.Text()
    flags: int = columns.Integer()


class PermissionOverwrite(models.Model):
    __table_name__ = 'permission_overwrites'
    channel_id: int = columns.BigInt(primary_key=True)
    id: str = columns.Text()
    allow: str = columns.Text()
    deny: str = columns.Text()


def transform_channel(channel: Channel):
    dict = channel.__dict__
    dict.pop('guild_id')
    transform_ids(dict=dict)

    if dict['type'] in (0, 2, 4, 5, 6, 7, 8):
        perm_overwrites = PermissionOverwrite.objects(
            PermissionOverwrite.channel_id == channel.id
        ).all()
        dict['overwrites']: list[PermissionOverwrite] = []

        for overwrite in perm_overwrites:
            dict['overwrites'].append(overwrite)

    if dict['type'] in (0, 1, 2, 3, 4, 5, 6, 7, 8):
        for value in ('member_count', 'application_id', 'icon', 'owner_id'):
            dict.pop(value)

    if dict['type'] not in (2, 7):
        for value in ('bitrate', 'voice_region'):
            dict.pop(value)

    if dict['type'] in (1, 3):
        for value in (
            'position',
            'nsfw',
            'permissions',
            'auto_archive_duration',
            'guild_id',
        ):
            dict.pop(value)

    if dict['type'] not in (5, 6):
        for value in 'auto_archive_duration':
            dict.pop(value)

    return dict
