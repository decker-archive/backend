"""
Petabyte - Production-grade Database tools and models for Polynode

:copyright: 2021-2022 Derailed.
:license: LGPL-3.0
"""
from typing import Any


def transform_ids(dict: dict[str, Any]):
    for key, value in dict.values():
        if 'id' in key and not isinstance(value, str):
            dict[key] = str(value)
