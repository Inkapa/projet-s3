# -*- coding: utf-8 -*-
"""
@author: Liam
"""

from typing import Optional, Literal, Union
import datetime
from pydantic import BaseModel, constr


# Shared properties
class Account_DataBase(BaseModel):
    first_name: constr(max_length=50)
    last_name: constr(max_length=50)
    postcode: constr(strip_whitespace=True, min_length=3, max_length=5)
    profile_picture: Optional[constr(strip_whitespace=True, max_length=300)] = None
    birthday: datetime.date
    about: Optional[constr(max_length=300)] = None
    gender: Union[Literal['m', 'M', 'F', 'f'], None] = None


# Properties to receive on data creation
class Account_DataCreate(Account_DataBase):
    pass


# Properties to receive on data update
class Account_DataUpdate(Account_DataBase):
    first_name: Optional[constr(max_length=50)] = None
    last_name: Optional[constr(max_length=50)] = None
    postcode: Optional[constr(strip_whitespace=True, min_length=3, max_length=5)] = None
    profile_picture: Optional[constr(strip_whitespace=True, max_length=300)] = None
    birthday: Optional[datetime.date] = None
    about: Optional[constr(max_length=300)] = None


# Properties shared by models stored in DB
class Account_DataInDBBase(Account_DataBase):
    owner_username: constr(strip_whitespace=True, min_length=4, max_length=40)

    class Config:
        orm_mode = True


# Properties to return to client
class Account_Data(Account_DataInDBBase):
    pass


# Properties properties stored in DB
class Account_DataInDB(Account_DataInDBBase):
    pass
