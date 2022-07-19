"""
Petabyte - Production-grade Database tools and models for Polynode

:copyright: 2021-2022 Derailed.
:license: LGPL-3.0
"""
from cassandra.cqlengine import columns, models


class Message(models.Model):
    __table_name__ = 'messages'
    id: int = columns.BigInt(primary_key=True)
    channel_id: int = columns.BigInt(primary_key=True)
    bucket_id: int = columns.Integer(primary_key=True)
    author_id: int = columns.BigInt()
    content: str = columns.Text()
    created_timestamp: str = columns.DateTime()
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
    embed_timestamp: str = columns.DateTime()
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
