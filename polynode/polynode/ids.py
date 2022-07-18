"""
Polynode - Production Grade node for Derailed

:copyright: 2021-2022 Derailed.
:license: LGPL-3.0
"""
import os
import threading
import time


class SnowflakeFactory:
    def __init__(self) -> None:
        self._epoch: int = 1641042000000
        self._incrementation = 0

    def forge(self) -> int:
        current_ms = int(time.time() * 1000)
        epoch = current_ms - self._epoch << 22

        curthread = threading.current_thread().ident
        assert (
            curthread is not None
        )  # NOTE: done for typing purposes, shouldn't ever actually be None.

        epoch |= (curthread % 32) << 17
        epoch |= (os.getpid() % 32) << 12

        epoch |= self._incrementation % 4096

        if self._incrementation == 9000000:
            self._incrementation = 0

        self._incrementation += 1

        return epoch


snowstorm = SnowflakeFactory()


if __name__ == '__main__':
    while True:
        import sys

        print(snowstorm.forge(), file=sys.stderr)
