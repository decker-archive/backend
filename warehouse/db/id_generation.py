"""
Copyright (c) 2022 Mozaiku Inc. All Rights Reserved.
"""
import os
import threading
import time


class SnowflakeFactory:
    def __init__(self) -> None:
        self._epoch: int = 1649325271415
        self._incrementation = 0

    def manufacture(self) -> int:
        current_ms = int(time.time() * 1000)
        epoch = current_ms - self._epoch << 22

        curthread = threading.current_thread().ident
        assert curthread is not None

        epoch |= (curthread % 32) << 17
        epoch |= (os.getpid() % 32) << 12

        epoch |= self._incrementation % 4096

        self._incrementation += 1

        return epoch


snowflake_factory = SnowflakeFactory()

if __name__ == '__main__':
    while True:
        print(snowflake_factory.manufacture())
