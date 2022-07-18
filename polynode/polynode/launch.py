"""
Polynode - Production Grade node for Derailed

:copyright: 2021-2022 Derailed.
:license: LGPL-3.0
"""
import threading
from uuid import uuid4

from flask import Response

from petabyte.connector import connect
from petabyte.errors import PetabyteException
from petabyte.forge import forger
from polynode.app import app
from polynode.routes import Users

app.config['FLASK_PYDANTIC_VALIDATION_ERROR_STATUS_CODE'] = 400

app.register_blueprint(Users)


@app.route('/__developers')
def ping():
    return {'acknowledgement': str(forger.forge())}


@app.errorhandler(404)
def not_found(_):
    return {'code': 1, 'message': '404: Not Found', 'type': 'default'}, 404


@app.errorhandler(405)
def method_invalid(_):
    return {'code': 2, 'message': '405: Method Not Allowed', 'type': 'default'}, 405


@app.errorhandler(429)
async def rate_limit(_):
    return {'code': 3, 'message': '429: Too Many Requests', 'type': 'default'}, 429


@app.errorhandler(PetabyteException)
def peta_exception(err: PetabyteException):
    return {'code': err.code, 'message': err.message, 'type': err.type}, err.status


@app.after_request
def after_request(resp: Response):
    resp.headers['x-track-id'] = hex(uuid4().int)
    resp.headers['x-poly-node'] = hex(threading.get_ident())

    return resp


@app.before_first_request
def startup():
    connect()
