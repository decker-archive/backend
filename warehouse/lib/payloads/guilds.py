###############################################################################
# The contents of this file are subject to the Common Public Attribution
# License Version 1.0. (the "License"); you may not use this file except in
# compliance with the License. You may obtain a copy of the License at
# http://onamii.com/assets/license. The License is based on the Mozilla Public
# License Version 1.1, but Sections 14 and 15 have been added to cover use of
# software over a computer network and provide for limited attribution for the
# Original Developer. In addition, Exhibit A has been modified to be consistent
# with Exhibit B.
#
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License for
# the specific language governing rights and limitations under the License.
#
# The Original Code is onamii.
#
# The Original Developer is the Initial Developer.  The Initial Developer of
# the Original Code is Onamii.
#
# All portions of the code written by onamii are Copyright (c) 2021-2022 onamii
# Inc. All Rights Reserved.
###############################################################################

from typing import Optional

from pydantic import BaseModel, Field


class CreateGuild(BaseModel):
    name: str = Field(min_length=1, max_length=21)
    nsfw: bool = Field(default=False)
    description: str = Field(default='', max_length=400)


class EditGuild(BaseModel):
    name: Optional[str] = Field(min_length=1, max_length=21)
    nsfw: Optional[bool]
    description: Optional[str]
