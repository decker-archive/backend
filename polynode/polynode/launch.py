"""
Polynode - Production Grade node for Derailed

:copyright: 2021-2022 Derailed.
:license: LGPL-3.0
"""
import threading
from uuid import uuid4

from flask import Response

from polynode.app import app


@app.route('/__developers')
def ping():
    return {'code': 0, 'message': '1'}


@app.errorhandler(404)
def not_found(_):
    return {'code': 1, 'message': '404: Not Found'}


@app.errorhandler(405)
def method_invalid(_):
    return {'code': 2, 'message': '405: Method Not Allowed'}


@app.errorhandler(429)
async def rate_limit(_):
    return {
        'code': 3,
        'message': '429: Too Many Requests',
    }


@app.after_request
def after_request(resp: Response):
    resp.headers['x-track-id'] = hex(uuid4().int)
    resp.headers['x-poly-node'] = hex(threading.get_ident())

    return resp
