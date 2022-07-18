"""
Petabyte - Production-grade Database tools and models for Polynode

:copyright: 2021-2022 Derailed.
:license: LGPL-3.0
"""
from functools import wraps
from typing import Callable

from .errors import PetabyteException


def validate_version(func: Callable):
    @wraps(func)
    def inner(version: int, *args, **kwargs):
        if version not in ('v1'):
            raise PetabyteException(10, 'Invalid API version')

        return func(*args, **kwargs)

    return inner
