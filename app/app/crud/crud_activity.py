# -*- coding: utf-8 -*-
"""
@author: Liam
"""

from typing import Optional, List, Union, Dict, Any
import datetime
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.crud.crud_misc import level
from app.models.activity import Activity
from app.models.reserved import Reserved
from app.schemas.activity import ActivityCreate, ActivityUpdate

class CRUDActivity(CRUDBase[Activity, ActivityCreate, None]):
    def create_with_organizer(
        self, db: Session, *, obj_in: ActivityCreate, organizer: str
    ) -> Activity:
        levels = level.get_by_names(db=db, names=obj_in.levels)
        obj_in_data = jsonable_encoder(obj_in, exclude={'levels'})
        db_obj = self.model(**obj_in_data, organizer=organizer, publi_date=datetime.date.today())
        db_obj.levels.extend(levels)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_id(self, db: Session, *, id: int) -> Optional[Activity]:
        return (
            db.query(Activity)
            .filter(Activity.id == id)
            .first())


    def get_with_queries(
        self, db: Session, *, organizer: str = None, sport_id: int = None, active: bool = None, postcode: str = None,
            levels: list = [], offset: int = None, limit: int = None
    ) -> List[Activity]:
        queries = []
        if organizer:
            queries.append(Activity.organizer == organizer)
        if sport_id:
            queries.append(Activity.sport_id == sport_id)
        if active:
            queries.append(Activity.event_date.is_(None) | (Activity.event_date >= datetime.date.today()))
        if postcode:
            queries.append(Activity.postcode.ilike(f'%{postcode}%'))
        if levels:
            level_ids = (level.id for level in level.get_by_names(db=db, names=levels))
            queries.append(Reserved.c.level_id.in_(level_ids))
        return (
            db.query(Activity)
            .join(Reserved, Reserved.c.activity_id == Activity.id)
            .filter(*queries)
            .offset(offset)
            .limit(limit)
            .all())

    def update(
        self,
        db: Session,
        *,
        db_obj: Activity,
        obj_in: Union[ActivityUpdate, Dict[str, Any]]
    ) -> Activity:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

activity = CRUDActivity(Activity)
