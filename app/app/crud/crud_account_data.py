# -*- coding: utf-8 -*-
"""
@author: Liam
"""

from typing import Any, Dict, Union, List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.account_data import Account_Data
from app.schemas.account_data import Account_DataCreate, Account_DataUpdate
from app.models.participation import Participation
from app.models.activity import Activity
from app.models.account import Account
from app.crud.crud_misc import level


class CRUDAccount_Data(CRUDBase[Account_Data, Account_DataCreate, Account_DataUpdate]):
    def create_with_owner(
            self, db: Session, *, obj_in: Account_DataCreate, owner_username: str
    ) -> Account_Data:
        obj_in_data = jsonable_encoder(obj_in)
        if obj_in_data.get("gender"):
            obj_in_data["gender"] = obj_in_data["gender"].lower()
        db_obj = self.model(**obj_in_data, owner_username=owner_username)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_owner(
            self, db: Session, *, owner_username: str
    ) -> Account_Data:
        return (
            db.query(self.model)
                .filter(Account_Data.owner_username == owner_username)
                .first()
        )

    def update(
            self,
            db: Session,
            *,
            db_obj: Account_Data,
            obj_in: Union[Account_DataUpdate, Dict[str, Any]]
    ) -> Account_Data:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    # def get_multi_by_owner(
    #     self, db: Session, *, owner_username: str
    # ) -> List[Account_Data]:
    #     return (
    #         db.query(self.model)
    #         .filter(Account_Data.owner_username == owner_username)
    #         .offset(0)
    #         .limit(1)
    #         .all()
    #     )

    def get_athletes_by_name(self,
                             db: Session,
                             current_account: str,
                             username: str,
                             me_excluded: bool = True,
                             postcode: str = None,
                             role_id: int = None,
                             sport_ids: list = [],
                             level_names: list = [],
                             offset: int = None, limit: int = None) -> List[Account_Data]:
        queries = [Account.username.ilike(f"%{username}%")]
        if me_excluded:
            queries.append(Account.username != current_account)
        if postcode:
            queries.append(Account_Data.postcode == postcode)
        if sport_ids:
            queries.append(Activity.sport_id.in_(tuple(sport_ids)))
        if level_names:
            level_ids = (level_obj.id for level_obj in level.get_by_names(db=db, names=level_names))
            queries.append(Participation.level_id.in_(level_ids))

        return (
            db.query(Account_Data)
                .join(Account, Account.username == Account_Data.owner_username)
                .join(Participation, Participation.participant == Account.username, isouter=True)
                .join(Activity, Activity.id == Participation.activity_id)
                .filter(*queries)
                .offset(offset)
                .limit(limit)
                .all())


account_data = CRUDAccount_Data(Account_Data)
