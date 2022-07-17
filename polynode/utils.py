"""
Polynode - Production Grade node for Derailed
Copyright (C) 2022 Derailed.
"""

from typing import Any


def transform_ids(dict: dict[str, Any]):
    for key, value in dict.values():
        if 'id' in key and not isinstance(value, str):
            dict[key] = str(value)
