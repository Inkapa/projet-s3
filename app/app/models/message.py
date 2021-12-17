# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 00:17:04 2021

@author: Liam
"""
from typing import TYPE_CHECKING
import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .account import Account  # noqa: F401


class Message(Base):
    __tablename__ = "message"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    recipient = Column(String, ForeignKey("account.username"), primary_key=True, nullable=False)
    sender = Column(String, ForeignKey("account.username"), primary_key=True, nullable=False)
    content = Column(String, nullable=False)
    image = Column(String, nullable=True)
    send_date = Column(DateTime, nullable=False, default=datetime.date.today())
    user_recipient = relationship("Account", backref="messages_received", foreign_keys=[recipient])
    user_sender = relationship("Account", backref="messages_sent", foreign_keys=[sender])
