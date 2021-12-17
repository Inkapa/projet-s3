# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 00:17:04 2021

@author: Liam
"""
from typing import TYPE_CHECKING
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, select, func, distinct
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from app.db.base_class import Base

from .reserved import Reserved

if TYPE_CHECKING:
    from .account import Account  # noqa: F401
    from .sport import Sport  # noqa: F401
    from .level import Levels  # noqa: F401
    from .participation import Participation # noqa: F401



class Activity(Base):
    __tablename__ = "activity"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    publi_date = Column(DateTime, nullable=False)
    event_date = Column(DateTime, nullable=True)
    postcode = Column(String, nullable=False)
    address = Column(String, nullable=True)
    image = Column(String, nullable=True)
    sport_id = Column(Integer, ForeignKey("sport.id"))
    organizer = Column(String, ForeignKey("account.username"))
    creator = relationship("Account", backref="created_activities", foreign_keys=[organizer])
    sport = relationship("Sport", backref="activities", lazy='subquery')
    levels = relationship("Level", secondary=Reserved, backref="activities", lazy='subquery')

    # participants

    @hybrid_property
    def participant_count(self):
        if self.participants:
            return len(self.participants)
        return 0

    @participant_count.expression
    def participant_count(cls):
        return (select([func.count(distinct(Participation.participant))])
                .where(Participation.activity_id == cls.id))
