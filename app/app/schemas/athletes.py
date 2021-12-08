# -*- coding: utf-8 -*-
"""
@author: Liam
"""

from pydantic import BaseModel, constr
from typing import Literal, Optional, Union, List
from app.schemas.misc import Level, Sport
from app.schemas.account_data import Account_Data
import datetime


class SportsLevels(BaseModel):
    sport: Sport
    level: Level

    class Config:
        orm_mode = True


class AthletesBase(BaseModel):
    account: Account_Data
    sports: List[SportsLevels]

    class Config:
        arbitrary_types_allowed = True
        orm_mode = True

