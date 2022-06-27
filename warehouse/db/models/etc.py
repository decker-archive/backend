"""
Copyright (c) 2022 Mozaiku Inc. All Rights Reserved.
"""
import functools


def _has_flag(v: int, f: int) -> bool:
    return True if v & f else False


class UserFlags:
    def __init__(self, __v: int):
        has = functools.partial(_has_flag, __v)

        self.early_supporter = has(1 << 0)
        self.staff = has(1 << 1)
        self.verified = has(1 << 2)
        self.bug_hunter = has(1 << 3)
