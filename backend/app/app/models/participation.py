# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 00:17:04 2021

@author: Liam
"""

from typing import TYPE_CHECKING
from sqlalchemy import Table, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .account import Account  # noqa: F401
    from .activity import Activity  # noqa: F401
    from .level import Level  # noqa: F401


class Participation(Base):
    __tablename__ = "participation"
    level_id = Column(Integer, ForeignKey("level.id"), nullable=False)
    participant = Column(String, ForeignKey("account.username"), primary_key=True, nullable=False)
    activity_id = Column(Integer, ForeignKey("activity.id"), primary_key=True, nullable=False)
    user = relationship("Account", backref="participations", lazy='subquery')
    activity = relationship("Activity", backref="participants", lazy='subquery')
    level = relationship("Level", backref="participations", lazy='subquery')
