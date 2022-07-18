"""
Petabyte - Production-grade Database tools and models for Polynode

:copyright: 2021-2022 Derailed.
:license: LGPL-3.0
"""
from ...errors import PetabyteException
from ..db import User as PolyDB
from ..poly import CreateUser
from ..poly import User as Poly


class User:
    def __init__(self, poly: Poly) -> None:
        self.poly = poly

    def select(self, id: int | list[int]):
        ...

    @classmethod
    def insert(cls, poly: CreateUser):
        insert = poly.dict()

        poly: PolyDB = PolyDB.create(**insert)

        return cls(poly=Poly(**dict(poly)))

    @classmethod
    def check_username(cls, username: str, discriminator: str):
        try:
            PolyDB.objects(
                PolyDB.username == username, PolyDB.discriminator == discriminator
            ).get()
        except:
            return
        else:
            raise PetabyteException(4, 'This username and discriminator is taken.')

    def delete(self):
        ...
