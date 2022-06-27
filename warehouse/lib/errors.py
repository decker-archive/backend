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


class GuildAlreadyExists(Exception):
    """
    This guild already exists.
    """


class UserDoesNotExist(Exception):
    """
    This user does not exist.
    """


class AuthenticationError(Exception):
    """
    When authentication fails.
    """


class AlreadyMember(Exception):
    """
    User is already a member.
    """


class NotAMember(Exception):
    """
    User is not a member.
    """
