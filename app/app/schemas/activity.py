# -*- coding: utf-8 -*-
"""
@author: Liam
"""

from typing import Optional, List, Literal
import datetime
from pydantic import BaseModel, constr
from app.schemas.account import Account
from app.schemas.misc import Sport, Level

# Shared properties
class ActivityBase(BaseModel):
    title: constr(max_length=50)
    description: constr(max_length=300)
    event_date: Optional[datetime.date] = None
    postcode: constr(strip_whitespace=True, min_length=3, max_length=5)
    address: Optional[constr(max_length=100)] = None
    image: Optional[constr(strip_whitespace=True, max_length=300)] = None


# Properties to receive on data creation
class ActivityCreate(ActivityBase):
    sport_id: int
    levels: Optional[List[Literal["débutant", "amateur", "intermédiaire", "confirmé", "expert"]]] = ["débutant",
                                                                                                     "amateur",
                                                                                                     "intermédiaire",
                                                                                                     "confirmé",
                                                                                                     "expert"]


# Properties to receive on data update
class ActivityUpdate(ActivityBase):
    title: Optional[constr(max_length=50)] = None
    description: Optional[constr(max_length=300)] = None
    event_date: Optional[datetime.date] = None
    postcode: Optional[constr(strip_whitespace=True, min_length=3, max_length=5)] = None
    address: Optional[constr(max_length=100)] = None
    image: Optional[constr(strip_whitespace=True, max_length=300)] = None
    sport_id: Optional[int] = None
    levels: Optional[List[Literal["débutant", "amateur", "intermédiaire", "confirmé", "expert"]]] = ["débutant",
                                                                                                     "amateur",
                                                                                                     "intermédiaire",
                                                                                                     "confirmé",
                                                                                                     "expert"]


# Properties shared by models stored in DB
class ActivityInDBBase(ActivityBase):
    id: int
    organizer: constr(strip_whitespace=True, min_length=4, max_length=40)
    publi_date: Optional[datetime.date] = datetime.date.today()

    class Config:
        orm_mode = True


# Properties to return to client
class Activity(ActivityInDBBase):
    sport: Sport
    levels: List[Level]


class ActivityWithParticipants(Activity):
    participants: Optional[List[Account]] = None


# Properties properties stored in DB
class ActivityInDB(ActivityInDBBase):
    sport_id: int
