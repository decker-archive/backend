"""
Copyright (c) 2022 Anavereum Inc. All Rights Reserved.
"""


class CommitError(Exception):
    """
    When a commit fails.
    """


class UserAlreadyExists(Exception):
    """
    This user already exists.
    """


class AuthenticationError(Exception):
    """
    When authentication fails.
    """
