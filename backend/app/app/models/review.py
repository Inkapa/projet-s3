# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 00:17:04 2021

@author: Liam
"""
from typing import TYPE_CHECKING
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .account import Account  # noqa: F401


class Review(Base):
    __tablename__ = "review"
    username = Column(String, ForeignKey("account.username"), primary_key=True, nullable=False)
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    note = Column(Integer, nullable=False)
    critic_username = Column(String, ForeignKey("account.username"))
    emitter = relationship("Account", backref="emitted_reviews", foreign_keys=[critic_username])
    receiver = relationship("Account", backref="received_reviews", foreign_keys=[username])
