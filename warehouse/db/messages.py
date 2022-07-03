###############################################################################
# The contents of this file are subject to the Common Public Attribution
# License Version 1.0. (the "License"); you may not use this file except in
# compliance with the License. You may obtain a copy of the License at
# http://mozaku.com/assets/license. The License is based on the Mozilla Public
# License Version 1.1, but Sections 14 and 15 have been added to cover use of
# software over a computer network and provide for limited attribution for the
# Original Developer. In addition, Exhibit A has been modified to be consistent
# with Exhibit B.
#
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License for
# the specific language governing rights and limitations under the License.
#
# The Original Code is mozaku.
#
# The Original Developer is the Initial Developer.  The Initial Developer of
# the Original Code is Mozaku.
#
# All portions of the code written by mozaku are Copyright (c) 2021-2022 mozaku
# Inc. All Rights Reserved.
###############################################################################
import os

import aiokafka
import aiokafka.helpers
import orjson


async def enable_production():
    global producer
    producer = aiokafka.AIOKafkaProducer(
        ssl_context=aiokafka.helpers.create_default_context(),
        value_serializer=orjson.dumps,
        bootstrap_servers=os.getenv('KAFKA_URL'),
        security_protocol='SASL_SSL',
        sasl_mechanism='PLAIN',
        sasl_plain_username=os.getenv('KAFKA_USERNAME'),
        sasl_plain_password=os.getenv('KAFKA_PASSWORD'),
    )
    await producer.start()


async def send_message(topic: str, message: dict, key: str = None):
    # NOTE: the key might be the guild, channel or user which caused the event.

    if key:
        key = bytes(key)

    await producer.send(topic, message, key=key)


async def send_messages(topic: str, messages: list[dict], key: str = None):
    for message in messages:
        await send_message(topic=topic, message=message, key=key)


if __name__ == '__main__':
    from dotenv import load_dotenv

    load_dotenv()

    async def test_message():
        await enable_production()

        await send_message('guild_messages', {'hello': 'world'})

    import asyncio

    asyncio.run(test_message())
