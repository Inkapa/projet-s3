# -*- coding: utf-8 -*-
"""
@author: Liam
"""

from typing import Any, Dict, Union, List
import datetime
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.crud.crud_misc import level, sport
from app.models.activity import Activity
from app.schemas.activity import ActivityCreate
from app.schemas.misc import Level

class CRUDActivity(CRUDBase[Activity, ActivityCreate, None]):
    def create_with_organizer(
        self, db: Session, *, obj_in: ActivityCreate, organizer: str
    ) -> Activity:
        activity_sport = sport.get_by_name(db=db, name=obj_in.sport_name)
        levels = level.get_by_names(db=db, names=obj_in.levels)
        obj_in_data = jsonable_encoder(obj_in, exclude={'sport_name', 'levels'})
        db_obj = self.model(**obj_in_data, organizer=organizer, sport_id=activity_sport.id)
        db_obj.levels.extend(levels)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_organizer(
        self, db: Session, *, organizer: str, active: bool
    ) -> List[Activity]:

        if active:
            return (
                db.query(Activity)
                .filter(Activity.organizer == organizer, Activity.end_date.is_(None) | (Activity.end_date > datetime.date.today()))
                .all())
        else:
            return (
                db.query(Activity)
                .filter(Activity.organizer == organizer)
                .all())




activity = CRUDActivity(Activity)
