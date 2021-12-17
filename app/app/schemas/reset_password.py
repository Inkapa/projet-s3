# -*- coding: utf-8 -*-
"""
@author: Liam
"""

from pydantic import BaseModel, constr

class Reset_Password(BaseModel):
    token: str
    new_password: constr(strip_whitespace=True, min_length=4, max_length=180)
