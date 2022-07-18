"""
Polynode - Production Grade node for Derailed

:copyright: 2021-2022 Derailed.
:license: LGPL-3.0
"""
import flask_limiter
import flask_limiter.util
from flask import Flask, request

from polynode.json import ORJSONDecoder, ORJSONEncoder

app = Flask(__name__)
app.json_encoder = ORJSONEncoder
app.json_decoder = ORJSONDecoder


def get_key():
    if not request.headers['Authorization']:
        return flask_limiter.util.get_remote_address()

    return flask_limiter.util.get_remote_address()


limiter = flask_limiter.Limiter(
    headers_enabled=True,
    default_limits=['50/second'],
    retry_after='delta-seconds',
    key_func=get_key,
    enabled=True,
    strategy='fixed-window-elastic-expiry',
)
