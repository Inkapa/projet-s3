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
from app.models.participation import Participation
from app.models.account import Account
from app.models.level import Level
from app.models.reserved import Reserved
from app.schemas.activity import ActivityCreate, ActivityUpdate
from sqlalchemy import distinct

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
            .join(Participation, Participation.activity_id == Activity.id, isouter=True)
            .join(Account, Account.username == Participation.participant, isouter=True)
            .join(Level, Level.id == Participation.level_id, isouter=True)
            .filter(Activity.id == id)

            .first())


    def get_with_queries(
        self, db: Session, *, current_account: str = None, organizer: str = None, sport_id: int = None,
            active: bool = None, postcode: str = None, exclude_participating: bool = None, me_excluded: bool = None,
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
        if me_excluded:
            queries.append(Activity.organizer != current_account)
        if exclude_participating:
            subquery = db.query(Activity.id).filter(Participation.participant == current_account, Participation.activity_id == Activity.id).subquery()
            print(subquery)
            queries.append((Participation.activity_id.not_in(subquery)) | (Participation.participant == None))
        if levels:
            level_ids = (level.id for level in level.get_by_names(db=db, names=levels))
            queries.append(Reserved.c.level_id.in_(level_ids))
        print(str(db.query(Activity)
            .join(Reserved, Reserved.c.activity_id == Activity.id)
            .join(Participation, Participation.activity_id == Activity.id, isouter=True)
            .filter(*queries)
            .offset(offset)
            .limit(limit)))
        return (
            db.query(Activity)
            .join(Reserved, Reserved.c.activity_id == Activity.id)
            .join(Participation, Participation.activity_id == Activity.id, isouter=True)
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
        if update_data.get("levels"):
            update_data["levels"] = level.get_by_names(db=db, names=obj_in.levels)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

activity = CRUDActivity(Activity)
