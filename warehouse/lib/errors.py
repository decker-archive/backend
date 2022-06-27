"""
Copyright (c) 2022 Mozaiku Inc. All Rights Reserved.
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


class GuildDoesNotExist(Exception):
    """
    This guild does not exist.
    """


class MemberIsMod(Exception):
    """
    This member is a mod.
    """


class AlreadyLoggedin(Exception):
    """
    This user is already logged into an account.
    """

class InvalidCredentials(Exception):
    """
    Given invalid credentials on login.
    """
