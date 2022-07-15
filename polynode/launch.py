"""
Polynode - Production Grade node for Derailed
Copyright (C) 2022 Derailed.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>. 
"""
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


@app.after_request
def after_request(resp: Response):
    resp.headers['x-track-id'] = hex(uuid4().int)

    return resp
