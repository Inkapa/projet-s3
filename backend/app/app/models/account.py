# -*- coding: utf-8 -*-
"""
Created on Tue Oct  5 03:25:10 2021

@author: Liam
"""
from typing import TYPE_CHECKING
import datetime
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .account_data import Account_Data  # noqa: F401
    from .role import Role  # noqa: F401
    from .activity import Activity  # noqa: F401
    from .review import Review  # noqa: F401
    from .message import Message  # noqa: F401


class Account(Base):
    __tablename__ = "account"
    username = Column(String, primary_key=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    is_confirmed = Column(Boolean, default=False, nullable=False)
    sign_up_date = Column(DateTime, nullable=False, default=datetime.date.today())
    role_id = Column(Integer, ForeignKey("role.id"))
    data = relationship("Account_Data", back_populates="owner", uselist=False)
    role = relationship("Role", backref="users")
    # created_activities
    # offers
    # emitted_reviews
    # received_reviews
    # sent_messages
    # received_messages
    # participations
