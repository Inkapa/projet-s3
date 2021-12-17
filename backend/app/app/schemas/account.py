# -*- coding: utf-8 -*-
"""
@author: Liam
"""

from typing import Optional
import datetime
from pydantic import BaseModel, EmailStr, constr

# ======================= Account =======================


# Shared properties
class AccountBase(BaseModel):
    username: constr(strip_whitespace=True, min_length=4, max_length=40)
    email: EmailStr

# Properties to receive via API on creation
class AccountCreate(AccountBase):
    is_superuser: bool = False
    is_confirmed: bool = False
    role_id: int = 0  # normal user
    password: constr(strip_whitespace=True, min_length=4, max_length=180)

# Properties to receive via API on register
class AccountRegister(AccountBase):
    password: constr(strip_whitespace=True, min_length=4, max_length=180)

# Properties to receive via API on update (admin)
class AccountUpdate(AccountBase):
    password: Optional[constr(strip_whitespace=True, min_length=4, max_length=180)] = None
    is_superuser: bool = False
    is_confirmed: bool = False
    role_id: int = 0  # normal user

# Properties to receive via API on update (user)
class AccountUpdateMe(BaseModel):
    username: Optional[constr(strip_whitespace=True, min_length=4, max_length=40)] = None
    password: Optional[constr(strip_whitespace=True, min_length=4, max_length=180)] = None

class AccountInDBBase(AccountBase):
    sign_up_date: datetime.date
    is_superuser: bool = False
    is_confirmed: bool = False
    role_id: int = 0  # normal user
    class Config:
        orm_mode = True


# Additional properties to return via API
class Account(AccountInDBBase):
    pass


# Additional properties stored in DB
class AccountInDB(AccountInDBBase):
    hashed_password: str
