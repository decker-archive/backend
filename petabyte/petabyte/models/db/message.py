"""
Petabyte - Production-grade Database tools and models for Polynode
Copyright (C) 2022 Derailed.
"""
from typing import Any

from cassandra.cqlengine import columns, models

from polynode.utils import transform_ids


class Message(models.Model):
    __table_name__ = 'messages'
    id: int = columns.BigInt(primary_key=True)
    channel_id: int = columns.BigInt(primary_key=True)
    bucket_id: int = columns.Integer(primary_key=True)
    author_id: int = columns.BigInt()
    content: str = columns.Text()
    timestamp: str = columns.DateTime()
    edited_timestamp: str = columns.DateTime()
    mention_everyone: bool = columns.Boolean()
    pinned: bool = columns.Boolean()
    referenced_message_id = columns.BigInt()
    thread_id: int = columns.BigInt()


class Attachment(models.Model):
    __table_name__ = 'attachments'
    id: int = columns.BigInt(primary_key=True)
    filename: str = columns.Text()
    description: str = columns.Text()
    content_type: str = columns.Text()
    size: int = columns.Integer()
    url: str = columns.Text()
    proxy_url: str = columns.Text()
    height: int = columns.Integer()
    width: int = columns.Integer()
    ephemeral: int = columns.Integer()


class Embed(models.Model):
    __table_name__ = 'embeds'
    message_id: int = columns.BigInt(primary_key=True)
    embed_id: int = columns.BigInt()
    title: str = columns.Text()
    type: str = columns.Text()
    description: str = columns.Text()
    url: str = columns.Text()
    timestamp: str = columns.DateTime()
    color: int = columns.Integer()


class EmbedProvider(models.Model):
    __table_name__ = 'embed_providers'
    embed_id: int = columns.BigInt(primary_key=True)
    name: str = columns.Text()
    url: str = columns.Text()


class EmbedFooter(models.Model):
    __table_name__ = 'embed_footers'
    embed_id: int = columns.BigInt(primary_key=True)
    text: str = columns.Text()
    icon_url: str = columns.Text()
    proxy_icon_url: str = columns.Text()


class EmbedField(models.Model):
    __table_name__ = 'embed_fields'
    embed_id: int = columns.BigInt(primary_key=True)
    name: str = columns.Text()
    value: str = columns.Text()
    inline: bool = columns.Boolean()


class EmbedAuthor(models.Model):
    __table_name__ = 'embed_author'
    embed_id: int = columns.BigInt(primary_key=True)
    name: str = columns.Text()
    url: str = columns.Text()
    icon_url: str = columns.Text()
    proxy_icon_url: str = columns.Text()


class EmbedImage(models.Model):
    __table_name__ = 'embed_images'
    embed_id: int = columns.BigInt(primary_key=True)
    url: str = columns.Text()
    proxy_url: str = columns.Text()
    height: int = columns.Integer()
    width: int = columns.Integer()


class EmbedVideo(models.Model):
    __table_name__ = 'embed_videos'
    embed_id: int = columns.BigInt(primary_key=True)
    url: str = columns.Text()
    proxy_url: str = columns.Text()
    height: int = columns.Integer()
    width: int = columns.Integer()


class EmbedThumbnail(models.Model):
    __table_name__ = 'embed_thumbnails'
    embed_id: int = columns.BigInt(primary_key=True)
    url: str = columns.Text()
    proxy_url: str = columns.Text()
    height: int = columns.Integer()
    width: int = columns.Integer()


class Reaction(models.Model):
    __table_name__ = 'reactions'
    message_id: int = columns.BigInt(primary_key=True)
    user_id: int = columns.BigInt()
    emoji_id: int = columns.BigInt()


class UserMention(models.Model):
    __table_name__ = 'user_mentions'
    message_id: int = columns.BigInt(primary_key=True)
    user_id: int = columns.BigInt()


class RoleMention(models.Model):
    __table_name__ = 'role_mentions'
    message_id: int = columns.BigInt(primary_key=True)
    role_id: int = columns.BigInt()


class ChannelMention(models.Model):
    __table_name__ = 'channel_mentions'
    message_id: int = columns.BigInt(primary_key=True)
    id: int = columns.BigInt()
    guild_id: int = columns.BigInt()
    type: int = columns.Integer()
    name: str = columns.Text()


def transform_embed_fields(embed: Embed):
    embed_fields = EmbedField.objects(EmbedField.embed_id == embed.embed_id).all()
    ret = []

    for field in embed_fields:
        f = dict(field)
        f.pop('embed_id')
        ret.append()

    return ret


def get_mentions(message: Message):
    user_mentions = UserMention.objects(UserMention.message_id == message.id).all()
    role_mentions = RoleMention.objects(RoleMention.message_id == message.id).all()
    channel_mentions = ChannelMention.objects(
        ChannelMention.message_id == message.id
    ).all()

    ret: dict[str, list[dict[str, Any]]] = {}
    ret['users'] = []
    ret['roles'] = []
    ret['channels'] = []

    for mention in user_mentions:
        mention = dict(mention)
        mention.pop('message_id')
        ret['users'].append(mention)

    for mention in role_mentions:
        mention = dict(mention)
        mention.pop('message_id')
        ret['roles'].append(mention)

    for mention in channel_mentions:
        mention = dict(mention)
        mention.pop('message_id')
        ret['channels'].append(mention)

    return ret


def transform_message(message: Message):
    dict = message.__dict__
    transform_ids(dict=dict)

    embeds: list[Embed] = Embed.objects(Embed.message_id == message.id).all()
    ems = []
    mentions = get_mentions(message=message)
    dict['mentions'] = mentions

    reactions: list[Reaction] = Reaction.objects(
        Reaction.message_id == message.id
    ).limit(70000)
    dict['reactions'] = []

    for reaction in reactions:
        # TODO: change emoji_id to a partial Emoji object.
        d = dict(reaction)
        d.pop('message_id')
        dict['reactions'].append(d)

    for embed in embeds:
        try:
            provider = EmbedProvider.objects(
                EmbedProvider.embed_id == embed.embed_id
            ).get()
            provider = dict(provider)
            provider.pop('embed_id')
        except:
            provider = None

        try:
            footer = EmbedFooter.objects(EmbedFooter.embed_id == embed.embed_id).get()
            footer = dict(footer)
            footer.pop('embed_id')
        except:
            footer = None

        try:
            author = EmbedAuthor.objects(EmbedAuthor.embed_id == embed.embed_id).get()
            author = dict(author)
            author.pop('embed_id')
        except:
            author = None

        try:
            image = EmbedImage.objects(EmbedImage.embed_id == embed.embed_id).get()
            image = dict(image)
            image.pop('embed_id')
        except:
            image = None

        try:
            thumbnail = EmbedThumbnail.objects(
                EmbedThumbnail.embed_id == embed.embed_id
            ).get()
            thumbnail = dict(thumbnail)
            thumbnail.pop('embed_id')
        except:
            thumbnail = None

        try:
            video = EmbedVideo.objects(EmbedVideo.embed_id == embed.embed_id).get()
            video = dict(video)
            video.pop('embed_id')
        except:
            video = None

        embed_dict = embed.__dict__
        embed_dict['footer'] = footer
        embed_dict['image'] = image
        embed_dict['thumbnail'] = thumbnail
        embed_dict['video'] = video
        embed_dict['provider'] = provider
        embed_dict['author'] = author
        embed_dict['fields'] = transform_embed_fields(embed=embed)
        ems.append(embed_dict)
