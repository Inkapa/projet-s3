# -*- coding: utf-8 -*-
"""
@author: Liam
"""

from typing import Optional, List

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.level import Level
from app.models.sport import Sport


class CRUDSport(CRUDBase[Sport, None, None]):

    def get_by_name(self, db: Session, *, name: str) -> Optional[Sport]:
        return db.query(Sport).filter(Sport.name == name.lower()).first()

    def get_all(self, db: Session) -> List[Sport]:
        return db.query(Sport).all()


class CRUDLevel(CRUDBase[Level, None, None]):

    def get_by_name(self, db: Session, *, name: str) -> Optional[Level]:
        return db.query(Level).filter(Level.level == name.lower()).first()

    def get_by_names(self, db: Session, *, names: List[str]) -> List[Level]:
        return db.query(Level).filter(Level.level.in_(tuple(names))).all()

    def get_all(self, db: Session) -> List[Level]:
        return db.query(Level).all()


sport = CRUDSport(Sport)
level = CRUDLevel(Level)
