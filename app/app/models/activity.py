# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 00:17:04 2021

@author: Liam
"""
from typing import TYPE_CHECKING
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from app.db.base_class import Base

from .participation import Participation
from .reserved import Reserved

if TYPE_CHECKING:
    from .account import Account  # noqa: F401
    from .sport import Sport  # noqa: F401
    from .level import Levels  # noqa: F401



class Activity(Base):
    __tablename__ = "activity"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=True)
    postcode = Column(String, nullable=False)
    address = Column(String, nullable=True)
    image = Column(String, nullable=True)
    sport_id = Column(Integer, ForeignKey("sport.id"))
    organizer = Column(String, ForeignKey("account.username"))
    creator = relationship("Account", backref="created_activities", foreign_keys=[organizer])
    participants = relationship("Account", secondary=Participation, backref="activities")
    sport = relationship("Sport", backref="activities")
    levels = relationship("Level", secondary=Reserved, backref="activities")
