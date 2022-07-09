###############################################################################
# The contents of this file are subject to the Common Public Attribution
# License Version 1.0. (the "License"); you may not use this file except in
# compliance with the License. You may obtain a copy of the License at
# http://plufify.com/assets/license. The License is based on the Mozilla Public
# License Version 1.1, but Sections 14 and 15 have been added to cover use of
# software over a computer network and provide for limited attribution for the
# Original Developer. In addition, Exhibit A has been modified to be consistent
# with Exhibit B.
#
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License for
# the specific language governing rights and limitations under the License.
#
# The Original Code is plufify.
#
# The Original Developer is the Initial Developer.  The Initial Developer of
# the Original Code is Plufify.
#
# All portions of the code written by plufify are Copyright (c) 2021-2022 plufify
# Inc. All Rights Reserved.
###############################################################################


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


class InvalidVersion(Exception):
    """
    Version Given was Invalid.
    """
