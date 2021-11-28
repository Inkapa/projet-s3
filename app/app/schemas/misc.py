# -*- coding: utf-8 -*-
"""
@author: Liam
"""
from pydantic import BaseModel, constr
from typing import Optional


class Sport(BaseModel):
    id: int
    name: constr(max_length=50, to_lower=True)
    image: Optional[constr(max_length=300)]

    class Config:
        orm_mode = True


class Level(BaseModel):
    id: int
    level: constr(max_length=50, to_lower=True)

    class Config:
        orm_mode = True