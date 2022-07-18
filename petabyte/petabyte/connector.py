"""
Petabyte - Production-grade Database tools and models for Polynode

:copyright: 2021-2022 Derailed.
:license: LGPL-3.0
"""
import logging
import os

from cassandra.auth import PlainTextAuthProvider
from cassandra.cqlengine import connection, management
from dotenv import load_dotenv

from petabyte.models import db

BUNDLE_LOC = os.getcwd() + r'\private\cass-bundle.zip'

if not os.getenv('CLIENT_ID'):
    load_dotenv()

cloud = {'secure_connect_bundle': BUNDLE_LOC}
auth_provider = PlainTextAuthProvider(
    os.getenv('CLIENT_ID'), os.getenv('CLIENT_SECRET')
)


def connect():
    try:
        if os.getenv('SAFE', 'true') == 'false':
            connection.setup(
                None,
                'petabyte',
                cloud=cloud,
                auth_provider=auth_provider,
                connect_timeout=100,
                retry_connect=True,
            )
        else:
            connection.setup(
                None,
                'petabyte',
                connect_timeout=100,
                retry_connect=True,
                compression=False,
            )
    except:
        connect()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    connect()

    # users
    management.sync_table(db.User)
    management.sync_table(db.UserSettings)
    # guilds
    management.sync_table(db.GuildPosition)
    # channels
    management.sync_table(db.Channel)
    management.sync_table(db.PermissionOverwrite)
    # messages
    management.sync_table(db.Message)
    management.sync_table(db.Attachment)
    management.sync_table(db.Embed)
    management.sync_table(db.EmbedProvider)
    management.sync_table(db.EmbedAuthor)
    management.sync_table(db.EmbedField)
    management.sync_table(db.EmbedFooter)
    management.sync_table(db.EmbedImage)
    management.sync_table(db.EmbedThumbnail)
    management.sync_table(db.EmbedVideo)
