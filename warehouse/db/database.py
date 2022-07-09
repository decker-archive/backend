###############################################################################
# The contents of this file are subject to the Common Public Attribution
# License Version 1.0. (the "License"); you may not use this file except in
# compliance with the License. You may obtain a copy of the License at
# http://plufify.com/assets/license. The License is based on the Mozilla Public
# License Version 1.1, but Sections 14 and 15 have been added to cover use of
# software over a computer network and provide for limited attribution for the
# Original Developer. In addition, Exhibit A has been modified to be consistent
# with Exhibit B.
#
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License for
# the specific language governing rights and limitations under the License.
#
# The Original Code is plufify.
#
# The Original Developer is the Initial Developer.  The Initial Developer of
# the Original Code is Plufify.
#
# All portions of the code written by plufify are Copyright (c) 2021-2022 plufify
# Inc. All Rights Reserved.
###############################################################################

import logging
import os

from cassandra.auth import PlainTextAuthProvider
from cassandra.cqlengine import connection, management
from dotenv import load_dotenv

from warehouse.db.models import Guild, GuildFeature, GuildMember, User

BUNDLE_LOC = os.getcwd() + r'\private\cass-bundle.zip'

if not os.getenv('CLIENT_ID'):
    load_dotenv()

cloud = {'secure_connect_bundle': BUNDLE_LOC}
auth_provider = PlainTextAuthProvider(
    os.getenv('CLIENT_ID'), os.getenv('CLIENT_SECRET')
)


def connect():
    try:
        if os.getenv('SAFE', 'true') == 'true':
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
    management.sync_table(GuildMember)
    management.sync_table(GuildFeature)
