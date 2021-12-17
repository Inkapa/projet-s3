# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 00:17:04 2021

@author: Liam
"""

from typing import TYPE_CHECKING
from sqlalchemy import Boolean, Float, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
import datetime
from app.db.base_class import Base

if TYPE_CHECKING:
    from .account import Account  # noqa: F401
    from .wear import Wear  # noqa: F401


class Offer(Base):
    __tablename__ = "offer"
    id = Column(Integer, primary_key=True, index=True)
    seller = Column(String, ForeignKey("account.username"), primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    postcode = Column(String, nullable=False)
    address = Column(String, nullable=True)
    can_trade = Column(Boolean, nullable=False)
    image = Column(String, nullable=True)
    publi_date = Column(DateTime, nullable=False, default=datetime.date.today())
    wear_level_id = Column(Integer, ForeignKey("wear.id"))
    user = relationship("Account", backref="offers")
    wear = relationship("Wear", backref="offers")
