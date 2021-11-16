# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 00:17:04 2021

@author: Liam
"""
from sqlalchemy import Column, Integer, String
from app.db.base_class import Base


class Sport(Base):
    __tablename__ = "sport"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    image = Column(String, nullable=True)
    # activities
    # coachings