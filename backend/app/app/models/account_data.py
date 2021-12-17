# -*- coding: utf-8 -*-
"""
Created on Wed Oct  6 00:17:04 2021

@author: Liam
"""
from typing import TYPE_CHECKING
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .account import Account  # noqa: F401


class Account_Data(Base):
    __tablename__ = "account_data"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    postcode = Column(String, nullable=False)
    profile_picture = Column(String, nullable=True)
    birthday = Column(DateTime, nullable=False)
    about = Column(String, nullable=True)
    gender = Column(String, nullable=True)
    owner_username = Column(String, ForeignKey("account.username"))
    owner = relationship("Account", back_populates="data")
