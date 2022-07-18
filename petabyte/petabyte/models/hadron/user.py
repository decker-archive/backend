"""
Petabyte - Production-grade Database tools and models for Polynode

:copyright: 2021-2022 Derailed.
:license: LGPL-3.0
"""
import base64
import itsdangerous
from random import randint

import bcrypt

from ...errors import PetabyteException
from ..db.user import User as PolyDB, UserSettings as PolySettings
from ..db.user import transform_user
from ..poly import CreateUser
from ..poly import User as Poly
from ...forge import forger


class User:
    def __init__(self, poly: Poly) -> None:
        self.poly = poly
        self.email: str = None
        self.password: str = None

    @classmethod
    def select(cls, id: int | list[int]):
        polydb: PolyDB = PolyDB.objects(PolyDB.id == id).get()
        self = cls(poly=Poly(**transform_user(dict(polydb))))
        self.email = polydb.email
        self.password = polydb.password
        return self

    @classmethod
    def insert(cls, poly: CreateUser):
        insert = poly.dict()
        insert['discriminator'] = cls.generate_discriminator(username=poly.username)
        password = bcrypt.hashpw(insert['password'].encode(), bcrypt.gensalt(14)).decode()
        insert['password'] = password

        # NOTE: Defaults
        insert['id'] = forger.forge()
        insert['flags'] = 0
        insert['avatar'] = ''
        insert['banner'] = ''
        insert['bio'] = ''
        insert['bot'] = False

        poly: PolyDB = PolyDB.create(**insert)
        PolySettings.create(
            user_id=insert['id'],
            locale='en-US',
            developer_mode=False,
            theme='dark'
        )
        self = cls(poly=Poly(**transform_user(user=insert, keep_email=True)))
        self.password = password
        self.email = insert['email']

        return self

    @classmethod
    def generate_discriminator(cls, username: str) -> str:
        for _ in range(500):
            try:
                discrim_number = randint(1, 9999)
                discriminator = "%04d" % discrim_number
                cls.check_username(username=username, discriminator=discriminator)
            except:
                continue

            return discriminator

        raise PetabyteException(
            11,
            'Failed to properly find a unused discriminator, please try another username.',
        )

    def generate_token(self) -> str:
        signer = itsdangerous.TimestampSigner(self.password)
        user_id = base64.b64encode(str(self.poly.id).encode())

        return signer.sign(user_id).decode()

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
        polydb: PolyDB = PolyDB.objects(PolyDB.id == self.poly.id).get()
        polydb.delete()
