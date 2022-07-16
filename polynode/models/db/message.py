"""
Polynode - Production Grade node for Derailed
Copyright (C) 2022 Derailed.
"""
from cassandra.cqlengine import columns, models
from polynode.utils import transform_ids


class Message(models.Model):
    id: str = columns.Text(primary_key=True)
    channel_id: str = columns.Text(primary_key=True)
    bucket_id: int = columns.Integer(primary_key=True)
    author_id: str = columns.Text()
    content: str = columns.Text()
    timestamp: str = columns.DateTime()
    edited_timestamp: str = columns.DateTime()
    mention_everyone: bool = columns.Boolean()


class Attachment(models.Model):
    id: str = columns.Text(primary_key=True)
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
    message_id: str = columns.Text(primary_key=True)
    embed_id: str = columns.Text()
    title: str = columns.Text()
    type: str = columns.Text()
    description: str = columns.Text()
    url: str = columns.Text()
    timestamp: str = columns.DateTime()
    color: int = columns.Integer()


class EmbedProvider(models.Model):
    embed_id: str = columns.Text(primary_key=True)
    name: str = columns.Text()
    url: str = columns.Text()


class EmbedFooter(models.Model):
    embed_id: str = columns.Text(primary_key=True)
    text: str = columns.Text()
    icon_url: str = columns.Text()
    proxy_icon_url: str = columns.Text()


class EmbedField(models.Model):
    embed_id: str = columns.Text(primary_key=True)
    name: str = columns.Text()
    value: str = columns.Text()
    inline: bool = columns.Boolean()


class Reaction(models.Model):
    message_id: str = columns.Text(primary_key=True)
    user_id: str = columns.Text()
    emoji_id: str = columns.Text()


class UserMention(models.Model):
    message_id: str = columns.Text(primary_key=True)
    user_id: str = columns.Text()


class RoleMention(models.Model):
    message_id: str = columns.Text(primary_key=True)
    role_id: str = columns.Text()


class ChannelMention(models.Model):
    message_id: str = columns.Text(primary_key=True)
    id: str = columns.Text()
    guild_id: str = columns.Text()
    type: int = columns.Integer()
    name: str = columns.Text()


def transform_message(message: Message):
    # TODO
    ...

