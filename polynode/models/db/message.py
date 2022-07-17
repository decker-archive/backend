"""
Polynode - Production Grade node for Derailed
Copyright (C) 2022 Derailed.
"""
from cassandra.cqlengine import columns, models

from polynode.utils import transform_ids


class Message(models.Model):
    id: int = columns.BigInt(primary_key=True)
    channel_id: int = columns.BigInt(primary_key=True)
    bucket_id: int = columns.Integer(primary_key=True)
    author_id: int = columns.BigInt()
    content: str = columns.Text()
    timestamp: str = columns.DateTime()
    edited_timestamp: str = columns.DateTime()
    mention_everyone: bool = columns.Boolean()


class Attachment(models.Model):
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
    message_id: int = columns.BigInt(primary_key=True)
    embed_id: int = columns.BigInt()
    title: str = columns.Text()
    type: str = columns.Text()
    description: str = columns.Text()
    url: str = columns.Text()
    timestamp: str = columns.DateTime()
    color: int = columns.Integer()


class EmbedProvider(models.Model):
    embed_id: int = columns.BigInt(primary_key=True)
    name: str = columns.Text()
    url: str = columns.Text()


class EmbedFooter(models.Model):
    embed_id: int = columns.BigInt(primary_key=True)
    text: str = columns.Text()
    icon_url: str = columns.Text()
    proxy_icon_url: str = columns.Text()


class EmbedField(models.Model):
    embed_id: int = columns.BigInt(primary_key=True)
    name: str = columns.Text()
    value: str = columns.Text()
    inline: bool = columns.Boolean()


class EmbedAuthor(models.Model):
    embed_id: int = columns.BigInt(primary_key=True)
    name: str = columns.Text()
    url: str = columns.Text()
    icon_url: str = columns.Text()
    proxy_icon_url: str = columns.Text()


class EmbedImage(models.Model):
    embed_id: int = columns.BigInt(primary_key=True)
    url: str = columns.Text()
    proxy_url: str = columns.Text()
    height: int = columns.Integer()
    width: int = columns.Integer()


class EmbedVideo(models.Model):
    embed_id: int = columns.BigInt(primary_key=True)
    url: str = columns.Text()
    proxy_url: str = columns.Text()
    height: int = columns.Integer()
    width: int = columns.Integer()


class EmbedThumbnail(models.Model):
    embed_id: int = columns.BigInt(primary_key=True)
    url: str = columns.Text()
    proxy_url: str = columns.Text()
    height: int = columns.Integer()
    width: int = columns.Integer()


class Reaction(models.Model):
    message_id: int = columns.BigInt(primary_key=True)
    user_id: int = columns.BigInt()
    emoji_id: int = columns.BigInt()


class UserMention(models.Model):
    message_id: int = columns.BigInt(primary_key=True)
    user_id: int = columns.BigInt()


class RoleMention(models.Model):
    message_id: int = columns.BigInt(primary_key=True)
    role_id: int = columns.BigInt()


class ChannelMention(models.Model):
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


def transform_message(message: Message):
    dict = message.__dict__
    transform_ids(dict=dict)

    embeds: list[Embed] = Embed.objects(Embed.message_id == message.id).all()
    ems = []

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
