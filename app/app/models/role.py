# -*- coding: utf-8 -*-
"""
Created on Wed Oct  6 00:17:04 2021

@author: Liam
"""

from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .account import Account  # noqa: F401


class Role(Base):
    __tablename__ = "role"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    role_name = Column(String, unique=True, index=True, nullable=False)
    # users
