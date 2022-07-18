"""
Polynode - Production Grade node for Derailed

:copyright: 2021-2022 Derailed.
:license: LGPL-3.0
"""

from flask_pydantic import validate

from petabyte.authorization import requires_authorization
from petabyte.models.poly import User as Poly
from petabyte.models.db import transform_user
from petabyte.utils import validate_version
from polynode.app import limiter


@limiter.limit('8/minute')
@validate_version
@requires_authorization
def req(user: Poly) -> Poly:
    return transform_user(user.poly.dict(exclude_none=True), keep_email=True)
