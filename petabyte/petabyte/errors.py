"""
Petabyte - Production-grade Database tools and models for Polynode

:copyright: 2021-2022 Derailed.
:license: LGPL-3.0
"""


class PetabyteException(Exception):
    def __init__(self, code: int, message: str) -> None:
        super().__init__(code, message)
