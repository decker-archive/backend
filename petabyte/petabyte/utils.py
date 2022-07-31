"""
Petabyte - Production-grade Database tools and models for Polynode

:copyright: 2021-2022 Derailed.
:license: LGPL-3.0
"""
from functools import wraps
from typing import Any, Callable

from cassandra.cqlengine import models

from .errors import PetabyteException
from .models.db import (
    Channel,
    ChannelMention,
    Embed,
    EmbedAuthor,
    EmbedField,
    EmbedFooter,
    EmbedImage,
    EmbedProvider,
    EmbedThumbnail,
    EmbedVideo,
    Message,
    PermissionOverwrite,
    Reaction,
    RoleMention,
    User,
    UserMention,
)


def validate_version(func: Callable):
    @wraps(func)
    def inner(version: int, *args, **kwargs):
        if version not in ('v1'):
            raise PetabyteException(10, 'Invalid API version')

        return func(*args, **kwargs)

    return inner


def to_dict(model: models.Model, keep_email: bool = False) -> dict[str, Any]:
    initial: dict[str, Any] = model.items()
    data: dict[str, Any] = dict(initial)

    for k, v in data.items():
        if 'id' in k:
            data[k] = str(v)

    if isinstance(model, User):
        if data.get('password'):
            data.pop('password')

        if not keep_email:
            data.pop('email')

    if isinstance(model, Message):
        dict['author'] = to_dict(User.select(dict.pop('author_id')))

        embeds: list[Embed] = Embed.objects(Embed.message_id == model.id).all()
        ems = []
        mentions = get_mentions(message=model)
        dict['mentions'] = mentions

        reactions: list[Reaction] = Reaction.objects(
            Reaction.message_id == model.id
        ).limit(70000)
        dict['reactions'] = []

        for reaction in reactions:
            # TODO: change emoji_id to a partial Emoji object.
            d = to_dict(reaction)
            dict['reactions'].append(d)

        for embed in embeds:
            try:
                provider = EmbedProvider.objects(
                    EmbedProvider.embed_id == embed.embed_id
                ).get()
                provider = to_dict(provider)
            except:
                provider = None

            try:
                footer = EmbedFooter.objects(
                    EmbedFooter.embed_id == embed.embed_id
                ).get()
                footer = to_dict(footer)
            except:
                footer = None

            try:
                author = EmbedAuthor.objects(
                    EmbedAuthor.embed_id == embed.embed_id
                ).get()
                author = to_dict(author)
            except:
                author = None

            try:
                image = EmbedImage.objects(EmbedImage.embed_id == embed.embed_id).get()
                image = to_dict(image)
            except:
                image = None

            try:
                thumbnail = EmbedThumbnail.objects(
                    EmbedThumbnail.embed_id == embed.embed_id
                ).get()
                thumbnail = to_dict(thumbnail)
            except:
                thumbnail = None

            try:
                video = EmbedVideo.objects(EmbedVideo.embed_id == embed.embed_id).get()
                video = to_dict(video)
            except:
                video = None

            embed_dict = to_dict(embed)
            embed_dict['footer'] = footer
            embed_dict['image'] = image
            embed_dict['thumbnail'] = thumbnail
            embed_dict['video'] = video
            embed_dict['provider'] = provider
            embed_dict['author'] = author
            embed_dict['fields'] = []
            embed_fields = EmbedField.objects(
                EmbedField.embed_id == embed.embed_id
            ).all()

            for field in embed_fields:
                f = to_dict(field)
                embed_dict['fields'].append(f)

            ems.append(embed_dict)
    elif isinstance(model, Channel):
        if model.type in (0, 2, 4, 5, 6, 7, 8):
            perm_overwrites = PermissionOverwrite.objects(
                PermissionOverwrite.channel_id == model.id
            ).all()
            data['overwrites']: list[PermissionOverwrite] = []

            for overwrite in perm_overwrites:
                data['overwrites'].append(overwrite)

        if dict['type'] in (0, 1, 2, 3, 4, 5, 6, 7, 8):
            for value in ('member_count', 'application_id', 'icon', 'owner_id'):
                data.pop(value)

        if dict['type'] not in (2, 7):
            for value in ('bitrate', 'voice_region'):
                data.pop(value)

        if dict['type'] in (1, 3):
            for value in (
                'position',
                'nsfw',
                'permissions',
                'auto_archive_duration',
                'guild_id',
            ):
                data.pop(value)

        if dict['type'] not in (5, 6):
            for value in 'auto_archive_duration':
                data.pop(value)

    for name, value in initial:
        if (
            name == 'id'
            or 'id' in name
            and len(str(value)) > 14
            and name != 'message_id'
            and name != 'guild_id'
            and name != 'bucket_id'
            and name != 'channel_id'
            and name != 'embed_id'
            or name == 'permissions'
        ):
            data[name] = str(value)

        elif name == 'bucket_id':
            data.pop(name)

        elif name == 'message_id':
            if isinstance(
                model,
                (
                    Embed,
                    EmbedAuthor,
                    EmbedVideo,
                    EmbedProvider,
                    EmbedField,
                    EmbedThumbnail,
                    EmbedFooter,
                    EmbedImage,
                ),
            ):
                data.pop(name)
            else:
                data[name] = str(value)

        elif name == 'embed_id':
            data.pop(name)

    return data


def get_mentions(message: Message):
    user_mentions = UserMention.objects(UserMention.message_id == message.id).all()
    role_mentions = RoleMention.objects(RoleMention.message_id == message.id).all()
    channel_mentions = ChannelMention.objects(
        ChannelMention.message_id == message.id
    ).all()

    ret: dict[str, list[dict[str, Any]]] = {
        'users': [],
        'roles': [],
        'channels': [],
    }

    for mention in user_mentions:
        mention = to_dict(mention)
        ret['users'].append(mention)

    for mention in role_mentions:
        mention = to_dict(mention)
        ret['roles'].append(mention)

    for mention in channel_mentions:
        mention = to_dict(mention)
        ret['channels'].append(mention)

    return ret
