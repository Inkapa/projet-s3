# -*- coding: utf-8 -*-
"""
@author: Liam
"""

from pydantic import BaseModel


class Msg(BaseModel):
    msg: str
