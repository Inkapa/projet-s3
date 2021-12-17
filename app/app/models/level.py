# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 00:17:04 2021

@author: Liam
"""
from typing import TYPE_CHECKING
from sqlalchemy import Column, Integer, String
from app.db.base_class import Base


if TYPE_CHECKING:
    from .account import Account  # noqa: F401

class Level(Base):
    __tablename__ = "level"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    level = Column(String, nullable=False)
    # activities
