# -*- coding: utf-8 -*-
"""
@author: Liam
"""

from pydantic import BaseModel, constr
from app.schemas.activity import Activity
from app.schemas.account import Account
from app.schemas.misc import Level
from typing import Literal, Optional, Union, List


class ParticipationBase(BaseModel):
    level: Literal["débutant", "amateur", "intermédiaire", "confirmé", "expert"]


# Properties to receive on data creation
class ParticipationCreate(ParticipationBase):

    participant: constr(strip_whitespace=True, min_length=4, max_length=40)
    activity_id: int


class CreateParticipationActivity(ParticipationBase):
    activity_id: int


class CreateParticipationUser(ParticipationBase):
    participant: constr(strip_whitespace=True, min_length=4, max_length=40)


class ParticipationUser(BaseModel):
    user: Account
    level: Level

    class Config:
        orm_mode = True


class ParticipationActivity(BaseModel):
    activity: Activity
    level: Level

    class Config:
        orm_mode = True


class Participation(BaseModel):
    user: Account
    activity: Activity
    level: Level

    class Config:
        orm_mode = True
