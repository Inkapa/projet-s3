# -*- coding: utf-8 -*-
"""
@author: Liam
"""

from typing import Optional, List
from fastapi.encoders import jsonable_encoder
import datetime
from sqlalchemy.orm import Session
from app.crud.crud_misc import level
from app.crud.base import CRUDBase
from app.models.participation import Participation
from app.models.activity import Activity
from app.models.account import Account
from app.models.account_data import Account_Data
from app.schemas.participation import ParticipationCreate
from sqlalchemy import distinct


class CRUDParticipation(CRUDBase[Participation, ParticipationCreate, None]):

    def get_by_user_and_id(self, db: Session, *, id: int, participant: str) -> Optional[Participation]:
        return db.query(Participation).filter(
            Participation.activity_id == id and Participation.participant == participant).first()

    def get_by_user(self, db: Session, *, participant: str, sport_id: int = None, active: bool = None,
                    postcode: str = None, level_names: list = [],
                    offset: int = None, limit: int = None) -> List[Participation]:
        queries = [Participation.participant == participant]
        if sport_id:
            queries.append(Activity.sport_id == sport_id)
        if active:
            queries.append(Activity.event_date.is_(None) | (Activity.event_date >= datetime.date.today()))
        if postcode:
            queries.append(Activity.postcode.ilike(f'%{postcode}%'))
        if level_names:
            level_ids = (level_obj.id for level_obj in level.get_by_names(db=db, names=level_names))
            queries.append(Participation.level_id.in_(level_ids))
        return (
            db.query(Participation)
                .join(Activity, Activity.id == Participation.activity_id)
                .filter(*queries)
                .offset(offset)
                .limit(limit)
                .all())

    def get_by_activity(self, db: Session, *, id: int, postcode: str = None,
                        role_ids: list = [], level_names: list = [], offset: int = None, limit: int = None) -> List[
        Participation]:
        queries = [Participation.activity_id == id]
        if level_names:
            level_ids = (level_obj.id for level_obj in level.get_by_names(db=db, names=level_names))
            queries.append(Participation.level_id.in_(level_ids))
        if postcode:
            queries.append(Account_Data.postcode.ilike(f'%{postcode}%'))
        if role_ids:
            queries.append(Account.role_id.in_(role_ids))
        return (
            db.query(Participation)
                .join(Account, Account.username == Participation.participant)
                .join(Account_Data, Account.username == Account_Data.owner_username)
                .filter(*queries)
                .offset(offset)
                .limit(limit)
                .all())

    def get_athletes(self, db: Session, current_account: str, postcodes: list, me_excluded: bool = True,
                     sport_ids: list = [],
                     level_names: list = [],
                     offset: int = None, limit: int = None) -> List[Participation]:

        queries = [(Account_Data.postcode.in_(tuple(postcodes))) | (Activity.postcode.in_(tuple(postcodes)))]
        if me_excluded:
            queries.append(Participation.participant != current_account)
        if sport_ids:
            queries.append(Activity.sport_id.in_(tuple(sport_ids)))
        if level_names:
            level_ids = (level_obj.id for level_obj in level.get_by_names(db=db, names=level_names))
            queries.append(Participation.level_id.in_(level_ids))

        return (
            db.query(Participation)
                .join(Activity, Activity.id == Participation.activity_id)
                .join(Account, Account.username == Participation.participant)
                .join(Account_Data, Account.username == Account_Data.owner_username)
                .filter(*queries)
                .offset(offset)
                .limit(limit)
                .all())

    def get_nb_participants(self, db: Session, id: int) -> int:
        return (
            db.query(distinct(Participation.participant).label('participant_count'))
              .filter(Participation.activity_id == id)
              .count())

    def get_all(self, db: Session) -> List[Participation]:
        return db.query(Participation).all()

    def create(self,
               db: Session, *,
               obj_in: ParticipationCreate) -> Participation:

        level_obj = level.get_by_name(db=db, name=obj_in.level)
        obj_in_data = jsonable_encoder(obj_in, exclude={'level'})
        db_obj = self.model(**obj_in_data, level_id=level_obj.id)
        # db_obj.level = level_obj
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int, username: str = None) -> int:
        queries = [Participation.activity_id == id]
        if username:
            queries.append(Participation.participant == username)
        rows = db.query(Participation).filter(*queries).delete()
        db.commit()
        return rows


participation = CRUDParticipation(Participation)
