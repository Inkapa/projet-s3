# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 00:17:04 2021

@author: Liam
"""

from typing import TYPE_CHECKING
from sqlalchemy import Table, Column, ForeignKey, Integer, String

from app.db.base_class import Base

if TYPE_CHECKING:
    from .account import Account  # noqa: F401
    from .activity import Activity  # noqa: F401


Reserved = Table(
    "reserved",
    Base.metadata,
    Column("level_id", Integer, ForeignKey("level.id"), primary_key=True, nullable=False),
    Column("activity_id", Integer, ForeignKey("activity.id"), primary_key=True, nullable=False)
    )
