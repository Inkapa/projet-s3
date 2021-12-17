# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 00:17:04 2021

@author: Liam
"""

from typing import TYPE_CHECKING
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.db.base_class import Base

if TYPE_CHECKING:
    from .account import Account  # noqa: F401
    from .sport import Sport  # noqa: F401


class Coaching(Base):
    __tablename__ = "coaching"
    id = Column(Integer, primary_key=True, index=True)
    student = Column(String, ForeignKey("account.username"), primary_key=True, nullable=False)
    coach = Column(String, ForeignKey("account.username"), primary_key=True, nullable=False)
    sport_id = Column(Integer, ForeignKey("sport.id"), primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    user_coach = relationship("Account", backref="emitted_coachings", foreign_keys=[coach])
    user_student = relationship("Account", backref="received_coachings", foreign_keys=[student])
    sport = relationship("Sport", backref="coachings")
