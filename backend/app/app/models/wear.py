# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 00:17:04 2021

@author: Liam
"""

from sqlalchemy import Column, Integer, String

from app.db.base_class import Base


class Wear(Base):
    __tablename__ = "wear"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    wear_level = Column(String, nullable=False)
    # offers (link => offer.wear_level_id)
