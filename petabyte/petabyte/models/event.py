"""
Petabyte - Production-grade Database tools and models for Polynode

:copyright: 2021-2022 Derailed.
:license: LGPL-3.0
"""
from typing import Any

import msgspec


class Event(msgspec.Struct):
    type: str
    data: dict[Any, Any]
