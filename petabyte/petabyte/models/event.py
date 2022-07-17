"""
Petabyte - Production-grade Database tools and models for Polynode
Copyright (C) 2022 Derailed.
"""
from typing import Any

import msgspec


class Event(msgspec.Struct):
    type: str
    data: dict[Any, Any]
