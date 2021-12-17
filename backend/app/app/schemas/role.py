# -*- coding: utf-8 -*-
"""
Created on Wed Oct  6 01:13:34 2021

@author: Liam
"""

from pydantic import BaseModel, constr

# Shared properties
class RoleBase(BaseModel):
    role_name: str


# Properties to receive on role creation
class RoleCreate(RoleBase):
    pass


# Properties to receive on role update
class RoleUpdate(RoleBase):
    pass

# Properties shared by models stored in DB
class RoleInDBBase(RoleBase):
    id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Role(RoleInDBBase):
    pass


# Properties properties stored in DB
class RoleInDB(RoleInDBBase):
    pass
