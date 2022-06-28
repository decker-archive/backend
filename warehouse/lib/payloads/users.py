###############################################################################
# The contents of this file are subject to the Common Public Attribution
# License Version 1.0. (the "License"); you may not use this file except in
# compliance with the License. You may obtain a copy of the License at
# http://veneralab.com/assets/license. The License is based on the Mozilla Public
# License Version 1.1, but Sections 14 and 15 have been added to cover use of
# software over a computer network and provide for limited attribution for the
# Original Developer. In addition, Exhibit A has been modified to be consistent
# with Exhibit B.
#
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License for
# the specific language governing rights and limitations under the License.
#
# The Original Code is venera.
#
# The Original Developer is the Initial Developer.  The Initial Developer of
# the Original Code is venera Inc.
#
# All portions of the code written by venera are Copyright (c) 2021-2022 venera
# Inc. All Rights Reserved.
###############################################################################

from pydantic import BaseModel, Field, EmailStr
from typing import Optional

USERNAME_REGEX = r'^(?=.{3,21}$)(?![_.])(?!.*[_.]{2})[a-zA-Z0-9._]+(?<![_.])$'
URL_REGEX = r'[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*'
DISPLAY_NAME_REGEX = r'[a-zA-Z0-9 ]+'


class Login(BaseModel):
    email: EmailStr
    password: str


class CreateUser(BaseModel):
    username: str = Field(max_length=30, regex=USERNAME_REGEX)
    email: EmailStr
    password: str


class EditUser(BaseModel):
    username: Optional[str] = Field(regex=USERNAME_REGEX)
    display_name: Optional[str] = Field(max_length=21, min_length=3, regex=DISPLAY_NAME_REGEX)
    email: Optional[EmailStr]
    password: Optional[str]
    avatar_url: Optional[str] = Field(max_length=50, regex=URL_REGEX)
    banner_url: Optional[str] = Field(max_length=50, regex=URL_REGEX)
    bio: Optional[str] = Field(max_length=300)
