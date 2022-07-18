"""
Polynode - Production Grade node for Derailed

:copyright: 2021-2022 Derailed.
:license: LGPL-3.0
"""

from flask_pydantic import validate

from petabyte.models.hadron import CreateUser, User
from petabyte.utils import validate_version
from polynode.app import limiter


@validate(body=CreateUser, on_success_status=201, exclude_none=True)
@limiter.limit('3/hour')
@validate_version
def req(body: CreateUser) -> User:
    user: User = User.insert(body)
    return {'token': user.generate_token()}
