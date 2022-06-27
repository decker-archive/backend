"""
Copyright (c) 2022 Mozaiku Inc. All Rights Reserved.
"""
import logging
import os

import dotenv
from cassandra.auth import PlainTextAuthProvider
from cassandra.cqlengine import connection, management

from .models import Guild, GuildFeature, User

dotenv.load_dotenv()
cloud = {'secure_connect_bundle': os.getcwd() + r'/private/cass-bundle.zip'}
auth_provider = PlainTextAuthProvider(
    os.getenv('CLIENT_ID'), os.getenv('CLIENT_SECRET')
)


def connect():
    try:
        if os.getenv('SAFE', 'false') == 'true':
            connection.setup(
                None,
                'warehouse',
                cloud=cloud,
                auth_provider=auth_provider,
                connect_timeout=100,
                retry_connect=True,
            )
        else:
            connection.setup(
                None,
                'warehouse',
                connect_timeout=100,
                retry_connect=True,
                compression=False,
            )
    except:
        connect()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    connect()
    management.sync_table(User)
    management.sync_table(Guild)
    management.sync_table(GuildFeature)
