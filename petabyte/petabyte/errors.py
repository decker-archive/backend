"""
Petabyte - Production-grade Database tools and models for Polynode

:copyright: 2021-2022 Derailed.
:license: LGPL-3.0
"""


class PetabyteException(Exception):
    def __init__(self, code: int, message: str, status: int = 400) -> None:
        self.code = code
        self.message = message
        self.type = 'database'
        self.status = status
        super().__init__(code, message)
