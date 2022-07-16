"""
Polynode - Production Grade node for Derailed
Copyright (C) 2022 Derailed.
"""
from typing import Any

import msgspec


class Event(msgspec.Struct):
    type: str
    data: dict[Any, Any]
