"""
Polynode - Production Grade node for Derailed
Copyright (C) 2022 Derailed.
"""
import secrets
from cassandra.cqlengine import models
from typing import Type


class IDGenerator:
    def generate(self, cls: Type[models.Model]):
        id = secrets.token_urlsafe(11).lower()

        try:
            cls.objects(
                cls.id == id
            ).get()
        except:
            pass
        else:
            return self.generate(cls=cls)
