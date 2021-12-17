# -*- coding: utf-8 -*-
"""
@author: Liam
"""

from pydantic import BaseModel, constr, confloat
from typing import Literal, Optional, Union, List
from app.schemas.misc import Level, Sport
from app.schemas.account_data import Account_Data


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


class FilterAthletes(BaseModel):
    me_excluded: Optional[bool] = None
    postal_code: Optional[constr(strip_whitespace=True, min_length=3, max_length=5)] = None
    sport_ids: Optional[List[int]] = None
    levels: Optional[
        Union[List[Literal["débutant", "amateur", "intermédiaire", "confirmé", "expert"]], None]] = None
    offset: Optional[int] = None
    limit: Optional[int] = None


class FilterAthletesRadius(FilterAthletes):
    radius: Optional[confloat(ge=1.0, le=320)] = 10.5
